# SilkyStream
目的是让streamlit使用更加丝滑顺畅。
streamlit前后端分离策略，解耦UI与逻辑，减少考虑循环执行过程。
减少bug发生、加快开发速度的同时，增强代码可读性。

## 介绍
- streamlit是一个面向数据展示的开发框架，数据驱动是最适合的开发方式。
- 面向streamlit添加了一些基于数据驱动的功能，使streamlit开发更加顺畅。

## 项目功能
- 基于python的前后端分离
- 跨页的
  - 数据模型datavm
  - 输入组件与datavm的自动封装
- 数据监视器watch
- 数据访问器action
- 计算属性computed
- 快速工具：用于读写文本文件
- 全局线程锁，可以安全的操作文件、数据库
- 组件封装
  - 图按表展示
  - 大模型聊天控件
  - 增强js和css有效范围


# 详细介绍

## 快速入门

### 编写数据模型文件

### 编写UI文件

### 运行streamlit

## 约定
数据模型中尽量少出现streamlit的
初始化函数均为无参函数，应当使用loadenv等方式从配置中初始化页面。

## 数据模型
### 数据定义

### 动作
动作是用于操作数据的函数，没有特殊要求，但是为了方便阅读，通常以action_开头。
通常为数据增删改查的组合、变化。
比如：

删除书本：
```python
class TestModel():
    def __init__(self):
        self.data_books:List = ["AVA","RVR","CVC","EVE"]
        self.data_selected_book:str = "RVR"
        self.data_operator = []
    def action_delete_book(self):
        book = self.data_books.pop()
        self.data_operator.append(f"删除书本{book}")
```
其中，`action_delete_book`就是动作。动作函数通常是

### 监视函数
以`watch_属性名(旧值,新值)`为格式的函数为监视函数。它会时刻监视基础类型，如int,float,str,complex,tuple等。
在使用集合数据操作函数时，可以监视更为宽泛的数据类型。

#### 监视自定义类
仿照集合通信函数的方式编写自定义类监视器。

### 计算属性

计算属性函数对，是一对缓存函数，分别由cache_开头和com_开头。
其中，com开头的函数没有参数，是真正的计算属性。

## 增强控件
增强控件是一系列绑定了SilkyStream框架的输入控件。

所有控件的value均被model替换。model和key成为必须值，model依赖于key。

v1.0 版本包括部分常用streamlit官方控件：
- selectbox

使用它们将可以更好地发挥SilkyStream带来效率优势。
本章节将一一介绍每个控件的使用方式。

### selecbox

### 其它控件增强

本章节介绍将第三方控件纳入SilkyStream框架管控范围的方法。

# 样例代码
## 样例1