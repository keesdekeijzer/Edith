from markdown_editor2 import Markdown_Editor
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout

def set_colors(window, background_color, text_color):
    window.setStyleSheet(f"background-color: {background_color}; color: {text_color};")

class Window(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.md = Markdown_Editor()
        layout.addWidget(self.md)

    def set_colors(self, background_color, text_color):
        self.setStyleSheet(f"background-color: {background_color}; color: {text_color};")
        self.md.setStyleSheet(f"background-color: {background_color}; color: {text_color};")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
