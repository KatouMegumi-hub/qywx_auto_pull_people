import pywinauto.application

def find_qywx_window():
    try:
        # 使用正则表达式匹配企业微信窗口，并指定类名为 WeWorkWindow
        app = pywinauto.Application(backend="uia").connect(
            title_re=".*企业微信.*",
            class_name="WeWorkWindow"
        )
        return app
    except pywinauto.findwindows.ElementAmbiguousError as e:
        print(f"找到多个符合条件的企业微信窗口: {e}")
        return None
    except Exception as e:
        print(f"连接企业微信窗口时发生错误: {e}")
        return None

# 调用函数
app = find_qywx_window()
if app:
    print("成功连接到企业微信窗口。")
else:
    print("未能连接到企业微信窗口。")