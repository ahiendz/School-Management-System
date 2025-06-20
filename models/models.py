import Data.data_io as data_io

class Admin:
    def __init__(self, classroom, teacher):

        self.classroom = classroom
        self.teacher = teacher

    def item_to_data(self):
        json_data = list()
        for item in self.classroom:
            json_data.append(item.__dict__)
        return json_data

    def add_classroom(self, classroom):
        pass
    
    def remove_classroom(self, classroom):
        pass

    def edit_classroom(self, classroom):
        pass

class Teacher:
    def __init__(self, username, password, teach, classroom=None):
        self.teachername = username
        self.password = password
        self.teach_what = teach
        self.classroom = list()
    
    def item_to_data(self):
        json_data = list()
        for item in self.classroom:
            json_data.append(item.__dict__)
        return json_data

    def add_classroom(self, classroom):
        pass
    
class Parent:
    def __init__(self, username, password, student):
        self.username = username
        self.password = password
        self.student = list()
    
    def item_to_data(self):
        json_data = list()
        for item in self.student:
            json_data.append(item.__dict__)
        return json_data

    def add_student(self, student):
        pass
    
    def remove_student(self, student):
        pass

class Classroom:
    def __init__(self, name, teacher, students=None):
        self.name = name
        self.teacher = teacher
        self.students = students if students is not None else list()

class ClassroomManager:

    def __init__(self):
        self.classroom = list()
        self.classroom_data_dict = data_io.load_json_data()    

    def load_classrooms(self):
        for classroom in self.classroom_data_dict:
            new_classroom = Classroom(
                name=classroom['class'],
                teacher=classroom['GVCN'],
                students=classroom.get('students', [])
            )
            self.classroom.append(new_classroom)

    def get_classroom_item_by_class(self, classroom_name):
        for classroom in self.classroom:
            if classroom.name == classroom_name:
                return classroom
        return None

    def add_classroom(self, classroom_dict):
        new_classroom = Classroom(
            name=classroom_dict['name'],
            teacher=classroom_dict['teacher']
        )

        self.classroom.append(new_classroom)
        self.classroom_data_dict.append(classroom_dict)
        data_io.write_json_data(self.classroom_data_dict)

    def remove_classroom(self, classroom_name):
        classroom = self.get_classroom_item_by_class(classroom_name)
        if classroom:
            self.classroom.remove(classroom)
            self.classroom_data_dict = [c for c in self.classroom_data_dict if c['class'] != classroom_name]
            data_io.write_json_data(self.classroom_data_dict)
        else:
            raise ValueError(f"Classroom '{classroom_name}' not found.")