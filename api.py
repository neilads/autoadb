from flask import Flask, jsonify
import logging
from datetime import datetime
import main

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Biến toàn cục để theo dõi trạng thái
is_running = False

@app.route('/create-ins', methods=['POST'])
def create_account():
    """API endpoint để tạo tài khoản Instagram - Trả về kết quả ngay lập tức"""
    global is_running
    
    try:
        # Kiểm tra xem có quá trình nào đang chạy không
        if is_running:
            return jsonify({
                'success': False,
                'message': 'Đang có quá trình tạo tài khoản khác đang chạy'
            }), 409
        
        # Đánh dấu đang chạy
        is_running = True
        
        # Tạo tài khoản đồng bộ
        automation = main.InstagramAutomation()
        
        # Chạy quá trình tự động
        result = automation.run_automation_process()
        
        if result and isinstance(result, dict) and result.get('success'):
            # Tạo thông tin tài khoản trả về
            account_info = {
                'email': result.get('email'),
                'password': result.get('password'),
                'created_at': datetime.now().strftime("%H:%M %d/%m"),
                'otp_link': f"https://api.taphoaneil.com/get-otp?to={result.get('email')}"
            }
            
            logger.info(f"Tạo tài khoản thành công: {result.get('email')}")
            
            # Đánh dấu hoàn thành
            is_running = False
            
            # Trả về thông tin tài khoản ngay lập tức
            return jsonify({
                'success': True,
                'message': 'Tạo tài khoản thành công',
                'account': account_info
            })
            
        else:
            logger.error("Quá trình tạo tài khoản thất bại")
            is_running = False
            
            return jsonify({
                'success': False,
                'message': 'Quá trình tạo tài khoản không thành công',
                'error': 'Tạo tài khoản thất bại'
            }), 500
            
    except Exception as e:
        logger.error(f"Lỗi trong quá trình tạo tài khoản: {e}")
        is_running = False
        
        return jsonify({
            'success': False,
            'message': f'Lỗi server: {str(e)}',
            'error': str(e)
        }), 500




@app.route('/', methods=['GET'])
def home():
    """Trang chủ với thông tin API"""
    return jsonify({
        'message': 'Instagram Account Creator API',
        'version': '1.0.0',
        'endpoints': {
            'POST /create-ins': 'Tạo tài khoản Instagram mới và trả về kết quả ngay lập tức'
        }
    })

if __name__ == '__main__':
    logger.info("Đang khởi động Instagram Account Creator API...")
    logger.info("API endpoints:")
    logger.info("  POST /create-ins - Tạo tài khoản mới và trả về kết quả ngay")
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
