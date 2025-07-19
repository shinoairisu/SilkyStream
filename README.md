# SilkyStream 4

SilkyStream 4 是在 SilkyStream 3 经历了大项目洗礼后，迭代的结果。

架构与版本3有巨大差别，包括设计哲学。

SilkyStream 4 是一个由FastAPI主导的前端项目，但是面向的是桌面端、端侧无状态用户。

本项目设计初衷仅仅就是面向家庭级（5~10人场景）的用户，其中有人必须至少拥有执行命令行命令的能力。

建议只用本项目设计低保真，然后测试无问题了，可以使用项目中的后端部分设计高保真。

## 版本

本项目要求Python版本为 `Python>=3.11`。

## 设计理念
第 4 代设计理念是在第三代的异步上加入组件化。只是提供了几个重要部件的雏形:
1. 路由：提供了一个极其简易的路由系统，可以快速地进行页面切换，无需依赖streamlit本身的page系统
2. key：所有部件使用的统一key结构为 —— 使用自身的key + 子部件的key 
3. Pydantic Class：所有组件基于Pydantic Class进行部署，方便访问
4. view参数提供页面导航，点击按钮、或者在对象新建时进行链接切换可以触发页面变化

注意：
- 所有用到 `create_task` 的地方都需要使用一个容器来固定自身
- `路由更改` 只能通过组件交互来完成，比如按一个按钮等。无法直接在代码中通过修改路由页面进行更改。
- `路由页面key` 页面的key就是他们的路由标签自身，比如 view=helloWorld，那么他的key就是helloWorld，这是全局唯一的。
- 异步前端中，`st.rerun` 是失效的。因为会被作为taskgroup的错误捕获。

## 项目执行

本项目是跨平台项目，支持 Windows、Linux、MAC等多种平台。

推荐顺序为：Centos == Ubuntu > MAC > Windows。

项目默认启动、执行脚本使用Windows的CMD。根据需要自行修改。

### 安装

安装文件是 `install.bat` 。需要根据本机情况改动。强力推荐使用conda/uv等版本管理器进行执行，防止污染环境。 在Windows下可以直接双击执行。

linux版本可以直接挪用，可交由Deepseek改写。不再赘述。

conda初始化命令为:

``` bat
conda create -n 项目名 python=3.11
```

执行本项目:

``` bat
install.bat
```

### 执行

本脚本依旧需要根据本机情况进行改动，比如裸跑的可以删除conda部分。在Windows下可以直接双击执行。

linux版本可以直接挪用，可交由Deepseek改写。不再赘述。

``` bat
run_frontend.bat
run_backend.bat
```

