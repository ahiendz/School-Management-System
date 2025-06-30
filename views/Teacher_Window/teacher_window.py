from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QListWidgetItem, QWidget, QTableView,
    QAbstractItemView, QMessageBox
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from PyQt6 import uic
from models.student import StudentManager

class TeacherWindow(QMainWindow):
    def __init__(self, teacher_dict):
        super().__init__()
        uic.loadUi(r"Ui\GV.ui", self)

        self.teacher_dict_data = teacher_dict
        self.lop_day = [str(item) for item in self.teacher_dict_data['lop day']]
        self.mon_day = self.teacher_dict_data['mon day']
        self.semester = "semester_1"  # mặc định

        self.bang_dict = {}
        self.model_dict = {}

        self.setUpUI()
        self.show()

    def setUpUI(self):
        while self.stackedWidget.count() > 0:
            widget = self.stackedWidget.widget(0)
            self.stackedWidget.removeWidget(widget)
            widget.deleteLater()

        self.danhsachlopday.clear()

        for ten_lop in self.lop_day:
            item = QListWidgetItem(ten_lop)
            self.danhsachlopday.addItem(item)

            trang = QWidget()
            layout = QVBoxLayout(trang)

            bang = QTableView()
            bang.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
            bang.verticalHeader().setVisible(True)
            bang.horizontalHeader().setVisible(True)
            layout.addWidget(bang)

            model = QStandardItemModel()

            self.bang_dict[ten_lop] = bang
            self.model_dict[ten_lop] = model
            self.stackedWidget.addWidget(trang)

        self.danhsachlopday.currentRowChanged.connect(self.change_lop)
        self.stackedWidget.setCurrentIndex(0)

        self.chonhocki.currentTextChanged.connect(
            lambda _: self.show_scores(self.chonhocki.currentText())
        )

        self.show_scores("Học kỳ 1")

        self.save_btn.clicked.connect(self.save_data)

    def change_lop(self, index):
        self.stackedWidget.setCurrentIndex(index)
        self.show_scores(self.chonhocki.currentText())

    def get_student_data(self, class_name, hk):
        if hk == "Học kỳ 1":
            hk = "semester_1"
        elif hk == "Học kỳ 2":
            hk = "semester_2"
        path = f"Data/Students/{class_name}.json"
        self.student_manager = StudentManager(path, class_name)
        data = self.student_manager.load_student_to_Teacher_Window(hk, self.mon_day)
        return data

    def safe_get_list_item(self, data_list, index):
        """
        Safely retrieves an item from a list at the specified index.
        
        This method provides a safe way to access list elements by:
        1. Checking if the input is actually a list
        2. Verifying the index is within bounds
        3. Ensuring the item exists and is not empty
        4. Converting the item to a string for consistent output
        
        Args:
            data_list: The list to extract an item from
            index: The position of the item to retrieve
            
        Returns:
            str: The item as a string if valid, empty string otherwise
        """
        # Check if data_list is a valid list and index is within bounds
        if isinstance(data_list, list) and len(data_list) > index:
            item = data_list[index]
            # Verify item exists and is not empty after converting to string
            if item is not None and str(item).strip():
                return str(item)
        return ""

    def show_scores(self, hk):
        if hk == "Học Kì 1":
            hk = "semester_1"
        elif hk == "Học Kì 2":
            hk = "semester_2"

        current_index = self.stackedWidget.currentIndex()
        if current_index < 0 or current_index >= len(self.lop_day):
            return

        ten_lop = self.lop_day[current_index]
        data = self.get_student_data(ten_lop, hk)

        model = self.model_dict[ten_lop]
        model.clear()

        headers = ["Họ tên", "Điểm miệng cột 1", "Điểm miệng cột 2", "Điểm 15p cột 1", "Điểm 15p cột 2", "Điểm 1 tiết cột 1", "Điểm 1 tiết cột 2", "Điểm Giữa kỳ", "Điểm Cuối kỳ"]
        model.setHorizontalHeaderLabels(headers)

        for idx, student in enumerate(data):
            values = [
                student.get('name', ''),
                self.safe_get_list_item(student.get('oral_scores', []), 0),
                self.safe_get_list_item(student.get('oral_scores', []), 1),
                self.safe_get_list_item(student.get('quiz_15min', []), 0),
                self.safe_get_list_item(student.get('quiz_15min', []), 1),
                self.safe_get_list_item(student.get('test_1period', []), 0),
                self.safe_get_list_item(student.get('test_1period', []), 1),
                str(student.get('midterm', '')) if student.get('midterm') is not None else "",
                str(student.get('final', '')) if student.get('final') is not None else ""
            ]

            row_items = []
            for val in values:
                item = QStandardItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                row_items.append(item)

            model.appendRow(row_items)
            model.setVerticalHeaderItem(idx, QStandardItem(str(idx + 1)))

        bang = self.bang_dict[ten_lop]
        bang.setModel(model)
        bang.resizeColumnsToContents()
        bang.resizeRowsToContents()

    def save_data(self):
        current_page_index = self.stackedWidget.currentIndex()
        if current_page_index < 0 or current_page_index >= len(self.lop_day):
            return

        current_lop = self.lop_day[current_page_index]
        current_semester = self.chonhocki.currentText()
        # xuwr lý tên học kỳ
        if current_semester == "Học Kì 1":
            current_semester = "semester_1"
        elif current_semester == "Học Kì 2":
            current_semester = "semester_2"


        #lấy dữ liêu từ bảng hiện tại
        model = self.model_dict[current_lop]

        data = []
        for row in range(model.rowCount()):
            student_data ={
                'name': model.item(row, 0).text(),
                'scores': {
                    'oral_scores': [
                        float(model.item(row, 1).text()) if model.item(row, 1).text() else None,
                        float(model.item(row, 2).text()) if model.item(row, 2).text() else None
                    ],
                    'quiz_15min': [
                        float(model.item(row, 3).text()) if model.item(row, 3).text() else None,
                        float(model.item(row, 4).text()) if model.item(row, 4).text() else None
                    ],
                    'test_1period': [
                        float(model.item(row, 5).text()) if model.item(row, 5).text() else None,
                        float(model.item(row, 6).text()) if model.item(row, 6).text() else None
                    ],
                    'midterm': float(model.item(row, 7).text()) if model.item(row, 7).text() else None,
                    'final': float(model.item(row, 8).text()) if model.item(row, 8).text() else None
                }
            }
            data.append(student_data)
        
        path = f"Data/Students/{current_lop}.json"
        self.student_manager = StudentManager(path, current_lop)
        self.student_manager.save_scores(self.mon_day, current_semester, data)
        QMessageBox.information(self, "Lưu thành công", "Dữ liệu đã được lưu thành công.")