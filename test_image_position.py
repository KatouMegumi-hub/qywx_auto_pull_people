import time
import pyautogui

time.sleep(5)

# 加载要匹配的模板图片
templates = {
    'YTJ.jpg': 'YTJ.jpg',
    'YTJ1.jpg': 'YTJ1.jpg',
    'ZNZS.jpg': 'ZNZS.jpg',
    'TJ.jpg': 'TJ.jpg'
}

# 检测屏幕是否包含模板图片
for name, template_path in templates.items():
    try:
        # 使用 pyautogui 查找模板图片的位置
        location = pyautogui.locateOnScreen(template_path, confidence=0.8)

        # 如果找到了匹配的位置
        if location is not None:
            # 计算匹配度
            match_confidence = 0.8
            print(f"{name} 匹配度: {match_confidence:.2f}, 匹配位置: {location}")
        else:
            print(f"{name} 未找到匹配的图片.")
    except Exception as e:
        print(f"处理 {name} 时出现错误: {e}")