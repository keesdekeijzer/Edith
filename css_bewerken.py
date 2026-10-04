from PyQt6.QtWidgets import QButtonGroup, QDialog, QLabel, QMessageBox, QRadioButton
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton as QButton
import yaml

from teksten_config import config_meldingen_de, config_meldingen_en, config_meldingen_nl



label_stylesheet = """
QLabel {        
                background-color: #58db40;        
                color: white;        
                border: none;        
                border-radius: 6px;        
                padding: 8px 16px;    }
"""

button_stylesheet = """
QPushButton {        
                background-color: #3498db;        
                color: white;        
                border: none;        
                border-radius: 6px;        
                padding: 8px 16px;    }
                QPushButton:hover {        
                background-color: #2980b9;    }
                QPushButton:pressed {        
                background-color: #1f618d;    }
"""

class CssBewerken(QDialog):
    def __init__(self, taal='nl'):
        super().__init__()
        self.taal = taal
        
        self.setModal(True)


        self.configuratie = self.load_css_config()  # Load configuration from css_config.yaml

        self.taal = self.configuratie.get("language", "nl")

        self.config_meldingen = {}

        if self.taal == "en":
            self.config_meldingen = config_meldingen_en
        elif self.taal == "de":
            self.config_meldingen = config_meldingen_de
        else:
            self.config_meldingen = config_meldingen_nl

        self.setup_ui()

        self.setWindowTitle(self.config_meldingen["CSS configureren"])

    def setup_ui(self):

        self.main_layout = QVBoxLayout()

        self.layout1 = QVBoxLayout()
        label = QLabel(self.config_meldingen["Hier kun je de configuratie bewerken."])
        self.layout1.addWidget(label)

        self.layout2 = QVBoxLayout()
        label2 = QLabel("Forground color:")
        label2.setStyleSheet(label_stylesheet)
        self.layout2.addWidget(label2)

        self.label3 = QLabel(self.configuratie.get("foreground_color", "#000000"))
        self.layout2.addWidget(self.label3)

        fg_button = QButton("Change foreground color")
        fg_button.setStyleSheet(button_stylesheet)
        self.layout2.addWidget(fg_button)
        fg_button.clicked.connect(self.change_foreground_color)

        self.label4 = QLabel("Background color:")
        self.label4.setStyleSheet(label_stylesheet)
        self.layout2.addWidget(self.label4)

        self.label5 = QLabel(self.configuratie.get("background_color", "#ffffff"))
        self.layout2.addWidget(self.label5)

        bg_button = QButton("Change background color")
        bg_button.setStyleSheet(button_stylesheet)
        self.layout2.addWidget(bg_button)
        bg_button.clicked.connect(self.change_background_color)

        #config = self.load_css_config()


        self.main_layout.addLayout(self.layout1) # intro
        self.main_layout.addLayout(self.layout2) # mode


        self.setLayout(self.main_layout)

    def load_css_config(self):
        try:
            with open("css_config.yaml", "r", encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            config = {}
        return config
    
    def save_css_config(self, config):
        with open("css_config.yaml", "w", encoding='utf-8') as f:
            yaml.safe_dump(config, f, sort_keys=False)



        
    def melding_opgeslagen(self):
        #print("self.configuratie opgeslagen!")
        QMessageBox.information(self, "Opgeslagen", "Configuratie is opgeslagen!")
        self.close()



    def change_foreground_color(self):
        from PyQt6.QtWidgets import QColorDialog
        color = QColorDialog.getColor()
        if color.isValid():
            self.configuratie["foreground_color"] = color.name()
            self.save_css_config(self.configuratie)
            QMessageBox.information(self, "Opgeslagen", f"Nieuwe voorgrondkleur is opgeslagen: {color.name()}")
            self.label3.setText(self.configuratie.get("foreground_color", "#000000"))

    def change_background_color(self):
        from PyQt6.QtWidgets import QColorDialog
        color = QColorDialog.getColor()
        if color.isValid():
            self.configuratie["background_color"] = color.name()
            self.save_css_config(self.configuratie)
            QMessageBox.information(self, "Opgeslagen", f"Nieuwe achtergrondkleur is opgeslagen: {color.name()}")
            self.label5.setText(self.configuratie.get("background_color", "#ffffff"))