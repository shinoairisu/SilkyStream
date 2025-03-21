"""增强对象
BaseItem与AutoUpdateBaseItem是可以作为绑定通用的data_数据模型
AIHistoryItem这种是复杂类模型，作用单一，不用于绑定数据模型，而主要是内部操作用。
BaseItem功能：平滑数据类型，可以多类型控件公用一个数据模型。并且可以用于操作list深层对象。
"""

import copy
from typing import Tuple, Callable, Any, Optional, List
from silkystream.custom_utils.abstract_item import AbstractItem


class BaseItem(AbstractItem):
    """用于基础类型，比如：int str float bool等"""

    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, (int, str, float, bool, complex)):
            func = type(self._value)
            try:
                value = func(value)
            except Exception:
                self._value = func()
        else:
            raise ValueError("不是基础类型，无法使用本类")


class AutoUpdateBaseItem(AbstractItem):
    """自动更新的基础参数"""

    def __init__(self, value, watch_func: Callable[[Any, Any], None]):
        super().__init__(value)
        self.watch_func = watch_func

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, (int, str, float, bool, complex)):
            if self._value == value:
                return
            else:
                func = type(self._value)
                try:
                    value = func(value)
                except Exception:
                    value = func()
                self.watch_func(self._value, value)  # old,new
                self._value = value
        else:
            raise ValueError("不是基础类型，无法使用本类")

    def __eq__(self, _):
        """本类更新参数时会自动执行watch_func，因此不参与全局监视运算
        适合List中使用
        """
        return True


class AIHistoryItem(AbstractItem):
    """用于AI对话历史记录"""

    def __init__(self, value: list):
        """
        value:是一个列表,可以是一个空列表，也可以是以前的历史记录
        value列表是复制品
        """
        if not value:
            super().__init__(value)
        else:
            super().__init__(copy.copy(value))

    @property
    def value(self):
        """拿到值就可以修改对应内容"""
        return self._value

    @value.setter
    def value(self, value: Tuple[str, str]):
        """输入值会变成添加值 ("user","你好")"""
        self._value.append(value)

    def __eq__(self, _):
        """当想关闭一个值的watch判断时，本函数返回True即可"""
        return True


class ProgressItem(AbstractItem):
    """用于进度条"""

    def __init__(
        self, value: Tuple[int | float, str] | int | float, min_value=0, max_value=100,text=""
    ):
        """
        方案1：(15,"等待中...")  同时放入数字和文字
        方案2：15 只放入数字
        """
        self.min_value = min_value
        self.max_value = max_value
        self.__value_setter(value=value)
        self.__regist = []  # 存储注册的进度条
        self.__validate_value(value=value)
        self.text = text

    def __validate_value(self, value):
        assert self.min_value <= value <= self.max_value, "value值超出进度条范围"

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: Tuple[int | float, str] | int | float):
        self.__value_setter(value=value)
        for progress in self.regist_progress:
            progress.progress(self._value, text=self.text)

    def __value_setter(self, value: Tuple[int | float, str] | int | float):
        """
        方案1：(15,"等待中...")  同时放入数字和文字
        方案2：15 只放入数字
        """
        assert isinstance(
            value, (tuple, int, float)
        ), "值类型错误，只可以是tuple，int或者float中的一种"
        if isinstance(value, tuple):
            self.__validate_value(value=value[0])
            self._value = value[0]
            self.text = value[1]
        else:
            self._value = value
            self.text = ""

    def regist_progress(self, obj):
        obj.progress(self._value, text=self.text) # 跨步到现在值
        self.__regist.append(obj)

    def __str__(self):
        return self.text

    def rerun(self):
        """重运行时清理进度条注册表"""
        self.__regist.clear()


class WatchDogItem(AbstractItem):
    """监视文件/数据等
    wi1 = WatchDogItem(list,self.set_file) # 每次rerun时会执行wi1下的rerun，就能监视一些硬盘数据等
    通过wi1.value可以获得最新的监视结果。
    """

    def __init__(
        self, data_type, watch_function: Callable, args: Optional[tuple] = None
    ):
        """先定义监视函数返回的数据类型，也可以理解为生成一个什么类型的数据"""
        super().__init__(None)
        self.watch_function = watch_function
        self.args = args
        self.data_type = data_type
        self.rerun()

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, self.data_type):
            self._value = value
        else:
            raise ValueError(f"输入类别与{self.data_type}不一致，watchdog门禁不通过")

    def rerun(self):
        if self.args:
            self.value = self.watch_function(*self.args)
        else:
            self.value = self.watch_function()


class OnceItem(AbstractItem):
    """只能访问一次就会变False的布尔值"""

    def __init__(self, value: bool):
        super().__init__(value)

    @property
    def value(self):
        if self._value:
            self._value = False
            return True
        return False

    @value.setter
    def value(self, value):
        self._value = value

    def __bool__(self):
        """bool模式下返回的是真实值，只有查看value时才会只能访问一次"""
        return self._value


class ListItem(AbstractItem):
    """列表"""

    def __init__(
        self, value: List[str] | str, watch_fun: Callable = None
    ):
        super().__init__(value if isinstance(value, list) else [value])
        self.watch_fun = watch_fun

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str | list):
        temp = self._value.copy()
        if isinstance(value, list):
            self._value = value.copy()
        else:
            self._value.append(value)
        if self.watch_fun:
            self.watch_fun(temp,self._value) # old,new

    def __eq__(self, _):
        return True
