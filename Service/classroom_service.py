from models.classroom import ClassroomManager
from models.teacher import TeacherManager
from Utils.validation_utils import ValidationUtils

class ClassroomService:
    def __init__(self):
        self.classroom_manager = ClassroomManager()
        self.teacher_manager = TeacherManager()
        self.validation_utils = ValidationUtils()

    def create_new_classroom(self, class_data):
        # Điều phối tạo lớp mới
        self.classroom_manager.add_classroom(class_data)

    def delete_classroom(self, class_name):
        # Kiểm tra ràng buộc trước khi xóa
        classroom_data = self.classroom_manager.get_classroom_dicty_by_class(class_name)
        if classroom_data:
            error_message = self.validation_utils.get_classroom_delete_message(classroom_data)
            if error_message:
                raise Exception(error_message)
        
        # Gọi classroom_manager lấy chi tiết lớp
        # Gọi teacher_manager unassign lớp khỏi giáo viên
        # Gọi classroom_manager xóa lớp
        self.classroom_manager.remove_classroom(class_name)

    def update_classroom_info(self, class_name, new_data):
        # Fix: Cần cập nhật cả teacher assignments khi thay đổi lớp
        old_data = self.classroom_manager.get_classroom_dicty_by_class(class_name)
        
        # Kiểm tra ràng buộc trước khi cập nhật
        if old_data:
            error_message = self.validation_utils.get_classroom_validation_message(old_data, new_data)
            if error_message:
                raise Exception(error_message)
        
        # Xóa lớp cũ khỏi các giáo viên liên quan
        if old_data:
            self._unassign_teachers_from_class(class_name, old_data)
        
        # Cập nhật thông tin lớp
        self.classroom_manager.edit_classroom(class_name, new_data)
        
        # Gán lớp mới cho các giáo viên
        self._assign_teachers_to_class(class_name, new_data)

    def get_classroom_list(self):
        """Lấy danh sách tất cả lớp học"""
        self.classroom_manager.load_classrooms()
        return self.classroom_manager.get_lop_list()

    def get_classroom_by_name(self, class_name):
        """Lấy thông tin chi tiết của một lớp"""
        return self.classroom_manager.get_classroom_dicty_by_class(class_name)

    def get_available_teachers(self):
        """Lấy danh sách giáo viên có thể gán cho lớp"""
        return self.teacher_manager.get_available_teachers()

    def get_available_classrooms(self):
        """Lấy danh sách lớp học có thể gán GVCN"""
        return self.classroom_manager.get_available_classroom()

    def view_classroom(self, class_name):
        """Xem thông tin chi tiết của một lớp"""
        return self.classroom_manager.view_class(class_name)

    def _unassign_teachers_from_class(self, class_name, class_data):
        """Gỡ lớp khỏi các giáo viên liên quan"""
        self.teacher_manager.load_teacher()
        
        # Gỡ GVCN
        if class_data.get('gvcn'):
            teacher = self.teacher_manager.get_teacher_by_name(class_data['gvcn'])
            if teacher:
                teacher.gvcn = None
                teacher_dict = self.teacher_manager.get_teacher_dict_by_name(class_data['gvcn'])
                if teacher_dict:
                    teacher_dict['gvcn lop'] = None
        
        # Gỡ GVBM
        gvbm = class_data.get('gvbm', {})
        for subject_key, teacher_name in gvbm.items():
            if teacher_name:
                teacher = self.teacher_manager.get_teacher_by_name(teacher_name)
                if teacher and class_name in teacher.lop_day:
                    teacher.lop_day.remove(class_name)
                    teacher_dict = self.teacher_manager.get_teacher_dict_by_name(teacher_name)
                    if teacher_dict and class_name in teacher_dict.get('lop day', []):
                        teacher_dict['lop day'].remove(class_name)
        
        # Lưu thay đổi
        data_io = __import__('Data.data_io', fromlist=['data_io'])
        data_io.write_json_data(self.teacher_manager.teacher_data_dict, self.teacher_manager.data_path)

    def _assign_teachers_to_class(self, class_name, class_data):
        """Gán lớp cho các giáo viên mới"""
        self.teacher_manager.load_teacher()
        
        # Gán GVCN
        if class_data.get('gvcn'):
            teacher = self.teacher_manager.get_teacher_by_name(class_data['gvcn'])
            if teacher:
                teacher.gvcn = class_name
                teacher_dict = self.teacher_manager.get_teacher_dict_by_name(class_data['gvcn'])
                if teacher_dict:
                    teacher_dict['gvcn lop'] = class_name
        
        # Gán GVBM
        gvbm = class_data.get('gvbm', {})
        for subject_key, teacher_name in gvbm.items():
            if teacher_name:
                teacher = self.teacher_manager.get_teacher_by_name(teacher_name)
                if teacher and class_name not in teacher.lop_day:
                    teacher.lop_day.append(class_name)
                    teacher_dict = self.teacher_manager.get_teacher_dict_by_name(teacher_name)
                    if teacher_dict:
                        if 'lop day' not in teacher_dict:
                            teacher_dict['lop day'] = []
                        if class_name not in teacher_dict['lop day']:
                            teacher_dict['lop day'].append(class_name)
        
        # Lưu thay đổi
        data_io = __import__('Data.data_io', fromlist=['data_io'])
        data_io.write_json_data(self.teacher_manager.teacher_data_dict, self.teacher_manager.data_path) 