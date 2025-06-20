from PyQt6.QtWidgets import (
    QApplication, QMainWindow
)
from PyQt6 import uic
import sys

from views import admin_them_giao_vien as ad
from widgets import dialog_themclass as dia

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
    
        dialog = dia.Dialog_Them_Class()
        if dialog.exec():
            class_data = dialog.return_input_fields()
            class_name = class_data['class_name']
            khoi = class_data['khoi']

            if khoi == '6':
                self.danhsachkhoi6.addItem(class_name)
            elif khoi == '7':
                self.danhsachkhoi7.addItem(class_name)
            elif khoi == '8':
                self.danhsachkhoi8.addItem(class_name)
            elif khoi == '9':
                self.danhsachkhoi9.addItem(class_name)
            else:
                print("khoilop khong hop lek")
                # them 1 thonng bao