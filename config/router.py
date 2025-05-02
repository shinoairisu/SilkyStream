"""此处编写路由"""

from components.example_sub_ui import SubUI1
from silky_stream.utils.stream_router import Router,RouterInfo


subui1_info = RouterInfo(SubUI1,"ui1","ui1_mq",key="test1").add_param("name",str,"火烈鸟")
subui2_info = RouterInfo(SubUI1,"ui2","ui2_mq",key="test2").add_param("name",str,"苏浩")


router = Router(root="router").add_router("index",subui1_info).add_router("subui2",subui2_info)