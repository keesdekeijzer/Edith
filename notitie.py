import sys

#from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtWidgets import QInputDialog, QTextEdit, QWidget
from PyQt6.uic import loadUi
import datetime
from PyQt6.QtGui import QTextCursor, QPainter, QColor, QTextFormat
from PyQt6.QtCore import Qt, QRect, QSize
#from PyQt6.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout, QTextEdit


# instellingen importeren
from config import configuratie




BLAUW = '''
                QWidget{
                    background-color: #0000AA;
                    color: #FFFFFF;
                    }
                QPlainTextEdit{  
                    background-color: #000BFF;
                    color: #FFFFFF;
                    }
                '''

DONKER = '''
            QWidget{
                background-color: rgb(33,33,33);
                color: #FFFFFF;
                }
            QPlainTextEdit{
                background-color: rgb(46,46,46);
            }
            '''

class LineNumberArea(QWidget):
    def __init__(self, notitie):
        super().__init__(notitie)
        self.notitie = notitie

    def sizeHint(self):
        return QSize(self.notitie.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.notitie.line_number_area_paint_event(event)

class Notitie(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memo")
        
        loadUi("plaintext3.ui",self)
        #self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle("Edith Notitie")

        self.unsaved_changes = False
        self.current_path = None
        self.plainTextEdit.textChanged.connect(self.on_text_changed)

        self.check_dark_mode()

        self.regelnummers = LineNumberArea(self)


        self.actionNieuw.triggered.connect(self.nieuw)
        self.actionOpslaan.triggered.connect(self.opslaan)
        self.actionOpslaan_als.triggered.connect(self.opslaan_als)

        self.actionOpen.triggered.connect(self.open)

        self.actionSluiten.triggered.connect(self.sluiten)

        self.actionKopieren.triggered.connect(self.kopieren)
        self.actionKnippen.triggered.connect(self.knippen)
        self.actionPlakken.triggered.connect(self.plakken)

        self.actionZoeken.triggered.connect(self.zoeken)

        self.actionUndo.triggered.connect(self.undo)
        self.actionRedo.triggered.connect(self.redo)

        self.actionAlles_selecteren.triggered.connect(self.alles_selecteren)

        self.actionNormaliseren.triggered.connect(self.normaliseren)

        self.actionGeen_hoofdletters.triggered.connect(self.geen_hoofdletters)

        self.actionSchrift.triggered.connect(self.schrift)

        self.actionDonkere_modus.triggered.connect(self.donkere_modus)
        self.actionLichte_modus.triggered.connect(self.lichte_modus)
        self.actionblauwe_modus.triggered.connect(self.blauwe_modus)

        self.actionFont.triggered.connect(self.font_aanpassen)
        self.actionLettergrootte.triggered.connect(self.font_aanpassen)

        self.actionDatum.triggered.connect(self.datum)
        self.actionTijd.triggered.connect(self.tijd)
        self.actionmd_afbeelding.triggered.connect(self.md_afbeelding)
        self.actionmd_link.triggered.connect(self.md_link)
        self.actionif_name_main.triggered.connect(self.if_name_main)

        self.actionOver_Edith.triggered.connect(self.over_edith)
        self.actionSneltoetsen.triggered.connect(self.sneltoetsen)
        self.actionSneltoetsen_Alt.triggered.connect(self.sneltoetsen_alt)

        print(self.regelnummers.sizeHint())

        print(self.line_number_area_width())
        self.plainTextEdit.blockCountChanged.connect(self.update_line_number_area_width)
        self.plainTextEdit.updateRequest.connect(self.update_line_number_area)
        self.plainTextEdit.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)

    def line_number_area_width(self):
        digits = len(str(self.plainTextEdit.blockCount()))
        space = 30 + self.plainTextEdit.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _):
        # Set viewport margins: left, top, right, bottom
        #self.plainTextEdit.setViewportMargins(self.line_number_area_width(), 20, 10, 20)
        self.plainTextEdit.setViewportMargins(50, 15, 10, 25)

    def update_line_number_area(self, rect, dy):
        # Ensure that updateRequest is handled safely
        if dy != 0:
            self.regelnummers.scroll(0, dy)
        else:
            self.regelnummers.update(0, rect.y(), self.regelnummers.width(), rect.height())

        # Ensure the area updates correctly if required
        if rect.contains(self.plainTextEdit.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        # Set the geometry of the window: x, y, width, height
        self.regelnummers.setGeometry(QRect(cr.left()+20, cr.top()+50, self.line_number_area_width(), cr.height()-100))

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.regelnummers)
        #painter.fillRect(event.rect(), Qt.GlobalColor.lightGray)

        block = self.plainTextEdit.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.plainTextEdit.blockBoundingGeometry(block).translated(self.plainTextEdit.contentOffset()).top()
        bottom = top + self.plainTextEdit.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.GlobalColor.black)
                painter.drawText(-3, int(top), self.regelnummers.width(), self.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.plainTextEdit.blockBoundingRect(block).height()
            block_number += 1


    def highlight_current_line(self):
        extra_selections = []

        selection = QTextEdit.ExtraSelection()
        line_color = QColor(Qt.GlobalColor.yellow).lighter(160)
        selection.format.setBackground(line_color)
        selection.cursor = self.plainTextEdit.textCursor()
        selection.cursor.clearSelection()
        extra_selections.append(selection)

        self.plainTextEdit.setExtraSelections(extra_selections)



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

    def check_dark_mode(self):
        dm = configuratie["darkmode"]
        print(f'donkere modus voor memo: {dm}')
        if dm == 'dark':
            self.setStyleSheet(DONKER)
        elif dm == 'light':
            self.setStyleSheet('')
        elif dm == 'blue':
            self.setStyleSheet(BLAUW)

    def blauwe_modus(self):
        configuratie["darkmode"] = 'blue'
        self.setStyleSheet(BLAUW)

    def lichte_modus(self):
        configuratie["darkmode"] = 'light'
        self.setStyleSheet('')

    def donkere_modus(self):
        configuratie["darkmode"] = 'dark'
        self.setStyleSheet(DONKER)

    def font_aanpassen(self):
        from PyQt6.QtWidgets import QFontDialog
        font, ok = QFontDialog.getFont()
        if ok:
            self.plainTextEdit.setFont(font)

    def on_text_changed(self):
        self.unsaved_changes = True
        self.statusbar.showMessage("Onopgeslagen wijzigingen")

    def nieuw(self):
        if self.unsaved_changes:
            reply = QMessageBox.question(self, 'Waarschuwing', 
                                         'Huidig bestand is nog niet opgeslagen. Wilt u de wijzigingen opslaan?')
            if reply == QMessageBox.StandardButton.Yes:
                self.opslaan()
        print("nieuw")
        self.plainTextEdit.clear()
        self.setWindowTitle("Geen naam")
        self.current_path = None   
    
    def opslaan(self):
        print("opslaan")
        if self.current_path is not None:
            filetext = self.plainTextEdit.toPlainText()
            print(filetext)
            try:
                with open(self.current_path, 'w') as f:
                    f.write(filetext)
                self.statusbar.showMessage("Bestand opgeslagen")
            except Exception as e:
                self.dialog_critical(str(e))
        else:
            self.opslaan_als()

    def opslaan_als(self):
        print("opslaan als")
        try:
            pathname = QFileDialog.getSaveFileName(self, 'Bestand opslaan', configuratie["opslaglocatie"], 'Tekst bestanden (*.txt)')
            print(pathname[0])
            filetext = self.plainTextEdit.toPlainText()
            with open(pathname[0], 'w') as f:
                f.write(filetext)
            self.current_path = pathname[0]
            self.setWindowTitle(pathname[0])
            self.statusbar.showMessage("Bestand opgeslagen")
        except Exception as e:
            self.dialog_critical(str(e))

    def open(self):
        if self.unsaved_changes:
            reply = QMessageBox.question(self, 'Waarschuwing', 
                                         'Huidig bestand is nog niet opgeslagen. Wilt u de wijzigingen opslaan?')
            if reply == QMessageBox.StandardButton.Yes:
                self.opslaan()
        print("open")
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open bestand', configuratie["opslaglocatie"], 'Tekst bestanden (*.txt);;Alle bestanden (*)')
            print(fname[0]) # gekozen bestand
            self.setWindowTitle(fname[0])
            with open(fname[0], 'r') as f:
                filetext = f.read()
                self.plainTextEdit.setPlainText(filetext)
            self.current_path = fname[0]
            self.statusbar.showMessage("Bestand geopend")
        except Exception as e:
            self.dialog_critical(str(e))

    def sluiten(self):

        self.close()   

    def kopieren(self):
        self.plainTextEdit.copy()

    def knippen(self):
        self.plainTextEdit.cut()

    def plakken(self):
        self.plainTextEdit.paste()

    def zoeken(self):
        text, ok = QInputDialog.getText(self, 'Zoeken', 'Voer de zoekterm in:')
        if ok and text:
            gevonden = self.plainTextEdit.find(text)
            if not gevonden:
                # weer naar boven
                cursor = self.plainTextEdit.textCursor()
                cursor.movePosition(QTextCursor.MoveOperation.Start)
                self.plainTextEdit.setTextCursor(cursor)
                gevonden = self.plainTextEdit.find(text)
                print(f"'{text}' niet gevonden")
                if not gevonden:
                    term = text.replace('<','&lt;')
                    term = term.replace('>','&gt;')
                    QMessageBox.information(self, "Vinden", f"'{term}' niet gevonden")

    def undo(self):
        self.plainTextEdit.undo()

    def redo(self):
        self.plainTextEdit.redo()

    def alles_selecteren(self):
        self.plainTextEdit.selectAll()

    def normaliseren(self):
        print("normaliseren")
        cursor = self.plainTextEdit.textCursor()
        volledige_tekst = self.plainTextEdit.toPlainText()
        tussenstap = ' '.join(volledige_tekst.split('\n'))
        genormaliseerde_tekst = '.\n'.join(tussenstap.split('.'))
        self.plainTextEdit.setPlainText(genormaliseerde_tekst)

    def geen_hoofdletters(self):
        print("geen hoofdletters")
        selectie = self.plainTextEdit.textCursor()
        if selectie.hasSelection():
            geselecteerde_tekst = selectie.selectedText()
            kleine_tekst = geselecteerde_tekst.lower()
            selectie.insertText(kleine_tekst)

    def schrift(self):
        selectie = self.plainTextEdit.textCursor()
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
        else:
            print("Geen tekst geselecteerd voor schrift conversie")
            QMessageBox.about(self, "Geen Selectie", "Selecteer eerst tekst om om te zetten naar schrift.")

    def datum(self): # todo
        nu = datetime.datetime.now()
        datum_nu = nu.strftime("%Y-%m-%d")
        print(f"datum: {datum_nu}")
        self.plainTextEdit.insertPlainText(datum_nu)

    def tijd(self):
        nu = datetime.datetime.now()
        tijd_nu = nu.strftime("%H:%M")
        print(f"tijd: {tijd_nu}")
        self.plainTextEdit.insertPlainText(tijd_nu)

    def if_name_main(self):
        self.plainTextEdit.insertPlainText("if__name__ == '__main__':\n    ")   

    def md_afbeelding(self):
        print("md afbeelding")
        pathname = QFileDialog.getOpenFileName(self, 'Afbeelding openen', configuratie["opslaglocatie"], 'Afbeeldingen (*.png *.jpg *.jpeg *.bmp *.gif);;Alle bestanden (*)')
        print(pathname[0]) # gekozen bestand
        if pathname[0]:
            bestandsnaam = pathname[0].split('/')[-1]
            md_code = f"![{bestandsnaam}]({pathname[0]})"
            self.plainTextEdit.insertPlainText(md_code)

    def md_link(self):
        print("md link")
        pathname = QFileDialog.getOpenFileName(self, 'Bestand openen', configuratie["opslaglocatie"], 'Alle bestanden (*)')
        print(pathname[0]) # gekozen bestand
        if pathname[0]:
            bestandsnaam = pathname[0].split('/')[-1]
            md_code = f"[{bestandsnaam}]({pathname[0]})"
            self.plainTextEdit.insertPlainText(md_code)

    def donkere_modus(self):
        configuratie["darkmode"] = True
        self.setStyleSheet('''
            QWidget{
                background-color: rgb(33,33,33);
                color: #FFFFFF;
                }
            QPlainTextEdit{
                background-color: rgb(46,46,46);
            }
            ''')
        
    def lichte_modus(self):
        configuratie["darkmode"] = False
        self.setStyleSheet('')

    def over_edith(self):
        QMessageBox.about(self, "Over Edith", "Edith versie 1.0\nEen eenvoudige teksteditor met memo functionaliteit.")

    def sneltoetsen(self):
        QMessageBox.about(self, "Sneltoetsen", "Ctrl+N: Nieuw\nCtrl+O: Openen\nCtrl+S: Opslaan\nCtrl+Shift+S: Opslaan als\nCtrl+Q: Sluiten\nCtrl+C: Kopiëren\nCtrl+X: Knippen\nCtrl+V: Plakken\nCtrl+F: Zoeken\nCtrl+Z: Ongedaan maken\nCtrl+Y: Opnieuw\nCtrl+A: Alles selecteren")

    def sneltoetsen_alt(self):
        QMessageBox.about(self, "Sneltoetsen Alt", "Alt+D: Datum\nAlt+T: Tijd\nAlt+L: md link\nAlt+A: md afbeelding\nAlt+N: Normaliseren\nAlt+U: Geen hoofdletters\nAlt+S: Schrift\nAlt+F: Font\nAlt+L: Lettergrootte\n")

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Icon.Critical)
        dlg.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    notitie = Notitie()
    notitie.show()
    sys.exit(app.exec())
