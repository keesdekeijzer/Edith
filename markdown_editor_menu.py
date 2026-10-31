from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QToolBar, QVBoxLayout, QWidget
import yaml
from PyQt6.QtGui import QAction
from code_editor import CodeEditor
from keuze_teksten_inhoud import keuze_teksten_inhoud, keuze_teksten_naam
# Import the styles from styles.py  
import styles

from teksten_menu import menu_teksten_nl, menu_teksten_en, menu_teksten_de
from teksten_meldingen import meldingen_nl, meldingen_en, meldingen_de
from keuze_teksten import keuze_teksten_nl, keuze_teksten_en, keuze_teksten_de

class Markdown_Editor_Menu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mijn_configuratie = self.load_config()

        # colormode
        if self.mijn_configuratie["darkmode"] == "light":
            self.lichte_modus()
            self.color_mode = "light"
        elif self.mijn_configuratie["darkmode"] == "dark":
            self.donkere_modus()
            self.color_mode = "dark"
        else:
            self.blauwe_modus()
            self.color_mode = "blue"

        # taal
        self.taal = self.mijn_configuratie.get("language", "nl")
        if self.taal == "nl":
            self.taal = "nl"
        elif self.taal == "de":
            self.taal = "de"
        else:
            self.taal = "en"

        self.actie = {}

        self.keuze_teksten_naam = keuze_teksten_naam
        self.keuze_teksten_inhoud = keuze_teksten_inhoud
        self.opslaglocatie_keuze_teksten = self.mijn_configuratie.get("opslaglocatie_keuze_teksten", "/home/kees/Data/keuze_teksten")
        self.config_keuze_teksten = self.load_config_keuze_teksten()

        for i in range(10):            
            if f"keuze_{i + 1}" in self.config_keuze_teksten:
                ki = self.config_keuze_teksten[f"keuze_{i + 1}"]
                kz = ki[:20] + "..." if len(ki) > 20 else ki
            else: 
                ki = self.keuze_teksten_inhoud.get(f"Keuze {i + 1}", f"Keuze {i + 1}") 
                kz = self.keuze_teksten_naam.get(f"Keuze {i + 1}", f"Keuze {i + 1}") 
            self.keuze_teksten_naam[f"Keuze {i + 1}"] = kz
            self.keuze_teksten_inhoud[f"Keuze {i + 1}"] = ki

        # Toolbar aanmaken        
        self.toolbar = QToolBar("Mijn toolbar", self)        
        self.addToolBar(self.toolbar)

        self.toolbar.setStyleSheet(styles.toolbar_style)

        self.meldingen = {}
        self.menu_teksten = {}

        if self.taal == "en":
            self.menu_teksten = menu_teksten_en
            self.meldingen = meldingen_en
        elif self.taal == "de":
            self.menu_teksten = menu_teksten_de
            self.meldingen = meldingen_de
        else:
            self.menu_teksten = menu_teksten_nl
            self.meldingen = meldingen_nl

        self.keuze_teksten = {}

        if self.taal == "en":
            self.keuze_teksten = keuze_teksten_en
        elif self.taal == "de":
            self.keuze_teksten = keuze_teksten_de
        else:
            self.keuze_teksten = keuze_teksten_nl

        # Acties (knoppen) maken        
        actie_datum = QAction(self.menu_teksten["Datum"], self)        
        actie_datum.triggered.connect(self.datum)
        self.toolbar.addAction(actie_datum)

        actie_tijd = QAction(self.menu_teksten["Tijd"], self)        
        actie_tijd.triggered.connect(self.tijd)
        self.toolbar.addAction(actie_tijd)

        actie_md_link = QAction(self.menu_teksten["md link"], self)
        actie_md_link.triggered.connect(self.md_link)
        self.toolbar.addAction(actie_md_link)

        actie_md_afbeelding = QAction(self.menu_teksten["md afbeelding"], self)
        actie_md_afbeelding.triggered.connect(self.md_afbeelding)
        self.toolbar.addAction(actie_md_afbeelding)

        actie_frontmatter = QAction(self.menu_teksten["Frontmatter"], self)
        actie_frontmatter.triggered.connect(self.frontmatter)
        self.toolbar.addAction(actie_frontmatter)

        actie_frontmatter_epub = QAction(self.menu_teksten["Frontmatter epub"], self)
        actie_frontmatter_epub.triggered.connect(self.frontmatter_epub)
        self.toolbar.addAction(actie_frontmatter_epub)

        actie_versleutel = QAction(self.menu_teksten["Versleutel Bestand"], self)
        actie_versleutel.triggered.connect(self.versleutelen)
        self.toolbar.addAction(actie_versleutel)

        actie_ontsleutel = QAction(self.menu_teksten["Ontsleutel Bestand"], self)
        actie_ontsleutel.triggered.connect(self.ontsleutelen)
        self.toolbar.addAction(actie_ontsleutel)

        actie_memo = QAction(self.menu_teksten["Memo"], self)
        actie_memo.triggered.connect(self.memo)
        self.toolbar.addAction(actie_memo)

        actie_memolijst = QAction(self.menu_teksten["Memolijst"], self)
        actie_memolijst.triggered.connect(self.memolijst)
        self.toolbar.addAction(actie_memolijst)

        # Central widget        
        self.editor = CodeEditor()  
        container = QWidget()

        self.layout = QVBoxLayout(container)
        self.h_layout = QHBoxLayout()
        self.layout.addLayout(self.h_layout)   

        self.setCentralWidget(container)

    def maak_menu_punt(self, naam_actie, naam_in_menu, sneltoets, functie):
        self.actie[naam_actie] = QAction(naam_in_menu, self)
        if len(sneltoets) > 1:
            self.actie[naam_actie].setShortcut(sneltoets)
        self.actie[naam_actie].triggered.connect(functie)
        return

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

