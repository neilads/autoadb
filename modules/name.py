import random

ho = [
    "Nguyen", "Tran", "Le", "Pham", "Hoang", "Huynh", "Phan", "Vu", "Vo", "Dang",
    "Bui", "Do", "Ho", "Ngo", "Duong", "Ly", "Dinh", "Mai", "To", "Trinh",
    "Doan", "Luu", "Tang", "Ha", "Lam", "Phung", "Ta", "Chau", "Truong", "Quach",
    "Hong", "Tong", "Thai", "Doan", "Luong", "Nghiem", "Vuong", "Tu", "Dinh", "Hua"
]

ten_dem = [
    "Thi", "Van", "Hoang", "Minh", "Thanh", "Cong", "Duc", "Huu", "Van", "The",
    "Xuan", "Hong", "Thanh", "Thi", "Kim", "Ngoc", "Bao", "Gia", "Quoc", "Dinh",
    "Phuong", "Thu", "Ha", "Linh", "Thao", "Mai", "Lan", "Huong", "Nga", "Trang",
    "Yen", "Hoa", "Dung", "Huyen", "Thuy", "Tuyet", "Bich", "Diep", "Hanh", "Nhu"
]

ten = [
    "An", "Binh", "Cuong", "Dung", "Em", "Phuong", "Huong", "Lan", "Mai", "Nga",
    "Oanh", "Phuong", "Quynh", "Thao", "Uyen", "Van", "Xinh", "Yen", "Anh", "Bao",
    "Cam", "Dung", "Giang", "Ha", "Hanh", "Hoa", "Huyen", "Khanh", "Linh", "Minh",
    "Nam", "Nhi", "Phuc", "Quan", "Sinh", "Thanh", "Thi", "Thuy", "Trang", "Tuyet",
    "Vinh", "Xuan", "Yen", "An", "Binh", "Cuong", "Dung", "Em", "Phuong", "Huong"
]

def generate_vietnamese_name():
    return f"{random.choice(ho)} {random.choice(ten_dem)} {random.choice(ten)}"
