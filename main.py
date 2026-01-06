import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from mainwindow import Ui_MainWindow

# pyuic6 -o mainwindow.py mainwindow.ui


class Venster(QWidget):
    def __init__(self):
        super().__init__()

        # Hoofdvenster
        self.ui = Ui_MainWindow()       
        self.ui.setupUi(self)       
        
        # laat het venster zien
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Ui_MainWindow()
    w = QMainWindow()
    ex.setupUi(w)
    w.show()
    sys.exit(app.exec())
