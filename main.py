import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QDialog, QMessageBox, QStatusBar, QLabel
from PyQt6.QtWidgets import QLineEdit, QHBoxLayout, QVBoxLayout, QInputDialog
# from mainwindow import Ui_MainWindow
from PyQt6.uic import loadUi
import datetime
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QTextCursor
import sqlite3

from notitie import Notitie
from memolijst import MemoLijst
from memo import Memo

# pyuic6 -o mainwindow.py mainwindow.ui

# Pad naar de database : instelbaar maken?

from config import configuratie

BLAUW = '''
            QWidget{
                background-color: #00BFFF;
                color: #000000;
                }
            QTextEdit{
                background-color: #000BFF;
                color: #FFFFFF;
                }
            QMenuBar::item:selected{
                color: #000000;
                }               
            '''

DONKER = '''
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
            '''


class ZoekenVervangenDialoog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Zoeken en Vervangen")
        self.setModal(False)
        self.parent = parent

        if configuratie["darkmode"]:
            self.setStyleSheet('''
                QWidget{
                    background-color: rgb(33,33,33);
                    color: #FFFFFF;
                    }
                QTextEdit{
                    background-color: rgb(46,46,46);
                    }''')

        self.vind_label = QLabel("Vind:")
        self.vind_invoer = QLineEdit()
        self.vervang_label = QLabel("Vervang:")
        self.vervang_invoer = QLineEdit()

        self.vind_volgende_knop = QPushButton("Vind volgende")
        self.vervang_knop = QPushButton("Vervang")
        self.alles_vervangen_knop = QPushButton("Alles vervangen")
        self.sluit_knop = QPushButton("Sluiten")

        h1 = QHBoxLayout()
        h1.addWidget(self.vind_label)
        h1.addWidget(self.vind_invoer)

        h2 = QHBoxLayout()
        h2.addWidget(self.vervang_label)
        h2.addWidget(self.vervang_invoer)

        h3 = QHBoxLayout()
        h3.addWidget(self.vind_volgende_knop)
        h3.addWidget(self.vervang_knop)
        h3.addWidget(self.alles_vervangen_knop)
        h3.addWidget(self.sluit_knop)

        v = QVBoxLayout()
        v.addLayout(h1)
        v.addLayout(h2)
        v.addLayout(h3)
        self.setLayout(v)

        self.vind_volgende_knop.clicked.connect(self.vind_volgende)
        self.vervang_knop.clicked.connect(self.vervang_een)
        self.alles_vervangen_knop.clicked.connect(self.vervang_alle)
        self.sluit_knop.clicked.connect(self.close)

    def vind_volgende(self):
        text = self.vind_invoer.text()
        if not text:
            return
        gevonden = self.parent.textEdit.find(text)
        if not gevonden:
            # weer naar boven
            cursor = self.parent.textEdit.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            self.parent.textEdit.setTextCursor(cursor)
            gevonden = self.parent.textEdit.find(text)
            print(f"'{text}' niet gevonden")
            if not gevonden:
                term = text.replace('<','&lt;')
                term = term.replace('>','&gt;')
                QMessageBox.information(self, "Vinden", f"'{term}' niet gevonden")

    def vervang_een(self):
        cursor = self.parent.textEdit.textCursor()
        if cursor.hasSelection():
            selectie = cursor.selectedText()
            zoek_tekst = self.vind_invoer.text()
            if (selectie == zoek_tekst):
                cursor.insertText(self.vervang_invoer.text())
        self.vind_volgende()

    def vervang_alle(self):
        zoek_tekst = self.vind_invoer.text()
        vervang_tekst = self.vervang_invoer.text()
        if not zoek_tekst:
            return
        doc = self.parent.textEdit.document()
        cursor = QTextCursor(doc)
        text = doc.toPlainText()
        nieuwe_tekst = text.replace(zoek_tekst, vervang_tekst)
        # vervang het hele document, met 1 undo te herstellen 
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.insertText(nieuwe_tekst)



class Venster(QMainWindow):
    def __init__(self):
        super().__init__()

        # Hoofdvenster
        loadUi("mainwindow2.ui",self)

        self.current_path = None
        self.current_fontsize = 12
        self.is_vet = False
        self.unsaved_changes = False
        self.docs = configuratie["opslaglocatie"]

        self.textEdit.textChanged.connect(self.on_text_changed)

        self.check_dark_mode()

        self.actionNieuw.triggered.connect(self.nieuw)
        self.actionOpslaan.triggered.connect(self.opslaan)
        self.actionOpslaan_als.triggered.connect(self.opslaan_als)
        self.actionOpslaan_als_HTML.triggered.connect(self.opslaan_als_html)
        self.actionOpslaan_als_Markdown.triggered.connect(self.opslaan_als_markdown)

        self.actionOpen.triggered.connect(self.open)
        self.actionOpen_HTML.triggered.connect(self.open_HTML)
        self.actionOpen_Markdown.triggered.connect(self.open_Markdown)

        self.actionAfdrukken.triggered.connect(self.afdrukken)

        self.actionSluiten.triggered.connect(self.sluiten)

        self.actionKopieren.triggered.connect(self.kopieren)
        self.actionKnippen.triggered.connect(self.knippen)
        self.actionPlakken.triggered.connect(self.plakken)

        self.actionZoeken.triggered.connect(self.zoeken)
        #self.actionVervangen.triggered.connect(self.vervangen)

        self.actionUndo.triggered.connect(self.undo)
        self.actionRedo.triggered.connect(self.redo)

        self.actionAlles_selecteren.triggered.connect(self.alles_selecteren)

        self.actionNormaliseren.triggered.connect(self.normaliseren)

        self.actionPlatte_Tekst.triggered.connect(self.platteTekst)

        self.actionGeen_hoofdletters.triggered.connect(self.geen_hoofdletters)

        self.actionSchrift.triggered.connect(self.schrift)

        self.actiondonkere_modus.triggered.connect(self.gebruik_donkere_modus)
        self.actionlichte_modus.triggered.connect(self.gebruik_lichte_modus)
        self.actionblauwe_modus.triggered.connect(self.gebruik_blauwe_modus)

        self.actionletters_groter.triggered.connect(self.letters_groter)
        self.actionletters_kleiner.triggered.connect(self.letters_kleiner)

        self.actionRechts.triggered.connect(self.rechts)
        self.actionMidden.triggered.connect(self.midden)
        self.actionLinks.triggered.connect(self.links)
        self.actionVerdelen.triggered.connect(self.verdelen)

        self.actionDatum.triggered.connect(self.datum)
        self.actionTijd.triggered.connect(self.tijd)
        self.actionVandaag.triggered.connect(self.vandaag)
        self.actionmd_afbeelding.triggered.connect(self.md_afbeelding)
        self.actionmd_link.triggered.connect(self.md_link)

        self.actionCursief.triggered.connect(self.cursief)
        self.actionVet.triggered.connect(self.vet)
        self.actionOnderstrepen.triggered.connect(self.onderstrepen)

        self.actionOpen_memo.triggered.connect(self.open_memo)
        self.actionMemo_lijst.triggered.connect(self.memo_lijst)
        self.actionNotitie.triggered.connect(self.notitie)

        self.actionOver_Edith.triggered.connect(self.over_edith)

        self.maak_statusbar()

    def on_text_changed(self):
        self.unsaved_changes = True
        self.statusbar.showMessage("Onopgeslagen wijzigingen")

    def closeEvent(self, event):
        if self.unsaved_changes:
            reply = QMessageBox.question(self, 'Waarschuwing', 
                                         'Huidig bestand is nog niet opgeslagen. Wilt u de wijzigingen opslaan?')
            if reply == QMessageBox.StandardButton.Yes:
                self.opslaan()
                event.accept()
            elif reply == QMessageBox.StandardButton.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def maak_statusbar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Begin")

    def nieuw(self):
        print("nieuw")
        self.textEdit.clear()
        self.setWindowTitle("Geen naam")
        self.current_path = None

    def opslaan(self):
        print("opslaan")
        if self.current_path is not None:
            if self.current_path.endswith('.html') or self.current_path.endswith('.htm'):
                htmltext = self.textEdit.toHtml()
                print(htmltext)
                try:
                    with open(self.current_path, 'w') as f:
                        f.write(htmltext)
                    self.unsaved_changes = False
                    self.statusbar.showMessage("Bestand opgeslagen")
                except Exception as e:
                    self.dialog_critical(str(e))
                return
            if self.current_path.endswith('.md') or self.current_path.endswith('.markdown'):
                mdtext = self.textEdit.toMarkdown()
                print(mdtext)
                try:
                    with open(self.current_path, 'w') as f:
                        f.write(mdtext)
                    self.unsaved_changes = False
                    self.statusbar.showMessage("Bestand opgeslagen")
                except Exception as e:
                    self.dialog_critical(str(e))
                return
            htmltext = self.textEdit.toHtml()
            print(htmltext)
            mdtext = self.textEdit.toMarkdown()
            print(mdtext)
            filetext = self.textEdit.toPlainText()
            print(filetext)
            try:
                with open(self.current_path, 'w') as f:
                    f.write(filetext)
                self.unsaved_changes = False
                self.statusbar.showMessage("Bestand opgeslagen")
            except Exception as e:
                self.dialog_critical(str(e))
        else:
            self.opslaan_als()

    def opslaan_als(self):
        print("opslaan als")
        try:
            pathname = QFileDialog.getSaveFileName(self, 'Bestand opslaan', self.docs, 'Tekst bestanden (*.txt)')
            print(pathname[0])
            filetext = self.textEdit.toPlainText()
            with open(pathname[0], 'w') as f:
                f.write(filetext)
            self.current_path = pathname[0]
            self.setWindowTitle(pathname[0])
            self.unsaved_changes = False
            self.statusbar.showMessage("Bestand opgeslagen")
        except Exception as e:
            self.dialog_critical(str(e))

    def opslaan_als_html(self):
        print("opslaan als html")
        try:
            pathname = QFileDialog.getSaveFileName(self, 'Bestand opslaan als HTML', self.docs, 'HTML bestanden (*.html *.htm)')
            print(pathname[0])
            htmltext = self.textEdit.toHtml()
            with open(pathname[0], 'w') as f:
                f.write(htmltext)
            self.unsaved_changes = False
            self.statusbar.showMessage("Bestand opgeslagen")
        except Exception as e:
            self.dialog_critical(str(e))

    def opslaan_als_markdown(self):
        print("opslaan als markdown")
        try:
            pathname = QFileDialog.getSaveFileName(self, 'Bestand opslaan als Markdown', self.docs, 'Markdown bestanden (*.md *.markdown)')
            print(pathname[0])
            mdtext = self.textEdit.toMarkdown()
            with open(pathname[0], 'w') as f:
                f.write(mdtext)
            self.unsaved_changes = False
            self.statusbar.showMessage("Bestand opgeslagen")
        except Exception as e:
            self.dialog_critical(str(e))

    def open(self):
        print("open")
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open bestand', self.docs, 'Tekst bestanden (*.txt *.md *.markdown *.html *.htm);;Alle bestanden (*)')
            print(fname[0]) # gekozen bestand
            self.setWindowTitle(fname[0])
            with open(fname[0], 'r') as f:
                filetext = f.read()
                self.textEdit.setText(filetext)
            self.current_path = fname[0]
            self.unsaved_changes = False
            self.statusbar.showMessage("Bestand geopend")
        except Exception as e:
            self.dialog_critical(str(e))

    def open_HTML(self):
        print("open html")
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open HTML bestand', self.docs, 'HTML bestanden (*.html *.htm);;Alle bestanden (*)')
            print(fname[0]) # gekozen bestand
            self.setWindowTitle(fname[0])
            with open(fname[0], 'r') as f:
                htmltext = f.read()
                self.textEdit.setHtml(htmltext)
            self.current_path = fname[0]
            self.unsaved_changes = False
            self.statusbar.showMessage("Bestand geopend")
        except Exception as e:
            self.dialog_critical(str(e))

    def open_Markdown(self):
        print("open markdown")
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open Markdown bestand', self.docs, 'Markdown bestanden (*.md *.markdown);;Alle bestanden (*)')
            print(fname[0]) # gekozen bestand
            self.setWindowTitle(fname[0])
            with open(fname[0], 'r') as f:
                mdtext = f.read()
                self.textEdit.setMarkdown(mdtext)
            self.current_path = fname[0]
            self.unsaved_changes = False
            self.statusbar.showMessage("Bestand geopend")
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
        self.close()

    def kopieren(self):
        self.textEdit.copy()

    def knippen(self):
        self.textEdit.cut()

    def plakken(self):
        self.textEdit.paste()

    def zoeken(self):
        if not hasattr(self, "_vind_dialoog") or self._vind_dialoog is None:
            self._vind_dialoog = ZoekenVervangenDialoog(self)
        self._vind_dialoog.show()
        self._vind_dialoog.raise_()
        self._vind_dialoog.activateWindow()

    def open_memo(self):
        print("open memo")
        self.memo_venster = Memo()
        self.memo_venster.show()

    def memo_lijst(self):
        print("memo lijst")
        self.memo_lijst_venster = MemoLijst()
        self.memo_lijst_venster.show()

    def undo(self):
        self.textEdit.undo()

    def redo(self):
        self.textEdit.redo()

    def alles_selecteren(self):
        self.textEdit.selectAll()

    def normaliseren(self):
        print("normaliseren")
        selectie = self.textEdit.toPlainText()
        tussenstap = ' '.join(selectie.split('\n'))
        genormaliseerde_tekst = '.\n'.join(tussenstap.split('.'))
        self.textEdit.clear()
        self.textEdit.insertPlainText(genormaliseerde_tekst)

    def geen_hoofdletters(self):
        print("geen hoofdletters")
        selectie = self.textEdit.textCursor()
        if selectie.hasSelection():
            geselecteerde_tekst = selectie.selectedText()
            kleine_tekst = geselecteerde_tekst.lower()
            selectie.insertText(kleine_tekst)

    def schrift(self):
        selectie = self.textEdit.textCursor()
        if selectie.hasSelection():
            geselecteerde_tekst = selectie.selectedText()
            schrift_tekst = ''
            for char in geselecteerde_tekst:
                if 'A' <= char <= 'Z':
                    schrift_char = chr(ord(char) + 0x1D4D0 - ord('A'))
                elif 'a' <= char <= 'z':
                    schrift_char = chr(ord(char) + 0x1D4EA - ord('a'))
                else:
                    schrift_char = char
                schrift_tekst += schrift_char
            selectie.insertText(schrift_tekst)

    def gebruik_donkere_modus(self):
        global configuratie
        configuratie["darkmode"] = 'dark'
        print(f"donkere modus: {configuratie['darkmode']}")
        self.setStyleSheet(DONKER)

    def gebruik_lichte_modus(self):
        configuratie["darkmode"] = 'light'
        self.setStyleSheet("")

        # laat het venster zien
        self.show()

    def gebruik_blauwe_modus(self):
        configuratie["darkmode"] = 'blue'
        print(f"blauwe modus: {configuratie['darkmode']}")
        self.setStyleSheet(BLAUW)

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
        #self.textEdit.insertPlainText(datum_nu)
        self.textEdit.insertHtml("<span style='color: #00FF00;'>"+datum_nu+"</span> ")

    def tijd(self):
        nu = datetime.datetime.now()
        tijd_nu = nu.strftime("%H:%M")
        print(f"tijd: {tijd_nu}")
        #self.textEdit.insertPlainText(tijd_nu)
        self.textEdit.insertHtml("<span style='color: #FF0000;'>"+tijd_nu+"</span> ")

    def vandaag(self):
        nu = datetime.datetime.now()
        datum_nu = nu.strftime("%Y-%m-%d")
        print(f"datum: {datum_nu}")
        self.textEdit.insertPlainText(datum_nu)

    def md_afbeelding(self):
        print("md afbeelding")
        pathname = QFileDialog.getOpenFileName(self, 'Afbeelding openen', self.docs, 'Afbeeldingen (*.png *.jpg *.jpeg *.bmp *.gif);;Alle bestanden (*)')
        print(pathname[0]) # gekozen bestand
        if pathname[0]:
            bestandsnaam = pathname[0].split('/')[-1]
            md_code = f"![{bestandsnaam}]({pathname[0]})"
            self.textEdit.insertPlainText(md_code)

    def md_link(self):
        print("md link")
        url, ok = QInputDialog.getText(self, 'Markdown Link', 'Voer de URL in:')
        if ok and url:
            link_tekst, ok2 = QInputDialog.getText(self, 'Link Tekst', 'Voer de link tekst in:')
            if ok2 and link_tekst:
                md_code = f"[{link_tekst}]({url})"
                self.textEdit.insertPlainText(md_code)

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
        print(f"onderstrepen: {self.textEdit.fontUnderline()}")
        if self.textEdit.fontUnderline():
            self.textEdit.setFontUnderline(False)
        else:
            self.textEdit.setFontUnderline(True)

    def over_edith(self):
        print("over edith")
        QMessageBox.about(self, "Over Edith", "Edith is een tekstbewerker gemaakt met Python en PyQt6")

    def platteTekst(self):
        print("platte tekst")
        plain_text = self.textEdit.toPlainText()
        self.textEdit.setPlainText(plain_text)

    def notitie(self):
        print("notitie")
        self.notitie_venster = Notitie()
        self.notitie_venster.show()

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Icon.Critical)
        dlg.show()

    def check_dark_mode(self):
        dm = configuratie["darkmode"]
        print(f'donkere modus voor hoofdvenster: {dm}')
        if dm == 'dark':
            self.setStyleSheet(DONKER)
        elif dm == 'light':
            self.setStyleSheet('')
        elif dm == 'blue':
            self.setStyleSheet(BLAUW)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Venster()
    ui.show()
    app.exec()

