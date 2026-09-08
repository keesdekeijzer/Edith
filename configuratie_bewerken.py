from PyQt6.QtWidgets import QButtonGroup, QDialog, QLabel, QMessageBox, QRadioButton, QVBoxLayout, QPushButton as QButton
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
        layout = QVBoxLayout()
        label = QLabel(self.config_meldingen["Hier kun je de configuratie bewerken."])
        layout.addWidget(label)
        label2 = QLabel("Light mode / Dark mode / Blue mode")
        layout.addWidget(label2)

        self.groep_mode = QButtonGroup(self)
        self.mode_choice1 = QRadioButton("Light mode")
        self.mode_choice2 = QRadioButton("Dark mode")
        self.mode_choice3 = QRadioButton("Blue mode")
        layout.addWidget(self.mode_choice1)
        layout.addWidget(self.mode_choice2)
        layout.addWidget(self.mode_choice3)
        self.groep_mode.addButton(self.mode_choice1, 1) 
        self.groep_mode.addButton(self.mode_choice2, 2)
        self.groep_mode.addButton(self.mode_choice3, 3)
        

        label3 = QLabel("Language / Taal / Sprache")
        layout.addWidget(label3)


        self.groep_taal = QButtonGroup(self)
        self.mode_choice4 = QRadioButton("Dutch")
        self.mode_choice5 = QRadioButton("English")
        self.mode_choice6 = QRadioButton("German")
        layout.addWidget(self.mode_choice4)
        layout.addWidget(self.mode_choice5)
        layout.addWidget(self.mode_choice6)
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

        label4 = QLabel("Save location: ")
        layout.addWidget(label4)

        self.label5 = QLabel(self.configuratie.get("opslaglocatie", "/home/kees/Data/"))
        layout.addWidget(self.label5)

        location_btn = QButton("Change location")
        layout.addWidget(location_btn)
        location_btn.clicked.connect(self.change_location)
        #self.label5.setText(self.configuratie.get("opslaglocatie", "/home/kees/Data/"))
        #layout.addWidget(self.label5)

        mode_btn = QButton("Opslaan")
        layout.addWidget(mode_btn)  
        mode_btn.clicked.connect(self.bevestig_mode)

        self.setLayout(layout)

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