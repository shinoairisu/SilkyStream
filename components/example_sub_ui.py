"""一个子页面样例"""

import asyncio

import streamlit as st

from silky_stream.baseclasses.base_ui import BaseUI
from silky_stream.utils.eventloop_executor import anext_tick
from silky_stream.baseclasses.base_view_model import BaseViewModel


class ViewModel(BaseViewModel):
    def __init__(self, namespace, mq_namespace, name):
        super().__init__(namespace, mq_namespace)
        self._init_queue()  # 新建一个message信道
        self._init_data(key="input1", value="试试看")  # 测试一下效果
        self.name = name

    @property
    def input1(self):
        return self._get_data("input1")

    @input1.setter
    def input1(self, value):
        self._set_data("input1", value)

    async def action_add(self):
        self.input1 += "++"

    async def action_output(self):
        await self._publish(f"点了我：{self.name}！")


class SubUI1(BaseUI):
    def __init__(
        self,
        namespace,
        mq_namespace,
        name="火烈鸟",
        slot=None,
        container="container",
        height=None,
        border=None,
        key=None,
    ):
        super().__init__(
            namespace,
            mq_namespace,
            slot,
            container,
            height,
            border,
            key,
        )
        self.data = ViewModel(namespace, mq_namespace, name=name)

    async def _update(self):
        st.markdown(f"## 看我看我！\n\n我是{self.data.name}")
        st.button(
            "发送一个消息",
            key=self._get_key("button1"),
            on_click=anext_tick,
            args=(self.data.action_output, None),
        )
