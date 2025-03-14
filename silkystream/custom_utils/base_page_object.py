"""数据模型继承本类进行数据检查"""
class BasePage(object):
    def data_validation(self):
        for attr in dir(self):
            if attr.startswith(("data_")) and getattr(self,attr) is None:
                raise ValueError("数据模型中不可存在None")
