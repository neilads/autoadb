import cv2
import subprocess
import time
from modules.get_scr import capture_screen

def preprocess_image(image):
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    return gray

def match_and_click(template_path, threshold=0.8, sleep_seconds=1, use_preprocessing=True):
    try:
        screen = capture_screen()
        if screen is None:
            return False
            
        template = cv2.imread(template_path)
        if template is None:
            return False
        
        if use_preprocessing:
            screen_processed = preprocess_image(screen)
            template_processed = preprocess_image(template)
        else:
            screen_processed = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY) if len(screen.shape) == 3 else screen
            template_processed = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY) if len(template.shape) == 3 else template
            
        result = cv2.matchTemplate(screen_processed, template_processed, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            h, w = template.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            
            subprocess.run(f"adb shell input tap {center_x} {center_y}", shell=True, check=True)
            time.sleep(sleep_seconds)
            print(f"Đã click template {template_path} tại ({center_x}, {center_y}) với độ tin cậy {max_val:.2f}")
            return True
        else:
            print(f"Không tìm thấy template {template_path}, độ tin cậy cao nhất: {max_val:.2f}")
            time.sleep(sleep_seconds)
            return False
            
    except Exception as e:
        print(f"Lỗi trong template matching: {e}")
        time.sleep(sleep_seconds)
        return False
