from PyQt6.QtWidgets import QDialog
from PyQt6 import uic

class Dialog_Them_Class(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Ui\Dialog_themlop.ui", self)
        
        # self.setUpUi()
        
        self.show()
    
    def setUpUi(self):
        self.comboBox.addItems(["Khoi 6", "Khoi 7", "Khoi 8", "Khoi 9"])
        self.comboBox.setEditable(True)
    
    def return_input_fields(self) -> dict:
        return  {
        'khoi' : self.khoi.currentText(),
        'class_name' : self.lop.text(),
        'GVCN' : self.gvcn.currentText(),
        'GV_Van': self.gvV.currentText(),
        'GV_Toan' : self.gvT.currentText(),
        'GV_Anh' : self.gvA.currentText(),
        'GV_KHTN' : self.gvK.currentText()
        }
