from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QVBoxLayout, QLabel, QPushButton, QDialog, QListWidgetItem, QListWidget, QDateEdit
)
from PyQt6 import uic
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
import sys
import json

class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Ui\ADMIN.ui", self)

# class TeacherWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         uic.loadUi(r"Gui\GV.ui", self)

# class PhuHuynhWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         uic.loadUi(r"Gui\PH.ui", self)




class SignInWindow(QMainWindow):
    def __init__(self, ADMIN_Window):
        super().__init__()
        uic.loadUi(r"Gui\Login.ui", self)

        self.ADMIN_Window = ADMIN_Window
        # self.Teacher_Window = Teacher_Window   #update sau
        # self.PhuHuynh_Window = PhuHuynh_Window
        
        self.AdminDN.clicked.connect(lambda: self.change_stacked_widget(0))
        # self.GVDN.clicked.connect(lambda: self.change_stacked_widget(1))
        # self.PHDN.clicked.connect(lambda: self.change_stacked_widget(2))

        self.ADMIN_DN_btt.clicked.connect(self.xulyDangNhapAdmin)
        # self.GV_DN_btt.clicked.connect(self.xulyDangNhapGiaoVien)
        # self.PH_DN_btt.clicked.connect(self.xulyDangNhapPhuHuynh)

    def change_stacked_widget(self, index):
        self.stackedWidget.setCurrentIndex(index)
    
    def xulyDangNhapAdmin(self):
        username = self.ADMIN_TK.text()
        password = self.ADMIN_MK.text()
        if username == "admin" and password == "admin":
            self.ADMIN_Window.show()
            self.close()
        elif username == "" or password == "":
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tài khoản và mật khẩu!")
        else:
            QMessageBox.warning(self, "Lỗi", "Tài khoản hoặc mật khẩu không đúng!")

    def xulyDangNhapGiaoVien(self):
        username = self.GV_TK.text()
        password = self.GV_MK.text()
        if username == "teacher" and password == "teacher":
            self.Teacher_Window.show()
            self.close()
        elif username == "" or password == "":
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tài khoản và mật khẩu!")
        else:
            QMessageBox.warning(self, "Lỗi", "Tài khoản hoặc mật khẩu không đúng!")

    def xulyDangNhapPhuHuynh(self):
        username = self.PH_TK.text()
        password = self.PH_MK.text()
        if username == "parent" and password == "parent":
            self.PhuHuynh_Window.show()
            self.close()
        elif username == "" or password == "":
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tài khoản và mật khẩu!")
        else:
            QMessageBox.warning(self, "Lỗi", "Tài khoản hoặc mật khẩu không đúng!")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Tạo các cửa sổ
    admin_window = AdminWindow()

    main_window = SignInWindow(admin_window)

    main_window.show()
    sys.exit(app.exec())

a = 1
print(type)