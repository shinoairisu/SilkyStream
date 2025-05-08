"""站点入口"""

import asyncio

import streamlit as st
from dotenv import load_dotenv

from config.router import router
from components.index_ui import IndexUI
from silky_stream.utils import namespace_manager as nm
from silky_stream.utils.style_manager import load_animate_css
from silky_stream.utils.eventloop_executor import process_callback


load_dotenv("./config/.env", verbose=True)  # 载入配置文件，必选
st.set_page_config(
    page_title="SilkyStream V3.4模板工程",
    layout="wide",
    initial_sidebar_state="collapsed",
)


async def main():
    """异步UI入口"""
    nm.init_app(router=router)  # 初始化app，router是可选的
    await process_callback()  # 处理所有回调
    await load_animate_css()  # 提前load本地的动画css，可选
    await IndexUI(namespace="index", mq_namespace="index_mq").render()  # 渲染主页


if __name__ == "__main__":
    asyncio.run(main())
