import time
import pyautogui
from pywinauto import Application, findwindows
import pyperclip
import pywinauto
import pyttsx3
from PIL import ImageGrab
import os

# 全局变量，用于保存上一次复制的内容
last_copied_text = ""


#检查当前屏幕是否显示企业微信
def find_qywx_window():
    try:
        time.sleep(2)
        # 尝试查找企业微信的主窗口 locateOnScreen 对else操作无效。
        qm_location = pyautogui.locateOnScreen('QM.jpg', confidence=0.9)
        if qm_location:
            return True
    except Exception as e:
        text = "企业微信未前置，请检查电脑是否将企业微信前置。"
        # 初始化 TTS 引擎
        engine = pyttsx3.init()
        # 设置要转换为语音的文本
        engine.say(text)
        # 播放语音
        engine.runAndWait()
        print(f"查找程序未能执行成功，请检查是否是置信度过高导致查找失效{e}")
        return False


#点击对应群名
def click_group_name():
    try:
        qm_location = pyautogui.locateOnScreen('QM.jpg', confidence=0.9)
        if qm_location:
            center_x, center_y = pyautogui.center(qm_location)
            center_x = center_x + 100
            pyautogui.moveTo(center_x, center_y, duration=0.2)
            pyautogui.click(center_x, center_y, clicks=1, button='left')
            return True
    except Exception as e:
        print(f"未能执行获取群名称程序，请检查是否是置信度过高导致查找失效{e}")
        return False


#检测点击群名后是否有弹窗
def check_pop_ups():
    try:
        tc_location = pyautogui.locateOnScreen('TC.jpg', confidence=0.8)
        if tc_location:
            center_x, center_y = pyautogui.center(tc_location)
            pyautogui.moveTo(center_x, center_y, duration=0.2)
            pyautogui.click(center_x, center_y, clicks=1, button='left')
            return True
    except Exception as e:
        print(f"当前页面无弹窗（或未能执行检测弹窗，请检查置信度是否过高导致无法检测{e}）")
        return False


#获取无法复制群名的图片
def gain_tc_group_name():
    try:
        qm_location = pyautogui.locateOnScreen('QM.jpg', confidence=0.9)
        if qm_location:
            left = qm_location.left + 68
            top = qm_location.top
            width = qm_location.width + 300
            height = qm_location.height + 5

            # 生成初始文件名
            base_filename = 'tc_group_name'
            file_extension = '.png'
            filename = f'{base_filename}{file_extension}'

            # 检查文件是否存在，如果存在则递增数字
            count = 1
            while os.path.exists(filename):
                filename = f'{base_filename}_{count}{file_extension}'
                count += 1
            # 截图并保存
            screenshot = ImageGrab.grab(bbox=(left, top, left + width, top + height))
            screenshot.save(filename)
            print(f'已保存为 {filename} 名图片')
            return True
    except Exception as e:
        print(f"未能成功保存对应无法获取群名的图片，请检查程序是否出错")
        return False


#复制获取群名并判断该群名是否为客户群
def fetch_and_check_group_name():
    global last_copied_text
    try:
        time.sleep(0.5)
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

        # 如果读取到的文本中包含这三个字段，就认为当前群聊是服务群，检测要拉人的群
        keywords = ["服务群", "交流群", "技术支持群", "技术交流"]
        if any(keyword in group_name for keyword in keywords):
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
    except Exception as e:
        print(f"未能正常获取群名，请检查程序是否出错{e}")


#查找对应添加按钮
def find_and_click_add_member_button():
    try:
        # 使用 pyautogui 定位添加成员按钮
        time.sleep(1)
        add_member_button_location = pyautogui.locateOnScreen('JH2.jpg', confidence=0.7)
        if add_member_button_location:
            # 点击添加成员按钮
            center_x, center_y = pyautogui.center(add_member_button_location)
            center_x = center_x + 20
            center_y = center_y
            pyautogui.moveTo(center_x, center_y, duration=0.2)
            pyautogui.click(center_x, center_y, clicks=1, button='left')
            return True
    except Exception as e:
        time.sleep(1)
        print(f"无法找到或点击添加成员按钮: {e}")
        return False


#定位搜索框并输入对应要添加成员名称
def dw_input_member_name():
    try:
        time.sleep(2)
        # 使用图像匹配查找搜索框
        search_box_location = pyautogui.locateOnScreen('SSK2.jpg', confidence=0.8)
        if search_box_location:
            # 点击搜索框
            center_x, center_y = pyautogui.center(search_box_location)
            center_x = center_x
            center_y = center_y
            pyautogui.moveTo(center_x, center_y, duration=0.2)
            pyautogui.click(center_x, center_y, clicks=1, button='left')
            time.sleep(2)  # 等待搜索框响应
            # 输入要拉进群的成员名称，使用模拟键盘操作，注意输入法
            pyautogui.typewrite('fuwuhaohuanan12', 0.05)
            time.sleep(2)  # 等待搜索结果出现
            return True
    except Exception as e:
        print(f"无法找到搜索框，请检查程序执行度是否过高{e}")
        return False


#检测已添加成员
def check_member_added():
    try:
        time.sleep(1)
        ytj_location = pyautogui.locateOnScreen('YTJ1.jpg', confidence=0.98)
        if ytj_location:
            time.sleep(1)
            pyautogui.hotkey("esc")
            time.sleep(1)
            pyautogui.hotkey("esc")
            pyautogui.hotkey("ctrl", "down")
            return True
    except Exception as e:
        print(f"未能检测到服务号华南2被添加执行下一步（或无法检测到服务号华南2已添加图片） {e}")
        return False


#检测未添加成员，由于定位的特殊性，无法使用if else，否则报错
def check_member_not_add():
    try:
        time.sleep(1)
        znzs_location = pyautogui.locateOnScreen('fwhhn2.jpg', confidence=0.9)
        if znzs_location:
            center_x, center_y = pyautogui.center(znzs_location)
            pyautogui.moveTo(center_x, center_y, duration=0.1)
            pyautogui.click(center_x, center_y, clicks=1, button='left')
            print("选中服务号华南2成功")
            return True
    except Exception as e:
        print("未能执行添加操作，请检查程序是否出错")
        return False


#实现点击添加操作
def add_member():
    try:
        tj_location = pyautogui.locateOnScreen('TJ.jpg', confidence=0.9)
        if tj_location:
            center_x, center_y = pyautogui.center(tj_location)
            pyautogui.moveTo(center_x, center_y, duration=0.1)
            pyautogui.click(center_x, center_y, clicks=1, button='left')
            #要注意点击后要迅速操作选则下一个群聊，否则新消息则会置顶
            pyautogui.hotkey("ctrl", "down")
            #检测是否会弹出当前群聊人数过多，要点击邀请按钮
            slgd_location = pyautogui.locateOnScreen('slgd.jpg', confidence=0.8)
            if slgd_location:
                center_x, center_y = pyautogui.center(slgd_location)
                center_x = center_x - 60
                center_y = center_y + 25
                pyautogui.moveTo(center_x, center_y, duration=0.1)
                pyautogui.click(center_x, center_y, clicks=1, button='left')
                pyautogui.click(center_x, center_y)
                return True  # 点击成功后直接返回
            print("成功添加成员，并跳转至下一群聊")
            return True
    except Exception as e:
        print(f"未能成功点击添加按钮，请检查程序是否出错 {e}")
        return False


#主程序运行
def main():
    while True:
        if find_qywx_window():
            print("企业微信已经在前端显示")
        else:
            print("企业微信未前置，请检查程序")
            continue
        if click_group_name():
            time.sleep(2)
            if check_pop_ups():
                if gain_tc_group_name():
                    print("成功获取群名称图片")
            else:
                print("执行正常获取群名称程序")
                if fetch_and_check_group_name():
                    print("当前为客户群")
                else:
                    print("当前不是客户群或者与上一次获取的群聊名称相同")
                    continue
        if find_and_click_add_member_button():
            if dw_input_member_name():
                if check_member_added():
                    print("成员已添加，跳过该群")
                    continue
                else:
                    check_member_not_add()
                    add_member()
                    continue
        else:
            print("无法定位到添加成员按钮")
            continue


if __name__ == "__main__":
    main()