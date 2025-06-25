from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox
)
from PyQt6 import uic
import sys

class TeacherWindow(QMainWindow):
    def __init__(self, teacher_dict):
        super().__init__()
        uic.loadUi(r"Ui\GV.ui", self)
        self.teacher_dict_data = teacher_dict
        self.lop_day = [str(item) for item in self.teacher_dict_data['lop day']]

        print(self.lop_day )
        self.setUpUI()

        self.show()

    def setUpUI(self):
        self.danhsachlopday.addItems(self.lop_day)