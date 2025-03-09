import streamlit as st
from silkystream.data_vm import DataViewModel as dvm
from silkystream.enhanced_widgets import EnhancedControl as ec

class TestModel():
    def __init__(self):
        self.data_text:str = ""
    def watch_data_text(self,old,new):
        print(f"内容变更")


ts = dvm.set_datavm("page_1",data_class_name=TestModel) # 返回当前页的数据模型
st.write("""# 数据模型绑定展示
         
- 修改任何一个文本框的内容，按下回车。
         
- 所有的文本框内容都会变化，并且会打印内容变更。
         
- 数据模型与key的不同即:可以多个控件，只要控件类型相同，都可以绑定在同一个数据模型上。
         
- 比如selectbox可以与文本框绑定在同一个数据模型上，编辑文本框即修改选中内容。

- key是控件的唯一值，全局对应控件只能有唯一的key。
""")
ec.text_input(label="输入你想输入的",model="data_text",key="test1")
ec.text_input(label="输入你想输入的",model="data_text",key="test2")
ec.text_input(label="输入你想输入的",model="data_text",key="test3")
ec.text_input(label="输入你想输入的",model="data_text",key="test4")
ec.text_input(label="输入你想输入的",model="data_text",key="test5")
ec.text_input(label="输入你想输入的",model="data_text",key="test6")