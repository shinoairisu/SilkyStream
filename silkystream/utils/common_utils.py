from copy import deepcopy
from typing import Type,TypeVar,Any
from dataclasses import dataclass
from loguru import logger

import streamlit as st

T = TypeVar("T")

def isinstance_base(obj) -> bool:
    """
    返回obj是否属于某个基础数值类型
    尽量减少在基础值中使用tuple，因为这会降低检测速度。
    """
    classes = [int,float,complex,str,bool,tuple] # tuple是不会变的类型，因此比较的是id
    result =  any(isinstance(obj,c) for c in classes)
    return result

def run_watch(obj,attr:str,new_value:Any):
    """
    针对一个变量，执行变量的watch。
    对于基础变量
    如果变量没有watch，也不会报错，将是一个警告。
    """
    watch_func = getattr(obj,f"watch_{attr}",None)
    old_data = getattr(obj,attr,None)
    assert old_data is not None,f"数据属性 {attr} 不存在！"
    assert type(old_data) == type(new_value),f"属性{attr}的新值类型是{old_data}，旧值类型是{new_value}，类型不匹配"
    if isinstance_base(old_data): 
        st.session_state[obj.page_id]["data_copy"] = new_value # 如果是基础类型，还需要更新内容到copy中，否则会被run_watch_base扫描出来
    if not watch_func: # 监视函数不存在就报个警告即可。防止使用错了变量
        logger.warning("不存在监视函数：watch_{}",attr)
        return
    watch_func(old_data,new_value) # 执行监视函数

def run_watch_base():
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
    pages= [st.session_state.now_page_id,*st.session_state.reference_page] # 获取所有要更新的页面
    for page_id in pages: # 拿到对应id
        now_page = st.session_state[page_id]["data"]
        for attr in dir(now_page):
            if not attr.startswith("data_"): # 如果不是数据属性就跳过
                continue
            new_data = getattr(now_page,attr,None) # 拿到数据
            if not isinstance_base(new_data): # 不是基础数据类型也不要
                continue
            old_data = getattr(st.session_state[page_id]["data_copy"],attr,None) # 拿到老数据
            if old_data == new_data: # 没变就不管
                continue
            assert type(old_data) == type(new_data),f"新旧属性类型不一致，位置为{page_id}的{attr},原始类型是{type(old_data)},新类型是{type(new_data)}"
            logger.debug("检测到属性 {} 发生变化",attr)
            watch_func = getattr(now_page,f"watch_{attr}",None)
            if watch_func:
                logger.debug("检测到变化属性 {} 是被监视的属性，执行监视函数",attr)
                watch_func(old_data,new_data) # 监视函数
            setattr(st.session_state[page_id]["data_copy"],attr,new_data) # 存储数据变化