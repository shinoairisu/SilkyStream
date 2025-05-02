import streamlit as st

def aa(k,a,b,d,c):
    print(a,b,c)
    print(k,d)


f = {
    "a":15,
    "b":16,
    "c":17
}

aa(k=19,d=20,**f)