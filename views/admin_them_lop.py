from PyQt6.QtWidgets import (
    QApplication, QMainWindow
)
from PyQt6 import uic
import sys

from views import admin_them_giao_vien as ad

class Admin_Them_Lop(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Ui\admin_themlop.ui", self)
        
        self.setUpUi()

        self.show()
    
    def setUpUi(self):
        self.khoi6_btn.clicked.connect(lambda: self.change_stacked_widget(0))
        self.khoi7_btn.clicked.connect(lambda: self.change_stacked_widget(1))
        self.khoi8_btn.clicked.connect(lambda: self.change_stacked_widget(2))
        self.khoi9_btn.clicked.connect(lambda: self.change_stacked_widget(3))

        self.add_btn.clicked.connect(self.add_class)

        self.themgiaovien.clicked.connect(self.change_admin_themgiaovien)

    def change_stacked_widget(self, index): 
        self.stackedWidget.setCurrentIndex(index)

    def change_admin_themgiaovien(self):
        self.admin_them_giaovien = ad.Admin_Them_Giao_Vien()
        self.admin_them_giaovien.show()
        self.close()

    def add_class(self):
    
        stacked_index = self.stackedWidget.currentIndex()
        if stacked_index == 0:
            print("Adding class to Khoi 6")
        elif stacked_index == 1:
            print("Adding class to Khoi 7")
        elif stacked_index == 2:
            print("Adding class to Khoi 8")
        else:
            print("Adding class to Khoi 9")