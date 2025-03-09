"""数据操作函数集合，支持dict，list，set
todo:
本函数并未实现当初要求的内容。
现在想要实现的是：插入list时，watch拿到的是新旧list。

"""
from typing import Any

from silkystream.internal_utils.common_utils import update_data

class DataOperator(object):
    @staticmethod
    def data_set(obj,attr,value):
        """
        使用本函数设置int,float,complex,str,bool,tuple,abstract item
        会触发对应页面的watch函数，
        """
        update_data(obj,attr,value)
    @staticmethod
    def list_append(obj,attr,value):
        """
        data_handler_function是一个：
        func(obj,value)函数
        """
        def append(li:list,value:Any):
            li.append(value)
            return li
        update_data(obj,attr,value,data_handler_function=append) # 这个函数已经检查过数据是否正确，new_value是插入的值
    @staticmethod
    def list_insert(obj,attr,index,value):
        def insert(li:list,value):
            li.insert(value[0],value[1])
            return li
        update_data(obj,attr,(index,value),insert)
    @staticmethod
    def list_extend(obj,attr,value):
        def extend(li:list,value):
            li.extend(value)
            return li
        update_data(obj,attr,value,extend)
    @staticmethod
    def list_remove(obj,attr,value):
        def remove(li:list,value):
            li.remove(value)
            return li
        update_data(obj,attr,value,remove)
    @staticmethod
    def list_pop(obj,attr,value=-1):
        """默认pop最后一个元素"""
        def pop(li:list,value):
            li.pop(value)
            return li
        update_data(obj,attr,value,pop)
    @staticmethod
    def list_clear(obj,attr):
        def pop(li:list,_):
            li.clear()
            return li
        update_data(obj,attr,0,pop)

    