import cv2
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
    print("1. Chụp màn hình hiện tại")
    print("2. Chọn vùng template (Kéo khung chữ nhật, ấn q để chọn lại vùng)")
    print("3. Nhập tên template")

    screen = capture_screen()
    if screen is None:
        print("Không thể chụp màn hình")
        return

    window_name = 'Chọn vùng template (Kéo khung chữ nhật, ấn q để chọn lại vùng)'
    while True:
        drawing = False
        ix, iy = -1, -1
        fx, fy = -1, -1
        rect_img = screen.copy()
        selection_complete = False

        def on_mouse(event, x, y, flags, param):
            nonlocal drawing, ix, iy, fx, fy, rect_img, selection_complete
            if event == cv2.EVENT_LBUTTONDOWN:
                drawing = True
                ix, iy = x, y
                fx, fy = x, y
            elif event == cv2.EVENT_MOUSEMOVE:
                if drawing:
                    fx, fy = x, y
                    rect_img = screen.copy()
                    cv2.rectangle(rect_img, (ix, iy), (fx, fy), (0, 255, 0), 2)
            elif event == cv2.EVENT_LBUTTONUP:
                drawing = False
                fx, fy = x, y
                rect_img = screen.copy()
                cv2.rectangle(rect_img, (ix, iy), (fx, fy), (0, 255, 0), 2)
                selection_complete = True

        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(window_name, on_mouse)

        while True:
            cv2.imshow(window_name, rect_img)
            key = cv2.waitKey(50) & 0xFF
            if key == ord('q'):
                print("Bạn đã chọn lại vùng. Vui lòng kéo chọn lại.")
                cv2.destroyAllWindows()
                break
            if selection_complete:
                cv2.destroyAllWindows()
                if ix != fx and iy != fy:
                    x1, y1 = min(ix, fx), min(iy, fy)
                    x2, y2 = max(ix, fx), max(iy, fy)
                    template_name = input("Nhập tên template (không có đuôi .png): ")
                    if template_name:
                        create_template_from_region(screen, x1, y1, x2, y2, template_name)
                    return
                else:
                    print("Bạn cần kéo chọn một vùng hợp lệ. Ấn q để chọn lại.")
                    break

if __name__ == "__main__":
    interactive_template_creator()
