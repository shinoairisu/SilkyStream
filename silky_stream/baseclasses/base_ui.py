from contextlib import contextmanager
from typing import TypeAlias, Literal

import streamlit as st
from silky_stream.baseclasses.base_view_model import BaseViewModel
from silky_stream.utils.namespace_manager import get_namespace_key

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
        self._namespace = namespace
        self._mq_namespace = mq_namespace
        self._slot = slot
        self._router = get_namespace_key("app", "data", "router")
        self._data: BaseViewModel | None = None
        if slot is None:  # 没有插槽的话，就使用st直属container
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
        return f"{self._namespace}::data::{key}"

    @contextmanager
    def _slot_context(self, slot):
        """
        slot 是父组件给的插槽，一般是个column，也可以是别的
        用于锚定自己在页面的位置，UI定义在哪，显示在哪
        """
        if slot is None:
            with self.container:
                yield
        else:
            with slot:
                with self.container:
                    yield

    async def _update(self):
        """
        ui渲染逻辑
        继承本类后，重写本函数
        """
        pass

    async def render(self):
        """
        渲染ui调用本函数，但是本函数不承担ui逻辑
        """
        if self._data is not None:
            await self._data.listen() # 监听所有信号
        with self._slot_context(self._slot):
            await self._update() # 绘制UI逻辑
