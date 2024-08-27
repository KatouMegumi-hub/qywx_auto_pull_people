import pyautogui
import time

# 等待一段时间以确保窗口稳定
time.sleep(3)

screen_width, screen_height = pyautogui.size()
# 计算屏幕中心的坐标
center_x = screen_width // 2
center_y = screen_height // 2 - 500
# 模拟点击屏幕中心
pyautogui.click(center_x, center_y)
# 添加延时以观察效果
time.sleep(2)