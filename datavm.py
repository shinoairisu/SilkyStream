"""
数据模型定义、获取
dataclass定义数据时，必须使用data开头
dataclass只支持基础类型，如 str,int,float,list,tuple,set,dict等。可以使用List[str]一类的数据。
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
from typing import Type,TypeVar
from dataclasses import dataclass
from loguru import logger

import streamlit as st

T = TypeVar("T")


def _isinstance(obj) -> bool:
    """返回是否属于某个基础数值类型"""
    classes = [int,float,complex,str,bool,tuple] # tuple是不会变的类型，因此比较的是id
    result =  any(isinstance(obj,c) for c in classes)
    return result

def _auto_copy_data():
    """
    弃用 这是冗余操作
    基础只拷贝str int float
    """
    now_page = st.session_state[st.session_state.now_page_id]
    for attr in dir(now_page["data"]):
        value = getattr(now_page["data"],attr)
        if attr.startswith("data_") and _isinstance(value):
            setattr(now_page["data_copy"],attr,value) 
            logger.debug("更新属性：{}数据",attr)

def _run_watch():
    """
    执行所有页面的watch函数
    本函数只是自动设置基础类型 int,float,complex,str,bool
    如果是list set dict 三种类型，请使用data_operator中的对应函数。
    tuple不会变化，所有不在处理范围。

    流程：
    1. 遍历所有基础数据，查看是否有变化。
    2. 有变化的数据查看是否有对应的watch函数。
    3. 如果有，调用watch函数。
    4. 对有变化的数据进行复制操作
    """
    pages= [st.session_state.now_page_id,*st.session_state.reference_page] # 获取所有要更新的页面
    for page_id in pages: # 拿到对应id
        now_page = st.session_state[page_id]
        for attr in dir(now_page["data"]):
            if attr.startswith("watch_"): # 找到一个watch
                s = attr.split("_")[1:]
                data_name = "_".join(["data"] + s) # 数据的名字
                
                now = getattr(now_page["data"],data_name,None)
                old = getattr(now_page["data_copy"],data_name,None)
                if now != old:
                    watch_data = getattr(now_page["data"],attr)
                    watch_data(old,now)
                    setattr()

def set_datavm(page_id:str,data_class_name:Type[T]) -> T:
    """
    设置数据类
    page_id 是准备设置当前页面的id
    data_class_name 是用作参考的数据类
    set 必须出现在所有get 之前
    """
    if "get_flag" in st.session_state:
        assert not st.session_state.get_flag,"get_datavm不可以在set_datavm之前调用!"
    st.session_state.now_page_id = page_id
    st.session_state.get_flag = False  # set之前不能出现这个flag
    st.session_state.reference_page = []
    obj = data_class_name()
    # obj.page_id = page_id
    obj_copy = data_class_name()
    # obj_copy.page_id = page_id
    if page_id in st.session_state and "data" in st.session_state[page_id]: # 如果有就获取
        obj = st.session_state[page_id]["data"]
    if page_id not in st.session_state: # 没有页就新建
        st.session_state[page_id] = {
            "data":obj
        }
    if "data" not in st.session_state[page_id]: # 没有data就新建
        st.session_state[page_id]["data"] = obj
    if "data_copy" not in st.session_state[page_id]: # 没有data_copy就新建
        st.session_state[page_id]["data_copy"] = obj_copy # 用来给watch用的，本部分已弃用
    return obj

def get_datavm(page_id:str,data_class_name:Type[T]) -> T:
    """
    获取数据类
    page_id 想要获取数据的页面id，如page1
    data_class_name  是用作参考的数据类
    """
    st.session_state.get_flag = True
    if "reference_page" not in st.session_state:
        st.session_state["reference_page"] = [page_id]

def page_update():
    """
    执行所有更新数据类的函数
    请在页面开始（在setvm和getvm之后调用）
    以及任何需要立即更新数据的地方，比如进度条的循环中调用本函数
    本函数错误调用不会导致报错和数据错乱，但是会导致一定程度的性能下降
    """
    _run_watch() # 执行所有相关页面的watch函数

if __name__ == "__main__":
    @dataclass
    class TestClass:
        data_uid:str = "00000000"
        data_uname:str = "nick"
        data_age:int = 18

        def watch_uname(old_value,new_value):
            """监控uname变化"""
            pass

        def computed_uidname():
            """计算属性,只要参数不变，返回内容就不变。"""
            pass
    vm = set_datavm("!0",TestClass)
    # logger.debug("本页面的id是{}",vm.page_id)
    _auto_copy_data()
    