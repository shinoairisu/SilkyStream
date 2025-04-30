"""站点入口"""

import asyncio
import streamlit as st
from dotenv import load_dotenv

load_dotenv("./config/.env", verbose=True)  # 载入配置文件


async def main():
    """异步"""
    if not st.session_state.get("main_thread_anchor", None):
        st.session_state["main_thread_anchor"] = True
        st.session_state["async_rerun_task"] = []  # 由next_tick打上来的可异步操作
        st.session_state["sync_rerun_task"] = []  # 由next_tick打上来的同步操作
    if async_tasks := st.session_state.get("async_rerun_task"):
        """搞定所有由next_tick打上来的可异步操作"""
        real_task = [
            async_task(*async_task_params)
            for async_task, async_task_params in async_tasks
        ]
        await asyncio.gather(*real_task)  # 把上次要执行的都执行完
        st.session_state.get("async_rerun_task").clear()
    if sync_tasks := st.session_state.get("sync_rerun_task"):
        """搞定所有由next_tick打上来的同步操作"""
        for sync_task, sync_task_params in sync_tasks:
            sync_task(*sync_task_params)
        st.session_state.get("sync_rerun_task").clear()

    await SPAPageUI(...).rander()  # 渲染主页


if __name__ == "__main__":
    asyncio.run(main())
