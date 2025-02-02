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
    """回调函数要同时执行两个"""
    model, key = parameters[:2]
    _rewrite_value(model, key)  # 进行赋值
    user_function_name = parameters[2]  # 拿到回调函数
    if not user_function_name:
        return  # 如果没有写回调函数，直接返回
    param = parameters[3:]  # 剩下的都是回调函数的参数
    page_id = st.session_state.now_page_id
    obj = st.session_state[page_id]["data"]
    function_obj = getattr(obj, user_function_name)
    if not param:
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


def _get_model_value(model, control_name, data_type):
    """使用数据模型获取数据，用于大记忆恢复术"""
    page_id = st.session_state.now_page_id
    obj = st.session_state[page_id]["data"]
    value = getattr(obj, model)
    assert model.startswith(("com_", "data_")), "使用的不是数据模型"
    value = value if model.startswith("data_") else value()
    assert isinstance(
        value, data_type
    ), f"{control_name}绑定的数据模型类型必须为{data_type}，此处为{type(value)}"
    return value


class EnhancedControl:
    @staticmethod
    def selectbox(
        label,
        model: str,
        key: str,
        options: Union[List[str], Tuple[str], Set[str]],  # 尽量不要放数字进来
        format_func: Callable[[Any], Any] = str,
        on_change_str: str = None,  # 此处只能使用当前页数据模型中的函数名
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

        绑定model要求数据类型为: str
        """
        value = _get_model_value(model=model,control_name="selectbox",data_type=str)

        if value in options:
            st.session_state[key] = value  # 将数据模型的数据供给到key中，大记忆恢复术，因为streamlit会清理部分过时key，导致结果不符合预期。这个操作等于是延时。
        else:
            logger.warning("值{}不存在", value)
            st.session_state[key] = (
                options[0] if options else ""
            )  # 否则才回复到初始为止

        args_list = ((model, key, on_change_str, *args),)  # 以下为真正的渲染函数。
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

    @staticmethod
    def text_input(
        label,
        model: str,
        key: str,
        max_chars=None,
        on_change_str: str = None,
        type="default",
        help=None,
        autocomplete=None,
        args=(),
        kwargs=None,
        placeholder=None,
        disabled=False,
        label_visibility="visible",
    ):
        """绑定model要求数据类型为: str"""

        value = _get_model_value(model=model,control_name="text_input",data_type=str)
        st.session_state[key] = value

        args_list = ((model, key, on_change_str, *args),)  # 以下为真正的渲染函数。
        st.text_input(
            label=label,
            key=key,
            max_chars=max_chars,
            type=type,
            help=help,
            autocomplete=autocomplete,
            kwargs=kwargs,
            placeholder=placeholder,
            disabled=disabled,
            label_visibility=label_visibility,
            on_change=_run_two_function,
            args=args_list,
        )

    @staticmethod
    def text_area(
        label,
        model: str,
        key: str,
        height=None,
        max_chars=None,
        help=None,
        on_change_str: str = None,
        args=(),
        kwargs=None,
        placeholder=None,
        disabled=False,
        label_visibility="visible",
    ):
        """绑定model要求数据类型为: str"""
        value = _get_model_value(model=model,control_name="text_area",data_type=str)
        st.session_state[key] = value
        args_list = ((model, key, on_change_str, *args),)  # 以下为真正的渲染函数

        st.text_area(
            label=label,
            key=key,
            height=height,
            max_chars=max_chars,
            help=help,
            kwargs=kwargs,
            placeholder=placeholder,
            disabled=disabled,
            label_visibility=label_visibility,
            on_change=_run_two_function,
            args=args_list,
        )

    @staticmethod
    def chat_input(
        model: str,
        key: str,
        placeholder="Your message",
        max_chars=None,
        disabled=False,
        on_submit_str: str = None,
        args=(),
        kwargs=None,
    ):
        """绑定model要求数据类型为: str
        此控件只向模型中写入，不读取"""

        # 以下部分内容就是写入
        args_list = ((model, key, on_submit_str, *args),)  # 以下为真正的渲染函数

        st.chat_input(
            key=key,
            placeholder=placeholder,
            max_chars=max_chars,
            disabled=disabled,
            kwargs=kwargs,
            on_submit=_run_two_function,
            args=args_list,
        )

    @staticmethod
    def checkbox(
        label,
        model: str,
        key: str,
        on_change_str=None,
        help=None,
        args=(),
        kwargs=None,
        disabled=False,
        label_visibility="visible",
    ):
        """绑定model要求数据类型为: bool"""

        value = _get_model_value(model=model,control_name="checkbox",data_type=bool)
        st.session_state[key] = value
        
        args_list = ((model, key, on_change_str, *args),)  # 以下为真正的渲染函数

        st.checkbox(
            label=label,
            key=key,
            help=help,
            kwargs=kwargs,
            disabled=disabled,
            label_visibility=label_visibility,
            on_change=_run_two_function,
            args=args_list,
        )
