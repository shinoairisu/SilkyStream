"""
有概率希望一个函数在下一次UI循环时执行。
比如修改st组件key中的值等等。
rerun可以解决一部分问题，但是为了扩展使用方法
提供了next_tick函数，可以随时放一个函数等待下一次UI循环前执行
"""
import asyncio
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

async def process_callback():
    if async_tasks := nm.get_namespace_key("app", "data", "async_rerun_task"):
        # 处理由next_tick加入的可异步操作
        # 每个任务callback结构都是：
        # (函数,(参数表)) 有参数函数
        # (函数,None) 无参数函数
        real_task = []
        for async_task, async_task_params in async_tasks:
            if async_task_params is None:
                real_task.append(async_task())
            else:
                real_task.append(async_task(*async_task_params))
        await asyncio.gather(*real_task)  # 把上次要执行的都执行完
        async_tasks.clear()  # 清空回调队列

    if sync_tasks := nm.get_namespace_key("app", "data", "sync_rerun_task"):
        # 处理所有由next_tick手动加入的同步操作 (函数,(参数表)) (函数,None)
        for sync_task, sync_task_params in sync_tasks:
            if sync_task_params is None:
                sync_task()
            else:
                sync_task(*sync_task_params)
        sync_tasks.clear()  # 清空回调队列