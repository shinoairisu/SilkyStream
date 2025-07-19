import asyncio
from typing import cast

import streamlit as st
from pydantic import BaseModel, Field


class InputModel(BaseModel):
    version: str


class InputBox:
    def __init__(self, key):
        self.key = key
        self.model = InputModel(version="3.1.0")

        if key not in st.session_state:
            st.session_state[key] = self.model
        else:
            self.model = cast(InputModel, st.session_state[key])

    async def render(self, slot, t_group: asyncio.TaskGroup):
        with slot:
            st.text_input(key=f"{self.key}_input", label="输入电话" ,placeholder="0010-0023-4478")
