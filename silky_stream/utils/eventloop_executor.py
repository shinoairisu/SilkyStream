"""
有概率希望一个函数在下一次UI循环时执行。
比如修改st组件key中的值等等。
rerun可以解决一部分问题，但是为了扩展使用方法
提供了next_tick函数，可以随时放一个函数等待下一次UI循环前执行
"""
from typing import Callable,Tuple,Any
from silky_stream.utils import namespace_manager as nm

def anext_tick(function:Callable[[Any],None],parameters:Tuple[Any]):
    """
    将要执行的内容放入异步回调队列中
    因为streamlit默认不支持异步回调
    并且有时候不仅仅是操作UI后需要回调，自己部分的功能需要手动回调。
    """
    artl_list:list = nm.get_namespace_key("app","data","async_rerun_task")
    artl_list.append((function,parameters))

def next_tick(function:Callable[[Any],None],parameters:Tuple[Any]):
    rtl_list:list = nm.get_namespace_key("app","data","sync_rerun_task")
    rtl_list.append((function,parameters))
