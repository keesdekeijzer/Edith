from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QPlainTextEdit, QTextEdit
import sys
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QPainter, QColor, QPen, QTextFormat, QFont
from line_numbers import LineNumberArea
from highlighter_python import PythonHighlighter
from themes import LIGHT_THEME, DARK_THEME
from PyQt6.QtGui import QTextCursor, QKeyEvent
from PyQt6.QtCore import Qt

class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighter = PythonHighlighter(self.document())

        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(' '))

    def lineNumberAreaWidth(self):
        digits = len(str(max(1, self.blockCount())))
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        return space
    
    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor(240, 240, 240))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.GlobalColor.black)
                painter.drawText(0, top, self.lineNumberArea.width(), self.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def highlightCurrentLine(self):
        if self.isReadOnly():
            return
        
        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(QColor(232, 232, 255))
        selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()

        self.setExtraSelections([selection])

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        cursor = self.textCursor()

        # Enter > kopieer indent + auto-indent na:
        if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            cursor.beginEditBlock()

            # Huidige regeltekst
            cursor.select(QTextCursor.SelectionType.LineUnderCursor)
            line_text = cursor.selectedText()


            # Bepaal inspringing van de huidige regel
            indent = ""
            for char in line_text:
                if char in (' ', '\t'):
                    indent += char
                else:
                    break


            # Extra inspringing voor bepaalde tekens
            extra = ""
            stripped = line_text.strip()
            if stripped.endswith(':'):
                extra = " " * 4  # Voeg 4 spaties toe na een dubbele punt


            # Normale enter-toets functionaliteit

            # verplaats cursor naar nieuwe regel
            cursor = self.textCursor()
            # verplaats naar einde van huidige regel
            cursor.movePosition(QTextCursor.MoveOperation.EndOfLine)
            # vervolgens naar volgende regel
            cursor.movePosition(QTextCursor.MoveOperation.NextBlock)
            self.setTextCursor(cursor)

            super().keyPressEvent(event)

            # Voeg de inspringing toe aan de nieuwe regel
            cursor.insertText(indent + extra)
            cursor.endEditBlock()
            return
        
        # TAB + indent selectie of cursor
        if key == Qt.Key.Key_Tab:
            cursor.beginEditBlock()
            if cursor.hasSelection():
                self._indent_selection(cursor)
            else:
                # Voeg inspringing toe aan geselecteerde tekst
                cursor.insertText(" " * 4)
            cursor.endEditBlock()
            return
        
        # Shift+TAB > unindent selectie of cursor
        if key == Qt.Key.Key_Backtab:
            cursor.beginEditBlock()
            self._unindent_selection(cursor)
            cursor.endEditBlock()
            return
        
        # Backspace + slimme unindent
        if key == Qt.Key.Key_Backspace:
            if self._handle_smart_backspace(cursor):
                return
        
        # auto-closing voor haakjes, aanhalingstekens, etc.
        pairs = {
            "(": ")",
            "[": "]",
            "{": "}",
            "\"": "\"",
            "'": "'"
        }

        text = event.text()

        # 1. Als gebruiker een openings-teken typt
        if text in pairs:
            closing = pairs[text]

            cursor = self.textCursor()

            # Als er een selectie is, omring de selectie met het paar
            if cursor.hasSelection():
                selected = cursor.selectedText()
                cursor.insertText(text + selected + closing)
                return
            
            # Als volgende karakter al de closing is, beweeg dan eroverheen in plaats van een nieuw paar toe te voegen
            next_char = self._char_right_of_cursor(cursor)
            if next_char == closing:
                cursor.movePosition(QTextCursor.MoveOperation.Right)
                self.setTextCursor(cursor)
                return
            
            # Normaal gedrag: voeg het openings-teken toe en het bijbehorende sluit-teken
            cursor.insertText(text + closing)
            cursor.movePosition(QTextCursor.MoveOperation.Left)
            self.setTextCursor(cursor)
            return
        
        # 2. Slimme backspace voor haakjes en aanhalingstekens
        if key == Qt.Key.Key_Backspace:
            cursor = self.textCursor()
            left = self._char_left_of_cursor(cursor)
            right = self._char_right_of_cursor(cursor)

            if left in pairs and pairs[left] == right:
                cursor.deletePreviousChar()  # Verwijder het linker-teken
                cursor.deleteChar()          # Verwijder het rechter-teken
                return

    

        # Default gedrag voor andere toetsen
        super().keyPressEvent(event)

    def _indent_selection(self, cursor):
        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.setPosition(start)
        cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)

        while cursor.position() <= end:
            cursor.insertText(" " * 4)
            cursor.movePosition(QTextCursor.MoveOperation.Down)
            cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
            end += 4  # Verhoog eindpositie vanwege toegevoegde spaties ###

    def _unindent_selection(self, cursor):
        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.setPosition(start)
        cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)

        while cursor.position() <= end:
            cursor.select(QTextCursor.SelectionType.LineUnderCursor)
            line = cursor.selectedText()

            if line.startswith(" " * 4):
                cursor.removeSelectedText()
                cursor.insertText(line[4:])  # Verwijder de eerste 4 spaties
            elif line.startswith("\t"):
                cursor.removeSelectedText()
                cursor.insertText(line[1:])  # Verwijder de eerste tab
           
            cursor.movePosition(QTextCursor.MoveOperation.Down)
            cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)

    def _handle_smart_backspace(self, cursor):
        # Controleer of de cursor zich in de inspringing bevindt
        cursor_pos = cursor.positionInBlock()
        block_text = cursor.block().text()

        # alleen Whitespace vóór de cursor
        if block_text[:cursor_pos].strip() == "":
            # Verwijder 4 spaties tegeijk
            remove = min(4, cursor_pos)
            for _ in range(remove):
                cursor.deletePreviousChar()
            return True
        return False
    
    def _char_left_of_cursor(self, cursor):
        pos = cursor.positionInBlock()
        if pos == 0:
            return ""
        block = cursor.block().text()
        return block[pos - 1]
    
    def _char_right_of_cursor(self, cursor):
        block = cursor.block().text()
        pos = cursor.positionInBlock()
        if pos >= len(block):
            return ""
        return block[pos]

class Window(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.editor = CodeEditor()
        layout.addWidget(self.editor)
        self.setWindowTitle("Code Editor with Line Numbers")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
