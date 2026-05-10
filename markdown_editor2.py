from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPlainTextEdit, QMessageBox, QMenuBar
from PyQt6.QtWebEngineWidgets import QWebEngineView
from highlighter_markdown import MarkdownHighlighter
from highlighter_python import PythonHighlighter
from highlighter_html import HtmlHighlighter
from markdown_renderer import render_markdown
from e2 import CodeEditor
import re
from outline_panel import OutlinePanel 
from pathlib import Path
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QImage, QGuiApplication, QAction
from PyQt6.QtCore import QStandardPaths
import os
from frontmatter_panel import FrontmatterPanel

class Markdown_Editor(QWidget):
    def __init__(self):
        super().__init__()

        # tijdelijk
        #self.current_file_path = "./test.md"

        # menu begin

        # Maak acties        
         
        # Bestand - Nieuw, Openen, Opslaan, Opslaan als, Sluiten

        nieuw_actie = QAction("Nieuw", self)        
        nieuw_actie.setShortcut("Ctrl+N")        
        nieuw_actie.triggered.connect(self.nieuw)
        
        openen_actie = QAction("Openen...", self)        
        openen_actie.setShortcut("Ctrl+O")        
        openen_actie.triggered.connect(self.openen)

        opslaan_actie = QAction("Opslaan...", self)        
        opslaan_actie.setShortcut("Ctrl+S")        
        opslaan_actie.triggered.connect(self.opslaan)

        opslaan_als_actie = QAction("Opslaan als...", self)        
        opslaan_als_actie.setShortcut("Ctrl+Alt+S")        
        opslaan_als_actie.triggered.connect(self.opslaan_als)
        
        afsluiten_actie = QAction("Afsluiten", self)        
        afsluiten_actie.setShortcut("Ctrl+Q")        
        afsluiten_actie.triggered.connect(self.close)

        # Bewerken - Kopieren, Plakken, Knippen, Zoeken, Alles selecteren, Ongedaan maken, Opnieuw doen,
        #     Normaliseren, Geen hoofdletters, Schrift

        kopieren_actie = QAction("Kopieren...", self)        
        kopieren_actie.setShortcut("Ctrl+C")        
        kopieren_actie.triggered.connect(self.kopieren)

        plakken_actie = QAction("Plakken...", self)        
        plakken_actie.setShortcut("Ctrl+V")        
        plakken_actie.triggered.connect(self.plakken)

        knippen_actie = QAction("Knippen...", self)        
        knippen_actie.setShortcut("Ctrl+X")        
        knippen_actie.triggered.connect(self.knippen)

        zoeken_actie = QAction("Zoeken...", self)        
        zoeken_actie.setShortcut("Ctrl+F")        
        zoeken_actie.triggered.connect(self.zoeken)

        alles_selecteren_actie = QAction("Alles selecteren", self)        
        alles_selecteren_actie.setShortcut("Ctrl+A")        
        alles_selecteren_actie.triggered.connect(self.alles_selecteren)

        ongedaan_maken_actie = QAction("Ongedaan maken", self)        
        ongedaan_maken_actie.setShortcut("Ctrl+Z")        
        ongedaan_maken_actie.triggered.connect(self.ongedaan_maken)

        opnieuw_doen_actie = QAction("Opnieuw doen", self)        
        opnieuw_doen_actie.setShortcut("Ctrl+R")        
        opnieuw_doen_actie.triggered.connect(self.opnieuw_doen)

        normaliseren_actie = QAction("Normaliseren", self)        
        normaliseren_actie.setShortcut("Alt+N")
        normaliseren_actie.triggered.connect(self.normaliseren)

        geen_hoofdletters_actie = QAction("Geen hoofdletters", self)        
        geen_hoofdletters_actie.setShortcut("Alt+U")        
        geen_hoofdletters_actie.triggered.connect(self.geen_hoofdletters)

        schrift_actie = QAction("Schrift", self)        
        schrift_actie.setShortcut("Alt+S") 
        schrift_actie.triggered.connect(self.schrift)

        # Beeld - Lichte modus, Donkere modus, Blauwe modus, Font, Lettergrootte

        # Invoegen - Datum, Tijd, md link, md afbeelding, if name == main

        # Apps - Memo, Memolijst

        # Help - Over Edith, Sneltoetsen, Sneltoetsen (Alt)
        
        over_actie = QAction("Over", self)        
        over_actie.triggered.connect(self.over)
        
        # Maak menubalk en menu's        
        
        menubalk = QMenuBar(self)                 # maak menubalk widget
        
        bestand_menu = menubalk.addMenu("Bestand")        
        bestand_menu.addAction(nieuw_actie)        
        bestand_menu.addAction(openen_actie)
        bestand_menu.addAction(opslaan_actie) 
        bestand_menu.addAction(opslaan_als_actie)
        bestand_menu.addSeparator()        
        bestand_menu.addAction(afsluiten_actie)

        bewerken_menu = menubalk.addMenu("Bewerken")
        bewerken_menu.addAction(kopieren_actie)
        bewerken_menu.addAction(knippen_actie)
        bewerken_menu.addAction(plakken_actie)
        bewerken_menu.addAction(zoeken_actie)
        bewerken_menu.addAction(alles_selecteren_actie)
        bewerken_menu.addAction(ongedaan_maken_actie)
        bewerken_menu.addAction(opnieuw_doen_actie)
        bewerken_menu.addAction(normaliseren_actie)
        bewerken_menu.addAction(geen_hoofdletters_actie)
        bewerken_menu.addAction(schrift_actie)

        beeld_menu = menubalk.addMenu("Beeld")

        invoegen_menu = menubalk.addMenu("Invoegen")

        apps_menu = menubalk.addMenu("Apps")
        
        hulp_menu = menubalk.addMenu("Help")        
        hulp_menu.addAction(over_actie)

        v_layout = QVBoxLayout(self)
        v_layout.setMenuBar(menubalk)  

        # menu einde

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)


        v_layout.addLayout(layout)
        #self.frontmatter = FrontmatterPanel(self)
        #layout.addWidget(self.frontmatter, 0)

        # Editor links
        self.editor = CodeEditor()
        self.editor.set_highlighter(MarkdownHighlighter)
        layout.addWidget(self.editor, 1)

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

    def load_file(self, path):
        text = Path(path).read_text(encoding="utf-8")
        self.editor.setPlainText(text)

        if path.endswith(".py"):
            self.editor.set_highlighter(PythonHighlighter)
        elif path.endswith(".md"):
            self.editor.set_highlighter(MarkdownHighlighter)
        elif path.endswith(".html", ".htm"):
            self.editor.set_highlighter(HtmlHighlighter)
        else:
            self.editor.set_highlighter(PythonHighlighter)

    # menu acties

    def nieuw(self):        
        QMessageBox.information(self, "Nieuw", "Nieuw bestand aangezaakt (voorbeeld).")

    def openen(self):        
        QMessageBox.information(self, "Openen", "Open dialoog (voorbeeld).")

    def opslaan(self):        
        QMessageBox.information(self, "Opslaan", "Opslaan dialoog (voorbeeld).")

    def opslaan_als(self):        
        QMessageBox.information(self, "Opslaan als", "Opslaan als dialoog (voorbeeld).")

    def kopieren(self):
        QMessageBox.information(self, "Kopieren", "Kopieren dialoog (voorbeeld).")

    def knippen(self):
        QMessageBox.information(self, "Knippen", "Knippen dialoog (voorbeeld).")

    def plakken(self):
        QMessageBox.information(self, "Plakken", "Plakken dialoog (voorbeeld).")
    
    def over(self):        
        QMessageBox.information(self, "Over", "Voorbeeldapp met PyQt6.")

    def zoeken(self):
        QMessageBox.information(self, "Zoeken", "Zoeken in de tekst")

    def alles_selecteren(self):
        QMessageBox.information(self, "Alles selecteren", "Alles selecteren in de tekst")

    def ongedaan_maken(self):
        QMessageBox.information(self, "Ongedaan maken", "Ongedaan maken (undo)")

    def opnieuw_doen(self):
        QMessageBox.information(self, "Opnieuw doen", "Opnieuw doen (redo)")

    def normaliseren(self):
        QMessageBox.information(self, "Normaliseren", "Normaliseren")

    def geen_hoofdletters(self):
        QMessageBox.information(self, "Geen hoofdletters", "Geen hoofdletters, alles naar kleine letters")

    def schrift(self):
        QMessageBox.information(self, "Schrift", "Omzetten naar schrift")

