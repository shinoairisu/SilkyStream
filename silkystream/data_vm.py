"""
数据模型定义、获取
dataclass定义数据时，必须使用data开头
dataclass只支持基础类型，如 str,int,float,list,tuple。可以使用List[str]一类的数据。
多级数据不被检测。

用法：
from xxdata import xxdatavm
set_datavm(id,xxdatavm)
get_datavm
get_datavm
...
page_update

正式的页面内容....
"""

from copy import deepcopy
from typing import Type, TypeVar
from dataclasses import dataclass

import streamlit as st
from loguru import logger

from silkystream.utils.common_utils import *


T = TypeVar("T")


class DataViewModel(object):
    @staticmethod
    def set_datavm(page_id: str, data_class_name: Type[T], now_page=True) -> T:
        """
        设置数据类
        page_id 是准备设置当前页面的id
        data_class_name 是用作参考的数据类
        set 必须出现在所有get 之前
        now_page 指这个set函数设置的是否是当前主页面。
        """
        if "get_flag" in st.session_state:
            assert (
                not st.session_state.get_flag
            ), "get_datavm不可以在set_datavm之前调用!"
        if now_page:  # 因为get调用时不一定是当前页面
            st.session_state.now_page_id = page_id
        st.session_state.get_flag = False  # set之前不能出现这个flag
        st.session_state.reference_page = [] # 每次都清空这个属性
        obj = data_class_name()
        obj_copy = data_class_name()
        obj.page_id = page_id
        obj_copy.page_id = page_id
        if (
            page_id in st.session_state and "data" in st.session_state[page_id]
        ):  # 如果有本页面的数据类就获取
            obj = st.session_state[page_id]["data"]
            DataViewModel.page_update() # 每次都会更新所有页面数据
        else:
            st.session_state[page_id] = {}
            st.session_state[page_id]["data"] = obj
            st.session_state[page_id]["data_copy"] = obj_copy
        return obj

    @staticmethod
    def get_datavm(page_id: str, data_class_name: Type[T]) -> T:
        """
        获取数据类
        只要获取了
        page_id 想要获取数据的页面id，如page1
        data_class_name  是用作参考的数据类
        """
        st.session_state.get_flag = True
        if "reference_page" not in st.session_state:
            st.session_state["reference_page"] = [page_id]
        else:
            st.session_state["reference_page"].append(page_id)
        if page_id not in st.session_state:
            logger.warning("未找到页面id:{}", page_id)
            obj = DataViewModel.set_datavm(page_id, data_class_name, now_page=False) # now_page为false指的是虽然新建了一个页面对象，但是不是现在的主页面
            return obj
        page = st.session_state[page_id]
        if not isinstance(page, data_class_name):
            # 类型错误不会导致报错，但是会警告。另外后续IDE提示都将是错误的。
            logger.warning("页面{}使用的数据模型类不是当前获取的类型，请自查...")
        return page # 返回的是对应页的对象

    @staticmethod
    def page_update():
        """
        执行所有更新数据类的函数
        请在页面开始（在setvm和getvm之后调用）
        以及任何需要立即更新数据的地方，比如有些值变化会导致后面要连锁watch进行显示的数据变化
        就需要调用本函数
        """
        update_all_page_data()  # 执行所有相关页面的watch函数


if __name__ == "__main__":
    class TestClass(object):
        def __init__(self):
            self.data_uid: str = "00000000"
            self.data_uname: str = "nick"
            self.data_age: int = 18

        def watch_data_uname(self, old_value, new_value): ...

        @st.cache_data
        @staticmethod
        def cache_pdf(path): ...  # 计算函数对
        def computed_pdf(self):
            return TestClass.cache_pdf(self.data_uname)
