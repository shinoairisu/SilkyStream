# SilkyStream 3.0

- SilkyStream 迭代到3.0版本是一个大更新，为一套异步低保真框架，开箱即用。
- 面向**SPA(Single Page Application)**设计，使用更丝滑。
- **组件、信道、路由**是SilkyStream 3.0的灵魂。

## 定位
SilkyStream 3.0是个规范模板，不是框架，不再像1.0那样是一个whl包安装上，导入数据类然后用。

这个版本是规范应用写法包括**代码**还有**文档**，要求所有组件构造一致，以实现：**易阅读、易扩展、易设计、易协作**。

项目包含一套高性能异步模板代码，一个以SS3.0协议规范书写的组件文档。

## 理念
- 让streamlit使用更加丝滑顺畅，尽量抵消`rerun python code`带来的不适；
- 使用流行的数据驱动模式：MVVM，代码编写更丝滑；
- 将所有任务分解为**组件、信道、路由**，通过异步特性进行实时显示、传参；
- 父子组件数据隔离，使多人协作开发更易上手；
- 完全解耦的UI渲染与数据管理，代码不再晦涩难懂；

## 使用方法
### conda
```bash
conda create -n silkystream python=3.10
conda activate silkystream
pip install -r requirements.txt
streamlit run main.py
```
**注意：**基于Python 3.10。3.10以上，可以删除依赖中的taskgroup。

## 细节介绍
### 异步`call_back`和`async_next_tick`