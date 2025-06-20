import Data.data_io as data_io

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
        self.classroom = list()
        self.classroom_data_dict = data_io.load_json_data()    

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
        data_io.write_json_data(self.classroom_data_dict)

    def remove_classroom(self, classroom_name):
        classroom = self.get_classroom_item_by_class(classroom_name)
        if classroom:
            self.classroom.remove(classroom)
            self.classroom_data_dict = [c for c in self.classroom_data_dict if c['lop'] != classroom_name]
            data_io.write_json_data(self.classroom_data_dict)
        else:
            raise ValueError(f"Classroom '{classroom_name}' not found.")