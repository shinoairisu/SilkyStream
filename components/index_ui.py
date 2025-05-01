"""主页面"""

import asyncio

import streamlit as st
from taskgroup import TaskGroup

from baseclasses.base_ui import BaseUI
from components.example_sub_ui import SubUI1
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

    async def listen(self):
        await self._on(
            namespace="sub1_mq", acallback=self.action_exchange
        )  # 监听信道sub1_mq
        await self._on(
            namespace="sub2_mq", acallback=self.action_exchange
        )  # 监听信道sub2_mq

    async def action_add(self):
        self.input1 += "++"

    async def action_exchange(self, value):
        self.input1 = value


class IndexUI(BaseUI):
    def __init__(self, namespace, mq_namespace):
        super().__init__(namespace, mq_namespace)
        self.data = ViewModel(namespace, mq_namespace)

    async def render(self):
        await self.data.listen()  # 监听关注的信道
        with self._slot_context(self.slot): # 这个最好写上，可以锚定自己在页面中的位置
            st.text_input("测试用的输入框", key=self._get_key("input1"))
            st.button(
                "点我添加一个 ++ ",
                on_click=anext_tick,
                args=(self.data.action_add, None),
            )
            # 测试使用slot进行UI挂载
            colum1, colum2 = st.columns(2)
            await SubUI1(
                namespace="sub1", mq_namespace="sub1_mq", slot=colum1, name="大公鸡",key="tester"
            ).render()
            await SubUI1(
                namespace="sub2", mq_namespace="sub2_mq", slot=colum2, name="猫猫鸡"
            ).render()

            # 测试异步UI
            async with TaskGroup() as tg:
                # 流程：先显示 markdown，然后中间对应位置才会挂载上对应的UI组件
                # 期望效果：最终是按顺序显示UI，但是中间的耗时组件可以后面再补上显示，不要只能按流程顺序走下去
                # 理论上可以做到生成一篇文章，哪个段落先生成完，就先显示哪个段落，其它的可以显示为进度条或者等待框，最后逐渐变成全文
                st.write("# 嚯嚯嚯胡")
                tg.create_task(
                    SubUI1(
                        namespace="sub3",
                        mq_namespace="sub3_mq",
                        name="苏浩",
                    ).render()
                )
                st.write("==== 他是老北京人 \n\n 但是他不喝豆汁 =====")
                tg.create_task(
                    SubUI1(
                        namespace="sub4",
                        mq_namespace="sub4_mq",
                        name="火龙果",
                    ).render()
                )
                st.write("要不要看看你在说啥")
