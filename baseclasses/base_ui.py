from typing import List
from contextlib import contextmanager

import streamlit as st

class BaseUI(object):
    def __init__(self,namespace,mq_namespace,slot=None,html_id:str=None,html_class:List[str]=None):
        """
        UI不得操作数据
        namespace 是本组件私有域
        mq_namespace 是公有信道域
        slot 是本组件插槽在哪个容器下
        html_id 是本组件的html标签的id是什么
        html_class 是本组件的class是什么
        """
        self.namespace = namespace
        self.mq_namespace = mq_namespace
        self.slot = slot
        self.html_id = html_id
        self.html_class = " ".join(self.html_class) if html_class else None
    
    def _class_and_id(self):
        if self.html_id is not None:
            st.markdown(f'<div id="{self.html_id}"></div>', unsafe_allow_html=True)
        elif self.html_class is not None:
            st.markdown(f'<div class="{self.html_class}"></div>', unsafe_allow_html=True)
        elif self.html_class is not None and self.html_id is not None:
            st.markdown(f'<div id="{self.html_id}" class="{self.html_class}"></div>', unsafe_allow_html=True)
        else:
            pass
    @contextmanager
    def _slot_context(self,slot):
        if slot is None:
            with st.container():
                self._class_and_id()
                yield
        else:
            with slot:
                with st.container():
                    self._class_and_id()
                    yield
    
    async def render(self):
        """渲染UI内容基于本函数"""
        pass