"""
提供快速线程锁功能，对一个变量进行全程保护
"""
from typing import Set
import threading
from loguru import logger

class SafeTools(object):
    @staticmethod
    def init_locks(lock_names:Set[str]=set()):
        """在初始化页面新建init_locks,均是全局变量。locks是只读的，不可写
        init函数有一个问题，就是必须写在主页中，而且服务器启动后，必须启动一次主页。如果不启动主页将出现问题
        lock_names 是一长串锁的名字
        """
        lock_names.add("global_variables") # 设置全局变量锁
        for lock_name in lock_names:
            if lock_name not in GlobalState._locks_dict:
                GlobalState._locks_dict[lock_name] = threading.Lock()
    @staticmethod
    def get_lock(lock_name) -> threading.Lock:
        """任意页面获取锁，如果不存在则报错，因为锁很重要！"""
        assert lock_name in GlobalState._locks_dict,f"锁{lock_name}不存在！"
        return GlobalState._locks_dict[lock_name]


class GlobalState():
    _version = "silkystream_1.0"
    _locks_dict = {}
    _global_value_dict = {}
    @staticmethod
    def init_value(key,value):
        """第一行设置全局变量应该用init
        初始化函数执行一次后再执行时无效的
        """
        try:
            glock = SafeTools.get_lock("global_variables") 
        except AssertionError as e:
            logger.error("init_value执行前必须先执行：SafeTools.init_locks")
            raise e
        with glock: # 防止同时读写导致的错误
            if key not in GlobalState._global_value_dict:
                GlobalState._global_value_dict[key] = value
    @staticmethod
    def set_value(key,value):
        """除了第一行以外都用这个"""
        glock = SafeTools.get_lock("global_variables")
        with glock: # 防止同时读写导致的错误
            GlobalState._global_value_dict[key] = value
    @staticmethod
    def get_value(key):
        """获取值"""
        glock = SafeTools.get_lock("global_variables")
        with glock: # 防止同时读写拿到脏数据
            value = GlobalState._global_value_dict.get(key,None)
        if not value:
            logger.warning("全局变量{}不存在",key)
        return value