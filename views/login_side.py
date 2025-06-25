from PyQt6.QtWidgets import (
    QApplication, QMainWindow
)
from PyQt6 import uic
import sys

from views.Admin_Window import admin_them_lop
from views.Teacher_Window import teacher_window
from Data import data_io
import config

class login(QMainWindow): 
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Ui\Login.ui", self)
        
        self.show()
        self.setUpUi()
    
    def setUpUi(self):
        self.config = config.Config()

        self.AdminDN.clicked.connect(lambda: self.change_stacked_widget(0))
        self.GVDN.clicked.connect(lambda: self.change_stacked_widget(1))
        self.PHDN.clicked.connect(lambda: self.change_stacked_widget(2))

        self.ADMIN_DN_btt.clicked.connect(self.openAdminWindow)
        self.GV_DN_btt.clicked.connect(self.openTeacherWindow)
    
    def change_stacked_widget(self, index):
        self.stackedWidget.setCurrentIndex(index)
        
    def openAdminWindow(self):
        username = self.ADMIN_TK.text()
        password = self.ADMIN_MK.text()
        if username == "admin" and password == "1":
            self.admin_window = admin_them_lop.Admin_Them_Lop()
            self.admin_window.show()
            self.close()

    def openTeacherWindow(self):
        username = self.GV_TK.text()
        password = self.GV_MK.text()

        print("Bạn nhập:", username, password)

        teachers = data_io.load_json_data(self.config.teacher_data_json_path)
        for teacher in teachers:
            print("So sánh với:", teacher.get("username"), teacher.get("password"))
            if teacher.get('username') == username and teacher.get('password') == password:
                self.teacher_window = teacher_window.TeacherWindow(teacher)
                self.teacher_window.show()
                self.close()
                return

        print("❌ Không tìm thấy tài khoản hợp lệ!")
