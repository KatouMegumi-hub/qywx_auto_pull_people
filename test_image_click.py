import pyautogui
import time

# 指定要识别的图片文件路径
time.sleep(2)
image_path = 'ZNZS.jpg'
region = (640, 237, 640, 560)
# 使用 locateOnScreen 函数进行图片识别
location = pyautogui.locateOnScreen(image_path, confidence=0.7, region=region)

# 输出识别结果并点击
if location is not None:
    print('Image found at position:', location)

    # 计算图像中心点坐标
    center_x, center_y = pyautogui.center(location)

    # 在找到的图像中心点位置点击
    pyautogui.click(center_x, center_y)
    print(f'Clicked at position: ({center_x}, {center_y})')
else:
    print('Image not found on screen. Please check the image and try again.')
