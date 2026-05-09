from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPlainTextEdit
from PyQt6.QtWebEngineWidgets import QWebEngineView
from highlighter_markdown import MarkdownHighlighter
from markdown_renderer import render_markdown
from e2 import CodeEditor
import re
from outline_panel import OutlinePanel 
from pathlib import Path
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QImage, QGuiApplication
from PyQt6.QtCore import QStandardPaths
import os
from frontmatter_panel import FrontmatterPanel

class Markdown_Editor(QWidget):
    def __init__(self):
        super().__init__()

        # tijdelijk
        #self.current_file_path = "./test.md"

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

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
