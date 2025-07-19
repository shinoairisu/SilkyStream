import asyncio
from typing import cast

import streamlit as st
from pydantic import BaseModel, Field

from frontend.components.input_box import InputBox


class HelloWorldModel(BaseModel):
    version: str


class HelloWorld:
    def __init__(self, key):
        self.key = key
        self.model = HelloWorldModel(version="3.1.0")

        if key not in st.session_state:
            st.session_state[key] = self.model
        else:
            self.model = cast(HelloWorldModel, st.session_state[key])

    def action_change_version(self):
        self.model.version = "1.8.0"

    def action_change_page(self):
        st.query_params["view"] = "showInfo"


    async def render(self, t_group: asyncio.TaskGroup):
        st.title("SilkyStream V4.0")
        st.subheader(self.model.version)
        con = st.container()
        t_group.create_task(InputBox(key=self.key + "input1").render(slot=con, t_group=t_group))
        st.button("改变版本信息", on_click=self.action_change_version)
        st.button("前往另一个页面", on_click=self.action_change_page)
