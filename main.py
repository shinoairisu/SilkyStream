import streamlit as st
from silkystream.data_vm import DataViewModel as dvm
from silkystream.enhanced_control import EnhancedControl as ec
from typing import List

class TestModel():
    def __init__(self):
        self.data_books:List = ["AVA","RVR","CVC","EVE"]
        self.data_selected_book:str = "RVR"
        self.data_operator = []
    def delete_book(self):
        book = self.data_books.pop()
        self.data_operator.append(f"删除书本{book}")

tm = dvm.set_datavm("test_page",TestModel)

ec.selectbox("书籍列表","data_selected_book","selector1",options=tm.data_books)

st.button("删除书籍",key="delbook",on_click=tm.delete_book)

st.write(tm.data_operator)