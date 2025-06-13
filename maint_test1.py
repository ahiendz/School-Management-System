from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QVBoxLayout, QLabel, QPushButton, QDialog, QListWidgetItem, QListWidget, QDateEdit
)
from PyQt6 import uic
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
import sys
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Ui\admin_window.ui", self)
        
        self.setUpUi()

        self.show()
    
    def setUpUi(self):
        self.khoi6_btn.clicked.connect(lambda: self.change_stacked_widget(0))
        self.khoi7_btn.clicked.connect(lambda: self.change_stacked_widget(1))
        self.khoi8_btn.clicked.connect(lambda: self.change_stacked_widget(2))
        self.khoi9_btn.clicked.connect(lambda: self.change_stacked_widget(3))

        
    def change_stacked_widget(self, index):
        self.stackedWidget.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())