from Data import data_io
import random, pandas
from openpyxl import Workbook
from Data.data_utils import replace_nan_with_none

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
        self.comment = comment if comment is not None else {
            "Toán": "",
            "Văn": "",
            "KHTN": "",
            "Anh": ""
        }

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
            print(f"Không tìm thấy điểm cho môn {mon_day} trong học kỳ {hk}.")
            return None

        print(self.scores)
        diem = self.scores[mon_day][hk]
        print(f"Current scores in {mon_day} trong {hk}: {diem}")
        if diem is None:
            print(f"Điểm cho môn {mon_day} trong học kỳ {hk} là None.")
            return None

        oral_scores = diem.get("oral_scores", [])
        quiz_15min = diem.get("quiz_15min", [])
        test_1period = diem.get("test_1period", [])
        midterm = diem.get("midterm")
        final = diem.get("final")
        print(oral_scores, quiz_15min, test_1period, midterm, final)
        # Kiểm tra xem có bất kỳ điểm nào bị trống không
        # Kiểm tra oral_scores (cần 2 điểm)
        if len(oral_scores) < 2 or any(score is None or str(score).strip() == "" for score in oral_scores):
            print(oral_scores)
            print(f"Có điểm miệng không hợp lệ cho môn {mon_day} trong học kỳ {hk}.")
            return None
        
        # Kiểm tra quiz_15min (cần 2 điểm)
        if len(quiz_15min) < 2 or any(score is None or str(score).strip() == "" for score in quiz_15min):
            print(f"Có điểm 15 phút không hợp lệ cho môn {mon_day} trong học kỳ {hk}.")
            return None
        
        # Kiểm tra test_1period (cần 2 điểm)
        if len(test_1period) < 2 or any(score is None or str(score).strip() == "" for score in test_1period):
            print(f"Có điểm 1 tiết không hợp lệ cho môn {mon_day} trong học kỳ {hk}.")
            return None
        
        # Kiểm tra midterm và final
        if midterm is None or str(midterm).strip() == "":
            print(f"Có điểm giữa kỳ không hợp lệ cho môn {mon_day} trong học kỳ {hk}.")
            return None
        if final is None or str(final).strip() == "":
            print(f"Có điểm cuối kỳ không hợp lệ cho môn {mon_day} trong học kỳ {hk}.")
            return None

        # Nếu tất cả điểm đều có thì mới tính trung bình
        total_scores = (
            sum(float(x) for x in oral_scores) +
            sum(float(x) for x in quiz_15min) +
            sum(float(x) for x in test_1period) +
            float(midterm) +
            float(final)
        )
        print(oral_scores)
        print(quiz_15min)
        print(test_1period)
        print(float(midterm), float(final))

        num_scores = 8

        print(total_scores, num_scores)
        return total_scores / num_scores
    
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
        data = replace_nan_with_none(data)
        data_io.write_json_data(data, self.json_data_path)

    def save_scores(self, mon_day, hk, data):
        print("Move to save_scores successfully")
        print(f"save_scores called with mon_day={mon_day}, hk={hk}")
        if not data:
            print("No data provided to save_scores.")
            return

        # Cập nhật điểm cho từng học sinh trong self.students
        for student in self.students:
            for d in data:
                if student.name == d.get("name"):
                    mon_scores = d.get("scores", {})
                    # CHỈ update đúng scores[mon_day][hk] là dict điểm, không gán cả dict scores
                    if mon_scores and mon_day in student.scores and hk in student.scores[mon_day]:
                        print(f"Updating scores for {student.name} in {mon_day} {hk}")
                        student.scores[mon_day][hk] = mon_scores[mon_day][hk] if mon_day in mon_scores and hk in mon_scores[mon_day] else mon_scores
                        average_score = student.tinh_diem_trung_binh(mon_day, hk)
                        student.scores[mon_day][hk]['average'] = average_score if average_score is not None else None

        # Lưu lại toàn bộ danh sách học sinh dưới dạng dict
        self.students_dict = [s.to_dict() for s in self.students]
        self.save_student_info(self.students_dict)
        print("Student info saved successfully.")

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

    def import_scores_from_excel_TEACHERNW(self, file_path, mon_day, semester):
        df = pandas.read_excel(file_path)

        if semester == "Học Kì 1":
            semester = "semester_1"
        elif semester == "Học Kì 2":
            semester = "semester_2"
        else:
            raise ValueError("Invalid semester")
        
        print("Importing scores from Excel file... with file path:", file_path, "and mon_day:", mon_day, "and semester:", semester)
        
        data = []

        for _, row in df.iterrows():
            student_name = row.get("Họ tên")

            # check if student already in data
            for st in self.students:
                if st.name == student_name:
                    print(f"{student_name} already in data")
                    break
                

            print(f"Processing student: {student_name}")
            student_item = self.get_student_by_name(student_name)
            if student_item is not None:
                scores = {
                    "oral_scores": [row.get("Điểm miệng cột 1") if row.get("Điểm miệng cột 1") != "" else None, 
                                   row.get("Điểm miệng cột 2") if row.get("Điểm miệng cột 2") != "" else None],
                    "quiz_15min": [row.get("Điểm 15p cột 1") if row.get("Điểm 15p cột 1") != "" else None, 
                                  row.get("Điểm 15p cột 2") if row.get("Điểm 15p cột 2") != "" else None],
                    "test_1period": [row.get("Điểm 1 tiết cột 1") if row.get("Điểm 1 tiết cột 1") != "" else None, 
                                    row.get("Điểm 1 tiết cột 2") if row.get("Điểm 1 tiết cột 2") != "" else None],
                    "midterm": row.get("Điểm Giữa kỳ") if row.get("Điểm Giữa kỳ") != "" else None,
                    "final": row.get("Điểm Cuối kỳ") if row.get("Điểm Cuối kỳ") != "" else None,
                    "average": None
                }
                print(f"New scores: {scores}")

                student_item.scores[mon_day][semester] = scores
                data.append(student_item.to_dict())
            else:
                print(f"Student {student_name} not found in current list.")

        print("All students processed. Saving scores...")
        print("All data to save:")
        for st in data:
            print(st["name"])
            print(st["scores"][mon_day][semester])

        self.save_scores(mon_day, semester, data)

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

    def export_to_excel_TEACHERNW(self, file_path, mon_day, semester):
        data = self.students_dict
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Students"

        headers = ["Họ tên", "Điểm miệng cột 1", "Điểm miệng cột 2", "Điểm 15p cột 1", "Điểm 15p cột 2", "Điểm 1 tiết cột 1", "Điểm 1 tiết cột 2", "Điểm Giữa kỳ", "Điểm Cuối kỳ"]
        ws.append(headers)

        for student in data:
            scores = student.get("scores", {})

            diem = scores.get(mon_day, {}).get(semester, {})
            row = [
            student.get("name", ""),
            diem.get("oral_scores", [None, None])[0],
            diem.get("oral_scores", [None, None])[1],
            diem.get("quiz_15min", [None, None])[0],
            diem.get("quiz_15min", [None, None])[1],
            diem.get("test_1period", [None, None])[0],
            diem.get("test_1period", [None, None])[1],
            diem.get("midterm", None),
            diem.get("final", None)
            ]
            ws.append(row)

        wb.save(file_path)

    def get_scores_for_teacher_view(self, hk, mon_day):
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
    
    def save_student_comment(self, student_name, mon_day, comment):
        student = self.get_student_by_name(student_name)
        if student:
            student.comment[mon_day] = comment
            for s in self.students_dict:
                if s["name"] == student_name:
                    s["comment"][mon_day] = comment
                    break
            self.save_student_info(self.students_dict)
            print(f"Comment for {student_name} in {mon_day} saved successfully.")
        else:
            print(f"Student {student_name} not found.")