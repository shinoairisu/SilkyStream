from abc import ABC, abstractmethod
import copy
from typing import Tuple, Union
from nanoid import generate
import streamlit as st


class AbstractItem(ABC):
    def __init__(self, value):
        super().__init__()
        self._value = value

    @property
    @abstractmethod
    def value(self): ...  # 值获取器

    @value.setter
    @abstractmethod
    def value(self,value): ...  # 值设置器

    def copy(self):
        return copy.copy(self)  # 构造一个新的对象出来

    def __eq__(self, value):
        """默认使用value判等"""
        return self._value == value

    def __int__(self) -> int:
        try:
            result = int(self._value)
        except Exception:
            result = 0
        return result

    def __float__(self) -> float:
        try:
            result = float(self._value)
        except Exception:
            result = 0.0
        return result

    def __str__(self) -> str:
        try:
            result = str(self._value)
        except Exception:
            result = ""
        return result
    
    def __bool__(self) -> bool:
        """默认的bool是True"""
        return True

    def rerun(self): ...  # 用于更新数据，比如进度条，可以清理被注册的进度条


class BaseItem(AbstractItem):
    """用于基础类型，比如：int str float bool等"""

    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


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

    def __eq__(self, value):
        """当想关闭一个值的watch判断时，本函数返回True即可"""
        return True


class ProgressItem(AbstractItem):
    """用于进度条"""

    def __init__(self, value: Tuple[int | float, str] | int | float, min_value=0, max_value=100):
        """
        方案1：(15,"等待中...")  同时放入数字和文字
        方案2：15 只放入数字
        """
        self.min_value = min_value
        self.max_value = max_value
        self.value_setter(value=value)
        self.regist = []  # 存储注册的进度条
        self.validate_value(value=value)

    def validate_value(self,value):
        assert self.min_value <= value <= self.max_value, "value值超出进度条范围"
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: Tuple[int | float, str] | int | float):
        self.value_setter(value=value)
        for progress in self.regist_progress:
            progress.progress(self._value, text=self.text)

    
    def value_setter(self,value: Tuple[int | float, str] | int | float):
        """
        方案1：(15,"等待中...")  同时放入数字和文字
        方案2：15 只放入数字
        """
        assert isinstance(value,(tuple,int,float)),"值类型错误，只可以是tuple，int或者float中的一种"
        if isinstance(value,tuple):
            self.validate_value(value=value[0])
            self._value = value[0]
            self.text = value[1]
        else:
            self._value = value
            self.text = ""

    def regist_progress(self, obj):
        self.regist.append(obj)

    def __str__(self):
        return self.text

    def rerun(self):
        """重运行时清理进度条注册表"""
        self.regist.clear()


class WatchDogItem(AbstractItem):
    """监视文件数据"""

class OnceItem(AbstractItem):
    """只能访问一次就会变False的布尔值"""
    def __init__(self, value:bool):
        super().__init__(value)

    @property
    @abstractmethod
    def value(self):
        if self._value:
            self._value = False
            return True
        return False

    @value.setter
    @abstractmethod
    def value(self,value): 
        self._value = value
    
    def __bool__(self):
        return self._value
    
if __name__ == "__main__":
    ai = AIHistory([124])
