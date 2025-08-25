# Instagram Account Creator API

API tự động tạo tài khoản Instagram sử dụng ADB để điều khiển thiết bị Android.

## Yêu cầu hệ thống

- Python 3.7+
- ADB (Android Debug Bridge)
- Thiết bị Android với USB Debugging được bật
- Ứng dụng Instagram đã được cài đặt trên thiết bị

## Cài đặt

1. Clone hoặc tải dự án về máy
2. Cài đặt các package cần thiết:
   ```bash
   pip install -r requirements.txt
   ```

## Khởi động API

### Cách 1: Sử dụng script khởi động
```bash
python start_api.py
```

### Cách 2: Chạy trực tiếp
```bash
python api.py
```

API sẽ chạy tại: `http://localhost:5000`

## API Endpoints

### 1. Tạo tài khoản mới
- **Endpoint**: `POST /api/create-account`
- **Mô tả**: Bắt đầu quá trình tạo tài khoản Instagram mới
- **Response**:
  ```json
  {
    "success": true,
    "message": "Đã bắt đầu quá trình tạo tài khoản",
    "status": {
      "is_running": true,
      "start_time": "2024-01-01T10:00:00",
      "progress": "Đang khởi tạo...",
      "result": null,
      "error": null
    }
  }
  ```

### 2. Kiểm tra trạng thái
- **Endpoint**: `GET /api/status`
- **Mô tả**: Kiểm tra trạng thái quá trình tạo tài khoản
- **Response**:
  ```json
  {
    "success": true,
    "status": {
      "is_running": false,
      "start_time": "2024-01-01T10:00:00",
      "progress": "Hoàn thành",
      "result": {
        "email": "abcde1234@taphoaneil.com",
        "password": "AbCdE1234@",
        "created_at": "2024-01-01T10:05:00",
        "otp_link": "https://api.taphoaneil.com/get-otp?to=abcde1234@taphoaneil.com"
      },
      "error": null
    }
  }
  ```

### 3. Lấy danh sách tài khoản
- **Endpoint**: `GET /api/accounts`
- **Mô tả**: Lấy danh sách tất cả tài khoản đã tạo
- **Response**:
  ```json
  {
    "success": true,
    "accounts": [
      {
        "email": "abcde1234@taphoaneil.com",
        "password": "AbCdE1234@",
        "otp_link": "https://api.taphoaneil.com/get-otp?to=abcde1234@taphoaneil.com",
        "created_at": "10:05 01/01"
      }
    ],
    "total": 1
  }
  ```

### 4. Kiểm tra sức khỏe
- **Endpoint**: `GET /api/health`
- **Mô tả**: Kiểm tra trạng thái hoạt động của API
- **Response**:
  ```json
  {
    "success": true,
    "message": "Service đang hoạt động bình thường",
    "timestamp": "2024-01-01T10:00:00"
  }
  ```

## Cách sử dụng

### 1. Sử dụng curl

```bash
# Tạo tài khoản mới
curl -X POST http://localhost:5000/api/create-account

# Kiểm tra trạng thái
curl http://localhost:5000/api/status

# Lấy danh sách tài khoản
curl http://localhost:5000/api/accounts
```

### 2. Sử dụng Python

```python
import requests
import time

# Tạo tài khoản mới
response = requests.post('http://localhost:5000/api/create-account')
print(response.json())

# Theo dõi trạng thái
while True:
    status_response = requests.get('http://localhost:5000/api/status')
    status = status_response.json()['status']
    
    print(f"Trạng thái: {status['progress']}")
    
    if not status['is_running']:
        if status['result']:
            print(f"Tài khoản đã tạo: {status['result']['email']}")
        elif status['error']:
            print(f"Lỗi: {status['error']}")
        break
    
    time.sleep(5)  # Chờ 5 giây trước khi kiểm tra lại
```

## Lưu ý

- Chỉ có thể chạy một quá trình tạo tài khoản tại một thời điểm
- Thiết bị Android phải được kết nối và bật USB Debugging
- Quá trình tạo tài khoản có thể mất 2-5 phút tùy thuộc vào tốc độ mạng
- Tài khoản được lưu vào file `ins.txt` với format: `email|password|otp_link|timestamp`

## Xử lý lỗi

Nếu gặp lỗi, hãy kiểm tra:
1. ADB đã được cài đặt và thiết bị đã kết nối
2. Ứng dụng Instagram đã được cài đặt trên thiết bị
3. Kết nối internet ổn định
4. Thiết bị có đủ dung lượng trống

## Hỗ trợ

Nếu gặp vấn đề, vui lòng kiểm tra log trong console hoặc liên hệ để được hỗ trợ.
