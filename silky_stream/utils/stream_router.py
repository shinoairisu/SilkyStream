"""
路由引擎

路由指的是通过uri里面的特殊字段，可以在网页显示不同东西的组件，是SPA核心组件之一。
SubRouter就是用于将一个组件注册进路由的
这个组件必须支持标准BaseUI组件的所有参数
"""

from typing import List, Dict

import streamlit as st
from loguru import logger

from silky_stream.baseclasses.base_ui import BaseUI


def trans_to_bool(s: str) -> bool:
    name = s.strip().lower()
    if name in ["true", "对", "right"]:
        return True
    return False


class RouterInfo(object):
    def __init__(
        self,
        ui_class,
        namespace: str,
        mq_namespace: str,
        html_id: str = None,
        html_class: str = None,
        container: str = "container",
        height: int = None,
        border: bool = None,
        key: str = None,
    ):
        """
        ui_class 是BaseUI派生类的类名，比如
        ui_class = SPAPageUI
        不是UI类的实例，是类本身。
        """
        self._ui_class = ui_class
        self._namespace = namespace
        self._mq_namespace = mq_namespace
        self._html_id = html_id
        self._html_class = html_class
        self._container = container
        self._height = height
        self._border = border
        self._key = key
        self._other_params = []
        self._other_param_dict = {}

    def add_param(
        self,
        param_name: str,
        param_type: type,
        default_value: int | float | str | None,
    ):
        """
        param_type 默认只支持int,float,str,bool,可以自定义转换器
        default_value 为None时，如果也没有uri输入，就会自动忽略此参数,不传入UI中
        """
        self._other_params.append(
            {
                "param_name": param_name,
                "param_type": param_type,
                "default_value": default_value,
            }
        )

    def _collect_params(self):
        self._namespace = (
            self._namespace
            if not st.query_params.get("namespace", "")
            else st.query_params["namespace"]
        )
        self._mq_namespace = (
            self._mq_namespace
            if not st.query_params.get("mq_namespace", "")
            else st.query_params["mq_namespace"]
        )
        self._html_id = (
            self._html_id
            if not st.query_params.get("html_id", "")
            else st.query_params["html_id"]
        )
        self._html_class = (
            self._html_class
            if not st.query_params.get_all("html_class")
            else st.query_params.get_all("html_class")
        )
        self._container = (
            self._container
            if not st.query_params.get("container", "")
            else st.query_params["container"]
        )
        self._height = (
            self._height
            if not st.query_params.get("height", "")
            else int(st.query_params["height"])
        )

        self._border = (
            self._border
            if not st.query_params.get("border", "")
            else trans_to_bool(st.query_params.get("border"))
        )
        self._key = (
            self._key if not st.query_params.get("key", "") else st.query_params["key"]
        )

        for param in self._other_params:
            if (param["default_value"] is None) and (
                st.query_params.get(param["param_name"], None) is None
            ):
                # 这种属于不必须得参数
                continue
            if par := st.query_params.get(param["param_name"], None):
                if param["param_type"] == bool:
                    self._other_param_dict[param["param_name"]] = trans_to_bool(par)
                else:
                    self._other_param_dict[param["param_name"]] = param["param_type"](
                        par
                    )

    def _init_com(self, slot=None) -> BaseUI:
        """初始化控件,返回一个BaseUI子类"""
        self._collect_params()
        ui = self._ui_class(
            namespace=self._namespace,
            mq_namespace=self._mq_namespace,
            html_id=self._html_id,
            html_class=self._html_class,
            container=self._container,
            height=self._height,
            border=self._border,
            key=self._key,
            slot=slot,
            **self._other_param_dict,
        )
        return ui


class Router(object):
    """
    路由组件
    Router
    """

    def __init__(self, root: str):
        """
        root 指的是 URL 中用来标定路由连接的参数
        http://localhost:8080/?router=hello
        以上链接的路由就是 hello
        http://localhost:8080/
        如果后面没有 router 的值，比如同上的链接，或者 router 为 index ，前往的就是标记为 index 的路由。
        index 组件建议不要有 other_params ，这样可以直接访问主页也可以用。
        """
        self.root = root
        self.router: Dict[str, RouterInfo] = {}

    async def add(self, route_path, router_info: RouterInfo):
        """
        注册一个路由对象，会自动将这个对象render用的参数变为uri参数
        """
        self.router[route_path] = router_info

    async def __call__(self, slot=None) -> BaseUI:
        """根据路由返回一个组装好的BaseUI对象"""
        root = st.query_params.get(self.root, "")
        route = root if root else "index"
        if route not in self.router:
            raise ValueError(f"路由错误！没有 {route} 路由！")
        return self.router[route]._init_com(slot=slot)
