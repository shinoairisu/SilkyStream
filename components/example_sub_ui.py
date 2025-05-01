"""一个子页面样例"""
import asyncio

import streamlit as st

from baseclasses.base_ui import BaseUI
from utils.eventloop_executor import anext_tick
from baseclasses.base_view_model import BaseViewModel


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
    def __init__(self, namespace, mq_namespace,slot=None,name="火烈鸟",key=None):
        super().__init__(namespace, mq_namespace,slot=slot,key=key)
        self.data = ViewModel(namespace, mq_namespace,name=name)

    async def render(self):
        await self.data.listen() # 监听关注的信道
        with self._slot_context(self.slot):
            st.markdown(f"## 看我看我！\n\n我是{self.data.name}")
            st.button("发送一个消息",key=self._get_key("button1"),on_click=anext_tick,args=(self.data.action_output,None))
            

