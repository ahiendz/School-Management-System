import Data.data_io as data_io
from models import teacher

class Classroom:
    def __init__(self, khoi, lop, gvcn, teachers=None):
        self.khoi = khoi
        self.lop = lop
        self.gvcn = gvcn
        self.teachers = teachers if teachers is not None else {
            "Toán": None,
            "Văn": None,
            "Anh": None,
            "KHTN": None
        }

class ClassroomManager:
    def __init__(self):
        self.data_path = "Data/data.json"
        self.classroom = list()
        self.classroom_data_dict = data_io.load_json_data(self.data_path)
        self.teacher_manager = teacher.TeacherManager()

    def load_classrooms(self):
        self.classroom = []
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
                }
            )
            self.classroom.append(new_classroom)

    def get_classroom_item_by_class(self, classroom_name):
        for classroom in self.classroom:
            if classroom.lop == classroom_name:
                return classroom
        return None
    
    def get_classroom_dicty_by_class(self, classroom_name):
        for classroom in self.classroom_data_dict:
            if classroom['lop'] == classroom_name:
                return classroom
        return None

    def get_lop_list(self):
        return [{'khoi' : classroom.khoi, 'lop' : classroom.lop} for classroom in self.classroom]

    def get_available_classroom(self):
        self.load_classrooms()
        classes = self.classroom
        return [classroom.lop for classroom in classes if classroom.gvcn == None]

    def assign_gvcn_to_class(self, lop, gvcn):
        self.load_classrooms()
        self.classroom_data_dict = data_io.load_json_data(self.data_path)
        classroom_change_data = self.get_classroom_item_by_class(lop)
        classroom_change_dict = self.get_classroom_dicty_by_class(lop)
        if classroom_change_data is not None and classroom_change_dict is not None:
            # Kiểm tra lớp đã có GVCN chưa
            if classroom_change_dict['gvcn'] and classroom_change_dict['gvcn'] != gvcn:
                raise Exception(f"Lop {lop} da co GVCN la {classroom_change_dict['gvcn']}!")
            classroom_change_data.gvcn = gvcn
            classroom_change_dict['gvcn'] = gvcn
        data_io.write_json_data(self.classroom_data_dict, self.data_path)

    def add_classroom(self, classroom_dict):   
        # Kiểm tra lớp đã có GVCN chưa
        if classroom_dict.get('gvcn'):
            for c in self.classroom_data_dict:
                if c.get('lop') == classroom_dict['lop'] and c.get('gvcn'):
                    raise Exception(f"Lop {classroom_dict['lop']} da co GVCN!")
        new_classroom = Classroom(
            khoi=classroom_dict['khoi'],
            lop=classroom_dict['lop'],
            gvcn=classroom_dict['gvcn'],
            teachers={
                "Toán": classroom_dict['gvbm'].get('toan'),
                "Văn": classroom_dict['gvbm'].get('van'),
                "Anh": classroom_dict['gvbm'].get('anh'),
                "KHTN": classroom_dict['gvbm'].get('khtn')
            }
        )
        self.classroom.append(new_classroom)
        self.classroom_data_dict.append(classroom_dict)
        data_io.write_json_data(self.classroom_data_dict, self.data_path)
        if classroom_dict.get("gvcn") is not None or any(v is not None for v in classroom_dict.get("gvbm", {}).values()):
            self.teacher_manager.update_teacher_mon_day(classroom_dict['lop'], classroom_dict["gvbm"], classroom_dict['gvcn'])
    
    def remove_classroom(self, lop):
        classroom = self.get_classroom_item_by_class(lop)
        if classroom:
            # Gỡ lớp khỏi giáo viên liên quan
            self.teacher_manager.load_teacher()
            for teacher in self.teacher_manager.teacher_data:
                if teacher.gvcn == lop:
                    teacher.gvcn = None
                if lop in teacher.lop_day:
                    teacher.lop_day.remove(lop)
            # Cập nhật lại teacher_data_dict sau khi chỉnh object
            for teacher in self.teacher_manager.teacher_data:
                teacher_dict = self.teacher_manager.get_teacher_dict_by_name(teacher.name)
                if teacher_dict:
                    teacher_dict['gvcn lop'] = teacher.gvcn
                    teacher_dict['lop day'] = teacher.lop_day
            data_io.write_json_data(self.teacher_manager.teacher_data_dict, self.teacher_manager.data_path)
            # Xóa lớp khỏi dữ liệu lớp học
            self.classroom.remove(classroom)
            self.classroom_data_dict = [c for c in self.classroom_data_dict if c['lop'] != lop]
            data_io.write_json_data(self.classroom_data_dict, self.data_path)

    def edit_classroom(self, class_name, new_data):
        classroom_item = self.get_classroom_item_by_class(class_name)
        classroom_dict = self.get_classroom_dicty_by_class(class_name)
        if classroom_item and classroom_dict:
            # Lưu lại GVCN và GVBM cũ để cập nhật lại danh sách lớp của giáo viên
            old_gvcn = classroom_dict.get('gvcn')
            old_gvbm = classroom_dict.get('gvbm', {})
            # Cập nhật thông tin lớp
            classroom_item.khoi = new_data['khoi']
            classroom_item.lop = new_data['lop']
            classroom_item.gvcn = new_data['gvcn']
            classroom_item.teachers = {
                "Toán": new_data['gvbm'].get("toan"),
                "Văn": new_data['gvbm'].get("van"),
                "Anh": new_data['gvbm'].get("anh"),
                "KHTN": new_data['gvbm'].get("khtn")
            }
            classroom_dict['khoi'] = new_data['khoi']
            classroom_dict['lop'] = new_data['lop']
            classroom_dict['gvcn'] = new_data['gvcn']
            classroom_dict['gvbm'] = {
                "toan": new_data['gvbm'].get("toan"),
                "van": new_data['gvbm'].get("van"),
                "anh": new_data['gvbm'].get("anh"),
                "khtn": new_data['gvbm'].get("khtn")
            }
            # Cập nhật lại danh sách lớp của giáo viên cũ nếu đổi GVCN hoặc GVBM
            self.teacher_manager.load_teacher()
            # Gỡ lớp khỏi GVCN cũ nếu đổi GVCN
            if old_gvcn and old_gvcn != new_data['gvcn']:
                t = self.teacher_manager.get_teacher_by_name(old_gvcn)
                if t:
                    t.gvcn = None
                    t_dict = self.teacher_manager.get_teacher_dict_by_name(old_gvcn)
                    if t_dict:
                        t_dict['gvcn lop'] = None
            # Gỡ lớp khỏi GVBM cũ nếu đổi giáo viên
            for mon in ["toan", "van", "anh", "khtn"]:
                old_teacher = old_gvbm.get(mon)
                new_teacher = new_data['gvbm'].get(mon)
                if old_teacher and old_teacher != new_teacher:
                    t = self.teacher_manager.get_teacher_by_name(old_teacher)
                    if t and class_name in t.lop_day:
                        t.lop_day.remove(class_name)
                        t_dict = self.teacher_manager.get_teacher_dict_by_name(old_teacher)
                        if t_dict and class_name in t_dict.get('lop day', []):
                            t_dict['lop day'].remove(class_name)
            # Gán lớp cho giáo viên mới
            self.teacher_manager.update_teacher_mon_day(new_data['lop'], new_data['gvbm'], new_data['gvcn'])
            data_io.write_json_data(self.classroom_data_dict, self.data_path)
    
    def view_class(self, class_name):
        self.load_classrooms()
        classroom = self.get_classroom_item_by_class(class_name)
        if not classroom:
            return
        return classroom

