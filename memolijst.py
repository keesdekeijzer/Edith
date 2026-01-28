
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QLabel
# from mainwindow import Ui_MainWindow
from PyQt6.uic import loadUi
from PyQt6.QtGui import QTextCursor
import sqlite3


# pyuic6 -o mainwindow.py mainwindow.ui

# Pad naar de database : instelbaar maken?

from config import configuratie

DONKER = '''
                QMenuBar::item:selected{
                    color: #000000;}
                QWidget{
                    background-color: rgb(33,33,33);
                    color: #FFFFFF;
                    }
                QTextBrowser{
                    background-color: rgb(46,46,46);
                    color: #FFFFFF;
                    }'''

BLAUW = '''
                QWidget{
                    background-color: #00BFFF;
                    color: #000000;
                    }
                QTextBrowser{
                    background-color: #000BFF;
                    color: #FFFFFF;
                }'''

class MemoLijst(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memo Lijst")
        self.setGeometry(100, 100, 600, 600)
        loadUi("memolijst4.ui",self)
        self.setWindowTitle("Edith Memo Lijst")

        self.check_dark_mode()

        self.docs = configuratie["opslaglocatie"]


        print('toon memo lijst')
        # Use 'with' to connect to the SQLite database
        with sqlite3.connect(configuratie["database"]) as connection:
            cursor = connection.cursor()

            # SQL command to select all memos
            select_query = '''
            SELECT * FROM memos ORDER BY title;
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
        dm = configuratie["darkmode"]
        print(f'donkere modus voor memo lijst: {dm}')
        if dm == 'dark':
            self.setStyleSheet(DONKER)
        elif dm == 'blue':
            self.setStyleSheet(BLAUW)
        else:
            self.setStyleSheet("")

    def exporteren(self):
        print('exporteren memo lijst')
        export = []
        # Use 'with' to connect to the SQLite database
        with sqlite3.connect(configuratie["database"]) as connection:
            cursor = connection.cursor()

            # SQL command to select all memos
            select_query = '''
            SELECT * FROM memos ORDER BY title;
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
                export.append(f"Titel:{memo[0]}\nInhoud: {memo[1]}\n---------------------\n")
        
        export_tekst = '\n'.join(export)
        try:
            pathname = QFileDialog.getSaveFileName(self, 'Bestand opslaan', self.docs, 'Tekst bestanden (*.txt)')
            print(pathname[0])
            filetext = export_tekst
            with open(pathname[0], 'w') as f:
                f.write(filetext)
            self.current_path = pathname[0]
            QMessageBox.about(self, "Geëxporteerd", "Het is gelukt. Memo lijst is geëxporteerd naar een bestand.")
        except Exception as e:
            self.dialog_critical(str(e))


    def sluiten(self):
        self.close()

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Icon.Critical)
        dlg.show()