"""
当一个页面并不想使用复杂的datavm时，可以直接使用本仓库中的多种datavm结构，快速开发页面
"""
from dataclasses import dataclass

@dataclass
class BaseUser:
    """一个基础的用户数据类，注册用，只有id和用户名"""
    data_uid:str = "00000000" # 八位数
    data_uname:str = "小明"