import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QLabel, QPlainTextEdit, QPushButton

class TabVenster(QMainWindow):    
    def __init__(self):        
        super().__init__()        
        self.setWindowTitle("Keuzeteksten")
        tabs = QTabWidget()        
        self.setCentralWidget(tabs)
        for i in range(10):            
            tab = QWidget()            
            layout = QVBoxLayout(tab)            
            layout.addWidget(QPlainTextEdit(f"Keuzetekst {i + 1}"))  
            layout.addWidget(QLabel(f"Dit is de inhoud van keuzetekst {i + 1}"))    
            layout.addWidget(QPushButton(f"Knop voor keuzetekst {i + 1}"))      
            tabs.addTab(tab, f"Keuzetekst {i + 1}")

def main():    
    app = QApplication(sys.argv)    
    win = TabVenster()    
    win.resize(1200, 600)    
    win.show()    
    sys.exit(app.exec())

if __name__ == "__main__":    
    main()