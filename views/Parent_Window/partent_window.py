from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QApplication, QTableWidgetItem, QHeaderView, QGraphicsScene, QGraphicsPixmapItem
)
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
from Service.student_service import StudentService
import sys

class ParentWindow(QMainWindow):
    def __init__(self, student_name, class_name, data_path):
        super().__init__()
        uic.loadUi(r"Assets\Ui\parent_window.ui", self)
        
        self.data_path = data_path

        self.student_service = StudentService(class_name=class_name, data_path=data_path)
        student = self.student_service.get_student_by_name_TEACHER_WINDOW(student_name)

        self.name = student_name
        self.gender = student.gender
        self.comment = student.comment
        self.class_name = class_name
        

        print(self.name)
        print(self.gender)
        print(self.comment)
        print(self.class_name)

        self.setUpUi()

        self.show()
    
    def setUpUi(self):
        self.setWindowTitle("Parent Window")
        
        # Set text
        self.label_name.setText(f"<b>Họ tên:</b> {self.name}")
        self.label_gender.setText(f"<b>Giới tính:</b> {self.gender}")
        self.label_class.setText(f"<b>Lớp:</b> {self.class_name}")
        self.label_welcome.setText(f"Xin chào phụ huynh của em, <b>{self.name}<b>!")

        # load comment lên table
        filtered_comments = [(mon, cmt) for mon, cmt in self.comment.items() if cmt.strip() != ""]
        self.table_comments.setRowCount(len(filtered_comments))
        self.table_comments.verticalHeader().setVisible(False)

        for row, (subject, cmt) in enumerate(filtered_comments):
            self.table_comments.setItem(row, 0, QTableWidgetItem(subject))
            self.table_comments.setItem(row, 1, QTableWidgetItem(cmt))

        # load scores lên table 
        for table in [self.table_hk1, self.table_hk2, self.table_year]:
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            table.verticalHeader().setVisible(False)
        
        self.load_scores_to_ui()

        self.btn_logout.clicked.connect(self.logout)

    def load_scores_to_ui(self):
        student_service = StudentService(class_name=self.class_name, data_path=self.data_path)
        HK1_SCORES, HK2_SCORES, YEAR_SCORES = student_service.get_student_scores(self.name)

        self.load_score_to_table(self.table_hk1, HK1_SCORES)
        self.load_score_to_table(self.table_hk2, HK2_SCORES)
        self.load_year_score_to_table(self.table_year, YEAR_SCORES)


    def load_score_to_table(self, table, score_data):
        table.setRowCount(len(score_data))
        for row, subject_scores in enumerate(score_data):
            print(f"DEBUG {row=} {type(subject_scores)=} {subject_scores=}")
            if not isinstance(subject_scores, dict):
                print(f"[WARNING] Dòng {row} không phải dict: {subject_scores}")
                continue
            
            subject, scores = list(subject_scores.items())[0]

            table.setItem(row, 0, QTableWidgetItem(subject))
            table.setItem(row, 1, QTableWidgetItem(self.format_list(scores.get("oral_scores"))))
            table.setItem(row, 2, QTableWidgetItem(self.format_list(scores.get("quiz_15min"))))
            table.setItem(row, 3, QTableWidgetItem(self.format_list(scores.get("test_1period"))))
            table.setItem(row, 4, QTableWidgetItem(str(scores.get("midterm")) if scores.get("midterm") is not None else ""))
            table.setItem(row, 5, QTableWidgetItem(str(scores.get("final")) if scores.get("final") is not None else ""))
            table.setItem(row, 6, QTableWidgetItem(str(scores.get("average")) if scores.get("average") is not None else ""))

    def load_year_score_to_table(self, table, year_scores):
        print(year_scores)
        print(type(year_scores))
        table.setRowCount(len(year_scores))

        year_averages = []
        for row, (subject, scores) in enumerate(year_scores.items()):
            print(subject, scores)

            # kiểm tra xem tính dc trung bình năm chưa, bằng cách tính tb năm
            ave_year_sc =  self.student_service.tinh_diem_trung_binh_nam(scores.get("semester_1"), scores.get("semester_2"))

            # list này để lưu trữ điểm trung cả năm nếu điểm không trống
            print("TBN: ", ave_year_sc)
            if ave_year_sc is not None:
                year_averages.append(ave_year_sc)

            table.setItem(row, 0, QTableWidgetItem(subject))
            table.setItem(row, 1, QTableWidgetItem(str(scores.get("semester_1")) if scores.get("semester_1") is not None else ""))
            table.setItem(row, 2, QTableWidgetItem(str(scores.get("semester_2")) if scores.get("semester_2") is not None else ""))
            table.setItem(row, 3, QTableWidgetItem(str(ave_year_sc) if ave_year_sc is not None else ""))

        # Check if all average semester scores are present before proceeding
        all_semester_scores_filled = all(
            scores.get("semester_1") is not None and scores.get("semester_2") is not None
            for scores in year_scores.values()
        )
        if all_semester_scores_filled and len(year_averages) == 4:
            # xếp loại học sinh
            print('year ave')
            print(year_averages)
            xep_loai = self.student_service.xep_loai_hoc_sinh(year_averages)

            if xep_loai:
                self.xeploai.setText(f"<b>Xếp loại:</b> {xep_loai}")

            # vẽ biểu đồ
            image_path = "Assets/Charts/parent_chart.png"
            self.student_service.tao_bieu_do_cot(avg_scores=year_scores, output_path=image_path)
            self.display_chart_image(self.chartViewPlaceholder, image_path)
        else:
            self.xeploai.setText("Chưa đủ điểm")
    def format_list(self, val):
        # Chuyển list như [8.5, 9] → '8.5, 9' — nếu None thì rỗng
        if isinstance(val, list):
            return "  ".join(str(v) for v in val if v is not None)
        return ""
    
    def display_chart_image(self, view_widget, image_path: str):
        scene = view_widget.scene()
        if scene is None:
            scene = QGraphicsScene()
            view_widget.setScene(scene)
        else:
            scene.clear()

        pixmap = QPixmap(image_path)
        scene.addItem(QGraphicsPixmapItem(pixmap))

    def logout(self):
        from views.login_side import login
        reply = QMessageBox.question(self, "Đăng xuất", "Bạn có chắc chắn muốn đăng xuất không?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            login_window = login()
            login_window.show()
            self.close()

        # else: do nothing, stay in the window