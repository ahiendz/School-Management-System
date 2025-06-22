from PyQt6.QtWidgets import QDialog
from PyQt6 import uic
from models import teacher

class Dialog_Them_Class(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Ui\Dialog_themlop.ui", self)
        
        self.setUpUi()
        
        self.show()
    
    def setUpUi(self):
        self.teacher = teacher.TeacherManager()
        teachers = self.teacher.get_available_teachers()

        self.gvcn.addItems(teachers["gvcn"])
        self.gvV.addItems(teachers["gvV"])
        self.gvT.addItems(teachers["gvT"])
        self.gvA.addItems(teachers["gvA"])
        self.gvK.addItems(teachers["gvK"])
    
    def return_input_fields(self) -> dict:
        return {
            'khoi': self.khoi.currentText(),
            'lop': self.lop.text(),
            'gvcn': self.gvcn.currentText(),
            'gvbm': {
                'khtn': self.gvK.currentText(),
                'anh': self.gvA.currentText(),
                'van': self.gvV.currentText(),
                'toan': self.gvT.currentText()
            },
            'students': ""
        }
