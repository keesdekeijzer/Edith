import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QFileDialog, QDialog, QMessageBox
from mainwindow import Ui_MainWindow
from PyQt6.uic import loadUi
import datetime
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QTextCharFormat

# pyuic6 -o mainwindow.py mainwindow.ui


class Venster(QMainWindow):
    def __init__(self):
        super().__init__()

        # Hoofdvenster
        # self.ui = Ui_MainWindow()       
        # self.ui.setupUi(self)
        loadUi("mainwindow.ui",self)

        self.current_path = None
        self.current_fontsize = 12
        self.is_vet = False

        self.actionNieuw.triggered.connect(self.nieuw)
        self.actionOpslaan.triggered.connect(self.opslaan)
        self.actionOpslaan_als.triggered.connect(self.opslaan_als)

        self.actionOpen.triggered.connect(self.open)

        self.actionAfdrukken.triggered.connect(self.afdrukken)

        self.actionSluiten.triggered.connect(self.sluiten)

        self.actionKopieren.triggered.connect(self.kopieren)
        self.actionKnippen.triggered.connect(self.knippen)
        self.actionPlakken.triggered.connect(self.plakken)

        self.actionZoeken.triggered.connect(self.zoeken)
        self.actionVervangen.triggered.connect(self.vervangen)

        self.actionUndo.triggered.connect(self.undo)
        self.actionRedo.triggered.connect(self.redo)

        self.actionAlles_selecteren.triggered.connect(self.alles_selecteren)

        self.actiondonkere_modus.triggered.connect(self.gebruik_donkere_modus)
        self.actionlichte_modus.triggered.connect(self.gebruik_lichte_modus)

        self.actionletters_groter.triggered.connect(self.letters_groter)
        self.actionletters_kleiner.triggered.connect(self.letters_kleiner)

        self.actionRechts.triggered.connect(self.rechts)
        self.actionMidden.triggered.connect(self.midden)
        self.actionLinks.triggered.connect(self.links)
        self.actionVerdelen.triggered.connect(self.verdelen)

        self.actionDatum.triggered.connect(self.datum)
        self.actionTijd.triggered.connect(self.tijd)
        self.actionVandaag.triggered.connect(self.vandaag)

        self.actionCursief.triggered.connect(self.cursief)
        self.actionVet.triggered.connect(self.vet)
        self.actionOnderstrepen.triggered.connect(self.onderstrepen)

        self.actionOver_Edith.triggered.connect(self.over_edith)

    def nieuw(self):
        print("nieuw")
        self.textEdit.clear()
        self.setWindowTitle("Geen naam")
        self.current_path = None

    def opslaan(self):
        print("opslaan")
        if self.current_path is not None:
            filetext = self.textEdit.toPlainText()
            print(filetext)
            try:
                with open(self.current_path, 'w') as f:
                    f.write(filetext)
            except Exception as e:
                self.dialog_critical(str(e))
        else:
            self.opslaan_als()

    def opslaan_als(self):
        print("opslaan als")
        try:
            pathname = QFileDialog.getSaveFileName(self, 'Bestand opslaan', 'Documenten', 'Tekst bestanden (*.txt, *.md)')
            print(pathname[0])
            filetext = self.textEdit.toPlainText()
            with open(pathname[0], 'w') as f:
                f.write(filetext)
            self.current_path = pathname[0]
            self.setWindowTitle(pathname[0])
        except Exception as e:
            self.dialog_critical(str(e))

    def open(self):
        print("open")
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open bestand', 'Documenten', 'Tekst bestanden (*.txt *.md)')
            print(fname[0]) # gekozen bestand
            self.setWindowTitle(fname[0])
            with open(fname[0], 'r') as f:
                filetext = f.read()
                self.textEdit.setText(filetext)
            self.current_path = fname[0]
        except Exception as e:
            self.dialog_critical(str(e))

    def afdrukken(self):
        print("afdrukken")
        try:
            printer = QPrinter()
            dlg = QPrintDialog(printer, self)
            if dlg.exec() == QDialog.accepted:
                self.textEdit.print(printer)
        except Exception as e:
            self.dialog_critical(str(e))

    def sluiten(self):
        print("sluiten")
        sys.exit()

    def kopieren(self):
        print("kopieren")
        self.textEdit.copy()

    def knippen(self):
        print("knippen")
        self.textEdit.cut()

    def plakken(self):
        print("plakken")
        self.textEdit.paste()

    def zoeken(self): # todo
        print("zoeken")

    def vervangen(self): # todo
        print("vervangen")

    def undo(self):
        print("undo")
        self.textEdit.undo()

    def redo(self):
        print("redo")
        self.textEdit.redo()

    def alles_selecteren(self):
        print("alles selecteren")

    def gebruik_donkere_modus(self):
        self.setStyleSheet('''
            QWidget{
                background-color: rgb(33,33,33);
                color: #FFFFFF;
                }
            QTextEdit{
                background-color: rgb(46,46,46);
                }
            QMenuBar::item:selected{
                color: #000000;
                }               
            ''')

    def gebruik_lichte_modus(self):
        self.setStyleSheet("")

        # laat het venster zien
        self.show()

    def letters_groter(self):
        self.current_fontsize +=1
        self.textEdit.setFontPointSize(self.current_fontsize)

    def letters_kleiner(self):
        self.current_fontsize -=1
        self.textEdit.setFontPointSize(self.current_fontsize)

    def rechts(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignRight)

    def midden(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def links(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def verdelen(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignJustify)

    def datum(self): # todo
        nu = datetime.datetime.now()
        datum_nu = nu.strftime("%Y-%m-%d")
        print(f"datum: {datum_nu}")
        self.textEdit.insertPlainText(datum_nu)

    def tijd(self):
        nu = datetime.datetime.now()
        tijd_nu = nu.strftime("%H:%M")
        print(f"tijd: {tijd_nu}")
        self.textEdit.insertPlainText(tijd_nu)

    def vandaag(self):
        nu = datetime.datetime.now()
        datum_nu = nu.strftime("%Y-%m-%d")
        print(f"datum: {datum_nu}")
        self.textEdit.insertPlainText(datum_nu)

    def cursief(self):
        print(f"cursief: {self.textEdit.fontItalic()}")
        if self.textEdit.fontItalic():
            self.textEdit.setFontItalic(False)
        else:
            self.textEdit.setFontItalic(True)
        

    def vet(self):
        print(f"vet: {self.textEdit.fontWeight()}")
        if self.is_vet:
            self.is_vet = False
            self.textEdit.setFontWeight(400)
        else:
            self.is_vet = True
            self.textEdit.setFontWeight(800)

    def onderstrepen(self):
        print("onderstrepen")
        if self.textEdit.fontUnderline():
            self.textEdit.setFontUnderline(False)
        else:
            self.textEdit.setFontUnderline(True)

    def over_edith(self):
        print("over edith")
        QMessageBox.about(self, "Over Edith", "Edith is een tekstbewerker gemaakt met Python en PyQt6")

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Icon.Critical)
        dlg.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Venster()
    ui.show()
    app.exec()

