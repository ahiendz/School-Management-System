from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableView, QPushButton
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import json

class ScoreEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chỉnh sửa điểm học sinh")
        self.resize(600, 300)

        self.table = QTableView()
        self.model = QStandardItemModel()
        self.table.setModel(self.model)

        self.btn_save = QPushButton("Lưu về JSON")
        self.btn_save.clicked.connect(self.save_to_json)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.btn_save)
        self.setLayout(layout)

        self.load_data()

    def load_data(self):
        # Giả lập file JSON
        with open("diem.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        self.model.setHorizontalHeaderLabels(["Tên", "Toán", "Văn", "Anh", "KHTN"])
        for student in data:
            items = [QStandardItem(student["name"])]
            for mon in ["math", "lit", "eng", "sci"]:
                item = QStandardItem(str(student.get(mon, "")))
                item.setEditable(True)
                items.append(item)
            self.model.appendRow(items)

    def save_to_json(self):
        result = []
        for row in range(self.model.rowCount()):
            student = {
                "name": self.model.item(row, 0).text(),
                "math": self.model.item(row, 1).text(),
                "lit": self.model.item(row, 2).text(),
                "eng": self.model.item(row, 3).text(),
                "sci": self.model.item(row, 4).text()
            }
            result.append(student)

        with open("diem.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print("Đã lưu!")

app = QApplication([])
window = ScoreEditor()
window.show()
app.exec()
