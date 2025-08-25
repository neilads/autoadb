import random
import string
import subprocess
import time
import requests
import re
import logging
from modules.name import generate_vietnamese_name
from modules.match import match_and_click
from config import *

### LOGGING ###
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

### CLASS ###
class InstagramAutomation:
    def __init__(self):
        self.email = None
        self.password = None

    ### XOÁ DỮ LIỆU INSTAGRAM ###
    def cleanup_and_exit(self, error_message=""):
        if error_message:
            logger.error(f"Lỗi: {error_message}")
        self.execute_adb_command("adb shell am force-stop com.instagram.android")
        time.sleep(1)
        self.execute_adb_command("adb shell pm clear com.instagram.android")
        time.sleep(2)
        logger.info("Đã đóng ứng dụng và xoá dữ liệu Instagram")
        return False
    
    ### THAY ĐỔI IP ###
    @staticmethod
    def initialize_session():
        try:
            response = requests.get(SESSION_URL, timeout=10)
            if response.status_code == 200:
                response_data = response.json()
                if isinstance(response_data, dict):
                    if response_data.get('result') == 'false' and response_data.get('statusCode') == '502':
                        status_message = response_data.get('status', '')
                        logger.error(f"{status_message}")
                        return False
                return True
            else:
                logger.error(f"Không thể thay đổi IP. ERROR: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Lỗi khi thay đổi IP: {e}")
            return False
    
    ### TẠO EMAIL RANDOM ###
    @staticmethod
    def generate_random_email():
        letters = ''.join(random.choices(string.ascii_lowercase, k=5))
        numbers = ''.join(random.choices(string.digits, k=4))
        email = f"{letters}{numbers}@{EMAIL_DOMAIN}"
        return email
    
    ### TẠO MẬT KHẨU RANDOM ###
    @staticmethod
    def generate_random_password():
        letters = ''.join(random.choices(string.ascii_letters, k=5))
        numbers = ''.join(random.choices(string.digits, k=4))
        password = f"{letters}{numbers}@"
        return password
    
    ### LƯU TÀI KHOẢN VÀO FILE TXT ###
    @staticmethod
    def save_account_to_txt(email, password):
        timestamp = time.strftime("%H:%M %d/%m")
        otp_link = f"{OTP_API_BASE}?to={email}"
        try:
            with open(ACCOUNTS_FILE, 'a', encoding='utf-8') as f:
                f.write(f"{email}|{password}|{otp_link}|{timestamp}\n")
        except Exception as e:
            logger.error(f"Không thể lưu tài khoản: {e}")
    
    ### LẤY MÃ OTP TỪ API ###
    @staticmethod
    def get_otp_code(email):
        for attempt in range(3):
            try:
                logger.info(f"Thử lấy mã OTP lần {attempt + 1}/3")
                response = requests.get(f"{OTP_API_BASE}?to={email}")
                if response.status_code == 200:
                    code_match = re.search(r'[0-9]{6}', response.text)
                    if code_match:
                        otp_code = code_match.group()
                        logger.info(f"Đã nhận mã OTP email: {otp_code}")
                        return otp_code
                    else:
                        logger.warning(f"Lần {attempt + 1}: Không tìm thấy mã OTP trong email")
                else:
                    logger.error(f"Lần {attempt + 1}: Không thể lấy mã OTP email.")
                
                if attempt < 1:
                    logger.info("Chờ 3 giây trước khi thử lại...")
                    time.sleep(3)
                    
            except Exception as e:
                logger.error(f"Lần {attempt + 1}: Lỗi khi lấy mã OTP email: {e}")
                if attempt < 1:
                    logger.info("Chờ 3 giây trước khi thử lại...")
                    time.sleep(3)
        logger.error("Đã thử 3 lần nhưng không thể lấy được mã OTP")
        return None
    
    ### THỰC THI LỆNH ADB ###
    @staticmethod
    def execute_adb_command(command):
        try:
            logger.debug(f"Đang thực thi lệnh ADB: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                logger.debug(f"Lệnh ADB thực thi thành công")
                return True
            else:
                logger.error(f"Lệnh ADB thất bại với mã trả về {result.returncode}")
                return False
        except Exception:
            logger.error(f"Lỗi khi thực thi lệnh ADB")
            return False
    
    ### NHẬP TEXT THÔNG QUA ADB ###
    def input_text(self, text):
        logger.debug(f"Đang nhập: {text}")
        return self.execute_adb_command(f'adb shell input text "{text}"')
    
    ### CLICK VÀ CHỜ THÔNG QUA ADB ###
    def tap_and_wait(self, x, y, delay=2):
        logger.debug(f"Đang click x={x}, y={y}, delay={delay}s")
        self.execute_adb_command(f"adb shell input tap {x} {y}")
        time.sleep(delay)
    
    ### NHẬP NĂM SINH ###
    def input_date_of_birth(self):
        self.tap_and_wait(720, 1130, 2)
        year = random.randint(1985, 2005)
        self.tap_and_wait(985, 1480, 1)
        self.input_text(str(year))
        time.sleep(1.5)
        self.tap_and_wait(1000, 1500, 1)
        self.tap_and_wait(720, 1590, 2)
        logger.info("Đã nhập năm sinh")
    
    ############################
    ### CÁC THAO TÁC ĐĂNG KÍ ###
    ############################

    def run_automation_process(self):

        ### ĐÓNG VÀ XOÁ DỮ LIỆU INSTAGRAM TRƯỚC KHI CHẠY ###
        self.execute_adb_command("adb shell am force-stop com.instagram.android")
        self.execute_adb_command("adb shell pm clear com.instagram.android")

        ### THAY ĐỔI IP ###
        if not self.initialize_session():
            logger.error("Không thể thay đổi IP. Bỏ qua bước này và tiếp tục quá trình đăng ký")
        
        ### YÊU CẦU QUYỀN ROOT ###
        if not self.execute_adb_command("adb root"):
            return self.cleanup_and_exit("Không thể yêu cầu quyền root")
        
        ### MỞ ỨNG DỤNG INSTAGRAM ###
        if not self.execute_adb_command("adb shell monkey -p com.instagram.android -c android.intent.category.LAUNCHER 1"):
            return self.cleanup_and_exit("Không thể mở ứng dụng Instagram")
        time.sleep(5)
        
        ### NHẤN NÚT TẠO TÀI KHOẢN MỚI HOẶC BẮT ĐẦU ###
        if not match_and_click("templates/taotaikhoan.png", 0.8, 3):
            return self.cleanup_and_exit("Không thể nhấn nút 'tạo tài khoản mới'")
            
        ### NHẤN NÚT ĐĂNG KÝ BẰNG EMAIL ###
        if not match_and_click("templates/dkemail.png", 0.8, 1):
            return self.cleanup_and_exit("Không thể nhấn nút 'đăng ký bằng email'")

        ### NHẤN VÀO Ô NHẬP EMAIL ###
        self.tap_and_wait(720, 920, 2)

        ### TẠO EMAIL RANDOM ###
        self.email = self.generate_random_email()
        logger.info(f"Sử dụng email: {self.email}")

        ### NHẬP EMAIL VÀO Ô NHẬP EMAIL ###
        if not self.input_text(self.email):
            return self.cleanup_and_exit("Không thể nhập email")
        
        ### ẤN TIẾP TỤC ###
        if not match_and_click("templates/tiep.png", 0.8, 3):
            return self.cleanup_and_exit("Không thể nhấn nút 'Tiếp'")
        
        ### LẤY MÃ OTP TỪ API ###
        otp_code = self.get_otp_code(self.email)
        if not otp_code:
            return self.cleanup_and_exit("Không thể lấy mã OTP")            
        if not self.input_text(otp_code):
            return self.cleanup_and_exit("Không thể nhập mã OTP")
        time.sleep(3)

        ### TẠO MẬT KHẨU RANDOM ###
        self.password = self.generate_random_password()
        if not self.input_text(self.password):
            return self.cleanup_and_exit("Không thể nhập mật khẩu")

        ### ẤN TIẾP TỤC ###
        if not match_and_click("templates/tiep.png", 0.8, 3):
            return self.cleanup_and_exit("Không thể nhấn nút 'Tiếp'")

        ### NHẤN VÀO LƯU NẾU CÓ ###
        match_and_click("templates/luu.png", 0.8, 3)

        ### NHẬP NĂM SINH ###
        self.input_date_of_birth()

        time.sleep(2)
        
        ### TẠO TÊN VIỆT NAM RANDOM ###
        name = generate_vietnamese_name()
        name_parts = name.split()
        for i, part in enumerate(name_parts):
            if not self.input_text(part):
                return self.cleanup_and_exit(f"Không thể nhập tên")
            if i < len(name_parts) - 1:
                self.execute_adb_command("adb shell input keyevent 62")

        ### ẤN TIẾP TỤC ###
        if not match_and_click("templates/tiep.png", 0.8, 3):
            return self.cleanup_and_exit("Không thể nhấn nút 'Tiếp'")

        match_and_click("templates/tiep.png", 0.8, 3)

        ### NHẤN VÀO TÔI ĐỒNG Ý ###
        if not match_and_click("templates/yes.png", 0.8, 10):
            return self.cleanup_and_exit("Không thể nhấn nút 'Tôi đồng ý'")

        ### LƯU TÀI KHOẢN VÀO FILE TXT ###
        self.save_account_to_txt(self.email, self.password)
        
        ### XOÁ DỮ LIỆU INSTAGRAM ###
        self.cleanup_and_exit()

        logger.info("Đã tạo tài khoản thành công")
        return True

    ###################################
    ### HOÀN THÀNH THAO TÁC ĐĂNG KÍ ###
    ###################################
    
def main():
    automation = InstagramAutomation()
    try:
        success = automation.run_automation_process()
        
        if success:
            logger.info("Ứng dụng hoàn thành thành công")
        else:
            logger.error("Ứng dụng không thể hoàn thành")   
    except KeyboardInterrupt:
        automation.cleanup_and_exit("Người dùng đã dừng chương trình")
    except Exception as e:
        automation.cleanup_and_exit(f"Lỗi không mong muốn: {e}")

if __name__ == "__main__":
    main()
