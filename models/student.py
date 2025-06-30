from Data import data_io
import random, pandas, os
from openpyxl import Workbook

DEFAULT_SCORES = {
    "Toán": {
        "semester_1": {"oral_scores": [], "quiz_15min": [], "test_1period": [], "midterm": None, "final": None, "average": None},
        "semester_2": {"oral_scores": [], "quiz_15min": [], "test_1period": [], "midterm": None, "final": None, "average": None},
    },
    "Văn": {
        "semester_1": {"oral_scores": [], "quiz_15min": [], "test_1period": [], "midterm": None, "final": None, "average": None},
        "semester_2": {"oral_scores": [], "quiz_15min": [], "test_1period": [], "midterm": None, "final": None, "average": None},
    },
    "KHTN": {
        "semester_1": {"oral_scores": [], "quiz_15min": [], "test_1period": [], "midterm": None, "final": None, "average": None},
        "semester_2": {"oral_scores": [], "quiz_15min": [], "test_1period": [], "midterm": None, "final": None, "average": None},
    },
    "Anh": {
        "semester_1": {"oral_scores": [], "quiz_15min": [], "test_1period": [], "midterm": None, "final": None, "average": None},
        "semester_2": {"oral_scores": [], "quiz_15min": [], "test_1period": [], "midterm": None, "final": None, "average": None},
    },
}

class Student:
    def __init__(self, id, name, gender, dob, parent_account, parent_password, class_name, scores=None, comment=None):
        self.id = id
        self.name = name
        self.gender = gender
        self.dob = dob
        self.parent_account = parent_account
        self.parent_password = parent_password
        self.class_name = class_name
        self.scores = scores if scores is not None else DEFAULT_SCORES.copy()
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

    # tính điểm trung bình cho một môn học trong học kỳ cụ thể
    def tinh_diem_trung_binh(self, mon_day, hk):
        if mon_day not in self.scores or hk not in self.scores[mon_day]:
            return None

        diem = self.scores[mon_day][hk]
        if diem is None:
            return None

        oral_scores = diem.get("oral_scores", [])
        quiz_15min = diem.get("quiz_15min", [])
        test_1period = diem.get("test_1period", [])
        midterm = diem.get("midterm")
        final = diem.get("final")

        # Kiểm tra xem có bất kỳ điểm nào bị trống không
        # Kiểm tra oral_scores (cần 2 điểm)
        if len(oral_scores) < 2 or any(score is None or str(score).strip() == "" for score in oral_scores):
            return None
        
        # Kiểm tra quiz_15min (cần 2 điểm)
        if len(quiz_15min) < 2 or any(score is None or str(score).strip() == "" for score in quiz_15min):
            return None
        
        # Kiểm tra test_1period (cần 2 điểm)
        if len(test_1period) < 2 or any(score is None or str(score).strip() == "" for score in test_1period):
            return None
        
        # Kiểm tra midterm và final
        if midterm is None or str(midterm).strip() == "":
            return None
        if final is None or str(final).strip() == "":
            return None

        # Nếu tất cả điểm đều có thì mới tính trung bình
        total_scores = (
            sum(float(x) for x in oral_scores) +
            sum(float(x) for x in quiz_15min) +
            sum(float(x) for x in test_1period) +
            float(midterm) +
            float(final)
        )

        num_scores = len(oral_scores) + len(quiz_15min) + len(test_1period) + 2  # +2 cho midterm và final

        print(total_scores, num_scores)
        return total_scores / num_scores if num_scores > 0 else None
    
class StudentManager:
    def __init__(self, data_path, class_name):
        self.json_data_path = data_path
        self.curr_lop = class_name
        self.students = []
        self.students_dict = self.load_from_file()
        self.load_student()

    def load_from_file(self):
        data = data_io.load_json_data(self.json_data_path)
        return data

    def save_student_info(self, data):
        data_io.write_json_data(data, self.json_data_path)

    def save_scores(self, mon_day, hk, data):
        if not data:
            return

        students_dict = []
        for student in data:
            student_name = student.get("name")
            student_item = self.get_student_by_name(student_name)
            if student_item is not None:
                student_scores = student.get("scores", {})
                # thực hiện tính toán điểm trung bình nếu đủ điều kiện
                if student_scores:
                    student_item.scores[mon_day][hk] = student_scores
                    average_score = student_item.tinh_diem_trung_binh(mon_day, hk)
                    if average_score is not None:
                        student_scores['average'] = average_score
                    else:
                        student_scores['average'] = None
                students_dict.append(student_item.to_dict())

        self.students_dict = students_dict
        self.save_student_info(self.students_dict)
                

    def load_student(self):
        for teacher in self.students_dict:
            scores = teacher.get("scores", DEFAULT_SCORES.copy())
            student = Student(
                id=teacher['id'],
                name=teacher["name"],
                gender=teacher["gender"],
                dob=teacher["dob"],
                parent_account=teacher["parent_account"],
                parent_password=teacher["parent_password"],
                class_name=teacher["class"],
                scores=scores,
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
            class_name=self.curr_lop
        )

        self.students.append(new_student)
        new_student = new_student.to_dict()
        self.students_dict.append(new_student)
        self.save_student_info(self.students_dict)

    def remove_students_by_ids(self, id_list: list):
        self.students = [s for s in self.students if s.id not in id_list]
        self.students_dict = [s for s in self.students_dict if s["id"] not in id_list]
        self.save_student_info(self.students_dict)

    def get_student_by_name(self, student_name):
        for student in self.students:
            if student.name == student_name:
                return student
        return None

    def import_from_excel_ADMINW(self, path):
        df = pandas.read_excel(path)

        self.students.clear()
        self.students_dict.clear()
        for _, row in df.iterrows():
            student_data = Student(
                id=row["id"],
                name=row["name"],
                gender=row["gender"],
                dob=row["dob"],
                parent_account=row["parent_account"],
                parent_password=row["parent_password"],
                class_name=self.curr_lop
            )
            self.students.append(student_data)
            student_data = student_data.to_dict()
            self.students_dict.append(student_data)

        self.save_student_info(self.students_dict)

    def import_from_excel_TEACHERNW():
        pass

    def export_to_excel_ADMINW(self, file_path=None):
        data = self.students_dict
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Students"

        headers = ["id", "name", "gender", "dob", "parent_account", "parent_password", "class"]
        ws.append(headers)

        for student in data:
            row = [student[key] for key in headers]
            ws.append(row)

        wb.save(file_path)

    def export_to_excel_TEACHERNW():
        pass

    def load_student_to_Teacher_Window(self, hk, mon_day):
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