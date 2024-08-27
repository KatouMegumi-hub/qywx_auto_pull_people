import time
import pyautogui
from pywinauto import Application, findwindows
import pyperclip
import pywinauto

# 全局变量，用于保存上一次复制的内容
last_copied_text = ""

def find_qywx_window():
    time.sleep(2)
    # 尝试查找企业微信的主窗口
    while True:
        try:
            app = pywinauto.Application(backend="uia").connect(
                title_re=".*企业微信.*",
                class_name="WeWorkWindow"
            )
            return app
        except findwindows.ElementNotFoundError:
            print("未找到企业微信窗口，请检查是否已打开并处于前台。")
            time.sleep(3)  # 等待3秒后再次尝试

def check_group_name(window):
    global last_copied_text
    try:
        # 定位到企业微信界面
        qm_location = pyautogui.locateCenterOnScreen('QM.jpg', confidence=0.8)
        if qm_location:
            # 在定位到的位置右侧100像素处点击，以打开群聊信息面板
            pyautogui.click(qm_location[0] + 100, qm_location[1], clicks=1, button='left')
            time.sleep(2)  # 等待群聊信息面板打开
            # 使用模拟键盘操作来复制群名称
            pyautogui.hotkey('ctrl', 'a')  # 全选文本
            time.sleep(0.5)  # 等待全选完成
            pyautogui.hotkey('ctrl', 'c')  # 复制文本
            time.sleep(0.5)  # 等待复制完成
            # 获取剪贴板的内容
            group_name = pyperclip.paste()

            # 检查是否与上次复制的内容相同
            if group_name == last_copied_text:
                print("当前群聊名称与上次相同，跳过。")
                screen_width, screen_height = pyautogui.size()
                # 计算屏幕中心的坐标
                center_x = screen_width // 2
                center_y = screen_height // 2 - 500
                # 模拟点击屏幕中心
                pyautogui.click(center_x, center_y)  # 点击屏幕中心上方500像素
                time.sleep(2)
                pyautogui.hotkey('ctrl', 'down')
                return False

            last_copied_text = group_name

            # 如果读取到的文本中包含“客户群”这三个字，就认为当前群聊是客户群，检测要拉人的群
            if "客户群" in group_name:
                return True
            else:
                print("当前不是客户群，跳过。")
                # 在这里添加点击屏幕中心和按下Ctrl+Down的操作
                screen_width, screen_height = pyautogui.size()
                # 点击屏幕中心上方500像素
                center_x = screen_width // 2
                center_y = screen_height // 2 - 500
                # 模拟点击屏幕中心
                pyautogui.click(center_x, center_y)
                time.sleep(2)
                pyautogui.hotkey('ctrl', 'down')
                return False
        else:
            print("无法找到企业微信。")
            return False
    except Exception as e:
        print(f"无法获取群聊名称: {e}")
        return False

def find_and_click_add_member_button(window):
    try:
        # 使用 pyautogui 定位添加成员按钮
        time.sleep(1)
        add_member_button_location = pyautogui.locateOnScreen('JH2.jpg', confidence=0.7)
        if add_member_button_location:
            # 点击添加成员按钮
            pyautogui.click(add_member_button_location[0] + 58, add_member_button_location[1] + 15, clicks=1, button='left')
            return True
        else:
            print("无法找到添加成员按钮。")
            time.sleep(2)
            pyautogui.hotkey('ctrl', 'down')
            return False
    except Exception as e:
        time.sleep(1)
        print(f"无法找到或点击添加成员按钮: {e}")
        return False

def input_member_name():
    # 使用图像匹配查找搜索框
    region = (640, 237, 640, 560)  # 这里的坐标和尺寸需根据实际情况调整
    search_box_location = pyautogui.locateOnScreen('SS1.jpg', confidence=0.5, region=region)
    if search_box_location:
        # 点击搜索框
        pyautogui.click(search_box_location[0] + 63, search_box_location[1] + 38, clicks=1, button='left')
        time.sleep(2)  # 等待搜索框响应
        # 输入要拉进群的成员名称，使用模拟键盘操作，注意输入法
        pyautogui.typewrite('zhinengzhushou1',0.2)
        time.sleep(2)  # 等待搜索结果出现
    else:
        print("未找到搜索框。")
        qx_location = pyautogui.locateOnScreen('QX.jpg', confidence=0.7, region=region)
        pyautogui.click(pyautogui.center(qx_location))

def check_member_exists(window, member_name):
    try:
        region = (640, 237, 640, 560)
        member_exists_location_1 = pyautogui.locateOnScreen('YTJ2.jpg', confidence=0.8, region=region)
        print("尝试定位第一张图片...")
        time.sleep(2)

        if member_exists_location_1:
            # 如果找到了第一张图片，则成员已经在群聊中
            print(f"{member_name} 已经在当前群聊中，无需添加。")
            qx_location = pyautogui.locateOnScreen('QX.jpg', confidence=0.7, region=region)
            if qx_location:
                pyautogui.click(pyautogui.center(qx_location))
                print("取消成功。")
                return True
            else:
                time.sleep(1)
                print("未找到取消按钮。")
                pyautogui.hotkey('esc')
                return False

        # 如果没有找到第一张图片，则继续定位第二张图片
        member_exists_location_2 = pyautogui.locateOnScreen('YTJ.jpg', confidence=0.8, region=region)
        print("尝试定位第二张图片...")
        time.sleep(2)

        if member_exists_location_2:
            # 如果找到了第二张图片，则成员已经在群聊中
            time.sleep(1)
            print(f"{member_name} 已经在当前群聊中，无需添加。")
            qx_location = pyautogui.locateOnScreen('QX.jpg', confidence=0.7, region=region)
            if qx_location:
                pyautogui.click(pyautogui.center(qx_location))
                print("取消成功。")
                return True
            else:
                time.sleep(0.5)
                print("未找到取消按钮。")
                pyautogui.hotkey('esc')
                return False

        # 如果两张图片都没有找到，则返回False
        return False

    except Exception as e:
        print(f"发生错误: {e}")
        return False

def add_member(window, member_name):
    try:
        region = (640, 237, 640, 560)
        time.sleep(2)
        znzs_location = pyautogui.locateOnScreen('ZNZS.jpg', confidence=0.7, region=region)
        # 输出识别结果并点击
        if znzs_location is not None:
            # 在找到的图像中心点位置点击
            time.sleep(1)
            pyautogui.click(pyautogui.center(znzs_location))
            print("选中智能助手成功。")
            # 定位添加按钮并点击
            time.sleep(2)
            tj_location = pyautogui.locateOnScreen('TJ.jpg', confidence=0.8, region=region)
            if tj_location:
                pyautogui.click(pyautogui.center(tj_location))
                print("点击添加成功。")
                return True  # 点击成功后直接返回
            else:
                print("未找到添加按钮。")
                time.sleep(0.5)
                pyautogui.hotkey('esc')
                return False
        else:
            print("未选中智能助手。")
            time.sleep(1)
            pyautogui.hotkey('esc')
            return False

    except Exception as e:
        print(f"发生错误: {e}")
        return False

def main():
    app = find_qywx_window()
    if not app:
        return

    window = app.window(title_re=".*企业微信.*")
    has_inputted_member_name = False  # 添加一个标志变量

    while True:
        if check_group_name(window):
            # 执行第一步，直到成功
            while not find_and_click_add_member_button(window):
                pass

            # 输入成员名称，仅执行一次
            if not has_inputted_member_name:
                input_member_name()
                has_inputted_member_name = True

            # 执行第二步，直到成功
            if check_member_exists(window, "智能助手"):
                print("智能助手已经在群聊中，无需添加。")
                # 重置标志变量，以便在下一次循环开始时重新输入成员名称
                has_inputted_member_name = False
                # 按下Ctrl+Down的操作
                time.sleep(2)
                pyautogui.hotkey('ctrl', 'down')  # 按下Ctrl+Down
                continue  # 如果智能助手已经存在，则直接跳回检查客户群
            else:
                #拉人的名称
                while not add_member(window, "智能助手"):
                    pass

                print("成功添加成员智能助手到客户群。")
                # 重置标志变量，以便在下一次循环开始时重新输入成员名称
                has_inputted_member_name = False
        else:
            print("当前不是客户群，跳过。")

        # 模拟选择下一个消息框的操作
        time.sleep(3)  # 等待一段时间以模拟切换操作
        has_inputted_member_name = False

    # 在这里添加点击屏幕中心和按下Ctrl+Down的操作
    screen_width, screen_height = pyautogui.size()
    # 点击屏幕中心上方500像素
    center_x = screen_width // 2
    center_y = screen_height // 2 - 500
    time.sleep(2)
    pyautogui.click(center_x, center_y)
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'down')
    # 重置标志变量，以便在下一次循环开始时重新输入成员名称
    has_inputted_member_name = False

if __name__ == "__main__":
    main()