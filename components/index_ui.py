"""主页面"""

import streamlit as st

from baseclasses.base_ui import BaseUI
from utils.eventloop_executor import anext_tick
from baseclasses.base_view_model import BaseViewModel


class ViewModel(BaseViewModel):
    def __init__(self, namespace, mq_namespace):
        super().__init__(namespace, mq_namespace)
        self._init_queue()  # 新建一个message信道
        self._init_data(key="input1", value="试试看")  # 测试一下效果

    @property
    def input1(self):
        return self._get_data("input1")

    @input1.setter
    def input1(self, value):
        self._set_data("input1", value)

    async def action_add(self):
        self.input1 += "++"


class IndexUI(BaseUI):
    def __init__(self, namespace, mq_namespace):
        super().__init__(namespace, mq_namespace)
        self.data = ViewModel(namespace, mq_namespace)

    async def render(self):
        await self.data.listen()
        with self._slot_context(self.slot):
            st.text_input("测试用的输入框", "测试用的内容")
            st.button(
                "点我添加一个 ++ ",
                on_click=anext_tick,
                args=(self.data.action_add, None),
            )
