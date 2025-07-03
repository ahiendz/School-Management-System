from PyQt6.QtWidgets import QDialog
from PyQt6 import uic
from models import student

class Dialog_Them_Student(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Assets\Ui\Dialog_Them_Student.ui", self)
        
        self.setUpUi()
        
        self.show()
    
    def setUpUi(self):
        pass
    
    def return_input_fields(self) -> dict:
        return {
            "name": self.name.text(),
            "gender": self.gender.currentText(),
            "dob": self.dob.text(),
        }

