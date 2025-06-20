from Data import data_io

class Teacher:
    def __init__(self, name, gioitinh, age, mon, gvcn):
        self.name = name
        self.gioitinh = gioitinh
        self.age = age
        self.mon = mon
        self.gvcn = gvcn

class TeacherManager:
    def __init__(self):
        self.data_path = r"Data\teachers_data.json"
        self.teacher_data = list()
        self.teacher_data_dict = data_io.load_json_data(self.data_path)
    
    def load_teacher(self):
        for teacher in self.teacher_data_dict:
            new_teacher = Teacher(
                name = teacher['name'],
                gioitinh = teacher['gioi tinh'],
                age = teacher['age'],
                mon = teacher['mon day'],
                gvcn = teacher['gvcn lop']
            ) 
            self.teacher_data.append(new_teacher)

    def get_teacher_list(self):
        return [teacher.name for teacher in self.teacher_data]

    def get_teacher_by_name(self, teacher_name):
        for teacher in self.teacher_data:
            if teacher.name == teacher_name:
                return teacher
        return None

    def add_teacher(self, teacher_dict):
        new_teacher = Teacher(
            name = teacher_dict['name'],
            gioitinh = teacher_dict['gioi tinh'],
            age = teacher_dict['age'],
            mon = teacher_dict['mon day'],
            gvcn = teacher_dict['gvcn lop']
        )
        self.teacher_data.append(new_teacher)
        self.teacher_data_dict.append(teacher_dict)
        data_io.write_json_data(self.teacher_data_dict, self.data_path)

    def remove_teacher(self, teacher_name):
        teacher = self.get_teacher_by_name(teacher_name)
        if teacher:
            self.teacher_data.remove(teacher)
            self.teacher_data_dict = [n for n in self.teacher_data_dict if n['name'] != teacher_name]
            data_io.write_json_data(self.teacher_data_dict, self.data_path)
