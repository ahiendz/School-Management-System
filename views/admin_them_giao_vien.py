from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox
)
from widgets import dialog_themgiaovien
from PyQt6 import uic
from models import teacher
import sys

from views import admin_them_lop as ad
class Admin_Them_Giao_Vien(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Ui\admin_themgiaovien.ui", self)
        
        self.setUpUi()

        self.show()
    
    def setUpUi(self):
        self.TeacherManager = teacher.TeacherManager()
        self.TeacherManager.load_teacher()

        self.load_teacher_to_ui()

        self.themlop.clicked.connect(self.change_admin_themlop)
        self.add_btn.clicked.connect(self.add_teacher)
        self.remove_btn.clicked.connect(self.remove_teacher
                                        )
    def change_admin_themlop(self):
        self.admin_them_lop = ad.Admin_Them_Lop()
        self.admin_them_lop.show()
        self.close()

    def load_teacher_to_ui(self):
        teachers_name = self.TeacherManager.get_teacher_list()
        self.danhsachGV.addItems(teachers_name)

    def add_teacher(self):
        dialog = dialog_themgiaovien.Dialog_Them_Giao_Vien()
        if dialog.exec():
            dt = dialog.return_input_fields()
            teacher_name = dt["name"]
            self.danhsachGV.addItem(teacher_name)
            self.TeacherManager.add_teacher(dt)

    def remove_teacher(self):
        teacher_item_id = self.danhsachGV.currentRow()
        teacher_name_selected = self.danhsachGV.item(teacher_item_id).text()

        choice = QMessageBox.question(self, "Remove Teacher",
                                            "Do you want to remove this teacher?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if choice == QMessageBox.StandardButton.Yes:
            self.danhsachGV.takeItem(teacher_item_id)
            self.TeacherManager.remove_teacher(teacher_name_selected)