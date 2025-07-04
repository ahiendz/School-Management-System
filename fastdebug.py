from views.Teacher_Window import teacher_window
from models.student import Student
# call qt6
from PyQt6.QtWidgets import QApplication
import sys


if __name__ == "__main__":
    teset =     {
        "name": "Lý Sugiiiii",
        "gioi tinh": "Nam",
        "age": "3",
        "mon day": "KHTN",
        "gvcn lop": "9A1",
        "lop day": [
            "6A1",
            "7A1",
            "8A1",
            "9A1"
        ],
        "username": "GV88833",
        "password": "1234"
    }
    

    app = QApplication(sys.argv)
    main_window = teacher_window.TeacherWindow(teset)
    sys.exit(app.exec())