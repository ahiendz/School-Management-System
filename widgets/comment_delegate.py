from PyQt6.QtWidgets import QStyledItemDelegate, QStyleOptionButton, QStyle
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class CommentButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent, on_click):
        super().__init__(parent)
        self.on_click = on_click
        self.icon = QIcon("reports\pencil_6218548.png")  # icon bạn chọn

    def paint(self, painter, option, index):
        if index.column() == 9:
            btn_option = QStyleOptionButton()
            btn_option.rect = option.rect
            btn_option.icon = self.icon
            btn_option.iconSize = option.rect.size()
            btn_option.state = QStyle.StateFlag.State_Enabled
            option.widget.style().drawControl(QStyle.ControlElement.CE_PushButtonLabel, btn_option, painter)
        else:
            super().paint(painter, option, index)

    def editorEvent(self, event, model, option, index):
        # Chỉ xử lý click chuột trái ở cột 9
        if index.column() == 9 and event.type() == event.Type.MouseButtonRelease:
            self.on_click(index)
            return True  # Đã xử lý event, không để Qt xử lý tiếp
        return False  # Các cột khác: để Qt xử lý mặc định (cho phép edit)
