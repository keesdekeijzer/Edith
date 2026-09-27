from PyQt6.QtWidgets import QButtonGroup, QDialog, QLabel, QMessageBox, QRadioButton
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton as QButton
import yaml

from teksten_config import config_meldingen_de, config_meldingen_en, config_meldingen_nl

#from config import self.configuratie

class ConfiguratieBewerken(QDialog):
    def __init__(self, taal='nl'):
        super().__init__()
        self.taal = taal
        
        self.setModal(True)
        #self.setup_ui()
        #self.test()

        self.configuratie = self.load_config()  # Load configuration from config.yaml

        self.taal = self.configuratie.get("language", "nl")

        self.config_meldingen = {}

        if self.taal == "en":
            self.config_meldingen = config_meldingen_en
        elif self.taal == "de":
            self.config_meldingen = config_meldingen_de
        else:
            self.config_meldingen = config_meldingen_nl

        self.setup_ui()

        self.setWindowTitle(self.config_meldingen["Configuratie bewerken"])

    def setup_ui(self):

        self.main_layout = QVBoxLayout()

        self.layout1 = QVBoxLayout()
        label = QLabel(self.config_meldingen["Hier kun je de configuratie bewerken."])
        self.layout1.addWidget(label)

        self.layout2 = QVBoxLayout()
        label2 = QLabel("Light mode / Dark mode / Blue mode")
        label2.setStyleSheet("""    
                QLabel {        
                background-color: #3498db;        
                color: white;        
                border: none;        
                border-radius: 6px;        
                padding: 8px 16px;    }
                """)
        self.layout2.addWidget(label2)

        self.groep_mode = QButtonGroup(self)
        self.mode_choice1 = QRadioButton("Light mode")
        self.mode_choice2 = QRadioButton("Dark mode")
        self.mode_choice3 = QRadioButton("Blue mode")
        self.layout2.addWidget(self.mode_choice1)
        self.layout2.addWidget(self.mode_choice2)
        self.layout2.addWidget(self.mode_choice3)
        self.groep_mode.addButton(self.mode_choice1, 1) 
        self.groep_mode.addButton(self.mode_choice2, 2)
        self.groep_mode.addButton(self.mode_choice3, 3)
        

        self.layout3 = QVBoxLayout()

        label3 = QLabel("Language / Taal / Sprache")
        label3.setStyleSheet("""    
                QLabel {        
                background-color: #3498db;        
                color: white;        
                border: none;        
                border-radius: 6px;        
                padding: 8px 16px;    }
                """)
        self.layout3.addWidget(label3)


        self.groep_taal = QButtonGroup(self)
        self.mode_choice4 = QRadioButton("Dutch")
        self.mode_choice5 = QRadioButton("English")
        self.mode_choice6 = QRadioButton("German")
        self.layout3.addWidget(self.mode_choice4)
        self.layout3.addWidget(self.mode_choice5)
        self.layout3.addWidget(self.mode_choice6)
        self.groep_taal.addButton(self.mode_choice4, 1)
        self.groep_taal.addButton(self.mode_choice5, 2)
        self.groep_taal.addButton(self.mode_choice6, 3)
        

        config = self.load_config()

        if config.get('darkmode') == 'light':
            self.mode_choice1.setChecked(True)
        elif config.get('darkmode') == 'dark':
            self.mode_choice2.setChecked(True)
        else:
            self.mode_choice3.setChecked(True)

        if config.get('language') == 'nl':
            self.mode_choice4.setChecked(True)
        elif config.get('language') == 'en':    
            self.mode_choice5.setChecked(True)
        else:
            self.mode_choice6.setChecked(True)

        self.layout4 = QVBoxLayout()

        label4 = QLabel("Save location: ")
        label4.setStyleSheet("""    
                QLabel {        
                background-color: #3498db;        
                color: white;        
                border: none;        
                border-radius: 6px;        
                padding: 8px 16px;    }
                """)
        self.layout4.addWidget(label4)

        self.label5 = QLabel(self.configuratie.get("opslaglocatie", "/home/kees/Data/"))
        self.layout4.addWidget(self.label5)

        location_btn = QButton("Change location")
        self.layout4.addWidget(location_btn)
        location_btn.clicked.connect(self.change_location)
        #self.label5.setText(self.configuratie.get("opslaglocatie", "/home/kees/Data/"))
        #layout.addWidget(self.label5)

        self.layout5 = QVBoxLayout()

        mode_btn = QButton("Submit")
        self.layout5.addWidget(mode_btn)  
        mode_btn.clicked.connect(self.bevestig_mode)

        #self.layout = QVBoxLayout


        self.main_layout.addLayout(self.layout1)
        self.main_layout.addLayout(self.layout2)
        self.main_layout.addLayout(self.layout3)
        self.main_layout.addLayout(self.layout4)
        self.main_layout.addLayout(self.layout5)

        self.setLayout(self.main_layout)

    def load_config(self):
        try:
            with open("config.yaml", "r", encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            config = {}
        return config
    
    def save_config(self, config):
        with open("config.yaml", "w", encoding='utf-8') as f:
            yaml.safe_dump(config, f, sort_keys=False)

    """
    def test(self):
        config = self.load_config()
        print(config)
        config['darkmode'] = 'light'
        self.save_config(config)
    """

    def bevestig_mode(self):
        print("Mode opgeslagen!")
        config = self.load_config()

        #config["language"] = self.configuratie.get("language", "nl")
        #print("config", config)

        if self.mode_choice1.isChecked():
            config['darkmode'] = 'light'
        elif self.mode_choice2.isChecked():
            config['darkmode'] = 'dark'
        else:
            config['darkmode'] = 'blue'

        if self.mode_choice4.isChecked():
            config['language'] = 'nl'
        elif self.mode_choice5.isChecked(): 
            config['language'] = 'en'
        else:
            config['language'] = 'de'

        self.save_config(config)
        self.melding_opgeslagen()

        
    def melding_opgeslagen(self):
        print("self.configuratie opgeslagen!")
        QMessageBox.information(self, "Opgeslagen", "self.configuratie is opgeslagen!")
        self.close()

    def change_location(self):
        from PyQt6.QtWidgets import QFileDialog
        new_location = QFileDialog.getExistingDirectory(self, "Selecteer nieuwe opslaglocatie")
        if new_location:
            self.configuratie["opslaglocatie"] = new_location
            self.save_config(self.configuratie)
            QMessageBox.information(self, "Opgeslagen", f"Nieuwe opslaglocatie is opgeslagen: {new_location}")
            self.label5.setText(self.configuratie.get("opslaglocatie", "/home/kees/Data/"))