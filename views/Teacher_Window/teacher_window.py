from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QListWidgetItem, QWidget, QTableView,
    QAbstractItemView
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6 import uic
from models.student import StudentManager


class TeacherWindow(QMainWindow):
    def __init__(self, teacher_dict):
        super().__init__()
        print("Initializing TeacherWindow with teacher_dict:", teacher_dict)
        uic.loadUi(r"Ui\GV.ui", self)
        
        self.teacher_dict_data = teacher_dict
        self.lop_day = [str(item) for item in self.teacher_dict_data['lop day']]
        self.mon_day = self.teacher_dict_data['mon day']
        self.semester = "semester_1"  # mặc định

        # dict lưu model + bảng theo lớp
        self.bang_dict = {}
        self.model_dict = {}

        self.setUpUI()
        self.show()

    def setUpUI(self):
        print("Setting up UI...")
        # Xóa trang cũ nếu có
        while self.stackedWidget.count() > 0:
            widget = self.stackedWidget.widget(0)
            self.stackedWidget.removeWidget(widget)
            widget.deleteLater()

        self.danhsachlopday.clear()

        # Tạo các bảng điểm cho từng lớp
        for ten_lop in self.lop_day:
            print(f"Adding class to list: {ten_lop}")
            item = QListWidgetItem(ten_lop)
            self.danhsachlopday.addItem(item)

            trang = QWidget()
            layout = QVBoxLayout(trang)

            bang = QTableView()
            bang.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
            layout.addWidget(bang)

            model = QStandardItemModel()
            model.setHorizontalHeaderLabels([
                "Họ tên", "Điểm miệng", "Điểm 15 phút", "Điểm 1 tiết", "Điểm giữa kỳ", "Điểm cuối kỳ"
            ])
            bang.setModel(model)

            # Style
            bang.setStyleSheet("""
                QTableView {
                    border: 1px solid #ccc;
                    gridline-color: #aaa;
                    font-size: 14px;
                    selection-background-color: #000000;
                    selection-color: white;
                }
                QHeaderView::section {
                    background-color: #000000;
                    color: white;
                    padding: 4px;
                    border: 1px solid #ccc;
                }
            """)

            self.bang_dict[ten_lop] = bang
            self.model_dict[ten_lop] = model

            self.stackedWidget.addWidget(trang)

        # Sự kiện chọn lớp
        self.danhsachlopday.currentRowChanged.connect(self.change_lop)
        self.stackedWidget.setCurrentIndex(0)

        # Sự kiện đổi học kỳ
        self.chonhocki.currentTextChanged.connect(
            lambda _: self.show_scores(self.chonhocki.currentText())
        )

        # Load dữ liệu ban đầu
        print("Loading initial scores for semester: Học kỳ 1")
        self.show_scores("Học kỳ 1")

    def change_lop(self, index):
        print(f"Class changed to index: {index}")
        self.stackedWidget.setCurrentIndex(index)
        self.show_scores(self.chonhocki.currentText())

    def get_student_data(self, class_name, hk):
        print(f"Getting student data for class: {class_name}, semester: {hk}")
        if hk == "Học kỳ 1":
            hk = "semester_1"
        elif hk == "Học kỳ 2":
            hk = "semester_2"
        path = f"Data/Students/{class_name}.json"
        print(f"Student data path: {path}")
        self.student_manager = StudentManager(path, class_name)
        data = self.student_manager.load_student_to_Window(hk, self.mon_day)
        print(f"Loaded student data: {data}")
        return data

    def show_scores(self, hk):
        # biến đổi kh
        if hk == "Học Kì 1":
            hk = "semester_1"
        elif hk == "Học Kì 2":
            hk = "semester_2"

        current_index = self.stackedWidget.currentIndex()
        print(f"Showing scores for semester: {hk}, current_index: {current_index}")
        if current_index < 0 or current_index >= len(self.lop_day):
            print("Invalid class index, skipping show_scores.")
            return
        ten_lop = self.lop_day[current_index]
        print(f"Current class: {ten_lop}")
        data = self.get_student_data(ten_lop, hk)

        model = self.model_dict[ten_lop]
        model.removeRows(0, model.rowCount())

        # Ensure we are updating the correct QTableView for the current class
        bang = self.bang_dict[ten_lop]
        bang.setModel(model)  # Make sure the model is set for the correct table

        for student in data:
            print(f"Adding student to table: {student}")
            model.appendRow([
            QStandardItem(student.get('name', '')),
            QStandardItem(str(student.get('oral_scores', ''))),
            QStandardItem(str(student.get('quiz_15min', ''))),
            QStandardItem(str(student.get('test_1period', ''))),
            QStandardItem(str(student.get('midterm', ''))),
            QStandardItem(str(student.get('final', '')))
            ])
