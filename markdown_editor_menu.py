from PyQt6.QtWidgets import QMainWindow
import yaml


class Markdown_Editor_Menu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mijn_configuratie = self.load_config()

        # taal
        self.taal = self.mijn_configuratie.get("language", "nl")
        if self.taal == "nl":
            self.taal = "nl"
        elif self.taal == "de":
            self.taal = "de"
        else:
            self.taal = "en"

    def load_config(self):
        try:
            with open("config.yaml", "r", encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            config = {}
        return config

    def load_config_keuze_teksten(self):
        try:
            with open(self.opslaglocatie_keuze_teksten, "r", encoding='utf-8') as f:
                config_keuze_teksten = yaml.safe_load(f)
        except FileNotFoundError:
            config_keuze_teksten = {}
        return config_keuze_teksten
    