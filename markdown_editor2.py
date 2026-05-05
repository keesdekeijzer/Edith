from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPlainTextEdit
from PyQt6.QtWebEngineWidgets import QWebEngineView
from highlighter_markdown import MarkdownHighlighter
from markdown_renderer import render_markdown
from e2 import CodeEditor

class Markdown_Editor(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Editor links
        self.editor = CodeEditor()
        self.editor.set_highlighter(MarkdownHighlighter)
        layout.addWidget(self.editor, 1)

        # Preview rechts
        self.preview = QWebEngineView()
        layout.addWidget(self.preview, 1)

        # Live updates
        self.editor.textChanged.connect(self.update_preview)

        # Initial render
        self.update_preview()

    def update_preview(self):
        text = self.editor.toPlainText()
        html = render_markdown(text)
        self.preview.setHtml(html)
        