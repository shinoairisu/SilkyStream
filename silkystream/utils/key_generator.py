"""各种自动key"""
class KeyGenerator(object):
    def __init__(self,key_base_name):
        self.count = 0
        self.name = key_base_name

    def get_key(self):
        self.count += 1
        return f"{self.name}_{self.count}"