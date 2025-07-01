from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from PyQt6 import uic

class DialogComment(QDialog):
    def __init__(self, student_name, hocki, old_comment, scores):
        super().__init__()
        uic.loadUi("Ui\Dialog_nhanxet_hocsinh.ui", self)

        self.student_name = student_name
        self.hocki = hocki
        self.old_comment = old_comment
        self.scores = scores
        print("old_comment là :", self.old_comment)

        self.setWindowTitle("Nhận xét học sinh")
        
        self.setupUI()


    def setupUI(self):
        #set casc thong  tin
        self.name_label.setText(self.student_name)
        self.hocki_label.setText(self.hocki)
        self.nx_edit.setText(self.old_comment)

        self.miNgLineEdit.setText("   ".join(str(x) if x is not None else "" for x in self.scores["oral_scores"]))
        self.PhTLineEdit.setText("   ".join(str(x) if x is not None else "" for x in self.scores["quiz_15min"]))
        self.TiTLineEdit.setText("   ".join(str(x) if x is not None else "" for x in self.scores["test_1period"]))
        self.giAKLineEdit.setText(str(self.scores["midterm"]) if self.scores["midterm"] is not None else "")
        self.cuIKLineEdit.setText(str(self.scores["final"]) if self.scores["final"] is not None else "")

        # set các qline là ko thể edit
        self.miNgLineEdit.setReadOnly(True)
        self.PhTLineEdit.setReadOnly(True)
        self.TiTLineEdit.setReadOnly(True)
        self.giAKLineEdit.setReadOnly(True)
        self.cuIKLineEdit.setReadOnly(True)

        self.nxot_btn.clicked.connect(lambda: self.save_comment("Tốt"))
        self.nxccg_btn.clicked.connect(lambda: self.save_comment("Cần cố gắng"))
        self.nxtb_btn.clicked.connect(lambda: self.save_comment("Tiến bộ"))

    def save_comment(self, option):
        if option == "Tốt":
            text = "Em học tốt, chăm chỉ và có thái độ học tập nghiêm túc. Cô/Thầy rất hài lòng với sự cố gắng của em 💯"
            self.nx_edit.setText(text)
        elif option == "Cần cố gắng":
            text = "Em có tiềm năng, nhưng cần tập trung và nỗ lực hơn nữa để phát huy hết khả năng của mình. Cố lên nha 💪"
            self.nx_edit.setText(text)
        elif option == "Tiến bộ":
            text = "Em đã có sự tiến bộ rõ rệt trong thời gian qua. Cố gắng duy trì và phát triển hơn nữa nhé, rất đáng khen 👏"
            self.nx_edit.setText(text)

    def get_comment(self):
        return self.nx_edit.text()