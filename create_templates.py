import cv2
import numpy as np
import os
from modules.get_scr import capture_screen

def create_template_from_region(screen, x1, y1, x2, y2, template_name):
    try:
        template = screen[y1:y2, x1:x2]
        
        os.makedirs("templates", exist_ok=True)
        
        template_path = f"templates/{template_name}.png"
        cv2.imwrite(template_path, template)
        print(f"Đã tạo template: {template_path}")
        return template_path
    except Exception as e:
        print(f"Lỗi khi tạo template: {e}")
        return None

def interactive_template_creator():
    """Tạo template tương tác bằng cách click chuột"""
    print("=== CÔNG CỤ TẠO TEMPLATE ===")
    print("1. Chụp màn hình hiện tại")
    print("2. Click để chọn vùng template")
    print("3. Nhập tên template")
    
    screen = capture_screen()
    if screen is None:
        print("Không thể chụp màn hình")
        return
    
    coords = []
    window_name = 'Chọn vùng template (Click 2 điểm)'
    selection_complete = False

    def on_click(event, x, y, flags, param):
        nonlocal selection_complete
        if event == cv2.EVENT_LBUTTONDOWN:
            coords.append((x, y))
            print(f"Đã chọn điểm: ({x}, {y})")
            if len(coords) == 2:
                selection_complete = True

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window_name, on_click)
    
    print("Click 2 điểm để chọn vùng template...")
    print("Nhấn 'q' để thoát nếu cần")
    cv2.imshow(window_name, screen)
    
    while not selection_complete:
        key = cv2.waitKey(50) & 0xFF
        if key == ord('q'):
            break
    
    cv2.destroyAllWindows()
    
    if len(coords) == 2:
        x1, y1 = min(coords[0][0], coords[1][0]), min(coords[0][1], coords[1][1])
        x2, y2 = max(coords[0][0], coords[1][0]), max(coords[0][1], coords[1][1])
        
        template_name = input("Nhập tên template (không có đuôi .png): ")
        if template_name:
            create_template_from_region(screen, x1, y1, x2, y2, template_name)
    else:
        print("Cần chọn đúng 2 điểm")

if __name__ == "__main__":
    interactive_template_creator()
