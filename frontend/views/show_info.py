import asyncio
from typing import cast

import streamlit as st
from pydantic import BaseModel, Field


class ShowInfoModel(BaseModel):
    version: str


class ShowInfo:
    def __init__(self, key):
        self.model = ShowInfoModel(version="3.1.0")

        # 将本类的数据注入到streamlit中
        if key not in st.session_state:
            st.session_state[key] = self.model
        else:
            self.model = cast(ShowInfoModel, st.session_state[key])

    def action_change_page(self):
        st.query_params["view"] = "helloWorld"

    async def render(self, t_group: asyncio.TaskGroup):
        st.markdown("带你看一个真实的世界")
        st.button("返回主页", on_click=self.action_change_page)
