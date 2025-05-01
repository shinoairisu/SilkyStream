"""此处编写路由
路由指的是通过uri里面的特殊字段，可以在网页显示不同东西的组件，是SPA核心组件之一。
工具函数to_router可以快速帮你改造你的组件，使其能够装载进路由；
但并非所有组件都能装进路由：
即它需要的参数会变成uri里面的参数。(前提是能序列化为str)
所以你的组件参数尽量全部使用str,int,float一类的。
这个功能不需要你在子组件里面进行操作。
一般来说，一个应用页面，只需要一个路由组件就够了，可以切换页面的主体即可。
streamlit只适合用于做低保真项目，所以路由实现的较为简单，但是可用。

r = Router(root="router",{
    # 配置你的hello组件路由为 http://localhost:8080/?router=hello&参数名=参数值
    "/":to_router(组件类名,{"参数名":{"required":True,"default":默认值,"type":int}}) # 默认路由
    "hello":to_router(组件类名,{"参数名":{"required":True,"default":默认值,"type":int}}) 
})

Router 在页面里才执行。此时只剩一个slot参数需要填写。

from xx import r

r(slot=xxx).render()
"""
import streamlit as st

def to_router():
    pass


class Router(object):
    """
    路由组件
    """
    pass