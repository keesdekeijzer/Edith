from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont

class OutlinePanel(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Arial", 12))
        self.headings = []  # level, text, line

    def update_outline(self, headings):
        self.clear()
        self.headings = headings

        for level, text, line in self.headings:
            item = QListWidgetItem(text)
            indent = (level - 1) * 20
            item.setData(32, line)  # Store line number in user data
            item.setText(" " * (level - 1) * 2 + text)  # Indent based on heading level
            self.addItem(item)

