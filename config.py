### CONFIG ###
EMAIL_DOMAIN = "taphoaneil.com"
OTP_API_BASE = "https://api.taphoaneil.com/get-otp"
SESSION_URL = "LINK-XOAY-PROXY"

### TELEGRAM BOT CONFIG ###
TELEGRAM_BOT_TOKEN = "BOT_TOKEN"

BOT_CONFIG = {
    'timeout': 10,
    'long_polling_timeout': 5,
    'retry_after': 3,
    'max_retries': 3
}

MESSAGES = {
    'process_running': "⚠️ Bạn đang có một quá trình tạo tài khoản đang chạy. Vui lòng đợi hoàn thành!",
    'unknown_command': "❓ Lệnh không được nhận diện. Gửi /mua để tạo tài khoản hoặc /status để kiểm tra trạng thái."
}

ADMIN_CONFIG = {
    'admin_ids': [ADMIN_ID_TELEGRAM],
    'enable_admin_commands': True
}
