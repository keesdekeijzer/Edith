import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QDialog, QMessageBox, QStatusBar, QLabel
from PyQt6.QtWidgets import QLineEdit, QHBoxLayout, QVBoxLayout, QListWidgetItem, QListWidget, QAbstractItemView
# from mainwindow import Ui_MainWindow
from PyQt6.uic import loadUi
import datetime
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QTextCursor
import sqlite3

# pyuic6 -o mainwindow.py mainwindow.ui

# todo waarschuwing als bestand niet is opgeslagen 


# Pad naar de database : instelbaar maken?

DATABASE = "/home/kees/Data/memo.db"

DARKMODE = False

class MemoLijst(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memo Lijst")
        self.setGeometry(100, 100, 600, 600)
        loadUi("memolijst4.ui",self)
        self.setWindowTitle("Edith Memo Lijst")

        self.check_dark_mode()


        print('toon memo lijst')
        # Use 'with' to connect to the SQLite database
        with sqlite3.connect(DATABASE) as connection:
            cursor = connection.cursor()

            # SQL command to select all memos
            select_query = '''
            SELECT * FROM memos;
            '''

            # Execute the SQL command
            cursor.execute(select_query)

            # Fetch all records
            memos = cursor.fetchall()

            # Print each memo
            labels = []
            for memo in memos:

                labels.append(QLabel(f"<b>{memo[0]}</b><br>{memo[1]}"))

            vulling = ''
            for label in labels:
                vulling += f"{label.text()}<br><br>"
            self.textBrowser.setHtml(vulling)
            self.textBrowser.moveCursor(QTextCursor.MoveOperation.Start)

        self.actionExporteren.triggered.connect(self.exporteren)
        
        self.actionSluiten.triggered.connect(self.sluiten   )

    def check_dark_mode(self):
        dm = DARKMODE
        print(f'donkere modus voor memo lijst: {dm}')
        if dm:
            self.setStyleSheet('''
                QMenuBar::item:selected{
                    color: #000000;}
                QWidget{
                    background-color: rgb(33,33,33);
                    color: #FFFFFF;
                    }
                QTextBrowser{
                    background-color: rgb(46,46,46);
                    color: #FFFFFF;
                    }''')
        else:
            self.setStyleSheet("")

    def exporteren(self):
        print('exporteren memo lijst')
        # Use 'with' to connect to the SQLite database
        with sqlite3.connect(DATABASE) as connection:
            cursor = connection.cursor()

            # SQL command to select all memos
            select_query = '''
            SELECT * FROM memos;
            '''

            # Execute the SQL command
            cursor.execute(select_query)

            # Fetch all records
            memos = cursor.fetchall()

            # Print each memo
            for memo in memos:
                print(f'Titel: {memo[0]}')
                print(f'Inhoud: {memo[1]}')
                print('---------------------')

        QMessageBox.about(self, "Geëxporteerd", "Het is gelukt. Memo lijst is geëxporteerd naar de console.")

    def sluiten(self):
        self.close()


class Memo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memo")
        self.setGeometry(100, 100, 600, 400)
        loadUi("memo.ui",self)
        self.setWindowTitle("Edith Memo")

        self.check_dark_mode()

        self.pushButton.clicked.connect(self.zoeken_memo)
        self.pushButton_2.clicked.connect(self.opslaan_memo)
        self.pushButton_3.clicked.connect(self.verwijderen_memo)
        self.pushButton_4.clicked.connect(self.close)

        # Connect to the SQLite database (or create it if it doesn't exist)
        with sqlite3.connect(DATABASE) as self.connection:
            self.cursor = self.connection.cursor()
            # Create the memos table if it doesn't exist
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS memos (
                    title TEXT NOT NULL PRIMARY KEY,
                    content TEXT NOT NULL
                )
            ''')
            self.connection.commit()   

    def check_dark_mode(self):
        dm = DARKMODE
        print(f'donkere modus voor memo: {dm}')
        if dm:
            self.setStyleSheet('''
                QWidget{
                    background-color: rgb(33,33,33);
                    color: #FFFFFF;
                    }
                QTextEdit{
                    background-color: rgb(46,46,46);
                }
                QPushButton{
                    background-color: rgb(70,70,70);
                    color: #FFFFFF;
                    }
                QLineEdit{
                    background-color: rgb(46,46,46);
                    }''')

    def opslaan_memo(self):
        print('opslaan memo')
        titel = self.lineEdit.text()
        inhoud = self.plainTextEdit.toPlainText()
        if not titel or not inhoud:
            return
        print(f'titel: {titel}')
        print(f'inhoud: {inhoud}')
        with sqlite3.connect(DATABASE) as connection:

            # Create a cursor object
            cursor = connection.cursor()

            # Write the SQL command to insert a new record into the memos table
            insert_query = "INSERT OR REPLACE INTO memos (title, content) VALUES (?, ?);"

            # Execute the SQL command with the data
            cursor.execute(insert_query, (titel, inhoud))

            # Commit the changes to save the new record
            connection.commit()

            print(f"Inserted memo record for {titel}.")
            QMessageBox.about(self, "Opgeslagen", f"Het is gelukt! Memo {titel} opgeslagen.")

    def zoeken_memo(self):
        print('zoeken memo')
        zoekwoord = self.lineEdit.text()
        if not zoekwoord:
            return
        print(f'zoekwoord: {zoekwoord}')
        with sqlite3.connect(DATABASE) as connection:

            # Create a cursor object
            cursor = connection.cursor()

            # Write the SQL command to select all records from the memos table
            select_query = "SELECT * FROM memos WHERE title LIKE ? OR content LIKE ?;"

            # Execute the SQL command
            cursor.execute(select_query, (f'%{zoekwoord}%', f'%{zoekwoord}%'))

            # Fetch one record
            titel = cursor.fetchone()

            # Display the result
            print("First Memo:")
            print(titel)
            if titel:
                self.lineEdit.setText(titel[0])
                self.plainTextEdit.setPlainText(titel[1])
            else:
                self.plainTextEdit.setPlainText("Geen memo gevonden")
                QMessageBox.about(self, "Niet gevonden", "Geen memo gevonden met dat zoekwoord.")

    def verwijderen_memo(self):
        print('verwijderen memo')
        # Use 'with' to connect to the SQLite database
        with sqlite3.connect(DATABASE) as connection:
            cursor = connection.cursor()

            # SQL command to delete a memo by name
            delete_query = '''
            DELETE FROM memos 
            WHERE title = ?;
            '''

            # Name of the memo to be deleted
            te_verwijderen = self.lineEdit.text()

            # Execute the SQL command with the data
            cursor.execute(delete_query, (te_verwijderen,))

            # Commit the changes to save the deletion
            connection.commit()

            # Print a confirmation message
            print(f"Deleted memo record for {te_verwijderen}.")
            QMessageBox.about(self, "Verwijderd", "Het is gelukt. Memo is verwijderd.")
        self.lineEdit.clear()
        self.plainTextEdit.clear()  



class ZoekenVervangenDialoog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Zoeken en Vervangen")
        self.setModal(False)
        self.parent = parent

        if DARKMODE:
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

        self.actionOpen_memo.triggered.connect(self.open_memo)
        self.actionMemo_lijst.triggered.connect(self.memo_lijst)

        self.actionOver_Edith.triggered.connect(self.over_edith)

        self.maak_statusbar()

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
                except Exception as e:
                    self.dialog_critical(str(e))
                return
            if self.current_path.endswith('.md') or self.current_path.endswith('.markdown'):
                mdtext = self.textEdit.toMarkdown()
                print(mdtext)
                try:
                    with open(self.current_path, 'w') as f:
                        f.write(mdtext)
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
            except Exception as e:
                self.dialog_critical(str(e))
        else:
            self.opslaan_als()

    def opslaan_als(self):
        print("opslaan als")
        try:
            pathname = QFileDialog.getSaveFileName(self, 'Bestand opslaan', 'Documenten', 'Tekst bestanden (*.txt)')
            print(pathname[0])
            filetext = self.textEdit.toPlainText()
            with open(pathname[0], 'w') as f:
                f.write(filetext)
            self.current_path = pathname[0]
            self.setWindowTitle(pathname[0])
        except Exception as e:
            self.dialog_critical(str(e))

    def opslaan_als_html(self):
        print("opslaan als html")
        try:
            pathname = QFileDialog.getSaveFileName(self, 'Bestand opslaan als HTML', 'Documenten', 'HTML bestanden (*.html *.htm)')
            print(pathname[0])
            htmltext = self.textEdit.toHtml()
            with open(pathname[0], 'w') as f:
                f.write(htmltext)
        except Exception as e:
            self.dialog_critical(str(e))

    def opslaan_als_markdown(self):
        print("opslaan als markdown")
        try:
            pathname = QFileDialog.getSaveFileName(self, 'Bestand opslaan als Markdown', 'Documenten', 'Markdown bestanden (*.md *.markdown)')
            print(pathname[0])
            mdtext = self.textEdit.toMarkdown()
            with open(pathname[0], 'w') as f:
                f.write(mdtext)
        except Exception as e:
            self.dialog_critical(str(e))

    def open(self):
        print("open")
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open bestand', 'Documenten', 'Tekst bestanden (*.txt *.md *.markdown *.html *.htm);;Alle bestanden (*)')
            print(fname[0]) # gekozen bestand
            self.setWindowTitle(fname[0])
            with open(fname[0], 'r') as f:
                filetext = f.read()
                self.textEdit.setText(filetext)
            self.current_path = fname[0]
        except Exception as e:
            self.dialog_critical(str(e))

    def open_HTML(self):
        print("open html")
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open HTML bestand', 'Documenten', 'HTML bestanden (*.html *.htm);;Alle bestanden (*)')
            print(fname[0]) # gekozen bestand
            self.setWindowTitle(fname[0])
            with open(fname[0], 'r') as f:
                htmltext = f.read()
                self.textEdit.setHtml(htmltext)
            self.current_path = fname[0]
        except Exception as e:
            self.dialog_critical(str(e))

    def open_Markdown(self):
        print("open markdown")
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open Markdown bestand', 'Documenten', 'Markdown bestanden (*.md *.markdown);;Alle bestanden (*)')
            print(fname[0]) # gekozen bestand
            self.setWindowTitle(fname[0])
            with open(fname[0], 'r') as f:
                mdtext = f.read()
                self.textEdit.setMarkdown(mdtext)
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
        sys.exit()

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
        # split() function divides the string into a list of words and join() reassembles them with a specified separator.
        cursor = self.textEdit.textCursor()
        if cursor.hasSelection():
            selectie = cursor.selectedText()
            genormaliseerde_tekst = '.\n'.join(selectie.split('.'))
            cursor.insertText(genormaliseerde_tekst)

    def gebruik_donkere_modus(self):
        global DARKMODE
        DARKMODE = True
        print(f"donkere modus: {DARKMODE}")
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
        DARKMODE = False
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

