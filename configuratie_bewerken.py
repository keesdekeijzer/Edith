from PyQt6.QtWidgets import QDialog, QLabel, QMessageBox, QRadioButton, QVBoxLayout, QPushButton as QButton
import yaml

from teksten_config import config_meldingen_de, config_meldingen_en, config_meldingen_nl

from config import configuratie

class ConfiguratieBewerken(QDialog):
    def __init__(self, taal='nl'):
        super().__init__()
        self.taal = taal
        
        self.setModal(True)
        self.setup_ui()
        #self.test()

        self.taal = configuratie.get("language", "nl")

        self.config_meldingen = {}

        if self.taal == "en":
            self.config_meldingen = config_meldingen_en
        elif self.taal == "de":
            self.config_meldingen = config_meldingen_de
        else:
            self.config_meldingen = config_meldingen_nl

        self.setWindowTitle(self.config_meldingen["Configuratie bewerken"])

    def setup_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Hier kun je de configuratie bewerken.")
        layout.addWidget(label)
        label2 = QLabel("Light mode / Dark mode / Blue mode")
        layout.addWidget(label2)
        self.mode_choice1 = QRadioButton("Light mode")
        self.mode_choice2 = QRadioButton("Dark mode")
        self.mode_choice3 = QRadioButton("Blue mode")
        layout.addWidget(self.mode_choice1)
        layout.addWidget(self.mode_choice2)
        layout.addWidget(self.mode_choice3)

        label3 = QLabel("Current language: " + configuratie.get("language", "nl"))
        layout.addWidget(label3)

        label4 = QLabel("Selected language: " + configuratie.get("language", "nl"))
        layout.addWidget(label4)

        config = self.load_config()
        if config.get('darkmode') == 'light':
            self.mode_choice1.setChecked(True)
        elif config.get('darkmode') == 'dark':
            self.mode_choice2.setChecked(True)
        else:
            self.mode_choice3.setChecked(True)

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
        if self.mode_choice1.isChecked():
            config['darkmode'] = 'light'
        elif self.mode_choice2.isChecked():
            config['darkmode'] = 'dark'
        else:
            config['darkmode'] = 'blue'
        self.save_config(config)
        self.melding_opgeslagen()

        
    def melding_opgeslagen(self):
        print("Configuratie opgeslagen!")
        QMessageBox.information(self, "Opgeslagen", "Configuratie is opgeslagen!")
        self.close()