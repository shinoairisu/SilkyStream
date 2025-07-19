@echo off
@REM 前端执行脚本
call activate silkystream
streamlit run index.py --server.address 127.0.0.1 --server.port 5555