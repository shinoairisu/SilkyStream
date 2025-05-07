"""样式管理器，主要是用于css设置"""

import streamlit as st
from loguru import logger
import aiofiles


async def load_animate_css():
    """
    给当前网页载入 animate_css
    """
    if not getattr(st, "animate_css", None):
        async with aiofiles.open("static/css/animate.min.css", "r", encoding="utf-8") as f:
            st.animate_css = await f.read()
    st.html(f"<style>{st.animate_css}</style>") # 载入动画css 可选的


def set_html_style(style: str, html_class: str = None):
    """
    st-key-html_class名字 是组件真正的类名
    style 是 style 内部代码，不含 style标签本身
    html_class 如果为空，就是设置全局的css
    """
    if html_class:
        style = f"""
<style>
.st-key-{html_class} {{
    {style}
}}
</style>
        """.strip()
    else:
        style = f"""
<style>
    {style}
</style>
""".strip()
    st.html(style)


