import asyncio
import streamlit as st
from loguru import logger
from frontend.views.show_info import ShowInfo
from frontend.views.hello_world import HelloWorld


class Router:
    def __init__(self):
        self.index = "helloWorld"
        self.routes = {
            "helloWorld": HelloWorld,
            "showInfo": ShowInfo
        }

    async def render(self, t_group: asyncio.TaskGroup):
        if "view" not in st.query_params:
            st.query_params["view"] = self.index

        if st.query_params["view"] not in self.routes:
            st.query_params["view"] = self.index

        logger.info(f"前往页面 {st.query_params['view']}")
        route = self.routes[st.query_params["view"]](key=st.query_params["view"])
        await route.render(t_group=t_group)
