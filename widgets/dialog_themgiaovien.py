from PyQt6.QtWidgets import QDialog
from PyQt6 import uic
from Service.classroom_service import ClassroomService

class Dialog_Them_Giao_Vien(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Assets\Ui\Dialog_them_giaovien.ui", self)
        
        self.setUpUi()
        
        self.show()
    
    def setUpUi(self):
        self.classroom_service = ClassroomService()
        classroom = self.classroom_service.get_available_classrooms()
        
        self.gvcn.addItems(classroom)

    def return_input_fields(self) -> dict:
        return  {
            'name' : self.name.text(),
            'gioi tinh' : self.gioitinh.currentText(),
            'age' : self.age.text(),
            'mon day' : self.mon.currentText(),
            'gvcn lop' : None if self.gvcn.currentText() == "Không có lớp trống" else self.gvcn.currentText(),
            'lop day' : list()
        }
