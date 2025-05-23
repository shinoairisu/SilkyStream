# SilkyStream 3

一个500行实现的MVVM异步前端框架，基于steamlit封装。

- SilkyStream 迭代到3版本是一个大更新，为一套异步低保真框架，开箱即用。
- 面向 **SPA(Single Page Application)** 设计，使用更丝滑。
- **组件、信道、路由**是SilkyStream 3的主要设计方向。

## 定位
SilkyStream 3是个规范模板，不是框架，不再像1.0那样是一个whl包安装上，导入数据类然后用。

这个版本是规范应用写法包括**代码**还有**文档**，要求所有组件构造一致，以实现：**易阅读、易扩展、易设计、易协作**。

项目包含一套高性能异步模板代码。

## 理念
- 让streamlit使用更加丝滑顺畅，尽量抵消`rerun python code`带来的不适；
- 使用流行的数据驱动模式：MVVM，代码编写更丝滑；
- 将所有任务分解为**组件、信道、路由**，通过异步特性进行实时显示、传参；
- 父子组件数据隔离，使多人协作开发更易上手；
- 完全解耦的UI渲染与数据管理，代码不再晦涩难懂；

## 效果

全异步的路由UI可以做到：

- 实时多任务显示进度
- 全项目不用换页，在一页上即可完成，不存在数据管理成本
- 异步UI，显示顺序不再是顺序执行，可以进行交错执行
- 可拆分的工程，可分为多组件开发

## 使用方法
### conda
```bash
conda create -n silkystream python=3.10
conda activate silkystream
pip install -r requirements.txt
streamlit run main.py
```
**注意：** 基于Python 3.10。3.10以上，可以删除依赖中的taskgroup。

## 细节介绍

### 配置文件
配置文件在config文件夹下的.env中，其中`debug=1`时开启DEBUG模式，会打印更多的东西，带有启动时命名空间重复自检机制。

### `main.py`

这是个项目模板，里面使用了 `SilkyStream 3.5` 大部分的功能，并且引入了`components`文件夹下的`index_ui`。

`index_ui` 一般是一个SPA的主页。只需修改这个文件即可。


### 异步事件回调引擎 `eventloop_executor.py`

这个文件是将streamlit的回调从同步改为异步的工具。

里面的`async_next_tick`主要用于“在下次循环时执行”，通常用于一个按钮点击后，callback为一个异步函数。

也支持同时放入多个函数，这些函数会全部以异步方式执行。

### 信道与数据空间管理器 `namespace_manager.py`

是所有数据、信道创建的基础。框架的整个信道架构基于本文件提供的能力。

使用框架开发时用的比较少。


### 路由引擎 `stream_router.py`

路由是SPA的灵魂，它使页面的主体可以在不换页的情况下被动态替换。

路由引擎在config下有router写了模板，全项目使用这个路由即可。

它主要是依赖url传参的方式，将注册在路由的组件渲染出来。

理论上可以注册多个路由。但是通常只需要一个路由器即可。

具体可以看源码，源码比较简单。

### 样式管理器 `style_manager.py`

默认加载了动画库 `Animate.css`

可以使用组件的key进行方便的样式设置。


### `base_ui.py`

所有UI的基类。可以参考`index_ui.py` 或者 `example_sub_ui.py`

### `base_view_model.py`

所有视图-数据模型的基类。可以参考`index_ui.py` 或者 `example_sub_ui.py`


## 注意

由于是异步框架，所以需要注意几点：
1. 每个需要异步的组件即使没有异步内容，都需要写足够多的 `await asyncio.sleep(1e-7)` 或者 `to_thread` 等异步方法，以及时释放 CPU 给别的对象。
2. `ctrl + c` 可能无法关闭服务器，此时需要刷新下浏览器，就关闭了。
3. 不可以对使用key的组件使用 while + empty 循环，这会导致重复创建大量对象，内存泄漏和报错。
4. ViewModel 的 `_set_data` 函数不仅仅可以在 on_click 中使用，也可以在组件渲染之后，对 key 进行设置，比如 `if button: self._data.xxx = 15` , 因为它的实现用了 `next_tick` 和 `st.rerun`。
5. 导入多余html，比如 css ，在快速点击按钮时会导致网页闪烁，因为加载太多东西。除非必要，否则不要用。
