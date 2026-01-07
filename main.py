import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from mainwindow import Ui_MainWindow
from PyQt6.uic import loadUi

# pyuic6 -o mainwindow.py mainwindow.ui


class Venster(QMainWindow):
    def __init__(self):
        super().__init__()

        # Hoofdvenster
        # self.ui = Ui_MainWindow()       
        # self.ui.setupUi(self)
        loadUi("mainwindow.ui",self)

        self.actionNieuw.triggered.connect(self.nieuw)
        self.actionOpslaan.triggered.connect(self.opslaan)
        self.actionOpslaan_als.triggered.connect(self.opslaan_als)

        self.actionOpen.triggered.connect(self.open)

        self.actionSluiten.triggered.connect(self.sluiten)

        self.actionKopieren.triggered.connect(self.kopieren)
        self.actionKnippen.triggered.connect(self.knippen)
        self.actionPlakken.triggered.connect(self.plakken)

        self.actionZoeken.triggered.connect(self.zoeken)
        self.actionVervangen.triggered.connect(self.vervangen)

        self.actionUndo.triggered.connect(self.undo)
        self.actionRedo.triggered.connect(self.redo)

    def nieuw(self):
        print("nieuw")

    def opslaan(self):
        print("opslaan")

    def opslaan_als(self):
        print("opslaan als")

    def open(self):
        print("open")

    def sluiten(self):
        print("sluiten")

    def kopieren(self):
        print("kopieren")

    def knippen(self):
        print("knippen")

    def plakken(self):
        print("plakken")

    def zoeken(self):
        print("zoeken")

    def vervangen(self):
        print("vervangen")

    def undo(self):
        print("undo")

    def redo(self):
        print("redo")

        # laat het venster zien
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Venster()
    ui.show()
    app.exec()

