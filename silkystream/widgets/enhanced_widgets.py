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
from silkystream.readybox.enhanced_param_types import AIHistoryItem,ProgressItem
from loguru import logger


def _run_two_function(parameters: tuple = None):
    """回调函数要同时执行两个"""
    model, key, page_obj = parameters[
        :3
    ]  # 进入本函数时说明 on_change 被触发，key的值已经更新为控件最新值
    _set_model_value(model, key, page_obj)  # 进行赋值
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


def _set_model_value(model: str | AbstractItem, key: str, page_obj=None):
    """
    重设最新的值,需要与key交互
    顺序：
    与控件交互 -> 将key值设置到数据模型中去 -> 将数据模型的值给key
    允许与其他页面模型进行交互。
    """
    if isinstance(model, AbstractItem):
        model.value = st.session_state[key]  # 浮空型的数据更新不会引起自动变化
    else:  # model is str
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
            setattr(
                page_obj, model, st.session_state[key]
            )  # 将交互的值直接设置给数据模型
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
    if isinstance(model, AbstractItem):  # 如果model直接是抽象Item(比如list中的元素)
        value = str(model)
    else:
        value = str(_get_model_value(model=model, page_obj=page_obj))

    if value in options:
        st.session_state[key] = (
            value  # 将数据模型的数据供给到key中，大记忆恢复术，因为streamlit会清理部分过时key，导致结果不符合预期。这个操作等于是延时。
        )
    else:
        logger.warning("值{}不存在", value)
        st.session_state[key] = options[0] if options else ""  # 否则才回复到初始为止

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
    if isinstance(model, AbstractItem):  # 如果model直接是抽象Item(比如list中的元素)
        value = str(model)
    else:
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
    if isinstance(model, AbstractItem):  # 如果model直接是抽象Item(比如list中的元素)
        value = str(model)
    else:
        value = str(_get_model_value(model=model, page_obj=page_obj))

    st.session_state[key] = value
    args_list = ((model, key, page_obj, on_change_str, *args),)  # 以下为真正的渲染函数

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


def chat_input(
    model: str | AIHistoryItem,
    key: str,
    page_obj: Any = None,  # 默认是当前页
    placeholder="Your message",
    max_chars=None,
    disabled=False,
    on_submit_str: str = None,
    args=(),
    kwargs=None,
):
    """绑定model要求数据类型必须为: AIHistoryItem
    此控件只向模型中写入，不读取"""

    # 以下部分内容就是写入
    args_list = ((model, key, page_obj, on_submit_str, *args),)  # 以下为真正的渲染函数

    st.chat_input(
        key=key,
        placeholder=placeholder,
        max_chars=max_chars,
        disabled=disabled,
        kwargs=kwargs,
        on_submit=_run_two_function,
        args=args_list,
    )


def checkbox(
    label,
    model: str | AbstractItem,
    key: str,
    page_obj: Any = None,  # 默认是当前页
    on_change_str=None,
    help=None,
    args=(),
    kwargs=None,
    disabled=False,
    label_visibility="visible",
):
    if isinstance(model, AbstractItem):  # 如果model直接是抽象Item(比如list中的元素)
        value = bool(model)
    else:
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


def color_picker(
    label,
    model: str | AbstractItem,
    key: str,
    page_obj: Any = None,  # 默认是当前页
    on_change_str=None,
    help=None,
    args=(),
    kwargs=None,
    disabled=False,
    label_visibility="visible",
):

    if isinstance(model, AbstractItem):  # 如果model直接是抽象Item(比如list中的元素)
        value = str(model)
    else:
        value = str(_get_model_value(model=model, page_obj=page_obj))

    st.session_state[key] = value

    args_list = ((model, key, page_obj, on_change_str, *args),)  # 以下为真正的渲染函数

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


def feedback(
    model: str | AbstractItem,
    key: str,
    options="thumbs",
    page_obj: Any = None,  # 默认是当前页
    on_change_str=None,
    args=(),
    kwargs=None,
    disabled=False,
    label_visibility="visible",
):
    if isinstance(model, AbstractItem):  # 如果model直接是抽象Item(比如list中的元素)
        value = int(model)
    else:
        value = int(_get_model_value(model=model, page_obj=page_obj))

    st.session_state[key] = value

    args_list = ((model, key, page_obj, on_change_str, *args),)  # 以下为真正的渲染函数

    st.feedback(
        options=options,
        key=key,
        kwargs=kwargs,
        disabled=disabled,
        label_visibility=label_visibility,
        on_change=_run_two_function,
        args=args_list,
    )


def radio(
    label: str,
    options: list,
    model: str | AbstractItem,
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
    if isinstance(model, AbstractItem):  # 如果model直接是抽象Item(比如list中的元素)
        value = model.value
    else:
        value = str(_get_model_value(model=model, page_obj=page_obj))
    if value in options:
        st.session_state[key] = value
    else:
        st.session_state[key] = options[0] if options else ""
    args_list = ((model, key, page_obj, on_change_str, *args),)  # 以下为真正的渲染函数

    st.radio(
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


def multiselect(
    label: str,
    options: list,
    model: str | AbstractItem,
    key: str,
    page_obj: Any = None,  # 默认是当前页
    on_change_str=None,
    help=None,
    args=(),
    kwargs=None,
    disabled=False,
    label_visibility="visible",
    placeholder="Choose an option",
):
    if isinstance(model, AbstractItem):  # 如果model直接是抽象Item(比如list中的元素)
        value = model.value
    else:
        value = str(_get_model_value(model=model, page_obj=page_obj))

    st.session_state[key] = [i for i in value if i in options]  # 过滤还存在的键

    args_list = ((model, key, page_obj, on_change_str, *args),)  # 以下为真正的渲染函数

    st.multiselect(
        label=label,
        options=options,
        key=key,
        help=help,
        kwargs=kwargs,
        disabled=disabled,
        label_visibility=label_visibility,
        on_change=_run_two_function,
        args=args_list,
        placeholder=placeholder,
    )


def pills(
    label: str,
    options: list,
    model: str | AbstractItem,
    key: str,
    selection_mode: str = "single",
    page_obj: Any = None,  # 默认是当前页
    on_change_str=None,
    help=None,
    args=(),
    kwargs=None,
    disabled=False,
    label_visibility="visible",
):
    """本控件需要注意连个"""
    if isinstance(model, AbstractItem):  # 如果model直接是抽象Item(比如list中的元素)
        value = model.value
    else:
        value = str(_get_model_value(model=model, page_obj=page_obj))

    if selection_mode == "single":
        st.session_state[key] = value if value in options else ""
    else:
        st.session_state[key] = [i for i in value if i in options]  # 过滤还存在的键

    args_list = ((model, key, page_obj, on_change_str, *args),)  # 以下为真正的渲染函数

    st.pills(
        label=label,
        options=options,
        key=key,
        help=help,
        selection_mode=selection_mode,
        kwargs=kwargs,
        disabled=disabled,
        label_visibility=label_visibility,
        on_change=_run_two_function,
        args=args_list,
    )


def pills(
    label: str,
    options: list,
    model: str | AbstractItem,
    key: str,
    selection_mode: str = "single",
    page_obj: Any = None,  # 默认是当前页
    on_change_str=None,
    help=None,
    args=(),
    kwargs=None,
    disabled=False,
    label_visibility="visible",
):
    """本控件需要注意依附的模型类别， 一般是list或者base或者str，这是根据单选多选决定的"""
    if isinstance(model, AbstractItem):  # 如果model直接是抽象Item(比如list中的元素)
        value = model.value
    else:
        value = str(_get_model_value(model=model, page_obj=page_obj))

    if selection_mode == "single":
        st.session_state[key] = value if value in options else ""
    else:
        st.session_state[key] = [i for i in value if i in options]  # 过滤还存在的键

    args_list = ((model, key, page_obj, on_change_str, *args),)  # 以下为真正的渲染函数

    st.pills(
        label=label,
        options=options,
        key=key,
        help=help,
        selection_mode=selection_mode,
        kwargs=kwargs,
        disabled=disabled,
        label_visibility=label_visibility,
        on_change=_run_two_function,
        args=args_list,
    )


def segmented_control(
    label: str,
    options: list,
    model: str | AbstractItem,
    key: str,
    selection_mode: str = "single",
    page_obj: Any = None,  # 默认是当前页
    on_change_str=None,
    help=None,
    args=(),
    kwargs=None,
    disabled=False,
    label_visibility="visible",
):
    """本控件需要注意依附的模型类别， 一般是list或者base或者str，这是根据单选多选决定的"""
    if isinstance(model, AbstractItem):  # 如果model直接是抽象Item(比如list中的元素)
        value = model.value
    else:
        value = str(_get_model_value(model=model, page_obj=page_obj))

    if selection_mode == "single":
        st.session_state[key] = value if value in options else ""
    else:
        st.session_state[key] = [i for i in value if i in options]  # 过滤还存在的键

    args_list = ((model, key, page_obj, on_change_str, *args),)  # 以下为真正的渲染函数

    st.segmented_control(
        label=label,
        options=options,
        key=key,
        help=help,
        selection_mode=selection_mode,
        kwargs=kwargs,
        disabled=disabled,
        label_visibility=label_visibility,
        on_change=_run_two_function,
        args=args_list,
    )

def toggle(
    label,
    model: str | AbstractItem,
    key: str,
    page_obj: Any = None,  # 默认是当前页
    on_change_str=None,
    help=None,
    args=(),
    kwargs=None,
    disabled=False,
    label_visibility="visible",
):
    if isinstance(model, AbstractItem):  # 如果model直接是抽象Item(比如list中的元素)
        value = bool(model)
    else:
        value = bool(_get_model_value(model=model, page_obj=page_obj))

    st.session_state[key] = value
    args_list = ((model, key, on_change_str, *args),)  # 以下为真正的渲染函数

    st.toggle(
        label=label,
        key=key,
        help=help,
        kwargs=kwargs,
        disabled=disabled,
        label_visibility=label_visibility,
        on_change=_run_two_function,
        args=args_list,
    )

def progress(
    model: str | ProgressItem,
    value_type = "int", # "int" 或者 "float"
    page_obj: Any = None,
    text: str | None=None
):
    if isinstance(model, ProgressItem):
        model.regist_progress(st.progress(0 if value_type=="int" else 0.0,text))
    else:
        st.session_state.now_page_id
        page = page_obj if page_obj else st.session_state[st.session_state.now_page_id]["data"]
        getattr(page,model).regist_progress(st.progress(0 if value_type=="int" else 0.0,text))

    

