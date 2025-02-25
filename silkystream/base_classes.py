from abc import ABC,abstractmethod
import copy
from typing import Tuple
from nanoid import generate
import streamlit as st

class AbstractItem(ABC):
    def __init__(self,value):
        super().__init__()
        self._value = value

    @property
    @abstractmethod
    def value(self):... # 值获取器
    
    @value.setter
    @abstractmethod
    def value(self):... # 值设置器

    def copy(self):
        return copy.copy(self) # 构造一个新的对象出来
    
    def __eq__(self, value):
        """默认使用value判等"""
        return self._value == value
    
    def update(self):... # 用于更新数据，比如进度条，可以清理被注册的进度条

class BaseItem(AbstractItem):
    """用于基础类型，比如：int str float bool等"""
    def __init__(self,value):
        super().__init__(value)
    
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self,value):
        self._value = value

class AIHistory(AbstractItem):
    """用于AI对话历史记录"""
    def __init__(self, value:list):
        """
        value:是一个列表,可以是一个空列表，也可以是以前的历史记录
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
    def value(self,value:Tuple[str,str]):
        """输入值会变成添加值"""
        self._value.append(value)

    def __eq__(self, value):
        """当想关闭一个值的watch判断时，本函数返回True即可"""
        return True

class ProgressItem(AbstractItem):
    """用于进度条"""
    def __init__(self,value,min_value=0,max_value=100):
        assert min_value <= value <= max_value,"value值超出进度条范围"
        super().__init__(value)
        self.min_value = min_value
        self.max_value = max_value
        self.key = generate(size=10)
        self.regist = [] # 存储注册的进度条
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self,value):
        self._value = value
    
    def set_progress_value(self):
        """"""
        page_id = st.session_state.now_page_id
        obj = st.session_state[page_id]["data"]


if __name__ == "__main__":
    ai = AIHistory([124])