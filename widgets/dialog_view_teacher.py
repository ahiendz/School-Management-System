# 📁 File: widgets/dialog_view_teacher.py

from PyQt6.QtWidgets import QDialog, QListWidgetItem
from PyQt6 import uic
from models.teacher import TeacherManager

class Dialog_View_Teacher(QDialog):
    def __init__(self, teacher_name):
        super().__init__()
        uic.loadUi("Ui/Dialog_View_Teacher.ui", self)

        self.setWindowTitle("Thông tin giáo viên")
        
        self.teacher_mgr = TeacherManager()

        self.teacher = self.teacher_mgr.view_teacher(teacher_name)
        
        # Đổ dữ liệu vào các label readonly
        self.name_label.setText(self.teacher.name)
        self.gender_label.setText(self.teacher.gioitinh)  # Sửa lại
        self.age_label.setText(str(self.teacher.age))
        self.subject_label.setText(self.teacher.mon)       # Sửa lại

        # Nếu giáo viên này là GVCN
        if self.teacher.gvcn:
            self.gvcn_label.setText(self.teacher.gvcn)
        else:
            self.gvcn_label.setText("Không chủ nhiệm")

        # Hiển thị tất cả các lớp trong lop_day của giáo viên
        self.class_list.clear()
        for lop in self.teacher.lop_day:
            item = QListWidgetItem(f"{lop} - {self.teacher.mon}")
            self.class_list.addItem(item)
            
        # Disable tất cả để không chỉnh sửa được
        self.name_label.setEnabled(False)
        self.gender_label.setEnabled(False)
        self.age_label.setEnabled(False)
        self.subject_label.setEnabled(False)
        self.gvcn_label.setEnabled(False)
        self.class_list.setEnabled(False)
