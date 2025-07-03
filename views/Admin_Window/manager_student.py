import json
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QFileDialog, QAbstractItemView ,QHeaderView
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6 import uic
from Service.student_service import StudentService
from widgets import dialog_add_student

DEFAULT_SCORES = {
    "Toán": {
        "semester_1": {"oral_scores": [], "quiz_15min": [], "test_1period": [], "midterm": None, "final": None, "average": None},
        "semester_2": {"oral_scores": [], "quiz_15min": [], "test_1period": [], "midterm": None, "final": None, "average": None},
    },
    "Văn": {
        "semester_1": {"oral_scores": [], "quiz_15min": [], "test_1period": [], "midterm": None, "final": None, "average": None},
        "semester_2": {"oral_scores": [], "quiz_15min": [], "test_1period": [], "midterm": None, "final": None, "average": None},
    },
    "KHTN": {
        "semester_1": {"oral_scores": [], "quiz_15min": [], "test_1period": [], "midterm": None, "final": None, "average": None},
        "semester_2": {"oral_scores": [], "quiz_15min": [], "test_1period": [], "midterm": None, "final": None, "average": None},
    },
    "Anh": {
        "semester_1": {"oral_scores": [], "quiz_15min": [], "test_1period": [], "midterm": None, "final": None, "average": None},
        "semester_2": {"oral_scores": [], "quiz_15min": [], "test_1period": [], "midterm": None, "final": None, "average": None},
    },
}

class ManagerStudentsWindow(QMainWindow):
    def __init__(self, class_name):
        super().__init__()
        uic.loadUi(r"Assets\Ui\Manager_Stundets.ui", self)


        self.class_name = class_name
        self.json_path = f"Data/Students/{self.class_name}.json"
        self.students = []

        self.student_service = StudentService(class_name=self.class_name, data_path=self.json_path)

        self.setUpUi()
        self.show()

    def setUpUi(self):
        self.btnBack.clicked.connect(self.close)
        self.btnImport.clicked.connect(self.import_student)
        self.btnAdd.clicked.connect(self.add_student)
        self.btnRemove.clicked.connect(self.remove_student)
        self.btnSave.clicked.connect(lambda: self.save_student(self.model))
        self.btnExport.clicked.connect(self.export_student)

        self.labelClassName.setText(f"<b>📚 Đang quản lý học sinh lớp: {self.class_name}</b>")

        # tableStudents setup
        self.tableStudents.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.model = QStandardItemModel()
        self.tableStudents.setModel(self.model)
        self.model.setHorizontalHeaderLabels(
            ["ID", "Họ tên", "Giới tính", "Ngày sinh", "Tài khoản PH", "Mật khẩu PH"]
        )

        self.load_data_to_ui()

    def load_data_to_ui(self):
        students = self.student_service.load_student_info_ADMIN_WINDOW()
        self.model.removeRows(0, self.model.rowCount())

        for student_obj in students:
            self.model.appendRow([
                QStandardItem(student_obj.id),
                QStandardItem(student_obj.name),
                QStandardItem(student_obj.gender),
                QStandardItem(student_obj.dob),
                QStandardItem(student_obj.parent_account),
                QStandardItem(student_obj.parent_password),
            ])

        header = self.tableStudents.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)  # default
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # STT nhỏ gọn
        for col in range(1, self.model.columnCount()):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)

    def add_student(self):
        dialog = dialog_add_student.Dialog_Them_Student()
        if dialog.exec():
            student_data = dialog.return_input_fields()
            self.student_service.add_student_to_class_ADMIN_WINDOW(student_data)
            self.load_data_to_ui()

    def remove_student(self):
        selected_indexes = self.tableStudents.selectionModel().selectedRows()
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
        self.student_service.remove_student_from_class_ADMIN_WINDOW(removed_ids)

        QMessageBox.information(self, "Đã xóa", f"Đã xóa {len(removed_ids)} học sinh.")

    def import_student(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn file Excel",
            "./Data/Import",
            "Excel Files (*.xlsx *.xls)"
        )

        if file_path:
            # gọi hàm xử lý file Excel tại đây
            self.student_service.import_students_from_file_ADMIN_WINDOW(file_path)
            self.load_data_to_ui()  # cập nhật lại bảng sau khi import

    def export_student(self):
        export_folder = os.path.abspath(f"Data/Export")
        os.makedirs(export_folder, exist_ok=True)

        default_name = f"{self.class_name}_Student_List.xlsx"

        file_path, _ = QFileDialog.getSaveFileName(
            parent=None,
            caption="Export File",
            directory=os.path.join(export_folder, default_name),
            filter="Excel Files (*.xlsx)"
        )

        if not file_path:
            return
        self.student_service.export_students_to_file_ADMIN_WINDOW(file_path)

    def save_student(self, model: QStandardItemModel):
        data = []
        for row in range(model.rowCount()):
            item = {
                "id": model.item(row, 0).text(),
                "name": model.item(row, 1).text(),
                "gender": model.item(row, 2).text(),
                "dob": model.item(row, 3).text(),
                "parent_account": model.item(row, 4).text(),
                "parent_password": model.item(row, 5).text(),
                "class": self.class_name,
                "scores": DEFAULT_SCORES.copy(),
                "comment": {}
            }
            data.append(item)

        self.student_service.save_students_to_json_ADMIN_WINDOW(data)
        QMessageBox.information(self, "Lưu thành công", "Dữ liệu đã được lưu thành công.")