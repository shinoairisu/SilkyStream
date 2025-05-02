from contextlib import contextmanager
from typing import List, TypeAlias, Literal

import streamlit as st

Container: TypeAlias = Literal["container", "empty"]


class BaseUI(object):
    def __init__(
        self,
        namespace,
        mq_namespace,
        slot=None,
        container: Container = "container",
        height: int | None = None,  # container的高度
        border: bool | None = None,  # container是否有border
        key: (
            str | None
        ) = None,  # 给container提供一个由streamlit给于的稳定标识class:st-key-你给的这个key的名字
    ):
        """
        UI不得操作数据
        namespace 是本组件私有域
        mq_namespace 是公有信道域
        slot 是本组件插槽在哪个容器下
        html_id 是本组件的html标签的id是什么
        html_class 是本组件的class是什么
        container 是自己的容器，可以是container或者empty一类的。
        每个组件都应该用容器包裹自身！
        使用一个container可以把自己锚定在UI定义时的位置，不会被挤到页面下面去。而且可以定义id和class。
        """
        self.namespace = namespace
        self.mq_namespace = mq_namespace
        self.slot = slot

        if slot is None:
            self.container = (
                st.container(height=height, border=border, key=key)
                if container == "container"
                else st.empty()
            )
        else:
            self.container = (
                slot.container(height=height, border=border, key=key)
                if container == "container"
                else slot.empty()
            )

    def _get_key(self, key: str):
        """
        使用数据key获得真实的session_state中的key
        """
        return f"{self.namespace}::data::{key}"

    @contextmanager
    def _slot_context(self, slot):
        """
        slot 是父组件给的插槽，一般是个column，也可以是别的
        用于锚定自己在页面的位置，UI定义在哪，显示在哪
        """
        if slot is None:
            with self.container:
                # self._class_and_id()
                yield
        else:
            with slot:
                with self.container:
                    # self._class_and_id()
                    yield

    async def render(self):
        """渲染UI内容基于本函数"""
        pass
