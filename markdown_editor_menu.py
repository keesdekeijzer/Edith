from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QToolBar, QVBoxLayout, QWidget
import yaml
from PyQt6.QtGui import QAction
from code_editor import CodeEditor
from keuze_teksten_inhoud import keuze_teksten_inhoud, keuze_teksten_naam
# Import the styles from styles.py  
import my_constants
import styles

from teksten_menu import menu_teksten_nl, menu_teksten_en, menu_teksten_de
from teksten_meldingen import meldingen_nl, meldingen_en, meldingen_de
from keuze_teksten import keuze_teksten_nl, keuze_teksten_en, keuze_teksten_de

class Markdown_Editor_Menu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mijn_configuratie = self.load_config()

        self.unsaved_changes = False
        self.current_path = None  # pad naar het huidige bestand
        
        
        self.mijn_css_configuratie = self.load_css_config()  # Load configuration from css_config.yaml
        
        self.preview_stijl = {
            "voorgrondkleur": self.mijn_css_configuratie.get("foreground_color", "#47256D"),
            "achtergrondkleur": self.mijn_css_configuratie.get("background_color", "#FFFFFF")
        }

        self.zoek_suggesties = my_constants.ZOEK_SUGGESTIES
        
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


        self.maak_menu_punt("nieuw_actie", self.menu_teksten["Nieuw"], "Ctrl+N", self.nieuw)
        
        self.maak_menu_punt("openen_actie", self.menu_teksten["Openen"], "Ctrl+O", self.openen)

        self.maak_menu_punt("invoegen_actie", self.menu_teksten["Invoegen"], "", self.invoegen)

        self.maak_menu_punt("opslaan_actie", self.menu_teksten["Opslaan"], "Ctrl+S", self.opslaan)

        self.maak_menu_punt("opslaan_als_actie", self.menu_teksten["Opslaan als"], "Ctrl+Alt+S", self.opslaan_als)

        self.maak_menu_punt("selectie_opslaan_als_actie", self.menu_teksten["Selectie opslaan als"], "Ctrl+Alt+T", self.selectie_opslaan_als)

        self.maak_menu_punt("importeer_pdf_als_tekst_actie", self.menu_teksten["Importeer pdf als tekst"], "", self.import_pdf_as_text)

        self.maak_menu_punt("importeer_pdf_als_md_actie", self.menu_teksten["Importeer pdf als markdown"], "", self.import_pdf_as_md)

        self.maak_menu_punt("importeer_epub_actie", self.menu_teksten["Importeer ePub"], "Alt+E", self.import_epub)

        self.maak_menu_punt("export_pdf_actie", self.menu_teksten["Exporteer als PDF"], "", self.export_pdf)

        self.maak_menu_punt("export_word_actie", self.menu_teksten["Exporteer naar Word"], "", self.export_word)

        self.maak_menu_punt("export_epub_actie", self.menu_teksten["Exporteer naar ePub"], "", self.export_epub)

        self.maak_menu_punt("export_txt_actie", self.menu_teksten["Exporteer als tekst"], "", self.export_txt)

        self.maak_menu_punt("export_txt_per_hoofdstuk_actie", self.menu_teksten["Exporteer als tekstbestand per hoofdstuk"], "", self.export_txt_per_chapter)

        self.maak_menu_punt("epub_tts_teksten_actie", self.menu_teksten["Exporteer ePub naar TTS-teksten"], "Alt+Ctrl+E", self.export_epub_to_tts_texts)        

        self.maak_menu_punt("afsluiten_actie", self.menu_teksten["Afsluiten"], "Ctrl+Q", self.afsluiten)

        self.maak_menu_punt("kopieren_actie", self.menu_teksten["Kopieren"], "Ctrl+C", self.kopieren)

        self.maak_menu_punt("plakken_actie", self.menu_teksten["Plakken"], "Ctrl+V", self.plakken)

        self.maak_menu_punt("knippen_actie", self.menu_teksten["Knippen"], "Ctrl+X", self.knippen)

        self.maak_menu_punt("alles_selecteren_actie", self. menu_teksten["Alles selecteren"], "Ctrl+A", self.alles_selecteren)

        self.maak_menu_punt("ongedaan_maken_actie", self.menu_teksten["Ongedaan maken"], "Ctrl+Z", self.ongedaan_maken)

        self.maak_menu_punt("opnieuw_doen_actie", self.menu_teksten["Opnieuw doen"], "Ctrl+R", self.opnieuw_doen)

        self.maak_menu_punt("normaliseren_actie", self.menu_teksten["Normaliseren"], "Alt+N", self.normaliseren)

        self.maak_menu_punt("geen_hoofdletters_actie", self.menu_teksten["Geen hoofdletters"], "Alt+U", self.geen_hoofdletters)

        self.maak_menu_punt("hoofdletters_actie", self.menu_teksten["Hoofdletters"], "", self.hoofdletters)

        self.maak_menu_punt("schrift_actie", self.menu_teksten["Schrift"], "Alt+S", self.schrift)

        self.maak_menu_punt("spellcheck_actie", self.menu_teksten["Spelling controleren"], "F7", self.spellcheck)

        self.maak_menu_punt("woorden_vervangen_actie", self.menu_teksten["Woorden vervangen"], "", self.woorden_vervangen)

        self.maak_menu_punt("romeinse_cijfers_vervangen_actie", self.menu_teksten["Romeinse cijfers vervangen"], "Alt+R", self.romeinse_cijfers_vervangen)

        self.maak_menu_punt("alle_romeinse_cijfers_vervangen_actie", self.menu_teksten["Alle Romeinse cijfers vervangen"], "", self.alle_romeinse_cijfers_vervangen)

        self.maak_menu_punt("hoofdstukken_maken_cijfers_actie", self.menu_teksten["Hoofdstukken maken (cijfers)"], "", self.hoofdstukken_maken_cijfers)

        self.maak_menu_punt("hoofdstukken_maken_regels_actie", self.menu_teksten["Hoofdstukken maken (regels)"], "", self.hoofdstukken_maken_regels)
        
        self.maak_menu_punt("asterisken_verwijderen_actie", self.menu_teksten["Asterisken verwijderen"], "", self.asterisken_verwijderen)

        self.maak_menu_punt("afbeeldingen_verwijderen_actie", self.menu_teksten["Afbeeldingen verwijderen"], "", self.afbeeldingen_verwijderen)

        self.maak_menu_punt("lichte_modus_actie", self.menu_teksten["Lichte modus"], "", self.lichte_modus)

        self.maak_menu_punt("donkere_modus_actie", self.menu_teksten["Donkere modus"], "", self.donkere_modus)

        self.maak_menu_punt("blauwe_modus_actie", self.menu_teksten["Blauwe modus"], "", self.blauwe_modus)

        self.maak_menu_punt("font_actie", self.menu_teksten["Font"], "", self.font)

        self.maak_menu_punt("favoriete_font_actie", self.menu_teksten["Favoriete font"], "", self.favoriete_font)

        self.maak_menu_punt("naar_begin_actie", self.menu_teksten["Naar begin"], "Ctrl+Home", self.naar_begin)

        self.maak_menu_punt("naar_einde_actie", self.menu_teksten["Naar einde"], "Ctrl+End", self.naar_einde)

        self.maak_menu_punt("naar_begin_regel_actie", self.menu_teksten["Naar begin regel"], "Ctrl+[", self.naar_begin_regel)
        
        self.maak_menu_punt("naar_einde_regel_actie", self.menu_teksten["Naar einde regel"], "Ctrl+]", self.naar_einde_regel)

        self.maak_menu_punt("datum_actie", self.menu_teksten["Datum"], "Alt+D", self.datum)

        self.maak_menu_punt("tijd_actie", self.menu_teksten["Tijd"], "Alt+T", self.tijd)

        self.maak_menu_punt("md_link_actie", self.menu_teksten["md link"], "Alt+L", self.md_link)

        self.maak_menu_punt("md_afbeelding_actie", self.menu_teksten["md afbeelding"], "Alt+A", self.md_afbeelding)

        self.maak_menu_punt("paragraafteken_invoegen_actie", self.menu_teksten["Paragraafteken invoegen"], "Alt+P", self.paragraafteken_invoegen)

        self.maak_menu_punt("frontmatter_actie", self.menu_teksten["Frontmatter"], "Alt+F", self.frontmatter_popup)

        self.maak_menu_punt("memo_actie", self.menu_teksten["Memo"], "", self.memo)

        self.maak_menu_punt("memolijst_actie", self.menu_teksten["Memolijst"], "", self.memolijst)

        self.maak_menu_punt("configuratie_bewerken_actie", self.menu_teksten["Configuratie bewerken"], "", self.configuratie_bewerken)

        self.maak_menu_punt("over_actie", self.menu_teksten["Over Edith"], "", self.over)

        self.maak_menu_punt("help_actie", self.menu_teksten["Help"], "F1", self.edith_help)

        self.maak_menu_punt("keuzetekst1_actie", self.keuze_teksten_naam["Keuze 1"], "Alt+1", self.keuze_1)

        self.maak_menu_punt("keuzetekst2_actie", self.keuze_teksten_naam["Keuze 2"], "Alt+2", self.keuze_2)

        self.maak_menu_punt("keuzetekst3_actie", self.keuze_teksten_naam["Keuze 3"], "Alt+3", self.keuze_3)

        self.maak_menu_punt("keuzetekst4_actie", self.keuze_teksten_naam["Keuze 4"], "Alt+4", self.keuze_4)

        self.maak_menu_punt("keuzetekst5_actie", self.keuze_teksten_naam["Keuze 5"], "Alt+5", self.keuze_5)

        self.maak_menu_punt("keuzetekst6_actie", self.keuze_teksten_naam["Keuze 6"], "Alt+6", self.keuze_6)

        self.maak_menu_punt("keuzetekst7_actie", self.keuze_teksten_naam["Keuze 7"], "Alt+7", self.keuze_7)

        self.maak_menu_punt("keuzetekst8_actie", self.keuze_teksten_naam["Keuze 8"], "Alt+8", self.keuze_8)

        self.maak_menu_punt("keuzetekst9_actie", self.keuze_teksten_naam["Keuze 9"], "Alt+9", self.keuze_9)

        self.maak_menu_punt("keuzetekst10_actie", self.keuze_teksten_naam["Keuze 10"], "Alt+0", self.keuze_10)

        self.maak_menu_punt("versleutel_actie", self.menu_teksten["Versleutel Bestand"], "", self.versleutelen)

        self.maak_menu_punt("ontsleutel_actie", self.menu_teksten["Ontsleutel Bestand"], "", self.ontsleutelen)

        # themes ?

        bestand_menu = self.menuBar().addMenu(self.menu_teksten["Bestand"])        
        bestand_menu.addAction(self.actie["nieuw_actie"])        
        bestand_menu.addAction(self.actie["openen_actie"])
        bestand_menu.addAction(self.actie["invoegen_actie"])
        bestand_menu.addAction(self.actie["opslaan_actie"]) 
        bestand_menu.addAction(self.actie["opslaan_als_actie"])
        bestand_menu.addAction(self.actie["selectie_opslaan_als_actie"])
        bestand_menu.addSeparator()
        bestand_menu.addAction(self.actie["importeer_pdf_als_tekst_actie"])
        bestand_menu.addAction(self.actie["importeer_pdf_als_md_actie"])
        bestand_menu.addAction(self.actie["importeer_epub_actie"])
        bestand_menu.addSeparator()
        bestand_menu.addAction(self.actie["export_pdf_actie"])
        bestand_menu.addAction(self.actie["export_word_actie"])
        bestand_menu.addAction(self.actie["export_epub_actie"])
        bestand_menu.addAction(self.actie["export_txt_actie"])
        bestand_menu.addAction(self.actie["export_txt_per_hoofdstuk_actie"])
        bestand_menu.addAction(self.actie["epub_tts_teksten_actie"])
        bestand_menu.addSeparator()
        bestand_menu.addAction(self.actie["afsluiten_actie"])

        bewerken_menu = self.menuBar().addMenu(self.menu_teksten["Bewerken"])
        bewerken_menu.addAction(self.actie["kopieren_actie"])
        bewerken_menu.addAction(self.actie["knippen_actie"])
        bewerken_menu.addAction(self.actie["plakken_actie"])
        bewerken_menu.addSeparator()
        bewerken_menu.addAction(self.actie["alles_selecteren_actie"])
        bewerken_menu.addAction(self.actie["ongedaan_maken_actie"])
        bewerken_menu.addAction(self.actie["opnieuw_doen_actie"])
        bewerken_menu.addSeparator()
        bewerken_menu.addAction(self.actie["normaliseren_actie"])
        bewerken_menu.addAction(self.actie["geen_hoofdletters_actie"])
        bewerken_menu.addAction(self.actie["hoofdletters_actie"])
        bewerken_menu.addAction(self.actie["schrift_actie"])
        bewerken_menu.addSeparator()
        bewerken_menu.addAction(self.actie["spellcheck_actie"])
        bewerken_menu.addAction(self.actie["woorden_vervangen_actie"])
        bewerken_menu.addSeparator()
        bewerken_menu.addAction(self.actie["romeinse_cijfers_vervangen_actie"])
        bewerken_menu.addAction(self.actie["alle_romeinse_cijfers_vervangen_actie"])
        bewerken_menu.addSeparator()
        bewerken_menu.addAction(self.actie["hoofdstukken_maken_cijfers_actie"])
        bewerken_menu.addAction(self.actie["hoofdstukken_maken_regels_actie"])
        bewerken_menu.addSeparator()
        bewerken_menu.addAction(self.actie["frontmatter_actie"])
        bewerken_menu.addSeparator()
        bewerken_menu.addAction(self.actie["asterisken_verwijderen_actie"])
        bewerken_menu.addAction(self.actie["afbeeldingen_verwijderen_actie"])

        beeld_menu = self.menuBar().addMenu(self.menu_teksten["Beeld"])
        beeld_menu.addAction(self.actie["lichte_modus_actie"])
        beeld_menu.addAction(self.actie["donkere_modus_actie"])
        beeld_menu.addAction(self.actie["blauwe_modus_actie"])
        beeld_menu.addSeparator()
        beeld_menu.addAction(self.actie["font_actie"])
        beeld_menu.addAction(self.actie["favoriete_font_actie"])
        
        navigatie_menu = self.menuBar().addMenu(self.menu_teksten["Navigatie"])
        navigatie_menu.addAction(self.actie["naar_begin_actie"])
        navigatie_menu.addAction(self.actie["naar_einde_actie"])
        navigatie_menu.addAction(self.actie["naar_begin_regel_actie"])
        navigatie_menu.addAction(self.actie["naar_einde_regel_actie"])

        invoegen_menu = self.menuBar().addMenu(self.menu_teksten["Invoegen"])
        invoegen_menu.addAction(self.actie["datum_actie"])
        invoegen_menu.addAction(self.actie["tijd_actie"])
        invoegen_menu.addAction(self.actie["md_link_actie"])
        invoegen_menu.addAction(self.actie["md_afbeelding_actie"])
        invoegen_menu.addSeparator()
        invoegen_menu.addAction(self.actie["paragraafteken_invoegen_actie"])

        invoegen_menu = self.menuBar().addMenu(self.menu_teksten["Teksten"])
        invoegen_menu.addAction(self.actie["keuzetekst1_actie"])
        invoegen_menu.addAction(self.actie["keuzetekst2_actie"])
        invoegen_menu.addAction(self.actie["keuzetekst3_actie"])
        invoegen_menu.addAction(self.actie["keuzetekst4_actie"])
        invoegen_menu.addAction(self.actie["keuzetekst5_actie"])
        invoegen_menu.addAction(self.actie["keuzetekst6_actie"])
        invoegen_menu.addAction(self.actie["keuzetekst7_actie"])
        invoegen_menu.addAction(self.actie["keuzetekst8_actie"])
        invoegen_menu.addAction(self.actie["keuzetekst9_actie"])
        invoegen_menu.addAction(self.actie["keuzetekst10_actie"])

        extra_menu = self.menuBar().addMenu(self.menu_teksten["Extra"])
        extra_menu.addAction(self.actie["memo_actie"])
        extra_menu.addAction(self.actie["memolijst_actie"])
        extra_menu.addSeparator()
        extra_menu.addAction(self.actie["configuratie_bewerken_actie"])
        extra_menu.addSeparator()
        extra_menu.addAction(self.actie["versleutel_actie"])
        extra_menu.addAction(self.actie["ontsleutel_actie"])

        hulp_menu = self.menuBar().addMenu(self.menu_teksten["Help"])
        hulp_menu.addAction(self.actie["over_actie"])
        hulp_menu.addAction(self.actie["help_actie"])
 
        # set style for menubar and menu's
        self.menuBar().setStyleSheet(styles.menuBar_style)


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

