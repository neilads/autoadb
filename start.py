#!/usr/bin/env python3
"""
Script khởi động cho hệ thống tạo tài khoản Instagram
Hỗ trợ chạy API server hoặc Telegram Bot
"""

import sys
import os
import subprocess
import logging
import argparse

def setup_logging():
    """Thiết lập logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

def check_adb():
    """Kiểm tra ADB"""
    try:
        result = subprocess.run(['adb', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("✓ ADB đã được cài đặt")
            
            # Kiểm tra thiết bị
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            if 'device' in result.stdout:
                logger.info("✓ Thiết bị Android đã kết nối")
            else:
                logger.warning("⚠ Không có thiết bị Android nào được kết nối")
            return True
        else:
            logger.error("✗ ADB không hoạt động")
            return False
    except FileNotFoundError:
        logger.error("✗ ADB chưa được cài đặt hoặc không có trong PATH")
        return False

def check_requirements():
    """Kiểm tra các yêu cầu"""
    # Kiểm tra file cần thiết
    required_files = [
        'config.py',
        'main.py',
        'modules/name.py',
        'modules/match.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        logger.error(f"❌ Thiếu các file cần thiết: {', '.join(missing_files)}")
        return False
    
    # Kiểm tra thư viện cơ bản
    try:
        import requests
        import cv2
        import numpy
        logger.info("✓ Thư viện cơ bản đã được cài đặt")
    except ImportError as e:
        logger.error(f"❌ Thiếu thư viện: {e}")
        logger.error("💡 Chạy: pip install -r requirements.txt")
        return False
    
    return True

def start_api():
    """Khởi động API server"""
    logger.info("🚀 Đang khởi động API server...")
    logger.info("API sẽ chạy tại: http://localhost:3800")
    logger.info("Endpoint: POST /create-ins")
    logger.info("Nhấn Ctrl+C để dừng server")
    
    try:
        from api import app
        app.run(host='0.0.0.0', port=3800, debug=False, threaded=True)
    except KeyboardInterrupt:
        logger.info("👋 Đã dừng API server")
    except Exception as e:
        logger.error(f"❌ Lỗi khi khởi động API server: {e}")

def start_bot():
    """Khởi động Telegram Bot"""
    # Kiểm tra thư viện bot
    try:
        import telebot
        logger.info("✓ Thư viện Telegram Bot đã được cài đặt")
    except ImportError:
        logger.error("❌ Thiếu thư viện telebot")
        logger.error("💡 Chạy: pip install pyTelegramBotAPI")
        return
    
    logger.info("🚀 Đang khởi động Telegram Bot...")
    
    try:
        from telegram_bot import main
        main()
    except KeyboardInterrupt:
        logger.info("🛑 Bot đã được dừng")
    except Exception as e:
        logger.error(f"❌ Lỗi khi khởi động bot: {e}")

def start_both():
    """Khởi động cả API server và Telegram Bot"""
    import threading
    import time
    
    logger.info("🚀 Đang khởi động cả API server và Telegram Bot...")
    
    # Kiểm tra thư viện bot trước
    try:
        import telebot
        logger.info("✓ Thư viện Telegram Bot đã được cài đặt")
    except ImportError:
        logger.warning("⚠ Thiếu thư viện telebot - chỉ chạy API server")
        start_api()
        return
    
    def run_api():
        """Chạy API server trong thread riêng"""
        try:
            from api import app
            logger.info("📡 API server đang chạy tại: http://localhost:3800")
            app.run(host='0.0.0.0', port=3800, debug=False, threaded=True, use_reloader=False)
        except Exception as e:
            logger.error(f"❌ Lỗi API server: {e}")
    
    def run_bot():
        """Chạy Telegram bot trong thread riêng"""
        try:
            time.sleep(2)  # Đợi API khởi động trước
            from telegram_bot import main
            logger.info("🤖 Telegram Bot đang khởi động...")
            main()
        except Exception as e:
            logger.error(f"❌ Lỗi Telegram Bot: {e}")
    
    # Tạo và khởi động threads
    api_thread = threading.Thread(target=run_api, daemon=True)
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    
    api_thread.start()
    bot_thread.start()
    
    try:
        # Chờ cả 2 threads
        api_thread.join()
        bot_thread.join()
    except KeyboardInterrupt:
        logger.info("🛑 Đang dừng cả API server và Telegram Bot...")

def main():
    parser = argparse.ArgumentParser(description='Khởi động hệ thống tạo tài khoản Instagram')
    parser.add_argument('--mode', choices=['api', 'bot', 'both'], default='both',
                       help='Chọn chế độ: api (chỉ API), bot (chỉ Bot), both (cả hai - mặc định)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🤖 HỆ THỐNG TẠO TÀI KHOẢN INSTAGRAM")
    print("=" * 60)
    
    # Kiểm tra yêu cầu cơ bản
    if not check_requirements():
        logger.error("❌ Hệ thống chưa đáp ứng yêu cầu")
        sys.exit(1)
    
    if not check_adb():
        logger.error("❌ ADB chưa sẵn sàng")
        sys.exit(1)
    
    # Khởi động theo chế độ
    if args.mode == 'api':
        start_api()
    elif args.mode == 'bot':
        start_bot()
    else:  # both - mặc định
        start_both()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("👋 Chương trình đã được dừng")
        sys.exit(0)
    except Exception as e:
        logger.error(f"💥 Lỗi không mong muốn: {e}")
        sys.exit(1)
