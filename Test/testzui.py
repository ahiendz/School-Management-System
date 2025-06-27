import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from views.Teacher_Window.teacher_window import TeacherWindow
teacher_dict = {
        "name": "Meo Meo",
        "gioi tinh": "Nam",
        "age": "14",
        "mon day": "Toán",
        "gvcn lop": "6A1",
        "lop day": [
            "6A1",
            "7A1"
        ],
        "username": "GV27164",
        "password": "1234"
    }

tWIn = TeacherWindow(teacher_dict=teacher_dict)

