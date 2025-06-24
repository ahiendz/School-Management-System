from Data import data_io
from models import classroom

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
            self.teacher_data.remove(teacher)
            self.teacher_data_dict = [n for n in self.teacher_data_dict if n['name'] != teacher_name]
            data_io.write_json_data(self.teacher_data_dict, self.data_path)

    def edit_teacher(self, teacher_name):
        teacher = self.get_teacher_by_name(teacher_name)
        if teacher:
            print("đã qua test teacher")
            