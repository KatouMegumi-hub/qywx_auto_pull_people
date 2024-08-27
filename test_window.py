import pywinauto.application


def list_qywx_windows():
    try:
        # 使用正则表达式匹配企业微信窗口
        app = pywinauto.Application(backend="uia").connect(title_re=".*企业微信.*")
        windows = app.windows()

        if not windows:
            print("未找到符合条件的企业微信窗口。")
            return

        print("找到的企业微信窗口:")
        for window in windows:
            print(f"- 标题: {window.window_text()}")
            print(f"  - 类名: {window.class_name()}")
            print(f"  - 进程ID: {window.process_id()}")
            print(f"  - 位置: {window.rectangle()}")
            print()

    except pywinauto.findwindows.ElementAmbiguousError as e:
        print(f"找到多个符合条件的企业微信窗口: {e}")
    except Exception as e:
        print(f"连接企业微信窗口时发生错误: {e}")


# 调用函数
list_qywx_windows()