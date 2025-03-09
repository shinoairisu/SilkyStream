"""
增强控件主要多出一个model的功能。key变成一个必要的值。
不使用model的话就使用st模块下的原版控件
model指的就是当前页面对应的数据模型中：data_开头的属性/com_开头的函数。
com开头的计算属性，是只读的

增强控件是一系列精心设计的拥有与数据模型交互能力的控件
"""

import streamlit as st
from typing import Callable, Any, Union, List, Tuple, Set, Optional
from silkystream.data_vm import DataViewModel as dvm
from silkystream.custom_utils.abstract_item import AbstractItem
from loguru import logger


def _run_two_function(parameters: tuple = None):
    """回调函数要同时执行两个"""
    model, key, page_obj = parameters[
        :3
    ]  # 进入本函数时说明 on_change 被触发，key的值已经更新为控件最新值
    _rewrite_value(model, key, page_obj)  # 进行赋值
    user_function_name = parameters[3]  # 拿到回调函数
    if not user_function_name:
        return  # 如果没有写回调函数，直接返回
    param = parameters[4:]  # 剩下的都是回调函数的参数
    if not page_obj:
        page_id = st.session_state.now_page_id
        page_obj = st.session_state[page_id]["data"]
    function_obj = getattr(page_obj, user_function_name)
    if not param:
        function_obj()
    else:
        function_obj(*param)


def _rewrite_value(model: str, key: str, page_obj=None):
    """
    重设最新的值,需要与key交互
    顺序：
    与控件交互 -> 将key值设置到数据模型中去 -> 将数据模型的值给key
    允许与其他页面模型进行交互。
    """
    if not page_obj:
        page_id = st.session_state.now_page_id
        page_obj = st.session_state[page_id]["data"]
    obj = getattr(page_obj, model, None)
    if obj is None:
        raise ValueError("值对象不可以是None")
    if isinstance(obj, AbstractItem):
        obj.value = st.session_state[key]
    else:
        if not isinstance(st.session_state[key], type(obj)):
            raise ValueError(f"类型绑定错误，数据模型类型为{type(obj)}")
        setattr(page_obj, model, st.session_state[key])  # 将交互的值直接设置给数据模型
    dvm.page_update()  # 更新页面和参考页的所有数据


def _get_model_value(model, page_obj=None):
    """使用数据模型获取数据，用于大记忆恢复术"""
    if not page_obj:
        # 默认使用当前页面的数据模型
        page_id = st.session_state.now_page_id
        page_obj = st.session_state[page_id]["data"]
    if not model.startswith(("data_")):
        raise ValueError("使用的不是数据模型")
    value = getattr(page_obj, model)
    return value


class EnhancedControl:
    @staticmethod
    def selectbox(
        label,
        model: str | AbstractItem,
        key: str,
        options: List[str] | Tuple[str] | Set[str],  # 尽量不要放数字进来
        page_obj: Any = None,  # 默认是当前页
        format_func: Callable[[Any], Any] = str,
        on_change_str: str = None,  # 此处默认使用当前页对象下的函数，切换page_obj可以换对象
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
        value = str(_get_model_value(model=model, page_obj=page_obj))

        if value in options:
            st.session_state[key] = (
                value  # 将数据模型的数据供给到key中，大记忆恢复术，因为streamlit会清理部分过时key，导致结果不符合预期。这个操作等于是延时。
            )
        else:
            logger.warning("值{}不存在", value)
            st.session_state[key] = (
                options[0] if options else ""
            )  # 否则才回复到初始为止

        args_list = (
            (model, key, page_obj, on_change_str, *args),
        )  # 以下为真正的渲染函数。
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
        page_obj: Any = None,  # 默认是当前页
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

        value = str(_get_model_value(model=model, page_obj=page_obj))
        st.session_state[key] = value

        args_list = (
            (model, key, page_obj, on_change_str, *args),
        )  # 以下为真正的渲染函数。
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
        page_obj: Any = None,  # 默认是当前页
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
        value = str(_get_model_value(model=model, page_obj=page_obj))
        st.session_state[key] = value
        args_list = (
            (model, key, page_obj, on_change_str, *args),
        )  # 以下为真正的渲染函数

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
        page_obj: Any = None,  # 默认是当前页
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
        args_list = (
            (model, key, page_obj, on_submit_str, *args),
        )  # 以下为真正的渲染函数

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
        page_obj: Any = None,  # 默认是当前页
        on_change_str=None,
        help=None,
        args=(),
        kwargs=None,
        disabled=False,
        label_visibility="visible",
    ):

        value = bool(_get_model_value(model=model, page_obj=page_obj))
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

    @staticmethod
    def color_picker(
        label,
        model: str,
        key: str,
        page_obj: Any = None,  # 默认是当前页
        on_change_str=None,
        help=None,
        args=(),
        kwargs=None,
        disabled=False,
        label_visibility="visible",
    ):

        value = str(_get_model_value(model=model, page_obj=page_obj))
        st.session_state[key] = value

        args_list = (
            (model, key, page_obj, on_change_str, *args),
        )  # 以下为真正的渲染函数

        st.color_picker(
            label=label,
            key=key,
            help=help,
            kwargs=kwargs,
            disabled=disabled,
            label_visibility=label_visibility,
            on_change=_run_two_function,
            args=args_list,
        )

    @staticmethod
    def feedback(
        model: str,
        key: str,
        options="thumbs",
        page_obj: Any = None,  # 默认是当前页
        on_change_str=None,
        args=(),
        kwargs=None,
        disabled=False,
        label_visibility="visible",
    ):

        value = int(_get_model_value(model=model, page_obj=page_obj))
        st.session_state[key] = value

        args_list = (
            (model, key, page_obj, on_change_str, *args),
        )  # 以下为真正的渲染函数

        st.feedback(
            options=options,
            key=key,
            kwargs=kwargs,
            disabled=disabled,
            label_visibility=label_visibility,
            on_change=_run_two_function,
            args=args_list,
        )

    @staticmethod
    def radio(
        label: str,
        options: list,
        model: str,
        key: str,
        page_obj: Any = None,  # 默认是当前页
        on_change_str=None,
        help=None,
        args=(),
        kwargs=None,
        disabled=False,
        label_visibility="visible",
        horizontal=False,
        captions=None,
    ):

        value = str(_get_model_value(model=model, page_obj=page_obj))
        if value in options:
            st.session_state[key] = value
        else:
            st.session_state[key] = options[0] if options else ""
        args_list = (
            (model, key, page_obj, on_change_str, *args),
        )  # 以下为真正的渲染函数

        st.feedback(
            label=label,
            options=options,
            key=key,
            help=help,
            kwargs=kwargs,
            disabled=disabled,
            label_visibility=label_visibility,
            on_change=_run_two_function,
            args=args_list,
            horizontal=horizontal,
            captions=captions,
        )
