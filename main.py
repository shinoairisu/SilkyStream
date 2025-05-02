"""站点入口"""

import asyncio

import streamlit as st
from dotenv import load_dotenv
from silky_stream.utils import namespace_manager as nm
from components.index_ui import IndexUI

load_dotenv("./config/.env", verbose=True)  # 载入配置文件

st.set_page_config(
    page_title="SilkyStream V3.0模板工程",
    layout="wide",
    initial_sidebar_state="collapsed",
)

nm.init_data("app", "namespace", {})  # 初始化同步回调队列
nm.init_data("app", "async_rerun_task", [])  # 初始化异步回调队列
nm.init_data("app", "sync_rerun_task", [])  # 初始化同步回调队列
nm.set_namespace_key("app","data","namespace",set()) # 自扫描命名空间
nm.set_namespace_key("app","data","mq_namespace",set())


async def main():
    """异步UI入口"""
    if async_tasks := nm.get_namespace_key("app", "data", "async_rerun_task"):
        # 搞定所有由next_tick打上来的可异步操作
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
        # 搞定所有由next_tick手动打上来的同步操作 (函数,(参数表)) (函数,None)
        for sync_task, sync_task_params in sync_tasks:
            if sync_task_params is None:
                sync_task()
            else:
                sync_task(*sync_task_params)
        sync_tasks.clear()  # 清空回调队列

    await IndexUI(namespace="index",mq_namespace="index_mq").render()  # 渲染主页


if __name__ == "__main__":
    asyncio.run(main())
