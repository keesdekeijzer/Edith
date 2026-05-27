from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPlainTextEdit, QLineEdit, QPushButton, QCheckBox, QLabel
)
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor
from PyQt6.QtCore import Qt
import sys


class SearchReplaceWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zoek en Vervang met Highlight - QPlainTextEdit")
        self.resize(800, 520)

        self.editor = QPlainTextEdit()
        self.editor.setPlainText(
            "Voorbeeldtekst:\nDit is een regel.\nDit is nog een regel.\nZoeken en vervangen met PyQt6.\nZoeken is leuk. zoeken Zoeken."
        )

        # Zoek- en vervang widgets
        find_label = QLabel("Zoeken:")
        self.find_input = QLineEdit()
        self.case_cb = QCheckBox("Hoofdlettergevoelig")
        next_btn = QPushButton("Volgende")
        prev_btn = QPushButton("Vorige")

        replace_label = QLabel("Vervangen door:")
        self.replace_input = QLineEdit()
        replace_btn = QPushButton("Vervangen")
        replace_all_btn = QPushButton("Vervang alles")

        # Layout
        top_layout = QHBoxLayout()
        top_layout.addWidget(find_label)
        top_layout.addWidget(self.find_input)
        top_layout.addWidget(self.case_cb)
        top_layout.addWidget(prev_btn)
        top_layout.addWidget(next_btn)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(replace_label)
        bottom_layout.addWidget(self.replace_input)
        bottom_layout.addWidget(replace_btn)
        bottom_layout.addWidget(replace_all_btn)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.editor)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        # Signalen
        next_btn.clicked.connect(self.find_next)
        prev_btn.clicked.connect(self.find_previous)
        replace_btn.clicked.connect(self.replace_one)
        replace_all_btn.clicked.connect(self.replace_all)
        self.find_input.textChanged.connect(self.update_highlight)
        self.case_cb.stateChanged.connect(self.update_highlight)

        # Highlight format
        self.highlight_format = QTextCharFormat()
        self.highlight_format.setBackground(QColor("#FFF59D"))  # lichtgeel
        self.match_format = QTextCharFormat()
        self.match_format.setBackground(QColor("#FFCC80"))  # geselecteerde match iets donkerder

    def find_next(self):
        text = self.find_input.text()
        if not text:
            return
        flags = 0 if self.case_cb.isChecked() else Qt.MatchFlag.MatchFixedString
        # Use QTextDocument.find; for case-insensitive we use lower() fallback search loop
        doc = self.editor.document()
        cursor = self.editor.textCursor()
        start_pos = cursor.selectionEnd() if cursor.hasSelection() else cursor.position()
        it = doc.find(text, start_pos, 0 if self.case_cb.isChecked() else getattr(__import__('PyQt6.Qt', fromlist=['Qt']).Qt, 'CaseInsensitive', 0))
        if it.isNull():
            # wrap-around: search from start
            it = doc.find(text, 0, 0 if self.case_cb.isChecked() else getattr(__import__('PyQt6.Qt', fromlist=['Qt']).Qt, 'CaseInsensitive', 0))
        if not it.isNull():
            self.editor.setTextCursor(it)
            self.update_highlight()

    def find_previous(self):
        # backwards search: iterate matches and pick last before current position
        text = self.find_input.text()
        if not text:
            return
        doc = self.editor.document()
        # flags = 0 if self.case_cb.isChecked() else QtCore.Qt.CaseInsensitive
        flags = 0 if self.case_cb.isChecked() else getattr(__import__('PyQt6.Qt', fromlist=['Qt']).Qt, 'CaseInsensitive', 0)
        cur = self.editor.textCursor()
        pos = cur.selectionStart() if cur.hasSelection() else cur.position()
        it = doc.find(text, 0, flags)
        last = None
        while not it.isNull() and it.selectionEnd() <= pos:
            last = it
            it = doc.find(text, it.selectionEnd(), flags)
        if last:
            self.editor.setTextCursor(last)
        else:
            # wrap to last match in document
            it = doc.find(text, 0, flags)
            last = None
            while not it.isNull():
                last = it
                it = doc.find(text, it.selectionEnd(), flags)
            if last:
                self.editor.setTextCursor(last)
        self.update_highlight()

    def replace_one(self):
        cursor = self.editor.textCursor()
        find_text = self.find_input.text()
        if not find_text:
            return
        selected = cursor.selectedText()
        if cursor.hasSelection() and ((self.case_cb.isChecked() and selected == find_text) or (not self.case_cb.isChecked() and selected.lower() == find_text.lower())):
            cursor.insertText(self.replace_input.text())
            self.editor.setTextCursor(cursor)
        self.find_next()

    def replace_all(self):
        find_text = self.find_input.text()
        if not find_text:
            return
        text = self.editor.toPlainText()
        if self.case_cb.isChecked():
            new_text = text.replace(find_text, self.replace_input.text())
        else:
            # case-insensitive replace preserving original case is complex; use simple lower-replace
            import re
            pattern = re.compile(re.escape(find_text), re.IGNORECASE)
            new_text = pattern.sub(self.replace_input.text(), text)
        self.editor.setPlainText(new_text)
        self.update_highlight()

    def update_highlight(self):
        # Clear selections and add new extra selections for all matches.
        find_text = self.find_input.text()
        extra_selections = []

        if find_text:
            doc = self.editor.document()
            flags = 0 if self.case_cb.isChecked() else getattr(__import__('PyQt6.Qt', fromlist=['Qt']).Qt, 'CaseInsensitive', 0)
            #flags = 0
            it = doc.find(find_text, 0, flags)
            cursors = []
            while not it.isNull():
                cursors.append(it)
                it = doc.find(find_text, it.selectionEnd(), flags)

            # Create ExtraSelection objects
            for c in cursors:
                sel = QTextCursor(c)
                selection = QTextCursor(sel)
                extra = self._make_extra(selection, self.highlight_format)
                extra_selections.append(extra)

            # If current cursor is on a match, make it highlighted differently
            cur = self.editor.textCursor()
            for i, c in enumerate(cursors):
                if c.selectionStart() <= cur.position() <= c.selectionEnd():
                    # mark this one with match_format
                    extra_selections[i] = self._make_extra(QTextCursor(c), self.match_format)
                    break

        self.editor.setExtraSelections(extra_selections)

    def _make_extra(self, cursor: QTextCursor, fmt: QTextCharFormat):
        from PyQt6.QtWidgets import QTextEdit
        extra = QTextEdit.ExtraSelection()
        extra.cursor = cursor
        extra.format = fmt
        return extra

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SearchReplaceWidget()
    w.show()
    sys.exit(app.exec())
