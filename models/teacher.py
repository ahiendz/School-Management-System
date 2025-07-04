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
    MAX_CLASS_LIMIT = 4
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
    
    def get_available_teachers(self):
        self.load_teacher()
        teachers = self.teacher_data
        return {
            "gvcn" : [teacher.name for teacher in teachers if not teacher.gvcn],
            "gvV" : [teacher.name for teacher in teachers if teacher.mon == "Văn" and len(teacher.lop_day) < self.MAX_CLASS_LIMIT],
            "gvT" : [teacher.name for teacher in teachers if teacher.mon == "Toán" and len(teacher.lop_day) < self.MAX_CLASS_LIMIT],
            "gvA" : [teacher.name for teacher in teachers if teacher.mon == "Anh" and len(teacher.lop_day) < self.MAX_CLASS_LIMIT],
            "gvK" : [teacher.name for teacher in teachers if teacher.mon == "KHTN" and len(teacher.lop_day) < self.MAX_CLASS_LIMIT],
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
                        if len(teacher_change_data.lop_day) >= self.MAX_CLASS_LIMIT:
                            raise Exception(f"Giao vien {teacher} da day du {self.MAX_CLASS_LIMIT} lop!")
                        teacher_change_data.lop_day.append(lop)
                        teacher_change_dict['lop day'].append(lop)
        if gvcn_lop_moi:
            teacher_change_data = self.get_teacher_by_name(gvcn_lop_moi)
            teacher_change_dict = self.get_teacher_dict_by_name(gvcn_lop_moi)
            if teacher_change_data is not None and teacher_change_dict is not None:
                # Chỉ cho làm GVCN 1 lớp duy nhất
                if teacher_change_data.gvcn and teacher_change_data.gvcn != lop:
                    raise Exception(f"Giao vien {gvcn_lop_moi} da la GVCN lop {teacher_change_data.gvcn}!")
                teacher_change_data.gvcn = lop
                teacher_change_dict['gvcn lop'] = lop
                # Bỏ tính năng auto thêm lớp vào danh sách lớp dạy
                # GVCN có thể không dạy lớp đó
        data_io.write_json_data(self.teacher_data_dict, self.data_path)

    def add_teacher(self, teacher_dict):
        def generate_username(existing_usernames):
            while True:
                username = f"GV{random.randint(10000, 99999)}"
                if username not in existing_usernames:
                    return username
        existing_usernames = [t.get("username", "") for t in self.teacher_data_dict]
        username = generate_username(existing_usernames)
        password = "1234"
        teacher_dict["username"] = username
        teacher_dict["password"] = password
        # Kiểm tra GVCN
        if teacher_dict['gvcn lop']:
            for t in self.teacher_data_dict:
                if t.get('gvcn lop') == teacher_dict['gvcn lop']:
                    raise Exception(f"Lop {teacher_dict['gvcn lop']} da co GVCN!")
        # Kiểm tra số lớp dạy
        if teacher_dict.get('lop day') and len(teacher_dict['lop day']) > self.MAX_CLASS_LIMIT:
            raise Exception(f"Giao vien chi duoc day toi da {self.MAX_CLASS_LIMIT} lop!")
        new_teacher = Teacher(
            name = teacher_dict['name'],
            gioitinh = teacher_dict['gioi tinh'],
            age = teacher_dict['age'],
            mon = teacher_dict['mon day'],
            gvcn = teacher_dict['gvcn lop'],
            lop_day= teacher_dict.get('lop day', [])
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
            # Không cho xóa nếu đang là GVCN
            if teacher.gvcn:
                raise Exception(f"Khong the xoa giao vien {teacher_name} vi dang la GVCN lop {teacher.gvcn}!")
            cl_manager = classroom.ClassroomManager()
            cl_manager.load_classrooms()
            for class_dict in cl_manager.classroom_data_dict:
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
            old_gvcn_lop = teacher_data.gvcn
            new_gvcn_lop = new_teacher_dict['gvcn lop']
            # Kiểm tra GVCN mới
            if new_gvcn_lop and new_gvcn_lop != old_gvcn_lop:
                for t in self.teacher_data_dict:
                    if t.get('gvcn lop') == new_gvcn_lop:
                        raise Exception(f"Lop {new_gvcn_lop} da co GVCN!")
            # Kiểm tra số lớp dạy
            if new_teacher_dict.get('lop day') and len(new_teacher_dict['lop day']) > self.MAX_CLASS_LIMIT:
                raise Exception(f"Giao vien chi duoc day toi da {self.MAX_CLASS_LIMIT} lop!")
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
            # Nếu bỏ GVCN thì xóa thông tin lớp khỏi danh sách GVCN
            if old_gvcn_lop and not new_gvcn_lop:
                teacher_data.gvcn = None
                teacher_dict['gvcn lop'] = None
            cl_manager = classroom.ClassroomManager()
            cl_manager.load_classrooms()
            if old_gvcn_lop and old_gvcn_lop != new_gvcn_lop:
                old_class = cl_manager.get_classroom_dicty_by_class(old_gvcn_lop)
                if old_class:
                    old_class['gvcn'] = None
            if new_gvcn_lop:
                new_class = cl_manager.get_classroom_dicty_by_class(new_gvcn_lop)
                if new_class:
                    new_class['gvcn'] = new_teacher_dict['name']
            data_io.write_json_data(cl_manager.classroom_data_dict, cl_manager.data_path)
            data_io.write_json_data(self.teacher_data_dict, self.data_path)

    def filter_teachers(self, subject, gender, gvcn_role):
        self.load_teacher()
        all_teachers = self.teacher_data
        teacher_filtered = []
        for teacher in all_teachers:
            if subject != "Tất cả" and teacher.mon != subject:
                continue
            if gender != "Tất cả" and teacher.gioitinh != gender:
                continue
            if gvcn_role == "Là GVCN":
                if not teacher.gvcn:
                    continue
            elif gvcn_role == "Không Là GVCN":
                if teacher.gvcn:
                    continue
            teacher_filtered.append(teacher.name)
        return teacher_filtered
    
    def view_teacher(self, teacher_name):
        self.load_teacher()
        teacher = self.get_teacher_by_name(teacher_name)
        if not teacher:
            print("Ko thấy")
            return
        return teacher