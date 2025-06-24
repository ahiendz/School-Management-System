import Data.data_io as data_io
from models import teacher

class Classroom:
    def __init__(self, khoi, lop, gvcn, teachers=None, students=None):
        self.khoi = khoi
        self.lop = lop
        self.gvcn = gvcn
        self.teachers = teachers if teachers is not None else {
            "Toán": None,
            "Văn": None,
            "Anh": None,
            "KHTN": None
        }
        self.students = students if students is not None else list()

class ClassroomManager:
    def __init__(self):
        self.data_path = "Data\data.json"
        self.classroom = list()
        self.classroom_data_dict = data_io.load_json_data(self.data_path)    

    def load_classrooms(self):
        for classroom in self.classroom_data_dict:
            new_classroom = Classroom(
                khoi=classroom['khoi'],
                lop=classroom['lop'],
                gvcn=classroom['gvcn'],
                teachers={
                    "Toán": classroom['gvbm'].get('toan'),
                    "Văn": classroom['gvbm'].get('van'),
                    "Anh": classroom['gvbm'].get('anh'),
                    "KHTN": classroom['gvbm'].get('khtn')
                },
                students=classroom.get('students', [])
            )
            self.classroom.append(new_classroom)

    def get_classroom_item_by_class(self, classroom_name):
        for classroom in self.classroom:
            if classroom.lop == classroom_name:
                return classroom
        return None
    
    def get_classroom_dicty_by_class(self, classroom_name):
        for classroom in self.classroom_data_dict:
            if classroom['lop'] == classroom_name:
                return classroom
        return None

    def get_lop_list(self):
        return [{'khoi' : classroom.khoi, 'lop' : classroom.lop} for classroom in self.classroom]

    def get_available_classroom(self):
        self.load_classrooms()
        classes = self.classroom

        return [classroom.lop for classroom in classes if classroom.gvcn == None]

    def assign_gvcn_to_class(self, lop, gvcn):
        self.load_classrooms()
        self.classroom_data_dict = data_io.load_json_data(self.data_path)

        classroom_change_data = self.get_classroom_item_by_class(lop)
        classroom_change_dict = self.get_classroom_dicty_by_class(lop)

        if classroom_change_data is not None and classroom_change_dict is not None:
            classroom_change_data.gvcn = gvcn
            classroom_change_dict['gvcn'] = gvcn

        data_io.write_json_data(self.classroom_data_dict, self.data_path)

    def add_classroom(self, classroom_dict):   
        new_classroom = Classroom(
            khoi=classroom_dict['khoi'],
            lop=classroom_dict['lop'],
            gvcn=classroom_dict['gvcn'],
            teachers={
                "Toán": classroom_dict['gvbm'].get('toan'),
                "Văn": classroom_dict['gvbm'].get('van'),
                "Anh": classroom_dict['gvbm'].get('anh'),
                "KHTN": classroom_dict['gvbm'].get('khtn')
            },
            students=classroom_dict.get('students', [])
        )

        self.classroom.append(new_classroom)
        self.classroom_data_dict.append(classroom_dict)
        data_io.write_json_data(self.classroom_data_dict, self.data_path)

        if classroom_dict.get("gvcn") is not None or any(v is not None for v in classroom_dict.get("gvbm", {}).values()):
            teacher_class = teacher.TeacherManager()
            teacher_class.update_teacher_mon_day(classroom_dict['lop'], classroom_dict["gvbm"], classroom_dict['gvcn']) # cần đặt lại tên
        
    def remove_classroom(self, classroom_name):
        classroom = self.get_classroom_item_by_class(classroom_name)
        if classroom:
            self.classroom.remove(classroom)
            self.classroom_data_dict = [c for c in self.classroom_data_dict if c['lop'] != classroom_name]
            data_io.write_json_data(self.classroom_data_dict, self.data_path)