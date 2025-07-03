from PyQt6.QtWidgets import QDialog
from PyQt6 import uic
from Service.teacher_service import TeacherService

class Dialog_Edit_Class(QDialog):
    def __init__(self, old_data=None):
        super().__init__()
        uic.loadUi("Assets/Ui/Dialog_Edit_Class.ui", self)

        # Tải danh sách giáo viên phù hợp để lựa chọn
        self.teacher_service = TeacherService()
        available_teachers = self.teacher_service.get_available_teachers()

        # Gán danh sách GV phù hợp theo môn
        self.gvT_ipt.addItems(available_teachers["gvT"])
        self.gvV_ipt.addItems(available_teachers["gvV"])
        self.gvA_ipt.addItems(available_teachers["gvA"])
        self.gvK_ipt.addItems(available_teachers["gvK"])
        self.gvcn_ipt.addItems(available_teachers["gvcn"])

        if old_data:
            # Thêm GVCN/GVBM đang được gán để giữ lại lựa chọn cũ
            if old_data['gvcn'] and old_data['gvcn'] not in available_teachers['gvcn']:
                self.gvcn_ipt.addItem(old_data['gvcn'])
            if old_data['gvbm'].get("toan") and old_data['gvbm']['toan'] not in available_teachers['gvT']:
                self.gvT_ipt.addItem(old_data['gvbm']['toan'])
            if old_data['gvbm'].get("van") and old_data['gvbm']['van'] not in available_teachers['gvV']:
                self.gvV_ipt.addItem(old_data['gvbm']['van'])
            if old_data['gvbm'].get("anh") and old_data['gvbm']['anh'] not in available_teachers['gvA']:
                self.gvA_ipt.addItem(old_data['gvbm']['anh'])
            if old_data['gvbm'].get("khtn") and old_data['gvbm']['khtn'] not in available_teachers['gvK']:
                self.gvK_ipt.addItem(old_data['gvbm']['khtn'])

            # Set lại các giá trị cũ
            self.khoi_ipt.setCurrentText(old_data['khoi'])
            self.lop_ipt.setText(old_data['lop'])
            self.gvcn_ipt.setCurrentText(old_data['gvcn'])
            self.gvT_ipt.setCurrentText(old_data['gvbm'].get("toan", ""))
            self.gvV_ipt.setCurrentText(old_data['gvbm'].get("van", ""))
            self.gvA_ipt.setCurrentText(old_data['gvbm'].get("anh", ""))
            self.gvK_ipt.setCurrentText(old_data['gvbm'].get("khtn", ""))

    def process_field(self, text):
        return None if text.strip() == "Không có giáo viên trống" else text

    def return_input_fields(self):
        return {
            "khoi": self.khoi_ipt.currentText(),
            "lop": self.lop_ipt.text(),
            "gvcn": self.process_field(self.gvcn_ipt.currentText()),
            "gvbm": {
                "toan": self.process_field(self.gvT_ipt.currentText()),
                "van": self.process_field(self.gvV_ipt.currentText()),
                "anh": self.process_field(self.gvA_ipt.currentText()),
                "khtn": self.process_field(self.gvK_ipt.currentText())
            }
        }
