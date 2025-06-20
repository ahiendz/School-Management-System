from PyQt6.QtWidgets import (
    QApplication, QMainWindow
)
from PyQt6 import uic
import sys

from views import admin_them_lop as ad

class login(QMainWindow): 
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Ui\Login.ui", self)
        
        self.show()
        self.setUpUi()
    
    def setUpUi(self):
        self.AdminDN.clicked.connect(lambda: self.change_stacked_widget(0))
        self.GVDN.clicked.connect(lambda: self.change_stacked_widget(1))
        self.PHDN.clicked.connect(lambda: self.change_stacked_widget(2))

        self.ADMIN_DN_btt.clicked.connect(self.openAdminWindow)
    
    def change_stacked_widget(self, index):
        self.stackedWidget.setCurrentIndex(index)
        
    def openAdminWindow(self):
        username = self.ADMIN_TK.text()
        password = self.ADMIN_MK.text()
        if username == "admin" and password == "1":
            self.admin_window = ad.Admin_Them_Lop()
            self.admin_window.show()
            self.close()