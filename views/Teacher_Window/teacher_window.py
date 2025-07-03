from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QListWidgetItem, QWidget, QTableView, QFileDialog,
    QAbstractItemView, QMessageBox, QInputDialog
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from PyQt6 import uic
from Service.student_service import StudentService
from models import teacher
from widgets.DialogComment import DialogComment
from widgets.comment_delegate import CommentButtonDelegate  # nếu tách file
import os

class TeacherWindow(QMainWindow):
    def __init__(self, teacher_dict):
        super().__init__()
        uic.loadUi(r"Assets\Ui\GV.ui", self)

        self.teacher_dict_data = teacher_dict
        self.lop_day = [str(item) for item in self.teacher_dict_data['lop day']]
        self.mon_day = self.teacher_dict_data['mon day']
        self.semester = "semester_1"

        self.bang_dict = {}
        self.model_dict = {}

        self.setUpUI()
        self.show()

    def setUpUI(self):
        teacher_name = self.teacher_dict_data['name']
        self.welcomeLabel.setText(f"Xin chào, {teacher_name}!")

        while self.stackedScoreWidget.count() > 0:
            widget = self.stackedScoreWidget.widget(0)
            self.stackedScoreWidget.removeWidget(widget)
            widget.deleteLater()

        self.classListWidget.clear()

        for ten_lop in self.lop_day:    
            item = QListWidgetItem(ten_lop)
            self.classListWidget.addItem(item)

            trang = QWidget()
            layout = QVBoxLayout(trang)

            bang = QTableView()
            bang.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
            bang.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            bang.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            bang.verticalHeader().setVisible(True)
            bang.verticalHeader().setSectionsClickable(True)
            bang.horizontalHeader().setVisible(True)
            layout.addWidget(bang)

            model = QStandardItemModel()

            self.bang_dict[ten_lop] = bang
            self.model_dict[ten_lop] = model
            self.stackedScoreWidget.addWidget(trang)

        self.classListWidget.currentRowChanged.connect(self.change_lop)
        self.stackedScoreWidget.setCurrentIndex(0)

        self.semesterComboBox.currentTextChanged.connect(
            lambda _: self.show_scores(self.semesterComboBox.currentText())
        )

        self.show_scores("Học kỳ 1")

        self.saveButton.clicked.connect(self.save_data)
        self.importButton.clicked.connect(self.import_student_scores)
        self.exportButton.clicked.connect(self.export_student_scores)
        self.logoutButton.clicked.connect(self.logout)

    def logout(self):
        from views.login_side import login
        reply = QMessageBox.question(self, "Đăng xuất", "Bạn có chắc chắn muốn đăng xuất không?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            login_window = login()
            login_window.show()
            self.close()

    def show_message(self, text):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Thông báo")
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def change_lop(self, index):
        self.stackedScoreWidget.setCurrentIndex(index)
        try:
            if hasattr(self, 'semesterComboBox') and self.semesterComboBox is not None:
                self.show_scores(self.semesterComboBox.currentText())
            else:
                self.show_scores("Học Kì 1")
        except RuntimeError:
            self.show_scores("Học Kì 1")

    def get_student_data(self, class_name, hk):
        if hk == "Học kỳ 1":
            hk = "semester_1"
        elif hk == "Học kỳ 2":
            hk = "semester_2"
        path = f"Data/Students/{class_name}.json"
        self.studentservice = StudentService(path, class_name)
        data = self.studentservice.load_student_scores_TEACHER_WINDOW(hk, self.mon_day)
        return data

    def safe_get_list_item(self, data_list, index):
        if isinstance(data_list, list) and len(data_list) > index:
            item = data_list[index]
            if item is not None and str(item).strip():
                return str(item)
        return ""

    def show_scores(self, hk):
        if hk == "Học Kì 1":
            hk = "semester_1"
        elif hk == "Học Kì 2":
            hk = "semester_2"

        current_index = self.stackedScoreWidget.currentIndex()
        if current_index < 0 or current_index >= len(self.lop_day):
            return

        ten_lop = self.lop_day[current_index]
        data = self.get_student_data(ten_lop, hk)

        model = self.model_dict[ten_lop]
        model.clear()

        headers = ["Họ tên", "Điểm miệng cột 1", "Điểm miệng cột 2", "Điểm 15p cột 1", "Điểm 15p cột 2", "Điểm 1 tiết cột 1", "Điểm 1 tiết cột 2", "Điểm Giữa kỳ", "Điểm Cuối kỳ", "Nhận xét"]
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

            comment_btn = QStandardItem("📝")
            comment_btn.setEditable(False)
            comment_btn.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            row_items.append(comment_btn)

            model.appendRow(row_items)

        bang = self.bang_dict[ten_lop]
        bang.setModel(model)
        delegate = CommentButtonDelegate(bang, lambda index: self.open_dialog_comment(index, ten_lop))
        bang.setItemDelegateForColumn(9, delegate)
        bang.resizeColumnsToContents()
        bang.resizeRowsToContents()
        bang.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        bang.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        bang.verticalHeader().setSectionsClickable(True)

    def open_dialog_comment(self, index, ten_lop):  
        model = self.model_dict[ten_lop]
        name = model.item(index.row(), 0).text()

        student = self.studentservice.get_student_by_name_TEACHER_WINDOW(name)
        if student:
            comment = student.comment.get(self.mon_day, "")
        else:
            comment = ""

        hocki = self.semesterComboBox.currentText() if hasattr(self, 'semesterComboBox') and self.semesterComboBox else "Học Kì 1"
        if hocki == "Học Kì 1":
            hk = "semester_1"
        elif hocki == "Học Kì 2":
            hk = "semester_2"
        scores_dict = student.scores[self.mon_day][hk]

        dialog = DialogComment(student_name=name, hocki=hocki, old_comment=comment, scores=scores_dict)
        if dialog.exec():
            new_comment = dialog.get_comment()
            self.studentservice.save_student_comment_TEACHER_WINDOW(student_name=name, mon_day=self.mon_day, comment=new_comment)

    def save_data(self):
        current_page_index = self.stackedScoreWidget.currentIndex()
        if current_page_index < 0 or current_page_index >= len(self.lop_day):
            return

        current_lop = self.lop_day[current_page_index]
        current_semester = self.semesterComboBox.currentText()
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
        self.studentservice = StudentService(path, current_lop)
        self.studentservice.save_scores_TEACHER_WINDOW(data=data, hk=current_semester, mon_day=self.mon_day)
        QMessageBox.information(self, "Lưu thành công", "Dữ liệu đã được lưu thành công.")

    def import_student_scores(self):
        print("Import nha")
        """
        Import student scores from an Excel file.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn file Excel",
            "./Data/Import",
            "Excel Files (*.xlsx *.xls)"
        )

        if file_path:
            current_page = self.stackedScoreWidget.currentIndex()
            current_class = self.lop_day[current_page]
            data_path = f"Data/Students/{current_class}.json"
            
            semester = self.semesterComboBox.currentText()
            self.studentservice = StudentService(data_path, current_class)
            print("Importing scores from Excel file... with file path:", file_path, "and mon_day:", self.mon_day, "and semester:", semester)
            self.studentservice.import_scores_from_excel_TEACHER_WINDOW(file_path=file_path, mon_day=self.mon_day, semester=semester)
            self.show_scores(self.semesterComboBox.currentText())

    def export_student_scores(self):
        print("Exort nha")
        export_folder = os.path.abspath(f"Data/Export")
        os.makedirs(export_folder, exist_ok=True)

        current_lop = self.stackedScoreWidget.currentIndex()
        if current_lop < 0 or current_lop >= len(self.lop_day):
            QMessageBox.warning(self, "Lỗi", "Không có lớp học nào được chọn.")
            return
        default_name = f"{self.lop_day[current_lop]}_Student_List.xlsx"

        file_path, _ = QFileDialog.getSaveFileName(
            parent=None,
            caption="Export File",
            directory=os.path.join(export_folder, default_name),
            filter="Excel Files (*.xlsx)"
        )

        if not file_path:
            return
        
        hk = self.semesterComboBox.currentText()
        if hk == "Học Kì 1":
            hk = "semester_1"
        elif hk == "Học Kì 2":
            hk = "semester_2"
        self.studentservice.export_scores_to_excel_TEACHER_WINDOW(file_path=file_path, mon_day=self.mon_day, semester=hk)
