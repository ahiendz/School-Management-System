from models.student import StudentManager
# from models.classroom import ClassroomManager

class StudentService:
    def __init__(self, data_path, class_name):
        self.data_path = data_path
        self.class_name = class_name

    # Các phương thức để quản lý học sinh trong lớp học theo quyền là Admin

    def add_student_to_class_ADMIN_WINDOW(self, student_data):
        student_manager = StudentManager(self.data_path, self.class_name)
        student_manager.add_student(student_data)
        # Sau khi thêm, có thể cập nhật classroom nếu cần

    def remove_student_from_class_ADMIN_WINDOW(self, student_id):
        student_manager = StudentManager(self.data_path, self.class_name)
        student_manager.remove_students_by_ids([student_id])
        # Sau khi xóa, có thể cập nhật classroom nếu cần

    def import_students_from_file_ADMIN_WINDOW(self, file_path):
        student_manager = StudentManager(self.data_path, self.class_name)
        student_manager.import_from_excel_ADMINW(file_path)

    def export_students_to_file_ADMIN_WINDOW(self, file_path):
        student_manager = StudentManager(self.data_path, self.class_name)
        student_manager.export_to_excel_ADMINW(file_path)
        pass

    def save_students_to_json_ADMIN_WINDOW(self, data):
        student_manager = StudentManager(self.data_path, self.class_name)
        student_manager.save_student_info(data)
        # Sau khi lưu, có thể cập nhật classroom nếu cần

    def load_student_info_ADMIN_WINDOW(self):
        student_manager = StudentManager(self.data_path, self.class_name)
        return student_manager.students
    
    # Các phương thức để quản lý học sinh trong lớp học theo quyền là Teacher

    def load_student_scores_TEACHER_WINDOW(self, hk, mon_day):
        student_manager = StudentManager(self.data_path, self.class_name)
        return student_manager.get_scores_for_teacher_view(hk, mon_day)
    
    def get_student_name_TEACHER_WINDOW(self, name):
        student_manager = StudentManager(self.data_path, self.class_name)
        return student_manager.get_student_by_name(name)

    def save_scores_TEACHER_WINDOW(self, mon_day, hk, data):
        student_manager = StudentManager(self.data_path, self.class_name)
        student_manager.save_scores(mon_day=mon_day, hk=hk, data=data)
        # Sau khi lưu điểm, có thể cập nhật classroom nếu cần

    def import_scores_from_excel_TEACHER_WINDOW(self, file_path, mon_day, semester):
        student_manager = StudentManager(self.data_path, self.class_name)
        student_manager.import_scores_from_excel_TEACHERNW(file_path, mon_day, semester)
        # Sau khi import điểm, có thể cập nhật classroom nếu cần

    def export_scores_to_excel_TEACHER_WINDOW(self, file_path, mon_day, semester):
        student_manager = StudentManager(self.data_path, self.class_name)
        student_manager.export_to_excel_TEACHERNW(file_path=file_path, mon_day=mon_day, semester=semester)
        # Sau khi export điểm, có thể cập nhật classroom nếu cần

    def save_student_comment_TEACHER_WINDOW(self, student_name, mon_day, comment):
        student_manager = StudentManager(self.data_path, self.class_name)
        student_manager.save_student_comment(student_name=student_name, mon_day=mon_day, comment=comment)
        # Sau khi lưu bình luận, có thể cập nhật classroom nếu cần