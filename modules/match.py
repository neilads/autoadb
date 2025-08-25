import cv2
import numpy as np
import subprocess
import os
import time
from PIL import Image
from io import BytesIO

def preprocess_image(image):
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    # Làm mịn ảnh để giảm nhiễu
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    
    # Tăng độ tương phản
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(blurred)
    
    return enhanced

def preprocess_template(template_path):
    """
    Xử lý template trước khi so khớp
    """
    template = cv2.imread(template_path)
    if template is None:
        return None
    
    return preprocess_image(template)

def capture_screen():
    try:
        subprocess.run(
            "adb shell screencap -p /sdcard/screen.png && adb pull /sdcard/screen.png ./screen.png && adb shell rm /sdcard/screen.png",
            shell=True, check=True, capture_output=True
        )
        with open("screen.png", "rb") as f:
            img_bytes = f.read()
        os.remove("screen.png")
        image = cv2.cvtColor(np.array(Image.open(BytesIO(img_bytes))), cv2.COLOR_RGB2BGR)
        return image
    except Exception as e:
        print(f"Lỗi khi chụp màn hình: {e}")
        return None

def match_and_click(template_path, threshold=0.8, sleep_seconds=1, use_preprocessing=True):
    try:
        screen = capture_screen()
        if screen is None:
            return False
            
        template = cv2.imread(template_path)
        if template is None:
            print(f"Không thể đọc template: {template_path}")
            return False
        
        # Xử lý ảnh nếu được yêu cầu
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

def match_template_multi_scale(template_path, threshold=0.8, sleep_seconds=1, scale_range=(0.8, 1.2, 0.1)):
    """
    So khớp template với nhiều tỷ lệ khác nhau
    """
    try:
        screen = capture_screen()
        if screen is None:
            return False
            
        template = cv2.imread(template_path)
        if template is None:
            print(f"Không thể đọc template: {template_path}")
            return False
        
        # Xử lý ảnh
        screen_processed = preprocess_image(screen)
        template_processed = preprocess_image(template)
        
        best_match = None
        best_val = 0
        best_scale = 1.0
        
        # Thử với các tỷ lệ khác nhau
        for scale in np.arange(scale_range[0], scale_range[1], scale_range[2]):
            # Thay đổi kích thước template
            width = int(template_processed.shape[1] * scale)
            height = int(template_processed.shape[0] * scale)
            
            if width <= 0 or height <= 0:
                continue
                
            resized_template = cv2.resize(template_processed, (width, height))
            
            result = cv2.matchTemplate(screen_processed, resized_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val > best_val:
                best_val = max_val
                best_match = max_loc
                best_scale = scale
        
        if best_val >= threshold:
            h, w = template.shape[:2]
            center_x = best_match[0] + int(w * best_scale) // 2
            center_y = best_match[1] + int(h * best_scale) // 2
            
            subprocess.run(f"adb shell input tap {center_x} {center_y}", shell=True, check=True)
            time.sleep(sleep_seconds)
            print(f"Đã click template {template_path} tại ({center_x}, {center_y}) với độ tin cậy {best_val:.2f} (tỷ lệ: {best_scale:.2f})")
            return True
        else:
            print(f"Không tìm thấy template {template_path}, độ tin cậy cao nhất: {best_val:.2f}")
            time.sleep(sleep_seconds)
            return False
            
    except Exception as e:
        print(f"Lỗi trong multi-scale template matching: {e}")
        time.sleep(sleep_seconds)
        return False
