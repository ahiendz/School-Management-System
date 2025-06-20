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
        self.data_path = "Data\teachers_data.json"
        self.teacher_data = list()
        self.teacher_data_dict = data_io.load_json_data(self.data_path)
    
    def load_teacher(self):
        for teacher in self.teacher_data_dict:
            new_teacher = Teacher(
                name = teacher['ten'],
                gioitinh = teacher['Joi tinh'],
                age = teacher['Age'],
                mon = teacher['Mon Day'],
                gvcn = teacher['GVCN Lop']
            )
        self.teacher_data.append(new_teacher)

    def add_teacher(self):
        
