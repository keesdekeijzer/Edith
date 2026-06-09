from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout
import yaml

class ConfiguratieBewerken(QDialog):
    def __init__(self, taal='nl'):
        super().__init__()
        self.taal = taal
        self.setWindowTitle("Configuratie bewerken")
        self.setModal(True)
        self.setup_ui()
        self.test()

    def setup_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Hier kun je de configuratie bewerken.")
        layout.addWidget(label)
        label2 = QLabel("Deze functionaliteit is nog in ontwikkeling.")
        layout.addWidget(label2)
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

    def test(self):
        config = self.load_config()
        print(config)
        config['darkmode'] = 'light'
        self.save_config(config)

    