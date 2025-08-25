#!/usr/bin/env python3
"""
Script khởi động API Instagram Account Creator
"""

import os
import sys
import subprocess

def check_requirements():
    """Kiểm tra các yêu cầu hệ thống"""
    print("Đang kiểm tra yêu cầu hệ thống...")
    
    # Kiểm tra ADB
    try:
        result = subprocess.run(['adb', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ ADB đã được cài đặt")
        else:
            print("✗ ADB không hoạt động")
            return False
    except FileNotFoundError:
        print("✗ ADB chưa được cài đặt hoặc không có trong PATH")
        return False
    
    # Kiểm tra kết nối thiết bị
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        if 'device' in result.stdout:
            print("✓ Thiết bị Android đã kết nối")
        else:
            print("⚠ Không có thiết bị Android nào được kết nối")
            print("Vui lòng kết nối thiết bị và bật USB Debugging")
    except Exception as e:
        print(f"✗ Lỗi khi kiểm tra thiết bị: {e}")
    
    return True

def install_requirements():
    """Cài đặt các package cần thiết"""
    print("Đang cài đặt các package cần thiết...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✓ Đã cài đặt thành công các package")
        return True
    except subprocess.CalledProcessError:
        print("✗ Lỗi khi cài đặt packages")
        return False

def main():
    print("=" * 50)
    print("Instagram Account Creator API")
    print("=" * 50)
    
    # Kiểm tra yêu cầu
    if not check_requirements():
        print("\n❌ Hệ thống chưa đáp ứng yêu cầu. Vui lòng cài đặt ADB trước.")
        return
    
    # Cài đặt requirements nếu cần
    if not os.path.exists('requirements.txt'):
        print("⚠ Không tìm thấy requirements.txt")
    else:
        try:
            import flask
            print("✓ Flask đã được cài đặt")
        except ImportError:
            if not install_requirements():
                return
    
    print("\n🚀 Đang khởi động API server...")
    print("API sẽ chạy tại: http://localhost:3800")
    print("\nCác endpoints có sẵn:")
    print("  POST /api/create-account - Tạo tài khoản Instagram mới")
    print("  GET  /api/status        - Kiểm tra trạng thái")
    print("  GET  /api/accounts      - Lấy danh sách tài khoản đã tạo")
    print("  GET  /api/health        - Kiểm tra sức khỏe service")
    print("\nNhấn Ctrl+C để dừng server")
    print("-" * 50)
    
    # Khởi động API
    try:
        from api import app
        app.run(host='0.0.0.0', port=3800, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\n👋 Đã dừng API server")
    except Exception as e:
        print(f"\n❌ Lỗi khi khởi động server: {e}")

if __name__ == '__main__':
    main()
