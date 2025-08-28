import telebot
import threading
import time
import logging
from datetime import datetime
from main import InstagramAutomation
from config import *

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

user_processes = {}

def check_user_process(func):
    def wrapper(message):
        user_id = message.from_user.id
        if user_id in user_processes and user_processes[user_id].get('is_running'):
            bot.reply_to(message, MESSAGES['process_running'])
            return
        return func(message)
    return wrapper

def create_account_async(message):
    user_id = message.from_user.id
    
    try:
        user_processes[user_id] = {
            'is_running': True,
            'start_time': time.time()
        }
        
        bot.send_message(
            message.chat.id,
            "🚀 Đang bắt đầu tạo tài khoản Instagram. Vui lòng đợi...",
            parse_mode='Markdown'
        )
        
        automation = InstagramAutomation()
        
        result = automation.run_automation_process()
        
        if result and isinstance(result, dict) and result.get('success'):
            account_info = (
                f"*TK:* `{result.get('email')}`\n\n"
                f"*MK:* `{result.get('password')}`\n\n"
                f"Link OTP: https://api.taphoaneil.com/get-otp?to={result.get('email')}\n\n"
                f"Date: {datetime.now().strftime('%H:%M %d/%m/%Y')}"
            )
            bot.send_message(message.chat.id, account_info, parse_mode='Markdown')
            logger.info(f"✅ {user_id} - {result.get('email')}")
        else:
            error_message = "Tạo tài khoản thất bại. Hãy thử lại!"
            bot.send_message(message.chat.id, error_message, parse_mode='Markdown')
            logger.error(f"❌ {user_id}")
            
    except Exception as e:
        error_message = f"Lỗi: {str(e)}"
        bot.send_message(message.chat.id, error_message, parse_mode='Markdown')
        logger.error(f"❌ {user_id} - {e}")
        
    finally:
        if user_id in user_processes:
            user_processes[user_id]['is_running'] = False
            threading.Timer(300, lambda: user_processes.pop(user_id, None)).start()

@bot.message_handler(commands=['mua'])
@check_user_process
def handle_buy_command(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "User"
    logger.info(f"👤 {user_id} ({user_name}) đã yêu cầu tạo tài khoản.")
    thread = threading.Thread(target=create_account_async, args=(message,))
    thread.daemon = True
    thread.start()

def main():
    try:
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
