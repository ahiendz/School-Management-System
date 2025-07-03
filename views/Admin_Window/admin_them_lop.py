from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox
)
from PyQt6 import uic
import sys

from widgets.dialog_view_class import Dialog_View_Class
from views.Admin_Window import admin_them_giao_vien as ad
from widgets import dialog_themclass as dia
from widgets.dialog_edit_class import Dialog_Edit_Class
from Service.classroom_service import ClassroomService
from views.Admin_Window import manager_student

class Admin_Them_Lop(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Assets\Ui\admin_themlop.ui", self)
        
        self.setUpUi()

        self.show()
    
    def setUpUi(self):
        self.classroom_service = ClassroomService()
        self.load_classroom_to_ui()

        self.stackedWidget.setCurrentIndex(0)

        self.btnKhoi6.clicked.connect(lambda: self.change_stacked_widget(0))
        self.btnKhoi7.clicked.connect(lambda: self.change_stacked_widget(1))
        self.btnKhoi8.clicked.connect(lambda: self.change_stacked_widget(2))
        self.btnKhoi9.clicked.connect(lambda: self.change_stacked_widget(3))

        self.btnAddTeacher.clicked.connect(self.change_admin_themgiaovien)

        self.btnAdd.clicked.connect(self.add_class)
        self.btnRemove.clicked.connect(self.remove_class)
        self.btnEdit.clicked.connect(self.edit_class)
        self.btnView.clicked.connect(self.view_class)
        self.btnManagerStudent.clicked.connect(self.mangerstudent)
        self.btnLogout.clicked.connect(self.logout)

    def logout(self):
        from views.login_side import login
        reply = QMessageBox.question(self, "Đăng xuất", "Bạn có chắc chắn muốn đăng xuất không?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            login_window = login()
            login_window.show()
            self.close()

    def change_stacked_widget(self, index): 
        self.stackedWidget.setCurrentIndex(index)

    def change_admin_themgiaovien(self):
        self.admin_them_giaovien = ad.Admin_Them_Giao_Vien()
        self.admin_them_giaovien.show()
        self.close()

    def load_classroom_to_ui(self):
        lop_list = self.classroom_service.get_classroom_list()
        for lop in lop_list:
            if lop['khoi'] == '6':
                self.listWidget_Khoi6.addItem(lop['lop'])
            elif lop['khoi'] == '7':
                self.listWidget_Khoi7.addItem(lop['lop'])
            elif lop['khoi'] == '8':
                self.listWidget_Khoi8.addItem(lop['lop'])
            elif lop['khoi'] == '9':
                self.listWidget_Khoi9.addItem(lop['lop'])
        
    def add_class(self):
        dialog = dia.Dialog_Them_Class()
        if dialog.exec():
            class_data = dialog.return_input_fields()
            class_name = class_data['lop']
            khoi = class_data['khoi']

            if khoi == '6':
                self.listWidget_Khoi6.addItem(class_name)
            elif khoi == '7':
                self.listWidget_Khoi7.addItem(class_name)
            elif khoi == '8':
                self.listWidget_Khoi8.addItem(class_name)
            else:
                self.listWidget_Khoi9.addItem(class_name)
            
            self.classroom_service.create_new_classroom(class_data)

    def remove_class(self):
        current_stackedW_id = self.stackedWidget.currentIndex()
        if current_stackedW_id == 0:
            listWidget = self.listWidget_Khoi6
        elif current_stackedW_id == 1:
            listWidget = self.listWidget_Khoi7
        elif current_stackedW_id == 2:
            listWidget = self.listWidget_Khoi8
        elif current_stackedW_id == 3:
            listWidget = self.listWidget_Khoi9

        classroom_id = listWidget.currentRow()
        classroom_item = listWidget.item(classroom_id)
        if classroom_item:
            classroom_sel = classroom_item.text()
        else:
            return

        choice = QMessageBox.question(self, "Remove Teacher",
                                            "Do you want to remove this teacher?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if choice == QMessageBox.StandardButton.Yes:
            listWidget.takeItem(classroom_id)
            self.classroom_service.delete_classroom(classroom_sel)

    def edit_class(self):
        current_index = self.stackedWidget.currentIndex()
        listWidget = [self.listWidget_Khoi6, self.listWidget_Khoi7, self.listWidget_Khoi8, self.listWidget_Khoi9][current_index]
        row = listWidget.currentRow()

        if row >= 0:
            selected_lop = listWidget.item(row).text()
            old_data = self.classroom_service.get_classroom_by_name(selected_lop)

            dialog = Dialog_Edit_Class(old_data)
            if dialog.exec():
                new_data = dialog.return_input_fields()
                self.classroom_service.update_classroom_info(selected_lop, new_data)

                listWidget.item(row).setText(new_data['lop'])

    def view_class(self):
        current_index = self.stackedWidget.currentIndex()
        listWidget = [self.listWidget_Khoi6, self.listWidget_Khoi7, self.listWidget_Khoi8, self.listWidget_Khoi9][current_index]
        row = listWidget.currentRow()

        if row >= 0:
            class_name = listWidget.item(row).text()
            dialog = Dialog_View_Class(class_name)
            dialog.exec()

    def mangerstudent(self):
        current_index = self.stackedWidget.currentIndex()
        listWidget = [self.listWidget_Khoi6, self.listWidget_Khoi7, self.listWidget_Khoi8, self.listWidget_Khoi9][current_index]
        row = listWidget.currentRow()

        if row >= 0:
            class_name = listWidget.item(row).text()
            self.manager_student_window = manager_student.ManagerStudentsWindow(class_name)
            self.manager_student_window.show()