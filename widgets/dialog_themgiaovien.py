from PyQt6.QtWidgets import QDialog
from PyQt6 import uic

class Dialog_Them_Giao_Vien(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Ui\Dialog_them_giaovien.ui", self)
        
        # self.setUpUi()
        
        self.show()
    
    def setUpUi(self):
        self.comboBox.addItems(["Khoi 6", "Khoi 7", "Khoi 8", "Khoi 9"])
        self.comboBox.setEditable(True)
    
    def return_input_fields(self) -> dict:
        return  {
            'name' : self.name.text(),
            'gioi tinh' : self.gioitinh.currentText(),
            'age' : self.age.text(),
            'mon day' : self.mon.currentText(),
            'gvcn lop' : self.gvcn.currentText()
        }
