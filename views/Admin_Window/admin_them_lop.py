from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox
)
from PyQt6 import uic
import sys

from widgets.dialog_view_class import Dialog_View_Class
from views.Admin_Window import admin_them_giao_vien as ad
from widgets import dialog_themclass as dia
from widgets.dialog_edit_class import Dialog_Edit_Class
from models import classroom
from views.Admin_Window import manager_student

class Admin_Them_Lop(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Ui\admin_themlop.ui", self)
        
        self.setUpUi()

        self.show()
    
    def setUpUi(self):
        self.ClassroomManager = classroom.ClassroomManager()
        self.ClassroomManager.load_classrooms()
        self.load_classroom_to_ui()

        self.stackedWidget.setCurrentIndex(0)

        self.khoi6_btn.clicked.connect(lambda: self.change_stacked_widget(0))
        self.khoi7_btn.clicked.connect(lambda: self.change_stacked_widget(1))
        self.khoi8_btn.clicked.connect(lambda: self.change_stacked_widget(2))
        self.khoi9_btn.clicked.connect(lambda: self.change_stacked_widget(3))

        self.themgiaovien.clicked.connect(self.change_admin_themgiaovien)

        self.add_btn.clicked.connect(self.add_class)
        self.remove_btn.clicked.connect(self.remove_class)
        self.edit_btn.clicked.connect(self.edit_class)
        self.view_btn.clicked.connect(self.view_class)
        self.mngr_btn.clicked.connect(self.mangerstudent)


    def change_stacked_widget(self, index): 
        self.stackedWidget.setCurrentIndex(index)

    def change_admin_themgiaovien(self):
        self.admin_them_giaovien = ad.Admin_Them_Giao_Vien()
        self.admin_them_giaovien.show()
        self.close()

    def load_classroom_to_ui(self):
        lop_list = self.ClassroomManager.get_lop_list()
        for lop in lop_list:
            if lop['khoi'] == '6':
                self.danhsachkhoi6.addItem(lop['lop'])
            elif lop['khoi'] == '7':
                self.danhsachkhoi7.addItem(lop['lop'])
            elif lop['khoi'] == '8':
                self.danhsachkhoi8.addItem(lop['lop'])
            elif lop['khoi'] == '9':
                self.danhsachkhoi9.addItem(lop['lop'])
        
    def add_class(self):
        dialog = dia.Dialog_Them_Class()
        if dialog.exec():
            class_data = dialog.return_input_fields()
            class_name = class_data['lop']
            khoi = class_data['khoi']

            if khoi == '6':
                self.danhsachkhoi6.addItem(class_name)
            elif khoi == '7':
                self.danhsachkhoi7.addItem(class_name)
            elif khoi == '8':
                self.danhsachkhoi8.addItem(class_name)
            else:
                self.danhsachkhoi9.addItem(class_name)
            
            self.ClassroomManager.add_classroom(class_data)

    def remove_class(self):
        current_stackedW_id = self.stackedWidget.currentIndex()
        if current_stackedW_id == 0:
            listWidget = self.danhsachkhoi6
        elif current_stackedW_id == 1:
            listWidget = self.danhsachkhoi7
        elif current_stackedW_id == 2:
            listWidget = self.danhsachkhoi8
        elif current_stackedW_id == 3:
            listWidget = self.danhsachkhoi9

        classroom_id = listWidget.currentRow()
        classroom_sel = listWidget.item(classroom_id).text()

        choice = QMessageBox.question(self, "Remove Teacher",
                                            "Do you want to remove this teacher?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if choice == QMessageBox.StandardButton.Yes:
            listWidget.takeItem(classroom_id)
            self.ClassroomManager.remove_classroom(classroom_sel)

    def edit_class(self):
        current_index = self.stackedWidget.currentIndex()
        listWidget = [self.danhsachkhoi6, self.danhsachkhoi7, self.danhsachkhoi8, self.danhsachkhoi9][current_index]
        row = listWidget.currentRow()

        if row >= 0:
            selected_lop = listWidget.item(row).text()
            old_data = self.ClassroomManager.get_classroom_dicty_by_class(selected_lop)

            dialog = Dialog_Edit_Class(old_data)
            if dialog.exec():
                new_data = dialog.return_input_fields()
                self.ClassroomManager.edit_classroom(selected_lop, new_data)

                listWidget.item(row).setText(new_data['lop'])

    def view_class(self):
        current_index = self.stackedWidget.currentIndex()
        listWidget = [self.danhsachkhoi6, self.danhsachkhoi7, self.danhsachkhoi8, self.danhsachkhoi9][current_index]
        row = listWidget.currentRow()

        if row >= 0:
            class_name = listWidget.item(row).text()
            dialog = Dialog_View_Class(class_name)
            dialog.exec()

    def mangerstudent(self):
        current_index = self.stackedWidget.currentIndex()
        listWidget = [self.danhsachkhoi6, self.danhsachkhoi7, self.danhsachkhoi8, self.danhsachkhoi9][current_index]
        row = listWidget.currentRow()

        if row >= 0:
            class_name = listWidget.item(row).text()
            self.manager_student_window = manager_student.ManagerStudentsWindow(class_name)
            self.manager_student_window.show()