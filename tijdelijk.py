# tijdelijk

    """

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.AltModifier:
            if event.key() == Qt.Key.Key_D:
                self.datum()
            elif event.key() == Qt.Key.Key_T:
                self.tijd()
            elif event.key() == Qt.Key.Key_L:
                self.md_link()
            elif event.key() == Qt.Key.Key_A:
                self.md_afbeelding()
            elif event.key() == Qt.Key.Key_I:
                self.if_name_is_main()
            elif event.key() == Qt.Key.Key_F:
                self.frontmatter()
            elif event.key() == Qt.Key.Key_N:
                self.normaliseren()
            elif event.key() == Qt.Key.Key_U:
                self.geen_hoofdletters()
            elif event.key() == Qt.Key.Key_S:
                self.schrift()
        else:
            super().keyPressEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_preview()

    def on_text_changed(self):
        self.unsaved_changes = True
        self.update_preview()

    def update_preview(self):
        md_text = self.editor.toPlainText()
        html = render_markdown(md_text)
        self.preview.setHtml(html)

    def toggle_preview(self, checked):
        self.preview.setVisible(checked)

    def toggle_editor(self, checked):
        self.editor.setVisible(checked)

    def toggle_both(self, checked):
        self.editor.setVisible(checked)
        self.preview.setVisible(checked)

    def toggle_split(self, checked):
        self.editor.setVisible(True)
        self.preview.setVisible(True)

    def toggle_full_editor(self, checked):
        self.editor.setVisible(True)
        self.preview.setVisible(False)

    def toggle_full_preview(self, checked):
        self.editor.setVisible(False)
        self.preview.setVisible(True)

    def toggle_dark_mode(self, checked):
        if checked:
            self.donkere_modus()
        else:
            self.lichte_modus()

    def toggle_blue_mode(self, checked):
        if checked:
            self.blauwe_modus()
        else:
            self.lichte_modus()

    def toggle_font(self, checked):
        if checked:
            self.font()
        else:
            default_font = QFont()
            self.editor.setFont(default_font)

    def toggle_spellcheck(self, checked):
        if checked:
            self.spellcheck()
        else:
            self.disable_spellcheck()

    def spellcheck(self):
        self.spellchecker = SpellChecker()
        text = self.editor.toPlainText()
        matches = self.spellchecker.check(text)
        for match in matches:
            start = match.offset
            end = match.offset + match.errorLength
            cursor = self.editor.textCursor()
            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
            fmt = cursor.charFormat()
            fmt.setUnderlineColor(Qt.GlobalColor.red)
            fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)
            cursor.setCharFormat(fmt)

    def disable_spellcheck(self):
        text = self.editor.toPlainText()
        cursor = self.editor.textCursor()
        cursor.setPosition(0)
        cursor.setPosition(len(text), QTextCursor.MoveMode.KeepAnchor)
        fmt = cursor.charFormat()
        fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.NoUnderline)
        cursor.setCharFormat(fmt)

    def toggle_spellcheck(self, checked):
        if checked:
            self.spellcheck()
        else:
            self.disable_spellcheck()

    def spellcheck(self):
        if not hasattr(self, "spellchecker"):
            self.spellchecker = SpellChecker()
        text = self.editor.toPlainText()
        matches = self.spellchecker.check(text)
        for match in matches:
            start = match.offset
            end = match.offset + match.errorLength
            cursor = self.editor.textCursor()
            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
            fmt = cursor.charFormat()
            fmt.setUnderlineColor(Qt.GlobalColor.red)
            fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)
            cursor.setCharFormat(fmt)

    def disable_spellcheck(self):
        text = self.editor.toPlainText()
        cursor = self.editor.textCursor()
        cursor.setPosition(0)
        cursor.setPosition(len(text), QTextCursor.MoveMode.KeepAnchor)
        fmt = cursor.charFormat()
        fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.NoUnderline)
        cursor.setCharFormat(fmt)

    def toggle_spellcheck(self, checked):
        if checked:
            self.spellcheck()
        else:
            self.disable_spellcheck()

    def spellcheck(self):
        if not hasattr(self, "spellchecker"):
            self.spellchecker = SpellChecker()
        text = self.editor.toPlainText()
        matches = self.spellchecker.check(text)
        for match in matches:
            start = match.offset
            end = match.offset + match.errorLength
            cursor = self.editor.textCursor()
            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
            fmt = cursor.charFormat()
            fmt.setUnderlineColor(Qt.GlobalColor.red)
            fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)
            cursor.setCharFormat(fmt)

    def disable_spellcheck(self):
        text = self.editor.toPlainText()
        cursor = self.editor.textCursor()
        cursor.setPosition(0)
        cursor.setPosition(len(text), QTextCursor.MoveMode.KeepAnchor)
        fmt = cursor.charFormat()
        fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.NoUnderline)
        cursor.setCharFormat(fmt)

    def toggle_spellcheck(self, checked):
        if checked:
            self.spellcheck()
        else:
            self.disable_spellcheck()

    def spellcheck(self):
        if not hasattr(self, "spellchecker"):
            self.spellchecker = SpellChecker()
        text = self.editor.toPlainText()
        matches = self.spellchecker.check(text)
        for match in matches:
            start = match.offset
            end = match.offset + match.errorLength
            cursor = self.editor.textCursor()
            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
            fmt = cursor.charFormat()
            fmt.setUnderlineColor(Qt.GlobalColor.red)
            fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)
            cursor.setCharFormat(fmt)

    def disable_spellcheck(self):
        text = self.editor.toPlainText()
        cursor = self.editor.textCursor()
        cursor.setPosition(0)
        cursor.setPosition(len(text), QTextCursor.MoveMode.KeepAnchor)
        fmt = cursor.charFormat()
        fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.NoUnderline)
        cursor.setCharFormat(fmt)

    def toggle_spellcheck(self, checked):
        if checked:
            self.spellcheck()
        else:
            self.disable_spellcheck()

    """

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
