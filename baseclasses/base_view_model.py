import os
import asyncio
from typing import Any, Callable

from loguru import logger
from utils import namespace_manager as nm


class BaseViewModel(object):
    """
    负责在数据模型session_state/数据库之间上传下达，使数据驱动应用运转
    是ViewModel的基类。封装所有数据操作。数据-视图类不可以操作UI。
    """

    def __init__(self, namespace: str, mq_namespace: str):
        """
        namespace: 是本组件的私有域。这个域内所有的数据只有本组件可用。
        mq_namespace: 是信道域。通常由父组件给出，内部为本组件可用的信道。组件之间可以互相访问信道域。
        一般情况下，最好每个组件有自己的独立信道域。除非是实时组件交互，公用一个信道域。
        """
        self.namespace = namespace
        self.mq_namespace = mq_namespace
        nm_space:set = nm.get_namespace_key("app","data","namespace")
        mq_space:set = nm.get_namespace_key("app","data","mq_namespace")
        
        check = bool(int(os.environ.get("DEBUG",1)))
        if check:
            if namespace in nm_space:
                logger.error("私有namespace自检失败！重复的namespace：{}",namespace)
                raise ValueError(f"私有namespace自检失败！重复的namespace：{namespace}")
            elif namespace in mq_space:
                logger.error("私有namespace自检失败！使用的namespace为信道namespace：{}",namespace)
                raise ValueError(f"私有namespace自检失败！使用的namespace为信道namespace：{namespace}")
            elif mq_space in nm_space:
                logger.error("mq_namespace自检失败！信道namespace：{}存在于私有namespace中！",mq_namespace)
                raise ValueError(f"mq_namespace自检失败！信道namespace：{mq_namespace}存在于私有namespace中！")
            elif mq_namespace == namespace:
                logger.error("mq_namespace自检失败！私有namespace和信道namespace名称一样：{}！",namespace)
                raise ValueError(f"mq_namespace自检失败！私有namespace和信道namespace名称一样：{namespace}！")
            else:
                nm_space.add(namespace)
                mq_space.add(mq_namespace)



    def _init_data(self, key: str, value: Any):
        """
        为组件创建数据,这是streamlit的特性决定的
        初始化必须使用特殊的函数
        数据项想要和组件绑定的话，需要组件的key设置为一样的
        """
        nm.init_data(self.namespace, key, value)

    def _init_queue(self, channel: str = "message"):
        """
        每个组件可以创建自己的信道和公共信道。默认都是用message
        当namespace为None时，创建的是组件自身的信道，只用于发送不用于接收。
        """
        nm.init_mq(self.mq_namespace, channel)

    def _set_data(self, key: str, value: Any):
        """
        设置数据
        """
        nm.set_namespace_key(self.namespace, "data", key, value)

    def _get_data(self, key: str):
        """
        获取数据
        """
        return nm.get_namespace_key(self.namespace, "data", key)

    async def _publish(self, message, channel="message", namespace=None, switch=True):
        """
        默认是给mq的message信道里发消息
        switch 是否接收
        """
        if namespace is None:
            namespace = self.mq_namespace
        await nm.pub(namespace, channel, message, switch=switch)
        logger.debug("向{}的信道{}发送新消息：{}", namespace, channel, message)

    async def _on(
        self,
        namespace: str,
        acallback: Callable,
        channel: str = "message",
        timeout: float = 10.0,
        switch: bool = True,
    ) -> Any | None:
        """
        监听一个信道的消息，并执行一个回调
        本函数只执行一次。可以在while中执行实现实时异步监听。
        监听某个命名空间信道的数据，通常是子组件，或者别的组件
        timeout设置监听超时，超时返回空
        acallback是一个异步函数, 格式为：func。要有一个参数：message。
        修改数据时要不要带Lock由用户自行裁定。
        """
        try:
            message = await asyncio.wait_for(
                nm.sub(namespace=namespace, channel=channel, switch=switch),
                timeout=timeout,
            )
            logger.debug("从{}的信道{}收到新消息：{}", namespace, channel, message)
        except:
            logger.debug("{}的信道{}中，暂时消息为空")
            return
        if message is not None:
            await acallback(message)

    async def listen(self):
        """
        本函数用于整理监听所有信道，一般在UI函数的第一句，在with之前使用
        """
        pass
