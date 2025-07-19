"""前端的主入口"""
import os
import asyncio
from typing import cast

import streamlit as st
from loguru import logger
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from frontend.router import Router

# 载入环境变量
load_dotenv(dotenv_path="config/.env", verbose=True, override=True)
# 打印日志到文件
logger.add("server.log")

st.set_page_config(page_title="SilkyStream 4.0", layout="wide", initial_sidebar_state="collapsed", menu_items=None)

# 初始化全局变量
if "global_init" not in st.session_state:
    st.session_state.global_const_init = True
    st.session_state.global_async_action = []  # 所有的异步方法放在这里执行
    st.session_state.global_const_server_name = os.environ.get("server_name", "未命名服务")

with open("index.css", "r", encoding="utf-8") as f:
    css = f.read()

# 载入自定义的css文件
st.html(f"<style>\n{css}\n</style>")


async def main():
    try:
        if st.session_state.global_async_action:
            await asyncio.gather(*st.session_state.global_async_action)
            st.session_state.global_async_action = []
        async with asyncio.TaskGroup() as t_group:
            await Router().render(t_group=t_group)
    except* Exception as eg:
        logger.info("关闭后台线程，重新执行")
        logger.error(eg.exceptions)


if __name__ == "__main__":
    asyncio.run(main())
