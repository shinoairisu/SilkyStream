import asyncio
from typing import List,Any

import streamlit as st
from loguru import logger
from utils import namespace_manager as nm

class BaseData(object):
    def __init__(self,namespace):
        self.namespace = namespace
    
    def _init_data(self,key,value):
        """
        组件创建
        """
        nm.init_data(self.namespace,key,value)

    def _init_queue(self,channel="massage",namespace=None):
        """
        每个组件可以创建自己的信道和公共信道
        """
        if namespace is None:
            namespace = self.namespace
        nm.init_mq(namespace,channel)
        