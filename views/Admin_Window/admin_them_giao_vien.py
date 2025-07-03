from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox
)
from widgets import dialog_themgiaovien, dialog_editgiaovien, dialog_view_teacher
from PyQt6 import uic
from Service.teacher_service import TeacherService

from views.Admin_Window import admin_them_lop as ad
class Admin_Them_Giao_Vien(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Assets\Ui\admin_themgiaovien.ui", self)
        
        self.setUpUi()

        self.show()
    
    def setUpUi(self):
        self.teacher_service = TeacherService()

        self.load_teacher_to_ui()
        self.teacherList.setCurrentRow(0)

        self.btnAddClass.clicked.connect(self.change_admin_themlop)

        self.btnThem.clicked.connect(self.add_teacher)
        self.btnXoa.clicked.connect(self.remove_teacher)
        self.btnSua.clicked.connect(self.edit_Teacher)
        self.btnXem.clicked.connect(self.view_teacher)
        self.btnFilter.clicked.connect(self.filter_teacher)
        self.btnLogout.clicked.connect(self.logout)

    def logout(self):
        from views.login_side import login
        reply = QMessageBox.question(self, "Đăng xuất", "Bạn có chắc chắn muốn đăng xuất không?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            login_window = login()
            login_window.show()
            self.close()


    def change_admin_themlop(self):
        self.admin_them_lop = ad.Admin_Them_Lop()
        self.admin_them_lop.show()
        self.close()

    def load_teacher_to_ui(self):
        teachers_name = self.teacher_service.get_teacher_list()
        self.teacherList.addItems(teachers_name)

    def add_teacher(self):
        dialog = dialog_themgiaovien.Dialog_Them_Giao_Vien()
        if dialog.exec():
            dt = dialog.return_input_fields()
            teacher_name = dt["name"]
            self.teacherList.addItem(teacher_name)
            self.teacher_service.create_new_teacher(dt)

    def remove_teacher(self):
        teacher_item_id = self.teacherList.currentRow()
        teacher_name_selected = self.teacherList.item(teacher_item_id).text()

        choice = QMessageBox.question(self, "Remove Teacher",
                                            "Do you want to remove this teacher?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if choice == QMessageBox.StandardButton.Yes:
            self.teacherList.takeItem(teacher_item_id)
            self.teacher_service.delete_teacher(teacher_name_selected)

    def edit_Teacher(self):
        curr_id = self.teacherList.currentRow()
        teacher = self.teacherList.item(curr_id)
        teacher_name = teacher.text()

        teacher_data = self.teacher_service.get_teacher_by_name(teacher_name)

        dialog_edit_teacher = dialog_editgiaovien.Dialog_Edit_Giao_Vien(teacher_data)
        if dialog_edit_teacher.exec():
            data_return = dialog_edit_teacher.return_input_fields()
            data = data_return[0]
            self.teacherList.item(curr_id).setText(data['name'])
            self.teacher_service.update_teacher_info(data_return[1], data)

    def view_teacher(self):
        current_index = self.teacherList.currentRow()
        if current_index < 0:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn giáo viên để xem thông tin.")
            return

        teacher_name = self.teacherList.item(current_index).text()
        dialog = dialog_view_teacher.Dialog_View_Teacher(teacher_name)
        dialog.exec()

    def filter_teacher(self):
        subject = self.comboSubject.currentText()
        gender = self.comboGender.currentText()
        gvcn_role = self.comboHomeroom.currentText()

        teachers = self.teacher_service.filter_teachers(subject, gender, gvcn_role)
        self.teacherList.clear()
        self.teacherList.addItems(teachers)
