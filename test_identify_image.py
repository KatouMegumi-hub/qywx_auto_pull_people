import pyautogui
import time
from PIL import ImageGrab

# 等待2秒以便用户切换到需要的屏幕窗口
time.sleep(2)

# 指定要识别的图片文件路径
image_path = 'YTJ2.jpg'
# 这里的坐标和尺寸需根据实际情况调整
region = (640, 237, 640, 560)
# 使用locateOnScreen函数进行图片识别
location = pyautogui.locateOnScreen(image_path, confidence=0.7, region=region)

# 输出识别结果并截图保存
if location is not None:
    print('Image found at position:', location)

    # location是一个Box对象，包含left, top, width, height属性
    left, top, width, height = location.left, location.top, location.width, location.height

    # 获取屏幕截图
    screenshot = ImageGrab.grab(bbox=(left, top, left + width, top + height))

    # 保存截图到文件
    screenshot_path = 'matched_image.png'
    screenshot.save(screenshot_path)
    print(f'Screenshot saved to {screenshot_path}')
else:
    print('Image not found on screen. Please check the image and try again.')
