from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox
)
from widgets import dialog_themgiaovien, dialog_editgiaovien, dialog_view_teacher
from PyQt6 import uic
from models import teacher

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
        self.danhsachGV.setCurrentRow(0)

        self.themlop.clicked.connect(self.change_admin_themlop)
        self.add_btn.clicked.connect(self.add_teacher)
        self.remove_btn.clicked.connect(self.remove_teacher)
        self.edit_btn.clicked.connect(self.edit_Teacher)
        self.view_btn.clicked.connect(self.view_teacher)
        self.loc_btn.clicked.connect(self.filter_teacher)

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

    def edit_Teacher(self):
        curr_id = self.danhsachGV.currentRow()
        teacher = self.danhsachGV.item(curr_id)
        teacher_name = teacher.text()

        teacher_data = self.TeacherManager.get_teacher_by_name(teacher_name)

        dialog_edit_teacher = dialog_editgiaovien.Dialog_Edit_Giao_Vien(teacher_data)
        if dialog_edit_teacher.exec():
            data_return = dialog_edit_teacher.return_input_fields()
            data = data_return[0]
            self.danhsachGV.item(curr_id).setText(data['name'])
            self.TeacherManager.edit_teacher(data_return[1], data)

    def view_teacher(self):
        current_index = self.danhsachGV.currentRow()
        if current_index < 0:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn giáo viên để xem thông tin.")
            return

        teacher_name = self.danhsachGV.item(current_index).text()
        dialog = dialog_view_teacher.Dialog_View_Teacher(teacher_name)
        dialog.exec()

    def filter_teacher(self):
        option1 = self.loc_theo_mon.currentText()
        option2 = self.loc_theo_gioi_tinh.currentText()
        option3 = self.loc_theo_gvcn.currentText()

        teachers = self.TeacherManager.filter_teachers(option1, option2, option3)
        self.danhsachGV.clear()
        self.danhsachGV.addItems(teachers)
