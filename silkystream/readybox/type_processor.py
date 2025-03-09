"""处理各种类型"""

from .enhanced_param_types import BaseItem, AutoUpdateBaseItem


class TypeTools(object):
    @staticmethod
    def list2item(list_obj):
        """将list转换为"""
        return [BaseItem(i) for i in list_obj]

    @staticmethod
    def list2watchitem(list_obj, func):
        return [AutoUpdateBaseItem(i, func) for i in list_obj]
