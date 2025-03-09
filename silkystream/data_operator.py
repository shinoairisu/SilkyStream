"""数据操作函数集合，支持dict，list，set
todo:
本函数并未实现当初要求的内容。
现在想要实现的是：插入list时，watch拿到的是新旧list。

"""
from typing import List
import streamlit as st
from silkystream.utils.common_utils import *

class DataOperator(object):
    @staticmethod
    def data_set(obj,attr,value):
        """
        使用本函数设置int,float,complex,str,bool,tuple
        会触发对应页面的watch函数，
        """
        update_data(obj,attr,value)
    @staticmethod
    def list_append(obj,attr,value):
        """数组 old 是原始数组，new 是copy和处理后的数组，这个函数还有错误，需要修改"""
        assert old_value is not None,f"属性{attr}不存在"
        assert isinstance(old_value,list),f"属性{attr}类型不是list"
        old_value:list = getattr(obj,attr)
        update_data(attr,value) # 这个函数已经检查过数据是否正确，new_value是插入的值
        old_value.append(value)
    @staticmethod
    def list_insert(obj,attr,index,value):
        old_value:list = getattr(obj,attr)
        assert old_value is not None,f"属性{attr}不存在"
        assert isinstance(old_value,list),f"属性{attr}类型不是list"
        update_data(obj,attr,ListInsert(index,value))
    @staticmethod
    def list_extend():
        pass
    @staticmethod
    def list_remove(obj,attr,value):
        old_value:list = getattr(obj,attr,None)
        assert old_value is not None,f"属性{attr}不存在"
        assert isinstance(old_value,list),f"属性{attr}类型不是list"
        update_data(obj,attr,value) # 执行监视函数,list的new_value一般是插入，或删除的内容。
        old_value.remove(value)
    @staticmethod
    def list_pop():
        pass
    @staticmethod
    def list_clear():
        pass
    