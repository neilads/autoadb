import telebot
import threading
import time
import logging
from datetime import datetime
from main import InstagramAutomation
from config import *

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Tạo bot instance
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Biến toàn cục để theo dõi trạng thái
user_processes = {}

# Decorator để kiểm tra xem user có đang trong quá trình tạo tài khoản không
def check_user_process(func):
    def wrapper(message):
        user_id = message.from_user.id
        if user_id in user_processes and user_processes[user_id].get('is_running'):
            bot.reply_to(message, MESSAGES['process_running'])
            return
        return func(message)
    return wrapper

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Lệnh khởi động bot"""
    bot.reply_to(message, MESSAGES['welcome'], parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def send_help(message):
    """Lệnh trợ giúp"""
    bot.reply_to(message, MESSAGES['help'], parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def check_status(message):
    """Kiểm tra trạng thái hệ thống"""
    user_id = message.from_user.id
    
    if user_id in user_processes and user_processes[user_id].get('is_running'):
        process_info = user_processes[user_id]
        start_time = process_info.get('start_time')
        elapsed = int(time.time() - start_time) if start_time else 0
        
        status_text = f"""
📊 **Trạng thái hệ thống**

🔄 **Đang chạy:** Có
⏱️ **Thời gian đã chạy:** {elapsed} giây
👤 **Người dùng:** {message.from_user.first_name}

⚠️ Vui lòng đợi quá trình hoàn thành!
        """
    else:
        status_text = """
📊 **Trạng thái hệ thống**

✅ **Hệ thống sẵn sàng**
🔄 **Đang chạy:** Không
⚡ **Có thể tạo tài khoản mới**

Gửi `/mua` để bắt đầu tạo tài khoản!
        """
    
    bot.reply_to(message, status_text, parse_mode='Markdown')

def create_account_async(message):
    """Tạo tài khoản Instagram bất đồng bộ"""
    user_id = message.from_user.id
    
    try:
        # Đánh dấu bắt đầu quá trình
        user_processes[user_id] = {
            'is_running': True,
            'start_time': time.time()
        }
        
        # Gửi thông báo bắt đầu
        bot.send_message(
            message.chat.id,
            "🚀 **Đang bắt đầu tạo tài khoản Instagram...**\n\n"
            "⏳ Quá trình này có thể mất 2-3 phút\n"
            "🔄 Vui lòng không gửi lệnh khác trong lúc này",
            parse_mode='Markdown'
        )
        
        # Tạo instance automation
        automation = InstagramAutomation()
        
        # Chạy quá trình tự động
        result = automation.run_automation_process()
        
        if result and isinstance(result, dict) and result.get('success'):
            # Tạo thông tin tài khoản
            account_info = f"""
✅ **TẠO TÀI KHOẢN THÀNH CÔNG!**

📧 **Email:** `{result.get('email')}`
🔐 **Mật khẩu:** `{result.get('password')}`
🕒 **Thời gian tạo:** {datetime.now().strftime("%H:%M %d/%m/%Y")}
🔗 **Link OTP:** [Xem OTP]({OTP_API_BASE}?to={result.get('email')})

⚠️ **Lưu ý:** Hãy lưu thông tin này cẩn thận!
            """
            
            bot.send_message(message.chat.id, account_info, parse_mode='Markdown')
            logger.info(f"Tạo tài khoản thành công cho user {user_id}: {result.get('email')}")
            
        else:
            error_message = """
❌ **TẠO TÀI KHOẢN THẤT BẠI**

🔧 **Có thể do:**
- Lỗi kết nối mạng
- Lỗi ADB/thiết bị
- Instagram chặn IP
- Lỗi hệ thống

💡 **Giải pháp:**
- Thử lại sau vài phút
- Kiểm tra kết nối mạng
- Liên hệ admin nếu lỗi liên tục
            """
            bot.send_message(message.chat.id, error_message, parse_mode='Markdown')
            logger.error(f"Tạo tài khoản thất bại cho user {user_id}")
            
    except Exception as e:
        error_message = f"""
💥 **LỖI HỆ THỐNG**

❌ **Chi tiết lỗi:** {str(e)}

🔧 **Hành động:**
- Thử lại sau vài phút
- Liên hệ admin nếu lỗi liên tục

📝 **Lỗi đã được ghi nhận và sẽ được khắc phục**
        """
        bot.send_message(message.chat.id, error_message, parse_mode='Markdown')
        logger.error(f"Lỗi khi tạo tài khoản cho user {user_id}: {e}")
        
    finally:
        # Đánh dấu hoàn thành
        if user_id in user_processes:
            user_processes[user_id]['is_running'] = False
            # Xóa thông tin sau 5 phút
            threading.Timer(300, lambda: user_processes.pop(user_id, None)).start()

@bot.message_handler(commands=['mua'])
@check_user_process
def handle_buy_command(message):
    """Xử lý lệnh /mua để tạo tài khoản"""
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "User"
    
    logger.info(f"User {user_id} ({user_name}) yêu cầu tạo tài khoản")
    
    # Gửi thông báo xác nhận
    confirm_message = f"""
🛒 **XÁC NHẬN TẠO TÀI KHOẢN**

👤 **Người yêu cầu:** {user_name}
🕒 **Thời gian:** {datetime.now().strftime("%H:%M %d/%m/%Y")}

⚡ **Sẽ tự động tạo:**
- Email ngẫu nhiên (@{EMAIL_DOMAIN})
- Mật khẩu mạnh
- Tên Việt Nam ngẫu nhiên
- Năm sinh ngẫu nhiên (1985-2005)

🚀 **Đang khởi động quá trình...**
    """
    
    bot.reply_to(message, confirm_message, parse_mode='Markdown')
    
    # Chạy tạo tài khoản trong thread riêng
    thread = threading.Thread(target=create_account_async, args=(message,))
    thread.daemon = True
    thread.start()

@bot.message_handler(func=lambda message: True)
def handle_unknown_message(message):
    """Xử lý tin nhắn không xác định"""
    bot.reply_to(message, MESSAGES['unknown_command'], parse_mode='Markdown')

def main():
    """Hàm chính để chạy bot"""
    try:
        logger.info("🤖 Đang khởi động Telegram Bot...")
        logger.info(f"📧 Email domain: {EMAIL_DOMAIN}")
        logger.info(f"🔗 OTP API: {OTP_API_BASE}")
        
        # Kiểm tra token
        if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            logger.error("❌ Vui lòng thay thế TELEGRAM_BOT_TOKEN bằng token thật của bot Telegram!")
            return
        
        # Bắt đầu polling
        logger.info("✅ Bot đã sẵn sàng! Đang lắng nghe tin nhắn...")
        bot.infinity_polling(
            timeout=BOT_CONFIG['timeout'], 
            long_polling_timeout=BOT_CONFIG['long_polling_timeout']
        )
        
    except KeyboardInterrupt:
        logger.info("🛑 Bot đã được dừng bởi người dùng")
    except Exception as e:
        logger.error(f"💥 Lỗi khi chạy bot: {e}")

if __name__ == "__main__":
    main()
