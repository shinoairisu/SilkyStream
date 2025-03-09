"""处理各种类型"""

from .enhanced_param_types import BaseItem, AutoUpdateBaseItem


class TypeTools(object):
    @staticmethod
    def list2item(list_obj):
        """将list转换为baseitem"""
        return [BaseItem(i) for i in list_obj]

    @staticmethod
    def list2watchitem(list_obj, func):
        """如果数组成员是一个个字典的话，不需要包裹成baseitem。
        如有需要可以包裹成AutoUpdateBaseItem用于监视深层对象变化"""
        return [AutoUpdateBaseItem(i, func) for i in list_obj]
