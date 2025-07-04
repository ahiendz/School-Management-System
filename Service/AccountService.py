from Data import data_io
import os

class AccountService:
    def __init__(self):
        pass

    def change_password(self, username, old_password, new_password, role, class_name):
        if role == "teacher":
            path = "Data/teachers_data.json"
            data = data_io.load_json_data(path=path)
        elif role == "parent":
            path = f"Data/Students/{class_name}.json"
            data = data_io.load_json_data(path=path)
        else:
            return False, "Vai trò không hợp lệ."
        if role == "teacher":
            for user in data:
                if user.get('username') == username:
                    if user.get('password') != old_password:
                        return False, "Mật khẩu cũ không đúng."
                    user['password'] = new_password
                    data_io.write_json_data(data=data, path=path)
                    return True, "Đổi mật khẩu thành công."
            return False, "Không tìm thấy tài khoản."
        elif role == "parent":
            for student in data:
                if student.get('parent_account') == username:
                    if student.get('parent_password') != old_password:
                        return False, "Mật khẩu cũ không đúng."
                    student['parent_password'] = new_password
                    data_io.write_json_data(data=data, path=path)
                    return True, "Đổi mật khẩu thành công."
            return False, "Không tìm thấy tài khoản."
    
