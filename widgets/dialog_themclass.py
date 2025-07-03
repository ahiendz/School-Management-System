from PyQt6.QtWidgets import QDialog
from PyQt6 import uic
from Service.teacher_service import TeacherService

class Dialog_Them_Class(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Assets\Ui\Dialog_themlop.ui", self)
        
        self.setUpUi()
        
        self.show()
    
    def setUpUi(self):
        self.teacher_service = TeacherService()
        teachers = self.teacher_service.get_available_teachers()
        
        self.gvcn.addItems(teachers["gvcn"])
        self.gvV.addItems(teachers["gvV"])
        self.gvT.addItems(teachers["gvT"])
        self.gvA.addItems(teachers["gvA"])
        self.gvK.addItems(teachers["gvK"])
    
    def return_input_fields(self) -> dict:
        return {
            'khoi': self.khoi.currentText(),
            'lop': self.lop.text(),
            'gvcn': self.gvcn.currentText() if self.gvcn.currentText() != "Không có giáo viên trống" else None,
            'gvbm': {
                'khtn': self.gvK.currentText() if self.gvK.currentText() != "Không có giáo viên trống" else None,
                'anh': self.gvA.currentText() if self.gvA.currentText() != "Không có giáo viên trống" else None,
                'van': self.gvV.currentText() if self.gvV.currentText() != "Không có giáo viên trống" else None,
                'toan': self.gvT.currentText() if self.gvT.currentText() != "Không có giáo viên trống" else None
            },
            'students': ""
        }
