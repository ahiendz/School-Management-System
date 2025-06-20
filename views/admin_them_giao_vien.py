from PyQt6.QtWidgets import (
    QApplication, QMainWindow
)
from widgets import dialog_themgiaovien
from PyQt6 import uic
import sys

from views import admin_them_lop as ad
class Admin_Them_Giao_Vien(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Ui\admin_themgiaovien.ui", self)
        
        self.setUpUi()

        self.show()
    
    def setUpUi(self):
        self.themlop.clicked.connect(self.change_admin_themlop)

        self.add_btn.clicked.connect(self.add_teacher)
    

    def change_admin_themlop(self):
        self.admin_them_lop = ad.Admin_Them_Lop()
        self.admin_them_lop.show()
        self.close()

    def add_teacher(self):
        dialog = dialog_themgiaovien.Dialog_Them_Giao_Vien()
        if dialog.exec():
            dt = dialog.return_input_fields()
            teacher_name = dt["name"]
            self.danhsachGV.addItem(teacher_name)