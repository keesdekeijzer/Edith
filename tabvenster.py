import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QLabel, QPlainTextEdit, QPushButton
import yaml

from keuze_teksten import keuze_teksten_nl, keuze_teksten_en, keuze_teksten_de
from keuze_teksten_inhoud import keuze_teksten_inhoud, keuze_teksten_naam

class TabVenster(QMainWindow):    
    def __init__(self):        
        super().__init__()        
        self.setWindowTitle("Keuzeteksten")
        tabs = QTabWidget()        
        self.setCentralWidget(tabs)

        # read config
        config = self.load_config()

        # taal
        if config.get("language") == "nl":
            self.taal = "nl"
        elif config.get("language") == "en":
            self.taal = "en"
        else:
            self.taal = "de"

        self.keuze_teksten = {}
        
        if self.taal == "en":
            self.keuze_teksten = keuze_teksten_en
        elif self.taal == "de":
            self.keuze_teksten = keuze_teksten_de
        else:
            self.keuze_teksten = keuze_teksten_nl

        print("Keuze teksten:", self.keuze_teksten)  

        for i in range(10):            
            tab = QWidget()            
            layout = QVBoxLayout(tab)    
            kz = self.keuze_teksten.get(f"Keuze {i + 1}", f"Keuze {i + 1}")        
            layout.addWidget(QPlainTextEdit(kz))  
            layout.addWidget(QLabel(f"Dit is de inhoud van keuzetekst {i + 1}"))    
            layout.addWidget(QPushButton(f"Knop voor keuzetekst {i + 1}"))      
            tabs.addTab(tab, f"{kz}")


    def load_config(self):
        try:
            with open("config.yaml", "r", encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            config = {}
        return config

def main():    
    app = QApplication(sys.argv)    
    win = TabVenster()    
    win.resize(1200, 600)    
    win.show()    
    sys.exit(app.exec())

if __name__ == "__main__":    
    main()