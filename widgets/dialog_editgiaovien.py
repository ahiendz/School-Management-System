from PyQt6.QtWidgets import QDialog
from PyQt6 import uic
from models import classroom as CL

class Dialog_Edit_Giao_Vien(QDialog):
    def __init__(self, teacher_data):
        super().__init__()
        self.teacher_data = teacher_data
        uic.loadUi(r"Ui\Dialog_Edit_Teacher.ui", self)
        
        self.setUpUi()
        
        self.show()
    
    def setUpUi(self):
        self.classroom = CL.ClassroomManager()
        classroom = self.classroom.get_available_classroom()
        
        self.gvcn_ipt.addItems(classroom)
        if self.teacher_data.gvcn:
            self.gvcn_ipt.addItem(self.teacher_data.gvcn)

        self.name_ipt.setText(self.teacher_data.name)
        self.gioitinh_ipt.setCurrentText(self.teacher_data.gioitinh)
        self.age_ipt.setText(self.teacher_data.age)
        self.mon_ipt.setCurrentText(self.teacher_data.mon)
        self.gvcn_ipt.setCurrentText(self.teacher_data.gvcn)


    def return_input_fields(self) -> dict:
        return  [
            {
            'name' : self.name_ipt.text(),
            'gioi tinh' : self.gioitinh_ipt.currentText(),
            'age' : self.age_ipt.text(),
            'mon day' : self.mon_ipt.currentText(),
            'gvcn lop' : None if self.gvcn_ipt.currentText() == "Không có lớp trống" else self.gvcn_ipt.currentText(),
            'lop day' : list()
            },
            self.teacher_data.name
        ]