from models.classroom import ClassroomManager
from models.teacher import TeacherManager

class ValidationUtils:
    def __init__(self):
        self.classroom_manager = ClassroomManager()
        self.teacher_manager = TeacherManager()

    def can_update_classroom(self, old_data, new_data) -> bool:
        """
        Kiểm tra xem có thể cập nhật thông tin lớp học không
        Trả về False nếu lớp đã có giáo viên và đang thay đổi tên lớp hoặc khối
        """
        # Kiểm tra nếu thay đổi tên lớp hoặc khối
        if old_data['lop'] != new_data['lop'] or old_data['khoi'] != new_data['khoi']:
            # Kiểm tra xem lớp có giáo viên nào không
            has_teachers = False
            
            # Kiểm tra GVCN
            if old_data.get('gvcn'):
                has_teachers = True
            
            # Kiểm tra GVBM
            gvbm = old_data.get('gvbm', {})
            for subject, teacher in gvbm.items():
                if teacher:
                    has_teachers = True
                    break
            
            if has_teachers:
                return False
        
        return True

    def can_delete_classroom(self, classroom_data) -> bool:
        """
        Kiểm tra xem có thể xóa lớp học không
        Trả về False nếu lớp đang có bất kỳ giáo viên nào
        """
        # Kiểm tra GVCN
        if classroom_data.get('gvcn'):
            return False
        
        # Kiểm tra GVBM
        gvbm = classroom_data.get('gvbm', {})
        for subject, teacher in gvbm.items():
            if teacher:
                return False
        
        return True

    def can_update_teacher(self, old_data, new_data) -> bool:
        """
        Không cho sửa tên, tuổi, giới tính, môn dạy nếu giáo viên đang dạy lớp hoặc làm GVCN.
        Các trường khác sửa thoải mái.
        """
        # Kiểm tra xem giáo viên có đang dạy lớp hoặc làm GVCN không
        has_teaching_classes = False
        if old_data.get('gvcn lop'):
            has_teaching_classes = True
        lop_day = old_data.get('lop day', [])
        if lop_day:
            has_teaching_classes = True

        # Nếu giáo viên đang dạy/làm GVCN, cấm sửa 4 trường chính
        if has_teaching_classes:
            for field in ['name', 'gioi tinh', 'age', 'mon day']:
                if old_data.get(field) != new_data.get(field):
                    return False
        return True

    def can_delete_teacher(self, teacher_data) -> bool:
        """
        Kiểm tra xem có thể xóa giáo viên không
        Trả về False nếu giáo viên đang dạy hoặc làm GVCN bất kỳ lớp nào
        """
        # Kiểm tra GVCN
        if teacher_data.gvcn:
            return False
        
        # Kiểm tra lớp dạy
        if teacher_data.lop_day:
            return False
        
        return True

    def get_classroom_validation_message(self, old_data, new_data) -> str:
        """
        Trả về thông báo lỗi cụ thể cho việc cập nhật lớp học
        """
        if not self.can_update_classroom(old_data, new_data):
            return "Không thể sửa tên lớp hoặc khối lớp vì lớp đang có giáo viên dạy hoặc giáo viên chủ nhiệm."
        return ""

    def get_classroom_delete_message(self, classroom_data) -> str:
        """
        Trả về thông báo lỗi cụ thể cho việc xóa lớp học
        """
        if not self.can_delete_classroom(classroom_data):
            return "Không thể xóa lớp vì lớp đang có giáo viên dạy hoặc giáo viên chủ nhiệm."
        return ""

    def get_teacher_validation_message(self, old_data, new_data) -> str:
        """
        Trả về thông báo lỗi cụ thể cho việc cập nhật giáo viên
        """
        if not self.can_update_teacher(old_data, new_data):
            return "Không thể sửa tên, tuổi, giới tính hoặc môn dạy vì giáo viên đang dạy lớp hoặc làm GVCN."
        return ""

    def get_teacher_delete_message(self, teacher_data) -> str:
        """
        Trả về thông báo lỗi cụ thể cho việc xóa giáo viên
        """
        if not self.can_delete_teacher(teacher_data):
            return "Không thể xóa giáo viên vì giáo viên đang dạy hoặc làm GVCN bất kỳ lớp nào."
        return "" 