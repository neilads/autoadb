#!/usr/bin/env python3
"""
Ví dụ sử dụng Instagram Account Creator API
"""

import requests
import time

# Cấu hình API
API_BASE_URL = "http://localhost:3800"

def create_account():
    """Tạo tài khoản Instagram mới"""
    print("🚀 Bắt đầu tạo tài khoản Instagram...")
    
    try:
        response = requests.post(f"{API_BASE_URL}/api/create-account")
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print("✅ Đã bắt đầu quá trình tạo tài khoản")
                return True
            else:
                print(f"❌ Lỗi: {data['message']}")
                return False
        elif response.status_code == 409:
            print("⚠️  Đang có quá trình tạo tài khoản khác đang chạy")
            return False
        else:
            print(f"❌ Lỗi HTTP: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Không thể kết nối đến API. Vui lòng kiểm tra API server đã chạy chưa.")
        return False
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def monitor_progress():
    """Theo dõi tiến trình tạo tài khoản"""
    print("📊 Đang theo dõi tiến trình...")
    
    start_time = time.time()
    
    while True:
        try:
            response = requests.get(f"{API_BASE_URL}/api/status")
            
            if response.status_code == 200:
                data = response.json()
                status = data['status']
                
                elapsed_time = int(time.time() - start_time)
                print(f"⏱️  [{elapsed_time:03d}s] {status['progress']}")
                
                # Nếu quá trình đã hoàn thành
                if not status['is_running']:
                    if status['result']:
                        print("\n🎉 Tạo tài khoản thành công!")
                        print(f"📧 Email: {status['result']['email']}")
                        print(f"🔐 Password: {status['result']['password']}")
                        print(f"🔗 OTP Link: {status['result']['otp_link']}")
                        print(f"⏰ Tạo lúc: {status['result']['created_at']}")
                        return status['result']
                    elif status['error']:
                        print(f"\n❌ Quá trình thất bại: {status['error']}")
                        return None
                    else:
                        print(f"\n⚠️  Quá trình kết thúc không thành công")
                        return None
                
                time.sleep(5)
                
            else:
                print(f"❌ Lỗi khi kiểm tra trạng thái: {response.status_code}")
                break
                
        except requests.exceptions.ConnectionError:
            print("❌ Mất kết nối đến API")
            break
        except KeyboardInterrupt:
            print("\n⏹️  Người dùng dừng theo dõi")
            break
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            break
    
    return None

def get_all_accounts():
    """Lấy danh sách tất cả tài khoản đã tạo"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/accounts")
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                accounts = data['accounts']
                total = data['total']
                
                print(f"\n📋 Danh sách tài khoản ({total} tài khoản):")
                print("-" * 80)
                
                for i, account in enumerate(accounts, 1):
                    print(f"{i:2d}. Email: {account['email']}")
                    print(f"    Password: {account['password']}")
                    print(f"    Tạo lúc: {account['created_at']}")
                    print(f"    OTP Link: {account['otp_link']}")
                    print()
                
                return accounts
            else:
                print(f"❌ Lỗi: {data['message']}")
                return []
        else:
            print(f"❌ Lỗi HTTP: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return []

def check_api_health():
    """Kiểm tra trạng thái API"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API đang hoạt động bình thường")
            return True
        else:
            print(f"⚠️  API trả về status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Không thể kết nối đến API")
        return False
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def main():
    print("=" * 60)
    print("Instagram Account Creator - Client Example")
    print("=" * 60)
    
    # Kiểm tra API
    if not check_api_health():
        print("\n💡 Hướng dẫn:")
        print("1. Chạy lệnh: python start_api.py")
        print("2. Hoặc: python api.py")
        print("3. Đảm bảo API chạy tại http://localhost:5000")
        return
    
    while True:
        print("\n📋 Menu:")
        print("1. Tạo tài khoản mới")
        print("2. Xem danh sách tài khoản đã tạo")
        print("3. Kiểm tra trạng thái hiện tại")
        print("4. Thoát")
        
        try:
            choice = input("\nChọn tùy chọn (1-4): ").strip()
            
            if choice == '1':
                if create_account():
                    result = monitor_progress()
                    if result:
                        input("\nNhấn Enter để tiếp tục...")
                        
            elif choice == '2':
                get_all_accounts()
                input("Nhấn Enter để tiếp tục...")
                
            elif choice == '3':
                response = requests.get(f"{API_BASE_URL}/api/status")
                if response.status_code == 200:
                    data = response.json()
                    status = data['status']
                    print(f"\n📊 Trạng thái hiện tại:")
                    print(f"Đang chạy: {'Có' if status['is_running'] else 'Không'}")
                    print(f"Tiến trình: {status['progress']}")
                    if status['start_time']:
                        print(f"Bắt đầu lúc: {status['start_time']}")
                    if status['error']:
                        print(f"Lỗi: {status['error']}")
                else:
                    print("❌ Không thể lấy trạng thái")
                input("Nhấn Enter để tiếp tục...")
                
            elif choice == '4':
                print("👋 Tạm biệt!")
                break
                
            else:
                print("❌ Lựa chọn không hợp lệ")
                
        except KeyboardInterrupt:
            print("\n👋 Tạm biệt!")
            break
        except Exception as e:
            print(f"❌ Lỗi: {e}")

if __name__ == '__main__':
    main()
