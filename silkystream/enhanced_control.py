"""
增强控件主要多出一个model的功能。key变成一个必要的值。
不使用model的话就使用st模块下的原版控件
model指的就是当前页面对应的数据模型中：data_开头的属性/com_开头的函数。
com开头的计算属性，是只读的

增强控件是一系列精心设计的拥有与数据模型交互能力的控件
"""

import streamlit as st
from typing import Callable, Any, Union, List, Tuple, Set
from .data_vm import DataViewModel as dvm
from loguru import logger


def _run_two_function(parameters: tuple = None):
    model, key = parameters[:2]
    _rewrite_value(model, key)  # 进行赋值
    user_function_name = parameters[2]
    if not user_function_name:
        return  # 如果没有写回调函数，直接返回
    param = parameters[3:]  # 剩下的都是回调函数的参数
    page_id = st.session_state.now_page_id
    obj = st.session_state[page_id]["data"]
    function_obj = getattr(obj, user_function_name)
    if param:
        function_obj()
    else:
        function_obj(*param)


def _rewrite_value(model: str, key: str):
    """
    重设最新的值,需要与key交互
    顺序：
    与控件交互 -> 将key值设置到数据模型中去 -> 将数据模型的值给key
    """
    page_id = st.session_state.now_page_id
    obj = st.session_state[page_id]["data"]
    if model.startswith("com_"):
        return  # 如果是计算属性，则无法赋值，直接返回
    setattr(obj, model, st.session_state[key])  # 将交互的值设置给数据模型
    dvm.page_update()  # 更新页面和参考页的所有数据


class EnhancedControl:
    @staticmethod
    def selectbox(
        label,
        model: str,
        key: str,
        options: Union[List[str], Tuple[str], Set[str]],  # 尽量不要放数字进来
        format_func: Callable[[Any], Any] = str,
        on_change: str = None,  # 此处只能使用当前页数据模型中的函数名
        help=None,
        args=(),
        kwargs=None,
        placeholder="Choose an option",
        disabled=False,
        label_visibility="visible",
    ):
        """修复了：option变化时，selectbox会回弹到第一个值的问题
        在vue中，option也是靠在UI中渲染的。
        推荐使用一个数据属性或者一个函数进行管控更为便捷
        """
        page_id = st.session_state.now_page_id
        obj = st.session_state[page_id]["data"]
        value = getattr(obj, model)
        if model.startswith("com_"):
            k = value()
            if k in options:
                st.session_state[key] = k  # 计算属性返回值直接供给到key中
            else:
                logger.warning("值{}不存在", k)
                st.session_state[key] = options[0] if options else "" # 否则才回复到初始为止
        if model.startswith("data_"):
            if value in options:
                st.session_state[key] = value  # 将数据模型的数据供给到key中
            else:
                logger.warning("值{}不存在", value)
                st.session_state[key] = options[0] if options else ""  # 否则才回复到初始为止
        args_list = ((model, key, on_change, *args),)  # 以下为真正的渲染函数。
        st.selectbox(
            label=label,
            options=options,
            format_func=format_func,
            key=key,
            help=help,
            on_change=_run_two_function,
            args=args_list,
            kwargs=kwargs,
            placeholder=placeholder,
            disabled=disabled,
            label_visibility=label_visibility,
        )

