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
        
        self.gvcn_ipt.addItems(teachers["gvcn"])
        self.gvV_ipt.addItems(teachers["gvV"])
        self.gvT_ipt.addItems(teachers["gvT"])
        self.gvA_ipt.addItems(teachers["gvA"])
        self.gvK_ipt.addItems(teachers["gvK"])
    
    def return_input_fields(self) -> dict:
        return {
            'khoi': self.khoi_ipt.currentText(),
            'lop': self.lop_ipt.text(),
            'gvcn': self.gvcn_ipt.currentText() if self.gvcn_ipt.currentText() != "Không có giáo viên trống" else None,
            'gvbm': {
                'khtn': self.gvK_ipt.currentText() if self.gvK_ipt.currentText() != "Không có giáo viên trống" else None,
                'anh': self.gvA_ipt.currentText() if self.gvA_ipt.currentText() != "Không có giáo viên trống" else None,
                'van': self.gvV_ipt.currentText() if self.gvV_ipt.currentText() != "Không có giáo viên trống" else None,
                'toan': self.gvT_ipt.currentText() if self.gvT_ipt.currentText() != "Không có giáo viên trống" else None
            }
        }
