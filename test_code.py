import time
import pyautogui
from pywinauto import Application, findwindows
import easyocr

def find_qywx_window():
    # 尝试查找企业微信的主窗口
    while True:
        try:
            app = Application(backend="uia").connect(title_re=".*企业微信.*")
            return app
        except findwindows.ElementNotFoundError:
            print("未找到企业微信窗口，请检查是否已打开并处于前台。")
            time.sleep(5)  # 等待5秒后再次尝试

def check_group_name(window):
    # 使用 pyautogui 定位并读取群聊名称
    try:
        # 定位到企业微信图标
        qm_location = pyautogui.locateCenterOnScreen('QM.jpg', confidence=0.8)
        if qm_location:
            # 在定位到的位置右侧100像素处点击，以打开群聊信息面板
            pyautogui.click(qm_location[0] + 100, qm_location[1], clicks=1, button='left')
            time.sleep(1)  # 等待群聊信息面板打开

            # 直接从点击的位置上方截取群名称
            group_name_region = (qm_location[0] + 100, qm_location[1] - 20, 200, 20)
            # 读取群聊名称
            group_name_screenshot = pyautogui.screenshot(region=group_name_region)
            # 使用 OCR 读取文本
            reader = easyocr.Reader(['ch_sim', 'en'])
            group_name_text = reader.readtext(group_name_screenshot)
            group_name = group_name_text[0][1] if group_name_text else ""
            # 只要读取到的文本中包含“客户群”这三个字，就认为当前群聊是客户群
            if "客户群" in group_name:
                return True
            else:
                return False
        else:
            print("无法找到企业微信图标。")
            return False
    except Exception as e:
        print(f"无法获取群聊名称: {e}")
        return False

def find_and_click_add_member_button(window):
    try:
        # 使用 pyautogui 定位添加成员按钮
        add_member_button_location = pyautogui.locateOnScreen('JH2.jpg', confidence=0.7)
        if add_member_button_location:
            # 点击添加成员按钮
            pyautogui.click(add_member_button_location[0] + 58, add_member_button_location[1] + 15, clicks=1, button='left')
            return True
        else:
            print("无法找到添加成员按钮。")
            return False
    except Exception as e:
        print(f"无法找到或点击添加成员按钮: {e}")
        return False


def search_and_add_member(window, member_name):
    # 在添加成员界面搜索成员并添加
    try:
        # 使用 pyautogui 定位搜索框
        search_box_location = pyautogui.locateOnScreen('SS1.jpg', confidence=0.8)
        if search_box_location:
            # 点击搜索框
            pyautogui.click(search_box_location)
            # 输入成员名称
            pyautogui.write(member_name)
            time.sleep(1)  # 等待搜索结果出现

            # 使用 pyautogui 定位成员名称
            # 先定位代表成员存在的第一张图片
            member_exists_location_1 = pyautogui.locateOnScreen('YTJ.jpg', confidence=0.8)
            if member_exists_location_1:
                # 成员已经在群聊中，无需添加
                print(f"{member_name} 已经在当前群聊中，无需添加。")
                return False
            else:
                # 继续定位代表成员存在的第二张图片
                member_exists_location_2 = pyautogui.locateOnScreen('YTJ1.jpg', confidence=0.8)
                if member_exists_location_2:
                    # 成员已经在群聊中，无需添加
                    print(f"{member_name} 已经在当前群聊中，无需添加。")
                    return False
                else:
                    # 成员不在当前群聊中，继续添加流程
                    # 使用 pyautogui 定位成员名称
                    member_location = pyautogui.locateOnScreen('ZNZS.jpg', confidence=0.8)
                    if member_location:
                        # 点击成员名称
                        pyautogui.click(member_location)
                        # 使用 pyautogui 定位添加按钮
                        add_button_location = pyautogui.locateOnScreen('TJ.jpg', confidence=0.8)
                        if add_button_location:
                            # 点击添加按钮
                            pyautogui.click(add_button_location)
                            return True
                        else:
                            print("无法找到添加按钮。")
                            return False
                    else:
                        print(f"没有查找到到{member_name} 。")
                        return False
        else:
            print("无法找到搜索框。")
            return False
    except Exception as e:
        print(f"搜索或添加成员失败: {e}")
        return False

def main():
    app = find_qywx_window()
    if not app:
        return

    window = app.window(title_re=".*企业微信.*")
    while True:
        if check_group_name(window):
            if find_and_click_add_member_button(window):
                if search_and_add_member(window, "智能助手"):
                    print("成功添加成员智能助手到客户群。")
                else:
                    print("未能添加成员智能助手。")
            else:
                print("未能找到添加成员按钮。")
        else:
            print("当前不是客户群，跳过。")

        # 模拟选择下一个消息框的操作
        time.sleep(3)  # 等待一段时间以模拟切换操作

if __name__ == "__main__":
    main()