import streamlit as st

st.write(st.query_params.get_all("aa"))

if st.button("点我"):
    st.query_params["aa"] = 2