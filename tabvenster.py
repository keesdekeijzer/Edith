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
        self.opslaglocatie_keuze_teksten = config.get("opslaglocatie_keuze_teksten", "/home/kees/Data/keuze_teksten")

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

        #print("Keuze teksten:", self.keuze_teksten)  

        self.keuze_teksten_inhoud = keuze_teksten_inhoud
        self.keuze_teksten_naam = keuze_teksten_naam

        self.config_keuze_teksten = self.load_config_keuze_teksten()

        for i in range(10):            
            tab = QWidget()            
            layout = QVBoxLayout(tab)
            if f"keuze_{i + 1}" in self.config_keuze_teksten:
                ki = self.config_keuze_teksten[f"keuze_{i + 1}"]
                kz = ki[:20] + "..." if len(ki) > 20 else ki
            else: 
                ki = self.keuze_teksten_inhoud.get(f"Keuze {i + 1}", f"Keuze {i + 1}") 
                kz = self.keuze_teksten_naam.get(f"Keuze {i + 1}", f"Keuze {i + 1}") 
            layout.addWidget(QPlainTextEdit(ki))  
            layout.addWidget(QLabel(f"Tab {i + 1}"))  
            knop = QPushButton(f"Opslaan {i + 1}")  
            knop.clicked.connect(lambda checked, i=i: self.save_text(i))
            layout.addWidget(knop)      
            tabs.addTab(tab, f"{kz}")


    def load_config(self):
        try:
            with open("config.yaml", "r", encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            config = {}
        return config

    def save_text(self, index):
        # Get the current tab widget
        current_tab = self.centralWidget().widget(index)
        # Get the QPlainTextEdit from the current tab
        text_edit = current_tab.findChild(QPlainTextEdit)
        if text_edit:
            text_content = text_edit.toPlainText()
            # Save the text content to a file or handle it as needed
            try:
                with open(self.opslaglocatie_keuze_teksten, "r", encoding='utf-8') as f:
                    config_keuze_teksten = yaml.safe_load(f)
            except FileNotFoundError:
                config_keuze_teksten = {}
            config_keuze_teksten[f"keuze_{index + 1}"] = text_content
            with open(self.opslaglocatie_keuze_teksten, "w", encoding='utf-8') as f:
                yaml.safe_dump(config_keuze_teksten, f)
            """
            filename = f"{self.opslaglocatie_keuze_teksten}/keuze_{index + 1}.txt"
            with open(filename, "w", encoding='utf-8') as f:
                f.write(text_content)
            """
            print(f"Text for Keuze {index + 1} saved")

    def load_config_keuze_teksten(self):
        try:
            with open(self.opslaglocatie_keuze_teksten, "r", encoding='utf-8') as f:
                config_keuze_teksten = yaml.safe_load(f)
        except FileNotFoundError:
            config_keuze_teksten = {}
        return config_keuze_teksten

def main():    
    app = QApplication(sys.argv)    
    win = TabVenster()    
    win.resize(1600, 600)    
    win.show()    
    sys.exit(app.exec())

if __name__ == "__main__":    
    main()