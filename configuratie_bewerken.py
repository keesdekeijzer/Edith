from PyQt6.QtWidgets import QDialog, QVBoxLayout
import yaml

class ConfiguratieBewerken(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuratie bewerken")
        self.setModal(True)
        self.setup_ui()
        self.test()

    def setup_ui(self):
        layout = QVBoxLayout()
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

    