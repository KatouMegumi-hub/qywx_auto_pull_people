import pyautogui
import time

time.sleep(3)
def scroll_down(amount):
    # amount 是下滑的幅度，负值表示向下滚动
    pyautogui.scroll(-amount)

# 等待一秒钟，给用户时间准备
time.sleep(1)

# 执行下滑操作，幅度为 500 像素
scroll_down(230)

