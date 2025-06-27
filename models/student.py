from Data import data_io
import random, pandas, openpyxl, os
from openpyxl import Workbook
from widgets import dialog_add_student
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import QFileDialog

class Student:
    def __init__(self, id, name, gender, dob, parent_account, parent_password, class_name, scores=None, comment=None):
        self.id = id
        self.name = name
        self.gender = gender
        self.dob = dob
        self.parent_account = parent_account
        self.parent_password = parent_password
        self.class_name = class_name
        self.scores = scores if scores is not None else {}
        self.comment = comment if comment is not None else {}

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "dob": self.dob,
            "parent_account": self.parent_account,
            "parent_password": self.parent_password,
            "class": self.class_name,
            "scores": self.scores,
            "comment": self.comment
        }

class StudentManager:
    def __init__(self, data_path, class_name):
        self.json_data_path = data_path
        self.curr_lop = class_name
        self.students = []
        self.students_dict = self.load_from_file()

        # # thuộc tính để biết là teacher đang dạy môn nào để mà nhâp
        # self.mon_day = mon_day

        self.load_student()

    def load_from_file(self):
        data = data_io.load_json_data(self.json_data_path)
        return data

    def save_to_file(self,data):
        data_io.write_json_data(data, self.json_data_path)

    def save_from_table_model(self, model: QStandardItemModel):
        data = []
        for row in range(model.rowCount()):
            item = {
                "id": model.item(row, 0).text(),
                "name": model.item(row, 1).text(),
                "gender": model.item(row, 2).text(),
                "dob": model.item(row, 3).text(),
                "parent_account": model.item(row, 4).text(),
                "parent_password": model.item(row, 5).text(),
                "class": self.curr_lop,
                "scores": {},
                "comment": {}
            }
            data.append(item)

        self.students_dict = data
        self.save_to_file(data)

    def load_student(self):
        for teacher in self.students_dict:
            student = Student(
                id=teacher['id'],
                name=teacher["name"],
                gender=teacher["gender"],
                dob=teacher["dob"],
                parent_account=teacher["parent_account"],
                parent_password=teacher["parent_password"],
                class_name=teacher["class"],
                scores=teacher.get("scores", {}),
                comment=teacher.get("comment", {})
        )
            self.students.append(student)

    def add_student(self, student_dict):
        def generate_random_id():
            return f"MS{random.randint(10000, 99999)}"
        
        student_id = generate_random_id()
        parent_account = f"phhs_{student_id}"
        parent_password = f"{parent_account}_1234"

        new_student = Student(
            id=student_id,
            name=student_dict["name"],
            gender=student_dict["gender"],
            dob=student_dict["dob"],
            parent_account=parent_account,
            parent_password=parent_password,
            class_name= self.curr_lop,
            scores={},
            comment={}
        )

        self.students.append(new_student)
        new_student = new_student.to_dict()
        self.students_dict.append(new_student)
        self.save_to_file(self.students_dict)

    def remove_students_by_ids(self, id_list: list):
        self.students = [s for s in self.students if s.id not in id_list]
        self.students_dict = [s for s in self.students_dict if s["id"] not in id_list]
        self.save_to_file(self.students_dict)

    def get_student_by_id(self, student_id):
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def import_from_excel(self,path):
        df = pandas.read_excel(path)

        self.students.clear()
        self.students_dict.clear()
        for _, row in df.iterrows():
            student_data = Student(
                id = row["id"],
                name= row["name"],
                gender= row["gender"],
                dob=row["dob"],
                parent_account= row["parent_account"],
                parent_password= row["parent_password"],
                class_name=self.curr_lop
            )
            self.students.append(student_data)
            student_data = student_data.to_dict()
            self.students_dict.append(student_data)
        
        self.save_to_file(self.students_dict)

    def export_to_excel(self):
        data = self.students_dict

        export_folder = os.path.abspath(f"Data/Export")
        os.makedirs(export_folder, exist_ok=True)

        default_name = f"{self.curr_lop}_Student_List.xlsx"

        file_path, _ = QFileDialog.getSaveFileName(
            parent=None,
            caption="Export File",
            directory=os.path.join(export_folder, default_name),
            filter="Excel Files (*.xlsx)"
        )

        if not file_path:
            return

        wb = Workbook()
        ws = wb.active
        ws.title = "Students"

        headers = ["id", "name", "gender", "dob", "parent_account", "parent_password", "class"]
        ws.append(headers)

        for student in data:
            row = [student[key] for key in headers]
            ws.append(row)

        wb.save(file_path)

        # There are student data
        a = ["id", "name", "gender", "dob", "parent_account", "parent_password", "class"]

    def load_student_to_Window(self, hk, mon_day):
        data = []
        for student in self.students:
            student_name = student.name
            scores = student.scores
            diem_theo_mon = scores.get(mon_day)
            if diem_theo_mon is not None:
                diem_theo_hk = diem_theo_mon.get(hk)
                if diem_theo_hk is not None:
                    diem_theo_hk['name'] = student_name
                    data.append(diem_theo_hk)
        
        return data