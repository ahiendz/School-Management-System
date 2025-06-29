from Data import data_io
from models import classroom
import random

class Teacher:
    def __init__(self, name, gioitinh, age, mon, gvcn, lop_day):
        self.name = name
        self.gioitinh = gioitinh
        self.age = age
        self.mon = mon
        self.gvcn = gvcn
        self.lop_day = list() if not lop_day else lop_day

class TeacherManager:
    def __init__(self):
        self.data_path = r"Data\teachers_data.json"
        self.teacher_data = list()
        self.teacher_data_dict = data_io.load_json_data(self.data_path)
    
    def load_teacher(self):
        self.teacher_data.clear()

        for teacher in self.teacher_data_dict:
            new_teacher = Teacher(
                name = teacher['name'],
                gioitinh = teacher['gioi tinh'],
                age = teacher['age'],
                mon = teacher['mon day'],
                gvcn = teacher['gvcn lop'],
                lop_day = teacher['lop day']
            ) 
            self.teacher_data.append(new_teacher)

    def get_teacher_list(self):
        return [teacher.name for teacher in self.teacher_data]

    def get_teacher_by_name(self, teacher_name):
        for teacher in self.teacher_data:
            if teacher.name == teacher_name:
                return teacher
        return None

    def get_teacher_dict_by_name(self, teacher_name):
        for teacher in self.teacher_data_dict:
            if teacher['name'] == teacher_name:
                return teacher
        return None
    
    def get_available_teachers(self):  # hàm nảy để đưa cách dict giáo viên còn trống lên dialog  thêm clasrooom
        self.load_teacher()
        teachers = self.teacher_data

        return {
            "gvcn" : [teacher.name for teacher in teachers if not teacher.gvcn],
            "gvV" : [teacher.name for teacher in teachers if teacher.mon == "Văn" and len(teacher.lop_day) < 4],
            "gvT" : [teacher.name for teacher in teachers if teacher.mon == "Toán" and len(teacher.lop_day) < 4],
            "gvA" : [teacher.name for teacher in teachers if teacher.mon == "Anh" and len(teacher.lop_day) < 4],
            "gvK" : [teacher.name for teacher in teachers if teacher.mon == "KHTN" and len(teacher.lop_day) <4],
            
        }
    
    def update_teacher_mon_day(self, lop, teacher_dict, gvcn_lop_moi):

        self.load_teacher()
        self.teacher_data_dict = data_io.load_json_data(self.data_path)

        for teacher in teacher_dict.values():
            if teacher:
                teacher_change_data = self.get_teacher_by_name(teacher)
                teacher_change_dict = self.get_teacher_dict_by_name(teacher)

                if teacher_change_data is not None and teacher_change_dict is not None:
                    if lop not in teacher_change_data.lop_day and lop not in teacher_change_dict['lop day']:
                        teacher_change_data.lop_day.append(lop)
                        teacher_change_dict['lop day'].append(lop)
        
        if gvcn_lop_moi:
            teacher_change_data = self.get_teacher_by_name(gvcn_lop_moi)
            teacher_change_dict = self.get_teacher_dict_by_name(gvcn_lop_moi)

            if teacher_change_data is not None and teacher_change_dict is not None:
                teacher_change_data.gvcn = lop
                teacher_change_dict['gvcn lop'] = lop

        data_io.write_json_data(self.teacher_data_dict, self.data_path)

    

    def add_teacher(self, teacher_dict):
        def generate_username(existing_usernames):
            while True:
                username = f"GV{random.randint(10000, 99999)}"
                if username not in existing_usernames:
                    return username

        # Tạo username/mật khẩu mặc định
        existing_usernames = [t.get("username", "") for t in self.teacher_data_dict]
        username = generate_username(existing_usernames)
        password = "1234"

        # Gán tài khoản vào dict
        teacher_dict["username"] = username
        teacher_dict["password"] = password

        # Tạo object và lưu
        new_teacher = Teacher(
            name = teacher_dict['name'],
            gioitinh = teacher_dict['gioi tinh'],
            age = teacher_dict['age'],
            mon = teacher_dict['mon day'],
            gvcn = teacher_dict['gvcn lop'],
            lop_day= None
        )
        self.teacher_data.append(new_teacher)
        self.teacher_data_dict.append(teacher_dict)
        data_io.write_json_data(self.teacher_data_dict, self.data_path)

        if teacher_dict['gvcn lop']:
            cl = classroom.ClassroomManager()
            cl.assign_gvcn_to_class(teacher_dict["gvcn lop"], teacher_dict['name'])


    def remove_teacher(self, teacher_name):
        teacher = self.get_teacher_by_name(teacher_name)
        if teacher:
            # ✅ Update lớp học liên quan
            cl_manager = classroom.ClassroomManager()
            cl_manager.load_classrooms()

            for class_dict in cl_manager.classroom_data_dict:
                # GVCN bị xóa → null
                if class_dict.get("gvcn") == teacher_name:
                    class_dict["gvcn"] = None

                # GVBM bị xóa → null môn tương ứng
                for mon_key in ["toan", "van", "anh", "khtn"]:
                    if class_dict.get("gvbm", {}).get(mon_key) == teacher_name:
                        class_dict["gvbm"][mon_key] = None

            data_io.write_json_data(cl_manager.classroom_data_dict, cl_manager.data_path)

            self.teacher_data.remove(teacher)
            self.teacher_data_dict = [n for n in self.teacher_data_dict if n['name'] != teacher_name]
            data_io.write_json_data(self.teacher_data_dict, self.data_path)

    def edit_teacher(self, teacher_name, new_teacher_dict):
        teacher_data = self.get_teacher_by_name(teacher_name)
        teacher_dict = self.get_teacher_dict_by_name(teacher_name)

        if teacher_data and teacher_dict:
            old_gvcn_lop = teacher_data.gvcn  # Lưu lớp GVCN cũ
            new_gvcn_lop = new_teacher_dict['gvcn lop']

            # Cập nhật thông tin giáo viên
            teacher_data.name = new_teacher_dict['name']
            teacher_data.gioitinh = new_teacher_dict['gioi tinh']
            teacher_data.age = new_teacher_dict['age']
            teacher_data.mon = new_teacher_dict['mon day']
            teacher_data.gvcn = new_gvcn_lop

            teacher_dict['name'] = new_teacher_dict['name']
            teacher_dict['gioi tinh'] = new_teacher_dict['gioi tinh']
            teacher_dict['age'] = new_teacher_dict['age']
            teacher_dict['mon day'] = new_teacher_dict['mon day']
            teacher_dict['gvcn lop'] = new_gvcn_lop

            # Xử lý cập nhật lớp học nếu thay đổi GVCN
            cl_manager = classroom.ClassroomManager()
            cl_manager.load_classrooms()

            # Nếu có lớp GVCN cũ và nó khác lớp mới, xóa GVCN ở lớp cũ
            if old_gvcn_lop and old_gvcn_lop != new_gvcn_lop:
                old_class = cl_manager.get_classroom_dicty_by_class(old_gvcn_lop)
                if old_class:
                    old_class['gvcn'] = None

            # Nếu có lớp GVCN mới, cập nhật GVCN ở lớp mới
            if new_gvcn_lop:
                new_class = cl_manager.get_classroom_dicty_by_class(new_gvcn_lop)
                if new_class:
                    new_class['gvcn'] = new_teacher_dict['name']

            # Lưu lại dữ liệu lớp học
            data_io.write_json_data(cl_manager.classroom_data_dict, cl_manager.data_path)
            # Lưu lại dữ liệu giáo viên
            data_io.write_json_data(self.teacher_data_dict, self.data_path)

    def filter_teachers(self, subject, gender, gvcn_role):
        self.load_teacher()
        all_teachers = self.teacher_data

        teacher_filtered = []
        for teacher in all_teachers:
            print(teacher.name, teacher.gvcn, type(teacher.gvcn))

            if subject != "Tất cả" and teacher.mon != subject:
                continue
            if gender != "Tất cả" and teacher.gioitinh != gender:
                continue

            if gvcn_role == "Là GVCN":
                if not teacher.gvcn:
                    continue  # Không có lớp chủ nhiệm → bỏ
            elif gvcn_role == "Không Là GVCN":
                if teacher.gvcn:
                    continue  # Có lớp chủ nhiệm → bỏ

            teacher_filtered.append(teacher.name)

        return teacher_filtered
    
    def view_teacher(self, teacher_name):
        self.load_teacher()

        teacher = self.get_teacher_by_name(teacher_name)

        if not teacher:
            print("Ko thấy")
            return
        
        return teacher