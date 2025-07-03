import re
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QMessageBox
)
from PyQt6 import uic
import sys, os

from views.Admin_Window import admin_them_lop
from views.Teacher_Window import teacher_window
from views.Parent_Window import partent_window
from Data import data_io
import config
from Service.student_service import StudentService

class login(QMainWindow): 
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Assets\Ui\Login.ui", self)
        
        self.show()
        self.setUpUi()
    
    def setUpUi(self):
        self.config = config.Config()

        self.adminButton.clicked.connect(lambda: self.change_stacked_widget(0))
        self.teacherButton.clicked.connect(lambda: self.change_stacked_widget(1))
        self.parentButton.clicked.connect(lambda: self.change_stacked_widget(2))

        self.setup_eye_button(self.adminPasswordToggleButton, self.adminPasswordLineEdit)
        self.setup_eye_button(self.teacherPasswordToggleButton, self.teacherPasswordLineEdit)
        self.setup_eye_button(self.parentPasswordToggleButton, self.parentPasswordLineEdit)


        self.adminLoginButton.clicked.connect(self.openAdminWindow)
        self.teacherLoginButton.clicked.connect(self.openTeacherWindow)
        self.parentLoginButton.clicked.connect(self.openPhuHuynhWindow)
    
    def setup_eye_button(self,eye_button, password_lineedit):
        eye_button.pressed.connect(lambda: password_lineedit.setEchoMode(QLineEdit.EchoMode.Normal))
        eye_button.released.connect(lambda: password_lineedit.setEchoMode(QLineEdit.EchoMode.Password))
    
    def change_stacked_widget(self, index):
        self.stackedWidget.setCurrentIndex(index)
        
    def openAdminWindow(self):
        username = self.adminUsernameLineEdit.text()
        password = self.adminPasswordLineEdit.text()

        if not username or not password:
            self.showmessenger("Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")
            return

        if username == "a1" and password == "1":
            self.admin_window = admin_them_lop.Admin_Them_Lop()
            self.admin_window.show()
            self.close()
            return
        
        self.showmessenger("Tên đăng nhập hoặc mật khẩu không đúng.")


    def openTeacherWindow(self):
        username = self.teacherUsernameLineEdit.text()
        password = self.teacherPasswordLineEdit.text()

        if not username or not password:
            self.showmessenger("Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")
            return

        teachers = data_io.load_json_data(self.config.teacher_data_json_path)
        for teacher in teachers:
            if teacher.get('username') == username and teacher.get('password') == password:
                self.teacher_window = teacher_window.TeacherWindow(teacher)
                self.teacher_window.show()
                self.close()
                return

        self.showmessenger("Tên đăng nhập hoặc mật khẩu không đúng.")

    def openPhuHuynhWindow(self):
        username = self.parentUsernameLineEdit.text()
        password = self.parentPasswordLineEdit.text()

        if not username or not password:
            self.showmessenger("Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")
            return

        # kiểm tra từng học sinh trong từng file json trong Data/Student
        student_dir = r"Data\Students"
        found = False

        # get path và class bằng cách tách từ path

        for filename in os.listdir(student_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(student_dir, filename)
                class_name = filename[:-5]  # loại bỏ phần mở rộng .json
                student_service = StudentService(file_path, class_name)
                data = student_service.get_student_data()
                for student in data:
                    if student.parent_account == username and student.parent_password == password:
                        found = True
                        student_name = student.name
                        self.parent_window = partent_window.ParentWindow(student_name=student_name, class_name=class_name, data_path=file_path)
                        self.parent_window.show()
                        self.close()
                        return
        if not found:
            self.showmessenger("Tên đăng nhập hoặc mật khẩu không đúng.")
            return

    def showmessenger(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Thông báo")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
        