from Data.data_io import write_json_data, load_json_data


class Admin:
    def __init__(self, username, password, classroom):
        self.username = username
        self.password = password
        self.classroom = list()
    
    def item_to_data(self):
        json_data = list()
        for item in self.classroom:
            json_data.append(item.__dict__)
        return json_data

    def add_classroom(self, classroom):
        new_classroom = Classroom(name =classroom["id"],
                             teacher=classroom["title"],
                             students=classroom["release_date"])
        self.classroom.append(new_classroom)
        write_json_data(self.new_classroom)
    
    def remove_classroom(self, classroom):
        self.classroom.remove(classroom)
        write_json_data(self.classroom)

class Classroom:
    def __init__(self, name, teacher, students):
        self.name = name
        self.teacher = teacher
        self.students = []
    
    

    def add_student(self, student):
        self.students.append(student)
    
    def remove_student(self, student):
        self.students.remove(student)