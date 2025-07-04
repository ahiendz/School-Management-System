from models.teacher import TeacherManager
from models.classroom import ClassroomManager
from Utils.validation_utils import ValidationUtils

class TeacherService:
    def __init__(self):
        self.teacher_manager = TeacherManager()
        self.classroom_manager = ClassroomManager()
        self.validation_utils = ValidationUtils()

    def create_new_teacher(self, teacher_data):
        self.teacher_manager.add_teacher(teacher_data)

    def delete_teacher(self, teacher_name):
        # Kiểm tra ràng buộc trước khi xóa
        teacher_data = self.teacher_manager.get_teacher_by_name(teacher_name)
        if teacher_data:
            error_message = self.validation_utils.get_teacher_delete_message(teacher_data)
            if error_message:
                raise Exception(error_message)
        
        # Gọi classroom_manager unassign giáo viên khỏi tất cả lớp
        # Gọi teacher_manager xóa giáo viên
        self.teacher_manager.remove_teacher(teacher_name)

    def update_teacher_info(self, teacher_name, new_data):
        # Kiểm tra ràng buộc trước khi cập nhật
        old_data = self.teacher_manager.get_teacher_dict_by_name(teacher_name)
        if old_data:
            error_message = self.validation_utils.get_teacher_validation_message(old_data, new_data)
            if error_message:
                raise Exception(error_message)
        
        self.teacher_manager.edit_teacher(teacher_name, new_data)

    def get_teacher_list(self):
        """Lấy danh sách tất cả giáo viên"""
        self.teacher_manager.load_teacher()
        return self.teacher_manager.get_teacher_list()

    def get_teacher_by_name(self, teacher_name):
        """Lấy thông tin chi tiết của một giáo viên"""
        self.teacher_manager.load_teacher()
        return self.teacher_manager.get_teacher_by_name(teacher_name)

    def get_teacher_dict_by_name(self, teacher_name):
        """Lấy thông tin dict của một giáo viên"""
        return self.teacher_manager.get_teacher_dict_by_name(teacher_name)

    def get_available_teachers(self):
        """Lấy danh sách giáo viên có thể gán cho lớp"""
        return self.teacher_manager.get_available_teachers()

    def filter_teachers(self, subject, gender, gvcn_role):
        """Lọc giáo viên theo tiêu chí"""
        return self.teacher_manager.filter_teachers(subject, gender, gvcn_role)

    def view_teacher(self, teacher_name):
        """Xem thông tin chi tiết giáo viên"""
        return self.teacher_manager.view_teacher(teacher_name) 