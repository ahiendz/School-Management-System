# 📁 File: widgets/dialog_view_class.py

from PyQt6.QtWidgets import QDialog
from PyQt6 import uic
from Service.classroom_service import ClassroomService

class Dialog_View_Class(QDialog):
    def __init__(self, class_name):
        super().__init__()
        uic.loadUi(r"Assets\Ui\Dialog_View_Classroom.ui", self)

        self.setWindowTitle("Thông tin lớp học")

        self.classroom_service = ClassroomService()
        classroom = self.classroom_service.view_classroom(class_name)

        # Set thông tin cơ bản
        self.khoi_label.setText(classroom.khoi)
        self.lop_label.setText(classroom.lop)
        self.gvcn_label.setText(classroom.gvcn or "Không có GVCN")

        # Set GVBM
        gvbm = classroom.teachers
        self.gvT_label.setText(gvbm.get("toan") or "Không có")
        self.gvV_label.setText(gvbm.get("van") or "Không có")
        self.gvA_label.setText(gvbm.get("anh") or "Không có")
        self.gvK_label.setText(gvbm.get("khtn") or "Không có")

        # Disable chỉnh sửa
        for widget in [
            self.khoi_label, self.lop_label, self.gvcn_label,
            self.gvT_label, self.gvV_label, self.gvA_label, self.gvK_label
        ]:
            widget.setEnabled(False)
