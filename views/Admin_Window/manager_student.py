import json
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableView, QMessageBox, QFileDialog, QAbstractItemView
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6 import uic
import pandas as pd
from models import student
from widgets import dialog_add_student

class ManagerStudentsWindow(QMainWindow):
    def __init__(self, class_name):
        super().__init__()
        uic.loadUi("Ui/Manager_Stundets.ui", self)

        self.class_name = class_name
        self.json_path = f"Data/Students/{self.class_name}.json"
        self.students = []

        self.studenmanager = student.StudentManager(data_path=self.json_path, class_name=self.class_name)

        self.setUpUi()
        self.show()

    def setUpUi(self):
        self.back_btn.clicked.connect(self.close)
        self.import_btn.clicked.connect(self.import_teacher)
        self.add_btn.clicked.connect(self.add_student)
        self.remove_btn.clicked.connect(self.remove_student)
        self.save_btn.clicked.connect(lambda: self.studenmanager.save_from_table_model(self.model))
        self.export_btn.clicked.connect(self.export_student)

        # TableView setup
        self.tableView.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.model = QStandardItemModel()
        self.tableView.setModel(self.model)
        self.model.setHorizontalHeaderLabels(
            ["ID", "Họ tên", "Giới tính", "Ngày sinh", "Tài khoản PH", "Mật khẩu PH"]
        )

        self.load_data_to_ui()

    def load_data_to_ui(self):

        self.model.removeRows(0, self.model.rowCount())

        for student_obj in self.studenmanager.students:
            self.model.appendRow([
                QStandardItem(student_obj.id),
                QStandardItem(student_obj.name),
                QStandardItem(student_obj.gender),
                QStandardItem(student_obj.dob),
                QStandardItem(student_obj.parent_account),
                QStandardItem(student_obj.parent_password),
            ])

    def save_data(self):
        students = []

        for row in range(self.model.rowCount()):
            student = {
                "id": self.model.item(row, 0).text(),
                "name": self.model.item(row, 1).text(),
                "gender": self.model.item(row, 2).text(),
                "dob": self.model.item(row, 3).text(),
                "parent_account": self.model.item(row, 4).text(),
                "parent_password": self.model.item(row, 5).text(),
                "class": self.class_name,
                "scores": {},
                "comment": {}
            }
            students.append(student)

        from Data import data_io
        data_io.write_json_data(students, self.json_path)
        QMessageBox.information(self, "Đã lưu", f"Đã lưu {len(students)} học sinh vào lớp {self.class_name}.")

    def add_student(self):
        dialog = dialog_add_student.Dialog_Them_Student()
        if dialog.exec():
            student_data = dialog.return_input_fields()
            self.studenmanager.add_student(student_data)
            self.load_data_to_ui()

    def remove_student(self):
        selected_indexes = self.tableView.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.warning(self, "Chưa chọn", "Hãy chọn ít nhất 1 học sinh để xóa.")
            return

        confirm = QMessageBox.question(self, "Xác nhận", "Bạn chắc chắn muốn xóa học sinh này?")
        if confirm != QMessageBox.StandardButton.Yes:
            return

        # Lấy danh sách ID học sinh bị xóa
        removed_ids = [self.model.item(index.row(), 0).text() for index in selected_indexes]

        # Xóa khỏi model UI (từ dưới lên để không lệch index)
        for index in sorted(selected_indexes, key=lambda x: -x.row()):
            self.model.removeRow(index.row())

        # Gọi model để xóa trong danh sách và JSON
        self.studenmanager.remove_students_by_ids(removed_ids)

        QMessageBox.information(self, "Đã xóa", f"Đã xóa {len(removed_ids)} học sinh.")

    def import_teacher(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn file Excel",
            "./Data/Import",
            "Excel Files (*.xlsx *.xls)"
        )

        if file_path:
            # gọi hàm xử lý file Excel tại đây
            self.studenmanager.import_from_excel(file_path)
            self.load_data_to_ui()  # cập nhật lại bảng sau khi import

    def export_student(self):
        self.studenmanager.export_to_excel()