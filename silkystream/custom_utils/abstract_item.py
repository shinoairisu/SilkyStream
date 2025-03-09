import copy
from abc import ABC, abstractmethod


class AbstractItem(ABC):
    def __init__(self, value):
        super().__init__()
        self._value = value

    @property
    @abstractmethod
    def value(self): ...  # 值获取器

    @value.setter
    @abstractmethod
    def value(self, value): ...  # 值设置器

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