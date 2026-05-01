from PyQt6.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt6.QtCore import Qt, QRegularExpression

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document, theme=None):
        super().__init__(document)

        # Theme colors        
        self.theme = theme or {
            'keyword': "#569CD6",
            "operator": "#D4B7A3",
            "brace": "#D4B7A3",
            "defclass": "#4EC9B0",
            'string': "#D4B7A3",
            'comment': "#50A050",
            'number': "#B5CE9A",
        }

        self.rules = []

        # Keyword highlighting


        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif',
            'else', 'except', 'False', 'finally', 'for', 'from', 'global', 'if',
            'import', 'in', 'is', 'lambda', 'None', 'nonlocal', 'not', 'or',
            'pass', 'raise', 'return', 'True', 'try', 'while', 'with', 'yield'
        ]

        keyword_format = self.__fmt(self.theme["keyword"], bold=True)
        for kw in keywords:
            pattern = QRegularExpression(rf"\b{kw}\b")
            self.rules.append((pattern, keyword_format))

        # Strings
        string_format = self.__fmt(self.theme['string'])
        self.rules.append((QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        self.rules.append((QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))

        # Comments
        comment_format = self.__fmt(self.theme['comment'], italic=True)
        self.rules.append((QRegularExpression(r'#.*'), comment_format))

        # Numbers
        number_format = self.__fmt(self.theme['number'])
        self.rules.append((QRegularExpression(r'\b\d+(\.\d+)?\b'), number_format))

        # def and class names
        defclass_format = self.__fmt(self.theme['defclass'], bold=True)
        self.rules.append((QRegularExpression(r'\bdef\s+(\w+)'), defclass_format))
        self.rules.append((QRegularExpression(r'\bclass\s+(\w+)'), defclass_format))

        # Multi-line strings
        self.multi_string_format = string_format
        self.triple_single = QRegularExpression(r"'''")
        self.triple_double = QRegularExpression(r'"""')

    # Helper: create a QTextCharFormat with given color and style
    def __fmt(self, color, bold=False, italic=False):
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        if bold:
            fmt.setFontWeight(QFont.Weight.Bold)
        if italic:
            fmt.setFontItalic(True)
        return fmt
    
    # Main highlighting function
    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

        # Handle multi-line strings
        self.setCurrentBlockState(0)

        in_multiline = self.match_multiline(text, self.triple_single, self.multi_string_format)
        if not in_multiline:
            self.match_multiline(text, self.triple_double, self.multi_string_format)

    def match_multiline(self, text, delimiter, fmt):
        start = 0
        add = 0

        # if inside a multi-line string, start at 0
        if self.previousBlockState() == 1:
            start = 0
            match = delimiter.match(text)
            if match.hasMatch():
                end = match.capturedEnd()
                length = end - start
                self.setFormat(start, length, fmt)
                self.setCurrentBlockState(0)
                return True
            else:
                self.setFormat(start, len(text), fmt)
                return True
            
        # otherwise, look for the start of a multi-line string
        match = delimiter.match(text)
        if match.hasMatch():
            start = match.capturedStart()
            match2 = delimiter.match(text, match.capturedEnd())
            if match2.hasMatch():
                end = match2.capturedEnd()
                length = end - start
                self.setFormat(start, length, fmt)
            else:
                self.setFormat(start, len(text) - start, fmt)
                self.setCurrentBlockState(1)
            return True
        return False
    