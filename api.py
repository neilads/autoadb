from flask import Flask, jsonify
import threading
import logging
from datetime import datetime
import main
import os

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Biến toàn cục để theo dõi trạng thái
current_status = {
    'is_running': False,
    'start_time': None,
    'progress': 'Chờ yêu cầu',
    'result': None,
    'error': None
}

def run_automation_async():
    """Chạy quá trình tự động tạo tài khoản trong thread riêng"""
    global current_status
    
    try:
        current_status.update({
            'is_running': True,
            'start_time': datetime.now().isoformat(),
            'progress': 'Đang khởi tạo...',
            'result': None,
            'error': None
        })
        
        automation = main.InstagramAutomation()
        
        # Cập nhật trạng thái
        current_status['progress'] = 'Đang thực hiện quá trình tạo tài khoản...'
        
        # Chạy quá trình tự động
        result = automation.run_automation_process()
        
        if result and isinstance(result, dict) and result.get('success'):
            # Lấy thông tin tài khoản đã tạo
            account_info = {
                'email': result.get('email'),
                'password': result.get('password'),
                'created_at': datetime.now().isoformat(),
                'otp_link': f"https://api.taphoaneil.com/get-otp?to={result.get('email')}"
            }
            
            current_status.update({
                'is_running': False,
                'progress': 'Hoàn thành',
                'result': account_info,
                'error': None
            })
            
            logger.info(f"Tạo tài khoản thành công: {result.get('email')}")
            
        else:
            current_status.update({
                'is_running': False,
                'progress': 'Thất bại',
                'result': None,
                'error': 'Quá trình tạo tài khoản không thành công'
            })
            
            logger.error("Quá trình tạo tài khoản thất bại")
            
    except Exception as e:
        current_status.update({
            'is_running': False,
            'progress': 'Lỗi',
            'result': None,
            'error': str(e)
        })
        
        logger.error(f"Lỗi trong quá trình tạo tài khoản: {e}")

@app.route('/api/create-account', methods=['POST'])
def create_account():
    """API endpoint để tạo tài khoản Instagram"""
    global current_status
    
    try:
        # Kiểm tra xem có quá trình nào đang chạy không
        if current_status['is_running']:
            return jsonify({
                'success': False,
                'message': 'Đang có quá trình tạo tài khoản khác đang chạy',
                'status': current_status
            }), 409
        
        # Khởi động quá trình tạo tài khoản trong thread riêng
        thread = threading.Thread(target=run_automation_async)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Đã bắt đầu quá trình tạo tài khoản',
            'status': current_status
        })
        
    except Exception as e:
        logger.error(f"Lỗi API create-account: {e}")
        return jsonify({
            'success': False,
            'message': f'Lỗi server: {str(e)}'
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """API endpoint để kiểm tra trạng thái quá trình tạo tài khoản"""
    return jsonify({
        'success': True,
        'status': current_status
    })

@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    """API endpoint để lấy danh sách tài khoản đã tạo"""
    try:
        accounts = []
        
        # Đọc file tài khoản nếu tồn tại
        if os.path.exists('ins.txt'):
            with open('ins.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split('|')
                        if len(parts) >= 4:
                            accounts.append({
                                'email': parts[0],
                                'password': parts[1],
                                'otp_link': parts[2],
                                'created_at': parts[3]
                            })
        
        return jsonify({
            'success': True,
            'accounts': accounts,
            'total': len(accounts)
        })
        
    except Exception as e:
        logger.error(f"Lỗi API get-accounts: {e}")
        return jsonify({
            'success': False,
            'message': f'Lỗi server: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """API endpoint để kiểm tra sức khỏe của service"""
    return jsonify({
        'success': True,
        'message': 'Service đang hoạt động bình thường',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/', methods=['GET'])
def home():
    """Trang chủ với thông tin API"""
    return jsonify({
        'message': 'Instagram Account Creator API',
        'version': '1.0.0',
        'endpoints': {
            'POST /api/create-account': 'Tạo tài khoản Instagram mới',
            'GET /api/status': 'Kiểm tra trạng thái quá trình tạo tài khoản',
            'GET /api/accounts': 'Lấy danh sách tài khoản đã tạo',
            'GET /api/health': 'Kiểm tra sức khỏe service'
        }
    })

if __name__ == '__main__':
    logger.info("Đang khởi động Instagram Account Creator API...")
    logger.info("API endpoints:")
    logger.info("  POST /api/create-account - Tạo tài khoản mới")
    logger.info("  GET /api/status - Kiểm tra trạng thái")
    logger.info("  GET /api/accounts - Lấy danh sách tài khoản")
    logger.info("  GET /api/health - Kiểm tra sức khỏe")
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
