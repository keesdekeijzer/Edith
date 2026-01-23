import sys
from PyQt6.QtWidgets import QMainWindow, QMessageBox
# from mainwindow import Ui_MainWindow
from PyQt6.uic import loadUi
import sqlite3

# pyuic6 -o mainwindow.py mainwindow.ui

# Pad naar de database : instelbaar maken?

from config import configuratie

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
        with sqlite3.connect(configuratie["database"]) as self.connection:
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
        dm = configuratie["darkmode"]
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
        with sqlite3.connect(configuratie["database"]) as connection:

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
        with sqlite3.connect(configuratie["database"]) as connection:

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
        with sqlite3.connect(configuratie["database"]) as connection:
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
