from copy import copy,deepcopy
from typing import Type, TypeVar, Any, Callable, Optional
from dataclasses import dataclass
from loguru import logger

import streamlit as st

from .base_classes import AbstractItem

T = TypeVar("T")


def isinstance_base(obj) -> bool:
    """
    返回obj是否属于某个基础数值类型
    尽量减少在基础值中使用tuple，因为这会降低检测速度。
    """
    result = isinstance(obj, (int, float, complex, str, bool, tuple, AbstractItem))
    return result


def update_data(
    obj,
    attr: str,
    new_value: Any, # 可以对任何类型进行设置，包括AbstractItem和
    data_handler_function: Optional[Callable[[Any], Any]] = None,
):
    """
    针对一个变量，执行变量的watch。
    对于基础变量
    如果变量没有watch，也不会报错，将是一个警告。
    attr 要求是data开头的变量
    data_handler_function 比如list变量，本函数也可以处理，需要放入一个list的数据处理的函数
    data_handler_function 要求： func(obj,value)->新对象。func内部需要直接对比如list进行修改。
    """
    watch_func = getattr(obj, f"watch_{attr}", None)
    old_data = getattr(obj, attr, None)
    if old_data is None:
        raise ValueError(f"数据属性 {attr} 不存在！")
    if type(old_data.value if isinstance(old_data, AbstractItem) else old_data) != type(
        new_value
    ):
        raise ValueError(
            f"属性{attr}的新值类型是{old_data}，旧值类型是{new_value}，类型不匹配"
        )
    if isinstance_base(old_data):
        copy_obj = st.session_state[obj.page_id]["data_copy"]
        copy_obj_data = getattr(old_data, attr)
        if isinstance(old_data, AbstractItem):
            old_data.value = new_value
            if old_data != copy_obj_data: # 这会触发 __eq__
                if watch_func:
                    watch_func(copy_obj_data, old_data)
                setattr(copy_obj, attr, deepcopy(old_data))  # 复制
        else:
            if old_data != new_value:
                setattr(obj, attr, new_value)
                setattr(copy_obj, attr, new_value)
                if watch_func:
                    watch_func(old_data,new_value)
    else:
        """如果不是基础参数，调用data_handler_function进行数据处理"""
        if not data_handler_function:
            raise ValueError("对于非基础类型数据，必须提供一个数据处理函数")
        temp = copy(old_data) # 为了节省内存和时间，所以使用浅拷贝。因此本函数无法处理复杂情况。
        new_result = data_handler_function(old_data,new_value) # 比如：list.append(new_value)。
        if watch_func:
            watch_func(temp,new_result)

    if not watch_func:  # 监视函数不存在就报个警告即可。防止使用错了变量
        logger.warning("不存在监视函数：watch_{}", attr)
        return
    watch_func(old_data, new_value)  # 执行监视函数


def update_all_page_data():
    """
    执行所有页面的watch函数
    本函数只是自动设置基础类型 int,float,complex,str,bool,tuple
    如果是list set dict 三种类型，请使用data_operator中的对应函数。
    tuple不会变化，所有不在处理范围。

    流程：
    1. 遍历所有基础数据，查看是否有变化。
    2. 有变化的数据查看是否有对应的watch函数。
    3. 如果有，调用watch函数。
    4. 对有变化的数据进行复制操作
    """
    pages = [
        st.session_state.now_page_id,
        *st.session_state.reference_page,
    ]  # 获取所有要更新的页面
    for page_id in pages:  # 拿到对应id
        now_page = st.session_state[page_id]["data"] # 对所有记录在册的page进行迭代
        for attr in dir(now_page):
            if not attr.startswith("data_"):  # 如果不是数据属性就跳过
                continue
            new_data = getattr(now_page, attr, None)  # 拿到数据
            if not isinstance_base(new_data):  # 不是基础数据类型也不要
                continue
            watch_func = getattr(now_page, f"watch_{attr}", None)
            copy_now_page = st.session_state[page_id]["data_copy"]
            old_data = getattr(copy_now_page, attr, None)  # 拿到老数据
            if type(new_data) != old_data:
                raise ValueError(f"新旧数据类型不一致，请检查问题。新类型为：{type(new_data)}，旧类型为：{type(old_data)}")
            if new_data == old_data:
                continue # 数据没变就不管
            if watch_func:
                watch_func(old_data,new_data)
            setattr(copy_now_page,attr,deepcopy(new_data))