Tools reg Instagram sử dụng Python và Android Debug Brige bằng cách so khớp hình ảnh.

---

Workflow:
- Chụp ảnh màn hình thông qua ADB
- So khớp với template đã tạo trước đó
- Lấy toạ độ và thực hiện click

---

## Tác dụng của các file chính

### 1. `start.py`
- **Chức năng:** File khởi động chính của hệ thống.
- **Mô tả:** Cho phép lựa chọn chạy API server, Telegram Bot hoặc cả hai. Kiểm tra các yêu cầu cần thiết (thư viện, file cấu hình, ADB, thiết bị Android).
- **Cách dùng:**  
  - `python start.py --mode api` : Chỉ chạy API server  
  - `python start.py --mode bot` : Chỉ chạy Telegram Bot  
  - `python start.py --mode both` : Chạy cả hai (mặc định)

### 2. `api.py`
- **Chức năng:** Cung cấp API RESTful để tạo tài khoản Instagram.
- **Mô tả:**  
  - Endpoint chính: `POST /create-ins`  
  - Khi nhận request, sẽ tự động tạo tài khoản Instagram mới và trả về thông tin tài khoản (email, password, link OTP).
  - Có kiểm soát trạng thái để tránh tạo nhiều tài khoản cùng lúc.

### 3. `telegram_bot.py`
- **Chức năng:** Triển khai Telegram Bot để tạo tài khoản Instagram qua lệnh chat.
- **Mô tả:**  
  - Người dùng gửi lệnh `/mua` cho bot để tạo tài khoản mới.
  - Bot trả về thông tin tài khoản hoặc báo lỗi nếu có.
  - Quản lý trạng thái từng user, tránh spam lệnh.

### 4. `modules/get_scr.py`
- **Chức năng:** Hỗ trợ chụp màn hình thiết bị Android qua ADB.
- **Mô tả:**  
  - Sử dụng lệnh ADB để chụp màn hình, chuyển về dạng ảnh cho các module khác xử lý (ví dụ: kiểm tra giao diện, xác thực thao tác tự động).

### 5. `modules/make_template.py`
- **Chức năng:** Tạo template hình ảnh để phục vụ cho việc so khớp giao diện (template matching).
- **Mô tả:**  
  - Cho phép cắt, lưu lại các vùng ảnh mẫu (template) từ ảnh chụp màn hình thiết bị Android.
  - Các template này sẽ được sử dụng bởi các module khác (ví dụ: so khớp vị trí nút, kiểm tra trạng thái giao diện) để tự động thao tác chính xác hơn.
  - Hỗ trợ quá trình tự động hóa bằng cách chuẩn hóa các điểm nhận diện trên giao diện ứng dụng Instagram.

---

**Thông tin thiết bị test:**
- Hệ điều hành: Android 13
- Thiết bị: Samsung Note 9
- ROM: Custom ROM Pixel Experience

> Đã kiểm thử toàn bộ workflow trên thiết bị này.

---

**Tác giả:** Neil  
**Ngôn ngữ:** Python  
**Liên hệ:** [https://t.me/neiltopup](https://t.me/neiltopup)
