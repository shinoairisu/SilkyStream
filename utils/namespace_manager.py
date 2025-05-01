"""
命名空间管理器，管理信道、信息存储等
命名空间符号为`::`，比如`index::mq::output`
信道都是`mq`，数据都是`data`
"""

import asyncio
from typing import Any

import streamlit as st


def get_namespace_key(namespace, domain, channel):
    """
    获得一个值
    namespace 是控件的主命名空间，还会有radio_namespace是广播命名空间
    domain 是域名，比如: mq data 等，代表数据域
    channel 是信道，在data时就是一片数据存储仓库，在mq里是个消息队列
    """
    space = f"{namespace}::{domain}::{channel}"
    return st.session_state.get(space, None)


def set_namespace_key(namespace, domain, channel, value):
    """
    设置一个值
    namespace 是控件的主命名空间，还会有radio_namespace是广播命名空间
    domain 是域名，比如: mq data 等，代表数据域
    channel 是信道，在data时就是一片数据存储仓库，在mq里是个消息队列
    value 是要给这个命名空间放入的内容。
    """
    space = f"{namespace}::{domain}::{channel}"
    st.session_state[space] = value


def init_namespace_key(namespace, domain, channel, value):
    """
    初始化命名空间的值
    在类的初始化中，必须调用这个函数初始化值。
    namespace 是控件的主命名空间，还会有radio_namespace是广播命名空间
    domain 是域名，比如: mq data 等，代表数据域
    channel 是信道，在data时就是一片数据存储仓库，在mq里是个消息队列
    set初始化会导致值一直都是初始化的样子。
    """
    space = f"{namespace}::{domain}::{channel}"
    if space not in st.session_state:
        st.session_state[space] = value


def init_mq(namespace, channel) -> asyncio.Queue:
    """
    初始化一个消息队列
    namespace 是控件的主命名空间，还会有radio_namespace是广播命名空间
    channel 是信道，在mq里是个消息队列
    max_size 是异步队列的最大容量，如果到达最大容量会阻塞。如果不设置，可能生产者速度很快，就将数据全塞进去了。
    """
    init_namespace_key(namespace, "mq", channel, asyncio.Queue())
    return get_namespace_key(namespace, "mq", channel)


def init_data(namespace, key, value) -> Any:
    """
    初始化一个数据
    namespace 是控件的主命名空间，还会有radio_namespace是广播命名空间
    key 是键，也就是channel的别称
    value 是值
    返回设置的value
    """
    init_namespace_key(namespace, "data", key, value)
    return value


async def sub(namespace, channel, switch=True):
    """
    BridgeUI中可非阻塞订阅消息，直接写在for循环里即可。
    可以从消息队列中得到一个消息
    switch: 只有开启状态会接收消息
    """
    if not switch:  # 关闭订阅
        return
    # 开启订阅
    sub_queue: asyncio.Queue = get_namespace_key(namespace, "mq", channel)
    if (sub_queue is not None) and (not sub_queue.empty()):
        return await sub_queue.get()
    else:
        return None


async def pub(namespace, channel, value, switch=True):
    """
    BridgeUI中可以非阻塞发布消息
    可以给信道里发布一条消息，可以是一个元祖。
    """
    if not switch:  # 关闭发布
        return
    # 开启发布
    pub_queue: asyncio.Queue = get_namespace_key(namespace, "mq", channel)
    if pub_queue is None:
        pub_queue = init_mq(namespace, channel)
    await pub_queue.put(value)
    await asyncio.sleep(1e-3)  # 给消费者获取的时间,put的速度太快了。
