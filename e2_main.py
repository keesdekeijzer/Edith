from markdown_editor2 import Markdown_Editor
from PyQt6.QtWidgets import QApplication
import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout

class Window(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.md = Markdown_Editor()
        layout.addWidget(self.md)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
