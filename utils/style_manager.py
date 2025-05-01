"""样式管理器，主要是用于css设置"""

def load_animate_css():
    with open("/static/css/animate.min.css","r",encoding="utf-8") as f:
        acss = f.read()


def set_style_by_id(html_id):
    pass

def set_style_by_class(html_class):
    pass

def set_style_by_tag(html_tag):
    pass