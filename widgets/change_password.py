from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QMessageBox, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from Service import AccountService
import os

class ChangePasswordDialog(QDialog):
    def __init__(self, username, role, class_name=None):
        super().__init__()
        uic.loadUi(r"Assets\Ui\dialog_change_psW.ui", self)

        self.account_service = AccountService.AccountService()
        self.username = username
        self.role = role
        self.class_name = class_name

        # Setup icon eye state trackers
        self.eye_pressed_new = False
        self.eye_pressed_confirm = False

        # Kết nối các nút (đảm bảo tên đúng với file .ui)
        self.changePasswordButton.clicked.connect(self.handle_change_password)
        self.cancelButton.clicked.connect(self.reject)

        # Kết nối chức năng ẩn/hiện mật khẩu: chỉ hiện khi nhấn giữ QToolButton con mắt
        # Đảm bảo các trường và nút tồn tại đúng như trong file .ui bạn vừa gửi
        try:
            # Mật khẩu hiện tại
            self.eyeButtonOld.pressed.connect(
                lambda: self.oldPasswordLineEdit.setEchoMode(self.oldPasswordLineEdit.EchoMode.Normal)
            )
            self.eyeButtonOld.released.connect(
                lambda: self.oldPasswordLineEdit.setEchoMode(self.oldPasswordLineEdit.EchoMode.Password)
            )
            # Mật khẩu mới
            self.eyeButtonNew.pressed.connect(
                lambda: self.newPasswordLineEdit.setEchoMode(self.newPasswordLineEdit.EchoMode.Normal)
            )
            self.eyeButtonNew.released.connect(
                lambda: self.newPasswordLineEdit.setEchoMode(self.newPasswordLineEdit.EchoMode.Password)
            )
            # Nhập lại mật khẩu mới
            self.eyeButtonConfirm.pressed.connect(
                lambda: self.confirmPasswordLineEdit.setEchoMode(self.confirmPasswordLineEdit.EchoMode.Normal)
            )
            self.eyeButtonConfirm.released.connect(
                lambda: self.confirmPasswordLineEdit.setEchoMode(self.confirmPasswordLineEdit.EchoMode.Password)
            )
        except AttributeError:
            print("[INFO] Eye buttons or password fields not found. Show/hide password feature disabled.")

    def handle_change_password(self):
        try:
            old_pass = self.oldPasswordLineEdit.text()
            new_pass = self.newPasswordLineEdit.text()
            confirm_pass = self.confirmPasswordLineEdit.text()
        except AttributeError:
            QMessageBox.warning(self, "Lỗi", "Thiếu trường nhập mật khẩu trong UI. Kiểm tra lại .ui file.")
            return

        if not old_pass or not new_pass or not confirm_pass:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đủ thông tin.")
            return

        if new_pass != confirm_pass:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu mới không khớp.")
            return

        success, message = self.account_service.change_password(
            username=self.username,
            old_password=old_pass,
            new_password=new_pass,
            role=self.role,
            class_name=self.class_name
        )

        if success:
            QMessageBox.information(self, "Thành công", message)
            self.accept()
        else:
            QMessageBox.warning(self, "Lỗi", message)
