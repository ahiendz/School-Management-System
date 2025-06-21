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
