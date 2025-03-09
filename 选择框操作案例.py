"""本案例展示了：
数据模型使用
全局变量、全局锁使用
增强选择框使用、监视属性使用
"""
import streamlit as st
from silkystream.data_vm import DataViewModel as dvm
from silkystream.widgets.enhanced_widgets import EnhancedControl as ec
from silkystream.safe_tools import SafeTools as safe,GlobalState as gs
from typing import List

class TestModel():
    def __init__(self):
        self.data_books:List = ["AVA","RVR","CVC","EVE"]
        self.data_selected_book:str = "RVR"
        self.data_operator = []
        # 这里可以初始化全局变量锁。初始化全局变量锁必须发生在定义全局变量之前
        safe.init_locks() 
        # 初始化(定义)全局变量应当写在主页的数据模型初始化中，或者页面最前面几行。
        # 全局变量初始化最好写在init中，或者set之前。如果不初始化，则需要保证做加减乘除等操作时类型一致。
        gs.init_value("test",1) # 全局变量使用前最好先初始化。
    def action_delete_book(self):
        book = self.data_books.pop()
        self.data_operator.append(f"删除书本{book}")
    def watch_data_selected_book(self,old,new):
        print(f"书本选择变更，之前是{old},现在是{new}")
    def action_selected_book(self,num):
        print(f"现在选择的书本是：{self.data_selected_book},传入的参数是{num}")
    def action_global_add_1(self):
        """全局变量加1"""
        gs.set_value("test", gs.get_value("test") + 1) # 执行加1

tm = dvm.set_datavm("test_page",TestModel)
dvm.page_update()


# 增强控件的回调函数使用的是数据模型的字符串
ec.selectbox(label="书籍列表",model="data_selected_book",key="selector1",options=tm.data_books,on_change_str="action_selected_book",args=(186,))

st.button("删除书籍",key="delbook",on_click=tm.action_delete_book) # 普通的控件，回调函数使用的是函数指针


st.write(tm.data_operator)

st.button("全局变量加1",key="globle1",on_click=tm.action_global_add_1) # 普通的控件，回调函数使用的是函数指针
st.write(f"全局变量test内容为:{gs.get_value('test')}")