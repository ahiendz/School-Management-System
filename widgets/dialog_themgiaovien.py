from PyQt6.QtWidgets import QDialog
from PyQt6 import uic
from models import classroom as CL

class Dialog_Them_Giao_Vien(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Ui\Dialog_them_giaovien.ui", self)
        
        self.setUpUi()
        
        self.show()
    
    def setUpUi(self):
        self.classroom = CL.ClassroomManager()
        classroom = self.classroom.get_available_classroom()
        
        self.gvcn.addItems(classroom)

    def return_input_fields(self) -> dict:
        return  {
            'name' : self.name.text(),
            'gioi tinh' : self.gioitinh.currentText(),
            'age' : self.age.text(),
            'mon day' : self.mon.currentText(),
            'gvcn lop' : self.gvcn.currentText()
        }
