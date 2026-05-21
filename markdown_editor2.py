import datetime

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QFileDialog, QInputDialog, QLabel, QMainWindow
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPlainTextEdit, QMessageBox, QMenuBar
from PyQt6.QtWebEngineWidgets import QWebEngineView
from highlighter_markdown import MarkdownHighlighter
from highlighter_python import PythonHighlighter
from highlighter_html import HtmlHighlighter
from markdown_renderer import render_markdown
from e2 import CodeEditor
import re, yaml
from outline_panel import OutlinePanel 
from pathlib import Path
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QImage, QGuiApplication, QAction, QTextCursor
from PyQt6.QtCore import QStandardPaths
import os
from frontmatter_panel import FrontmatterPanel
import pdfplumber
import pytesseract
from PIL import Image
from langdetect import detect, LangDetectException
#import language_tool_python
from PyQt6.QtGui import QTextDocument
from PyQt6.QtPrintSupport import QPrinter

from docx import Document
from bs4 import BeautifulSoup

import hashlib

from _fontsize import fontsize_counts

# instellingen importeren
from config import FRONTMATTER_TEXT, configuratie, font_sizes
from memo import Memo
from memolijst import MemoLijst

class Markdown_Editor(QWidget):
    def __init__(self):
        super().__init__()

        self.unsaved_changes = False
        self.current_path = None

        LANG_MAP = {
            "nl": "nld",
            "en": "eng",
            "fr": "fra",
            "de": "deu",
            "es": "spa",
            "it": "ita",
        }
        

        # menu begin
        actie = {}

        def maak_menu_punt(self, naam_actie, naam_in_menu, sneltoets, functie):
            actie[naam_actie] = QAction(naam_in_menu, self)
            if len(sneltoets) > 1:
                actie[naam_actie].setShortcut(sneltoets)
            actie[naam_actie].triggered.connect(functie)
            return

        # Maak acties        
         
        # Bestand - Nieuw, Openen, Opslaan, Opslaan als, Sluiten

        maak_menu_punt(self, "nieuw_actie", "Nieuw", "Ctrl+N", self.nieuw)
        
        maak_menu_punt(self, "openen_actie", "Openen...", "Ctrl+O", self.openen)

        maak_menu_punt(self, "opslaan_actie", "Opslaan", "Ctrl+S", self.opslaan)

        maak_menu_punt(self, "opslaan_als_actie", "Opslaan als...", "Ctrl+Alt+S", self.opslaan_als)

        maak_menu_punt(self, "importeer_pdf_als_tekst_actie", "Importeer pdf als tekst", "", self.import_pdf_as_text)

        maak_menu_punt(self, "importeer_pdf_als_md_actie", "Importeer pdf als markdown", "", self.import_pdf_as_md)

        maak_menu_punt(self, "export_pdf_actie", "Exporteer als PDF", "", self.export_pdf)

        maak_menu_punt(self, "export_word_actie", "Exporteer naar Word", "", self.export_word)

        maak_menu_punt(self, "afsluiten_actie", "Afsluiten", "Ctrl+Q", self.afsluiten)
 
        # Bewerken - Kopieren, Plakken, Knippen, Zoeken, Alles selecteren, Ongedaan maken, Opnieuw doen,
        #     Normaliseren, Geen hoofdletters, Schrift

        maak_menu_punt(self, "kopieren_actie", "Kopieren", "Ctrl+C", self.kopieren)

        maak_menu_punt(self, "plakken_actie", "Plakken", "Ctrl+V", self.plakken)

        maak_menu_punt(self, "knippen_actie", "Knippen", "Ctrl+X", self.knippen)

        maak_menu_punt(self, "zoeken_actie", "Zoeken...", "Ctrl+F", self.zoeken)

        maak_menu_punt(self, "alles_selecteren_actie", "Alles selecteren", "Ctrl+A", self.alles_selecteren)

        maak_menu_punt(self, "ongedaan_maken_actie", "Ongedaan maken", "Ctrl+Z", self.ongedaan_maken)

        maak_menu_punt(self, "opnieuw_doen_actie", "Opnieuw doen", "Ctrl+R", self.opnieuw_doen)

        maak_menu_punt(self, "normaliseren_actie", "Normaliseren", "Alt+N", self.normaliseren)

        maak_menu_punt(self, "geen_hoofdletters_actie", "Geen hoofdletters", "Alt+U", self.geen_hoofdletters)

        maak_menu_punt(self, "schrift_actie", "Schrift", "Alt+S", self.schrift)

        # Beeld - Lichte modus, Donkere modus, Blauwe modus, Font, Lettergrootte

        maak_menu_punt(self, "lichte_modus_actie", "Lichte modus", "", self.lichte_modus)

        maak_menu_punt(self, "donkere_modus_actie", "Donkere modus", "", self.donkere_modus)

        maak_menu_punt(self, "blauwe_modus_actie", "Blauwe modus", "", self.blauwe_modus)

        maak_menu_punt(self, "font_actie", "Font...", "", self.font)

        # Invoegen - Datum, Tijd, md link, md afbeelding, if name == main, frontmatter

        maak_menu_punt(self, "datum_actie", "Datum", "Alt+D", self.datum)

        maak_menu_punt(self, "tijd_actie", "Tijd", "Alt+T", self.tijd)

        maak_menu_punt(self, "md_link_actie", "md link", "Alt+L", self.md_link)

        maak_menu_punt(self, "md_afbeelding_actie", "md afbeelding", "Alt+A", self.md_afbeelding)

        maak_menu_punt(self, "if_name_is_main_actie", "if name == main", "Alt+I", self.if_name_is_main)

        maak_menu_punt(self, "frontmatter_actie", "Frontmatter", "Alt+F", self.frontmatter)

        # Apps - Memo, Memolijst

        maak_menu_punt(self, "memo_actie", "Memo", "", self.memo)

        maak_menu_punt(self, "memolijst_actie", "Memolijst", "", self.memolijst)

        # Help - Over Edith, Sneltoetsen, Sneltoetsen (Alt), Markdown
        
        maak_menu_punt(self, "over_actie", "Over Edith", "", self.over)

        maak_menu_punt(self, "sneltoetsen_actie", "Sneltoetsen", "", self.sneltoetsen)

        maak_menu_punt(self, "sneltoetsen_alt_actie", "Sneltoetsen (Alt)", "", self.sneltoetsen_alt)

        maak_menu_punt(self, "markdown_actie", "Markdown", "", self.markdown_overzicht)
        
        # Maak menubalk en menu's        
        
        menubalk = QMenuBar(self)                 # maak menubalk widget
        menubalk.setStyleSheet("padding: 8px;")
        menubalk.setMinimumHeight(30)
        menubalk.setMaximumHeight(60)
        
        bestand_menu = menubalk.addMenu("Bestand")        
        bestand_menu.addAction(actie["nieuw_actie"])        
        bestand_menu.addAction(actie["openen_actie"])
        bestand_menu.addAction(actie["opslaan_actie"]) 
        bestand_menu.addAction(actie["opslaan_als_actie"])
        bestand_menu.addSeparator()
        bestand_menu.addAction(actie["importeer_pdf_als_tekst_actie"])
        bestand_menu.addAction(actie["importeer_pdf_als_md_actie"])
        bestand_menu.addSeparator()
        bestand_menu.addAction(actie["export_pdf_actie"])
        bestand_menu.addAction(actie["export_word_actie"])
        bestand_menu.addSeparator()
        bestand_menu.addAction(actie["afsluiten_actie"])

        bewerken_menu = menubalk.addMenu("Bewerken")
        bewerken_menu.addAction(actie["kopieren_actie"])
        bewerken_menu.addAction(actie["knippen_actie"])
        bewerken_menu.addAction(actie["plakken_actie"])
        bewerken_menu.addSeparator()
        bewerken_menu.addAction(actie["zoeken_actie"])
        bewerken_menu.addAction(actie["alles_selecteren_actie"])
        bewerken_menu.addAction(actie["ongedaan_maken_actie"])
        bewerken_menu.addAction(actie["opnieuw_doen_actie"])
        bewerken_menu.addSeparator()
        bewerken_menu.addAction(actie["normaliseren_actie"])
        bewerken_menu.addAction(actie["geen_hoofdletters_actie"])
        bewerken_menu.addAction(actie["schrift_actie"])

        beeld_menu = menubalk.addMenu("Beeld")
        beeld_menu.addAction(actie["lichte_modus_actie"])
        beeld_menu.addAction(actie["donkere_modus_actie"])
        beeld_menu.addAction(actie["blauwe_modus_actie"])
        beeld_menu.addSeparator()
        beeld_menu.addAction(actie["font_actie"])

        invoegen_menu = menubalk.addMenu("Invoegen")
        invoegen_menu.addAction(actie["datum_actie"])
        invoegen_menu.addAction(actie["tijd_actie"])
        invoegen_menu.addAction(actie["md_link_actie"])
        invoegen_menu.addAction(actie["md_afbeelding_actie"])
        invoegen_menu.addAction(actie["if_name_is_main_actie"])
        invoegen_menu.addAction(actie["frontmatter_actie"])

        apps_menu = menubalk.addMenu("Apps")
        apps_menu.addAction(actie["memo_actie"])
        apps_menu.addAction(actie["memolijst_actie"])
        
        hulp_menu = menubalk.addMenu("Help")        
        hulp_menu.addAction(actie["over_actie"])
        hulp_menu.addAction(actie["sneltoetsen_actie"])
        hulp_menu.addAction(actie["sneltoetsen_alt_actie"])
        hulp_menu.addAction(actie["markdown_actie"])

        v_layout = QVBoxLayout(self)
        v_layout.setMenuBar(menubalk)  

        self.file_label = QLabel("?")  # bestandsnaam
        self.file_label.setStyleSheet("padding: 8px;")
        self.file_label.setMinimumHeight(30)
        self.file_label.setMaximumHeight(60)


        v_layout.addWidget(self.file_label, 0)


        # menu einde

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)


        v_layout.addLayout(layout)
        #self.frontmatter = FrontmatterPanel(self)
        #layout.addWidget(self.frontmatter, 0)

        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.setStyleSheet("padding: 8px;")
        self.statusbar.setMinimumHeight(30)
        self.statusbar.setMaximumHeight(60)

        v_layout.addWidget(self.statusbar, 0)
        self.statusbar.showMessage("Ready", 3000)

        # Editor links
        self.editor = CodeEditor()
        self.editor.set_highlighter(MarkdownHighlighter)
        layout.addWidget(self.editor, 1)

        self.editor.textChanged.connect(self.on_text_changed)

        # Outline panel
        self.outline_panel = OutlinePanel()
        layout.addWidget(self.outline_panel, 0)
        self.outline_panel.itemClicked.connect(self.jump_to_heading)  # _panel


        # Preview rechts
        self.preview = QWebEngineView()
        layout.addWidget(self.preview, 1)

        # Live updates
        self.editor.textChanged.connect(self.update_preview)

        # Initial render
        self.update_preview()

        self.editor.verticalScrollBar().valueChanged.connect(self.sync_scroll_to_preview)


    def on_text_changed(self):
        self.unsaved_changes = True
        self.statusbar.showMessage("Onopgeslagen wijzigingen")

    def _editor_scroll_ratio(self):
        sb = self.editor.verticalScrollBar()
        if sb.maximum() == 0:
            return 0
        return sb.value() / sb.maximum()
    
    def sync_scroll_to_preview(self):
        ratio = self._editor_scroll_ratio()
        
        js = f"""
        (function() {{
            let h = document.body.scrollHeight - window.innerHeight;
            window.scrollTo(0, h * {ratio});
        }})();
        """

        self.preview.page().runJavaScript(js)

    def update_preview(self):
        text = self.editor.toPlainText()
        html = render_markdown(text)
        ratio = self._editor_scroll_ratio()

        #self.frontmatter.load_frontmatter(text)

        # bepaal directory van het huidige bestand
        base_path = getattr(self, "current_file_path", None)
        if base_path:
            base_url = QUrl((base_path))  # assets map in dezelfde directory)
        else:
            base_url = QUrl("file:///")  # fallback

        self.preview.setHtml(html, baseUrl=base_url)

        # Sroll herstellen zodra de pagina geladen is
        def after_load(_):
            """
            Dit berekent de maximale verticale scrollafstand (in pixels) die de gebruiker kan scrollen op de pagina.

            Uitleg kort:
            - document.body.scrollHeight = totale hoogte van de inhoud van de pagina.
            - window.innerHeight = hoogte van het zichtbare venster (viewport).
            - h = document.body.scrollHeight - window.innerHeight = 
            het verschil tussen inhoudshoogte en viewport‑hoogte → de maximale scrollTop-waarde (0 tot h). 
            Als h ≤ 0 is, is er niks om te scrollen.
            """
            js = f"""
            (function() {{
                let h = document.body.scrollHeight - window.innerHeight;
                window.scrollTo(0, h * {ratio});
            }})();
            """
            self.preview.page().runJavaScript(js)

        self.preview.page().loadFinished.connect(lambda _: after_load(None))

        self.outline_panel.update_outline(self.parse_headings())
        
    def parse_headings(self):
        text = self.editor.toPlainText().split("\n")
        headings = []

        for i, line in enumerate(text):
            match = re.match(r'^(#{1,6})\s+(.*)', line)
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                headings.append((level, title, i))

        return headings
    
    def jump_to_heading(self, item):
        line = item.data(32)  # Retrieve line number from user data
        cursor = self.editor.textCursor()
        cursor.movePosition(cursor.MoveOperation.Start)
        cursor.movePosition(cursor.MoveOperation.Down, n=line)
        self.editor.setTextCursor(cursor)
        self.editor.setFocus()

    def insertFromMimeData(self, source):
        # Controleer of de geplakte data een afbeelding bevat
        if source.hasImage():
            self._handle_paste_image(source)
            return
        else:
            super().insertFromMimeData(source)

    def _handle_paste_image(self, source):
        image = source.imageData()
        if not isinstance(image, QImage):
            return

        # Bepaal waar het huidige markdown-bestand staat
        editor = self.parent().parent() # Assuming the parent of Markdown_Editor is the main window
        base_path = getattr(editor, "current_file_path", None)

        if base_path:
            # geen bestand geopend, gebruik standaard afbeeldingenmap
            save_dir = Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.PicturesLocation))
            
        else:
            # Gebruik dezelfde map als het markdown-bestand
            save_dir = Path(base_path).parent / "assets"

        save_dir.mkdir(parents=True, exist_ok=True)

        # Genereer een unieke bestandsnaam
        filename = f"pasted_{QGuiApplication.applicationPid()}_{id(image)}.png"
        file_path = save_dir / filename

        # Sla de afbeelding op
        image.save(str(file_path))

        # Voeg markdown-syntax toe voor de afbeelding
        rel_path = file_path.relative_to(Path(base_path).parent) if base_path else file_path
        self.insertPlainText(f"![{filename}]({rel_path.as_posix()})")

    def load_markdown_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.editor.setPlainText(content)
            self.current_file_path = file_path
            self.update_preview()

    def to_file_uri(path_or_uri):    
        if path_or_uri.startswith("file://"):        
            return path_or_uri    
        return Path(path_or_uri).resolve().as_uri()
    
    def update_frontmatter_from_panel(self, new_data):
        text = self.editor.toPlainText()

        # Vervang bestaande frontmatter
        import yaml
        new_yaml = yaml.safe_dump(new_data, sort_keys=False).strip()

        new_frontmatter = f"---\n{new_yaml}\n---"
        
        # Vervang in document
        import re
        updated = re.sub(r"^---\n(.*?)\n---", new_frontmatter, text, flags=re.DOTALL)
        
        self.editor.blockSignals(True)
        self.editor.setPlainText(updated)
        self.editor.blockSignals(False)

        # Preview opnieuw renderen
        self.update_preview()

    def load_highlighter(self):
        path = ""
        i = self.current_path.rfind(".")  # index van de laatste punt       
        if i != -1:
            path = self.current_path[i:]

        if path == ".py":
            self.editor.set_highlighter(PythonHighlighter)
        elif path == ".md":
            self.editor.set_highlighter(MarkdownHighlighter)
        elif path == ".html" or path == ".htm":
            self.editor.set_highlighter(HtmlHighlighter)
        else:
            self.editor.set_highlighter(MarkdownHighlighter)

    # menu acties

    def nieuw(self):        
        if self.unsaved_changes:
            reply = QMessageBox.question(self, 'Waarschuwing', 
                                         'Huidig bestand is nog niet opgeslagen. Wil je de wijzigingen opslaan?')
            if reply == QMessageBox.StandardButton.Yes:
                self.opslaan()
        self.editor.clear()
        self.setWindowTitle("Geen naam")
        self.current_path = None 
        self.statusbar.showMessage("Nieuw Bestand")
        self.file_label.setText("?")

    def openen(self):        
        if self.unsaved_changes:
            reply = QMessageBox.question(self, 'Waarschuwing', 
                                         'Huidig bestand is nog niet opgeslagen. Wil je de wijzigingen opslaan?')
            if reply == QMessageBox.StandardButton.Yes:
                self.opslaan()
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open bestand', configuratie["opslaglocatie"], 'Alle bestanden (*)')
            self.setWindowTitle(fname[0])
            self.file_label.setText(fname[0])
            
            with open(fname[0], 'r') as f:
                filetext = f.read()
                self.editor.setPlainText(filetext)
            self.current_path = fname[0]
            self.load_highlighter()
            self.statusbar.showMessage("Bestand geopend")
        except Exception as e:
            self.dialog_critical(str(e))

    def opslaan(self):        
        if self.current_path is not None:
            filetext = self.editor.toPlainText()
            try:
                with open(self.current_path, 'w') as f:
                    f.write(filetext)
                self.statusbar.showMessage("Bestand opgeslagen")
                self.file_label.setText(self.current_path)
            except Exception as e:
                self.dialog_critical(str(e))
        else:
            self.opslaan_als()

    def opslaan_als(self):        
        try:
            pathname = QFileDialog.getSaveFileName(self, 'Bestand opslaan', configuratie["opslaglocatie"], 'Tekst bestanden (*.txt)')
            filetext = self.editor.toPlainText()
            with open(pathname[0], 'w') as f:
                f.write(filetext)
            self.current_path = pathname[0]
            self.setWindowTitle(pathname[0])
            self.file_label.setText(pathname[0])
            self.statusbar.showMessage("Bestand opgeslagen")
        except Exception as e:
            errortekst = "Bestand niet opgeslagen!\n" + str(e)
            self.dialog_critical(errortekst)

    def afsluiten(self):
        QMessageBox.information(self, "Afsluiten", "Programma afsluiten.")
        CodeEditor.close(self)

    def kopieren(self):
        self.editor.copy()

    def knippen(self):
        self.editor.cut()

    def plakken(self):
        self.editor.paste()

    def zoeken(self):
        text, ok = QInputDialog.getText(self, 'Zoeken', 'Voer de zoekterm in:')
        if ok and text:
            gevonden = self.editor.find(text)
            if not gevonden:
                # weer naar boven
                cursor = self.editor.textCursor()
                cursor.movePosition(QTextCursor.MoveOperation.Start)
                self.editor.setTextCursor(cursor)
                gevonden = self.editor.find(text)
                if not gevonden:
                    term = text.replace('<','&lt;')
                    term = term.replace('>','&gt;')
                    QMessageBox.information(self, "Vinden", f"'{term}' niet gevonden")

    def alles_selecteren(self):
        self.editor.selectAll()

    def ongedaan_maken(self):
        self.editor.undo()

    def opnieuw_doen(self):
        self.editor.redo()

    def normaliseren(self):
        cursor = self.editor.textCursor()
        volledige_tekst = self.editor.toPlainText()
        tussenstap = ' '.join(volledige_tekst.split('\n'))
        genormaliseerde_tekst = '.\n'.join(tussenstap.split('.'))
        self.editor.setPlainText(genormaliseerde_tekst)

    def geen_hoofdletters(self):
        selectie = self.editor.textCursor()
        if selectie.hasSelection():
            geselecteerde_tekst = selectie.selectedText()
            kleine_tekst = geselecteerde_tekst.lower()
            selectie.insertText(kleine_tekst)
        else:
            QMessageBox.about(self, "Geen Selectie", "Selecteer eerst tekst om om te zetten naar kleine letters.")

    def schrift(self):
        selectie = self.editor.textCursor()
        if selectie.hasSelection():
            geselecteerde_tekst = selectie.selectedText()
            schrift_tekst = ''
            for char in geselecteerde_tekst:
                if 'A' <= char <= 'Z':
                    schrift_char = chr(ord(char) + 0x1D4D0 - ord('A'))
                elif 'a' <= char <= 'z':
                    schrift_char = chr(ord(char) + 0x1D4EA - ord('a'))
                else:
                    schrift_char = char
                schrift_tekst += schrift_char
            selectie.insertText(schrift_tekst)
        else:
            QMessageBox.about(self, "Geen Selectie", "Selecteer eerst tekst om om te zetten naar schrift.")

    def lichte_modus(self):
        configuratie["darkmode"] = 'light'
        self.setStyleSheet('')

    def donkere_modus(self):
        configuratie["darkmode"] = 'dark'
        self.setStyleSheet('''
            QWidget{
                background-color: rgb(33,33,33);
                color: #FFFFFF;
                }
            QPlainTextEdit{
                background-color: rgb(46,46,46);
                color: #FFFFFF;
            }
            ''')

    def blauwe_modus(self):
        configuratie["darkmode"] = 'blue'
        self.setStyleSheet('''
                QWidget{
                    background-color: #0000AA;
                    color: #FFFFFF;
                    }
                QPlainTextEdit{  
                    background-color: #000BFF;
                    color: #FFFFFF;
                    }
                ''')

    def font(self):
        from PyQt6.QtWidgets import QFontDialog
        font, ok = QFontDialog.getFont()
        if ok:
            self.editor.setFont(font)

    def over(self):        
        QMessageBox.information(self, "Over Edith", "Markdown editor met preview.")

    def sneltoetsen(self):
        QMessageBox.about(self, "Sneltoetsen", "Ctrl+N: Nieuw\nCtrl+O: Openen\nCtrl+S: Opslaan\n" \
        "Ctrl+Shift+S: Opslaan als\nCtrl+Q: Sluiten\nCtrl+C: Kopiëren\nCtrl+X: Knippen\nCtrl+V: Plakken\n" \
        "Ctrl+F: Zoeken\nCtrl+Z: Ongedaan maken\nCtrl+R: Opnieuw doen\nCtrl+A: Alles selecteren")

    def sneltoetsen_alt(self):
        QMessageBox.about(self, "Sneltoetsen Alt", "Invoegen:\nAlt+D: Datum\nAlt+T: Tijd\nAlt+L: md link\n" \
                          "Alt+A: md afbeelding\nAlt+I: if name == main\nAlt+F: Frontmatter\n\n" \
                          "Bewerken:\nAlt+N: Normaliseren\nAlt+U: Geen hoofdletters\nAlt+S: Schrift\n\n")


    def markdown_overzicht(self):
        QMessageBox.about(self, "Markdown", 
                          "Koppen:\n" \
                          "# H1\n## H2\n### H3\n\n" \
                          "Vet (bold):\t**vet**\n\n" \
                          "Schuin (italic):\t*schuin*\n\n" \
                          "Blockquote:\n> blockquote\n\n" \
                          "Genummerde lijst:\n1. eerste item\n2. tweede item\n3. derde item\n\n" \
                          "Ongenummerde lijst:\n- item A\n- item B\n- item C\n\n" \
                          "Highlight:\t==highlighted==\n")

    def datum(self):
        nu = datetime.datetime.now()
        datum_nu = nu.strftime("%Y-%m-%d")
        self.editor.insertPlainText(datum_nu)

    def tijd(self):
        nu = datetime.datetime.now()
        tijd_nu = nu.strftime("%H:%M")
        self.editor.insertPlainText(tijd_nu)

    def md_link(self):
        pathname = QFileDialog.getOpenFileName(self, 'Bestand openen', configuratie["opslaglocatie"], 'Alle bestanden (*)')
        if pathname[0]:
            bestandsnaam = pathname[0].split('/')[-1]
            md_code = f"[{bestandsnaam}]({pathname[0]})"
            self.editor.insertPlainText(md_code)

    def md_afbeelding(self):
        pathname = QFileDialog.getOpenFileName(self, 'Afbeelding openen', configuratie["opslaglocatie"], 'Afbeeldingen (*.png *.jpg *.jpeg *.bmp *.gif);;Alle bestanden (*)')
        if pathname[0]:
            bestandsnaam = pathname[0].split('/')[-1]
            md_code = f"![{bestandsnaam}]({pathname[0]})"
            self.editor.insertPlainText(md_code)

    def if_name_is_main(self):
        self.editor.insertPlainText("if__name__ == '__main__':\n    ")

    def frontmatter(self):
        fm = FRONTMATTER_TEXT
        self.editor.insertPlainText(fm)


    def memo(self):
        self.memo_venster = Memo()
        self.memo_venster.show()

    def memolijst(self):
        self.memo_lijst_venster = MemoLijst()
        self.memo_lijst_venster.show()

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Icon.Critical)
        dlg.show()

    # self.import_pdf_as_text
    # > self.pdf_to_text(path)

    # self.import_pdf_as_md


    def pdf_to_text(self, path):
        text = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text.append(page.extract_text() or "")
        return "\n\n".join(text)
    
    def open_pdf_as_text(self, path):
        text = self.pdf_to_text(path)
        self.editor.setPlainText(text)

    def open_pdf_as_markdown(self, path):
        text = self.pdf_to_text(path)
        md = text.replace("\n", "  \n")
        self.editor.setPlainText(md)

    def import_pdf_as_text(self):
        path, _ = QFileDialog.getOpenFileName(self, "Kies een pdf om te importeren", "", "PDF-bestanden (*.pdf)")
        if not path:
            return
        try:
            text = self.pdf_to_text(path)  # self.pdf_to_text_with_ocr(path)
        except Exception as e:
            QMessageBox.critical(self, "Fout bij importeren", str(e))
            return
        # Plaats tekst in editor
        self.editor.setPlainText(text)

        self.current_file_path = None
        self.file_label.setText("?")

    def import_pdf_as_md(self):
        path, _ = QFileDialog.getOpenFileName(self, "Kies een pdf om te importeren", "", "PDF-bestanden (*.pdf)")
        if not path:
            return
        try:
            text = self.pdf_to_markdown(path)  # self.pdf_to_markdown_with_ocr
        except Exception as e:
            QMessageBox.critical(self, "Fout bij importeren", str(e))
            return
        # Plaats tekst in editor
        self.editor.setPlainText(text)

        self.current_file_path = None
        self.file_label.setText("?")

    def pdf_to_markdown(self, path: str) -> str:
        # fontsizes
        # counts_by_page, dict(total_counter) = fontsize_counts(path)
        per_page, totaal  = fontsize_counts(path)
        print("Per pagina (pagina, {fontsize: count}):")
        for pnum, ctr in per_page:
            print(f"Pagina {pnum}: {ctr}")

        print("\nTotaal over hele document (fontsize: count):")
        # Sorteer op fontsize oplopend
        grootste_font_aantal = 0
        grootste_font_size = 0
        for size in sorted(totaal):
            print(f"{size}: {totaal[size]}")
            fontmaat = size
            fontaantal = totaal[size]
            
            if fontaantal > grootste_font_aantal:
                grootste_font_aantal = fontaantal
                grootste_font_size = fontmaat
        print("meest gebruikte font maat: ", grootste_font_size)

        kop_fonts = {}
        for size in sorted(totaal):
            if size > grootste_font_size:
                kop_fonts[size] = totaal[size]
        lengte = len(kop_fonts)
        print("lengte: ",lengte)
        volgende = "H1"
        for fontmaat in (sorted(kop_fonts, reverse=True)):
            print(fontmaat)
            if lengte > 0:
                font_sizes[volgende] = fontmaat - 0.1
                if volgende == "H3":
                    lengte = 0
                if volgende == "H2":
                    volgende = "H3"
                if volgende == "H1":
                    volgende = "H2"
        print(font_sizes)




        #
        md_lines = []

        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                chars = page.chars  # individuele tekstfragmenten met font info
                lines = self.group_chars_into_lines(chars)
                md_lines.extend(self.convert_lines_to_md(lines))

        return "\n".join(md_lines)
    
    def group_chars_into_lines(self, chars):
        lines = {}
        for ch in chars:
            y = round(ch["top"], 1)
            lines.setdefault(y, []).append(ch)

        # sorteer op Y (boven naar beneden)
        sorted_lines = []
        for y in sorted(lines.keys()):
            line = sorted(lines[y], key=lambda c: c["x0"])
            sorted_lines.append(line)
        return sorted_lines
    
    def detect_heading_level(self, font_size):
        if font_size >= font_sizes["H1"]:
            return 1
        if font_size >= font_sizes["H2"]:
            return 2
        if font_size >= font_sizes["H3"]:
            return 3
        return None
    
    def style_text(self, text, fontname):
        if "Bold" in fontname:
            return f"**{text}**"
        if "Italic" in fontname or "Oblique" in fontname:
            return f"*{text}"
        return text
    
    def convert_lines_to_md(self, lines):
        md = []

        for line in lines:
            # combineer chars
            text = "".join(ch["text"] for ch in line).strip()
            if not text:
                md.append("")
                continue

            # detecteer heading
            avg_size = sum(ch["size"] for ch in line) / len(line)
            level = self.detect_heading_level(avg_size)
            if level:
                md.append("#" * level + " " + text)
                continue

            # detecteer bullet list
            if text.startswith(("•", "-", "◦", "‣")):
                md.append("- " + text.lstrip("•-◦‣ "))
                continue

            # detecteer bold/italic per char
            styled = "".join(self.style_text(ch["text"], ch["fontname"]) for ch in line)
            md.append(styled)

        return md
    
    def page_needs_ocr(self, page):
        text = page.extract_text()
        return not text or text.strip() == ""
    
    def ocr_page(self, page):
        # Render PDF-pagina als afbeelding
        img = page.to_image(resolution=300).original
        pil_img = Image.fromarray(img)  # gaat fou als er geen array is
        return pytesseract.image_to_string(pil_img)
    
    def pdf_to_text_with_ocr(self, path):
        pages_text = []

        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()

                if not text or text.strip() == "":
                    # OCR fallback
                    text = self.ocr_page(page)

                pages_text.append(text or "")

        return "\n\n".join(pages_text)
    
    def pdf_to_markdown_with_ocr(self, path):
        raw_text = self.pdf_to_text_with_ocr(path)
        return self.pdf_to_markdown(raw_text)
    
    def detect_language(self, text: str) -> str:
        try:
            return detect(text)
        except LangDetectException:
            return "unknown"
        
    def ocr_page_with_lang(self, page):
        # Render PDF-pagima als afbeelding
        img = page.to_image(resolution=300).original
        pil_img = Image.fromarray(img)  # gaat fout als er geen array is

        # Probeer eerst een kleine preview voor taal detectie
        preview_text = pytesseract.image_to_string(pil_img, lang="eng")[:500]

        lang = self.detect_language(preview_text)
        tess_lang = self.LANG_MAP.get(lang, "eng")  # fallback naar Engels

        # OCR met gedetecteerde taal
        return pytesseract.image_to_string(pil_img, lang=tess_lang)

    def pdf_to_text_with_auto_ocr(self, path):
        pages_text = []

        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()

                if not text or text.strip() == "":
                    # OCR fallback met automatische taal
                    text = self.ocr_page_with_lang(page)

                pages_text.append(text or "")

        return "\n\n".join(pages_text)

    def export_markdown_to_pdf(self, md_text, output_path):
        # 1. Markdown -> HTML
        html = render_markdown(md_text)

        # 2. HTML in QTextDocument
        doc = QTextDocument()
        doc.setHtml(html)

        # 3. PDF printer instellen
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(output_path)

        # 4. Renderen
        doc.print(printer)

    def export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporteer naar PDF",
            "",
            "PDF-bestanden (*.pdf)"
        )

        if not path:
            return
        
        try:
            md_text = self.editor.toPlainText()
            self.export_markdown_to_pdf(md_text, path)
        except Exception as e:
            QMessageBox.critical(self, "Fout bij exporteren", str(e))
            return
        
        QMessageBox.information(self, "Succes", "PDF succesvol opgeslagen!")

    def html_to_docx(self, html, output_path):
        doc = Document()
        soup = BeautifulSoup(html, "html.parser")

        for el in soup.recursiveChildGenerator():
            if el.name == "h1":
                doc.add_heading(el.get_text(), level=1)
            elif el.name == "h2":
                doc.add_heading(el.get_text(), level=2)
            elif el.name == "h3":
                doc.add_heading(el.get_text(), level=3)
            elif el.name =="p":
                doc.add_paragraph(el.get_text())
            elif el.name == "pre":
                doc.add_paragraph(el.get_text(), style="Intense Quote")
            elif el.name == "code":
                doc.add_paragraph(el.get_text(), style="Intense Quote")
            elif el.name == "li":
                doc.add_paragraph(el.get_text(), style="List Bullet")
            elif el.name == "img":
                src = el["src"]
                doc.add_picture(src, width=None)  # optioneel: breedte instellen

        doc.save(output_path)

    def export_markdown_to_word(self, md_text, output_path):
        # 1. Metadata
        meta = self.extract_metadata(md_text)

        # 2. Markdown -> HTML
        html = render_markdown(md_text)

        # 3. TOC genereren
        headings = self.extract_headings(md_text)
        toc_html = self.build_clickable_toc(headings)

        # 4. TOC + body combineren
        full_html = toc_html + "<hr>" + html

        # 5. HTML -> DOCX
        self.html_to_docx(full_html, output_path)

    def extract_metadata(self, md_text):
        """
        Verwacht YAML frontmatter bovenaan het document.
        """
        fm = re.match(r"---\n(.*?)\n---", md_text, re.DOTALL)
        if not fm:
            return {}
        
        data = yaml.safe_load(fm.group(1))
        return data or {}

    def slugify(self, text):
        # Unieke maar stabiele ID
        base = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
        h = hashlib.md5(text.encode()).hexdigest()[:6]
        return f"{base}-{h}"

    def extract_headings(self, md_text):
        headings = []
        HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)", re.MULTILINE)
        for match in HEADING_RE.finditer(md_text):
            level = len(match.group(1))
            title = match.group(2).strip()
            anchor = self.slugify(title)
            headings.append((level, title, anchor))
        return headings

    def build_clickable_toc(self, headings):
        html = "<h1>Inhoudsopgave</h1><ul>"
        prev_level = 1

        for level, title, anchor in headings:
            if level > prev_level:
                html += "<ul>" * (level - prev_level)
            elif level < prev_level:
                html += "</ul>" * (prev_level - level)

            html += f"<li><a href=\"#{anchor}\">{title}</a></li>"
            prev_level = level

        html += "</ul>" * prev_level
        return html


    def export_word(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporteer naar Word",
            "",
            "Word-bestanden (*.docx)"
        )

        if not path:
            return
        
        md_text = self.editor.toPlainText()
        self.export_markdown_to_word(md_text, path)

        QMessageBox.information(self, "Succes", "Word-document opgeslagen!")





"""
# spellcheck is te langzaam, het vertraagd het programma enorm

class SpellChecker:
    def __init__(self, lang="nl"):
        self.tool = language_tool_python.LanguageTool(lang)
        

    def check(self,text):
        return self.tool.check(text)
    
    def suggestions_for(self, word):
        matches = self.tool.check(word)
        if matches:
            return matches[0].replacements
        return []
"""
