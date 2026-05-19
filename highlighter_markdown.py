from PyQt6.QtCore import QRegularExpression, QRegularExpression, Qt
from PyQt6.QtGui import QFont, QSyntaxHighlighter, QTextCursor, QTextCharFormat, QColor, QTextCharFormat
#from markdown_editor2 import SpellChecker
#import language_tool_python

class MarkdownHighlighter(QSyntaxHighlighter):
    def __init__(self, document, theme=None):
        super().__init__(document)

        self.theme = theme or {
            'heading': QColor('#ff6347'),  # Tomato
            'bold': QColor('#1e90ff'),    # DodgerBlue
            'italic': QColor('#32cd32'),  # LimeGreen
            'strike': QColor('#8b0000'),  # DarkRed
            'code': QColor('#ffa500'),    # Orange
            'link_text': QColor('#0000ff'),  # Blue
            'link_url': QColor('#0000cd'),   # MediumBlue
            'frontmatter': QColor('#800080'),  # Purple
        }

        
        #self.spell_format = QTextCharFormat()
        #self.spell_format.setUnderlineColor(QColor("#ff5555"))
        #self.spell_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)

        self.rules = []

        # Headings
        heading_format = self._fmt(self.theme['heading'], bold=True)
        self.rules.append((QRegularExpression(r'^(#{1,6} .+)$'), heading_format))

        # Bold
        bold_format = self._fmt(self.theme['bold'], bold=True)
        self.rules.append((QRegularExpression(r'(\*\*(.*?)\*\*)'), bold_format))
        self.rules.append((QRegularExpression(r'__(.*?)__'), bold_format))

        # Italic
        italic_format = self._fmt(self.theme['italic'], italic=True)
        self.rules.append((QRegularExpression(r'(\*(.*?)\*)'), italic_format))
        self.rules.append((QRegularExpression(r'_(.*?)_'), italic_format))

        # Strikethrough
        strike_format = self._fmt(self.theme['strike'], strike=True)
        self.rules.append((QRegularExpression(r'(~~(.*?)~~)'), strike_format))

        # Inline code
        code_format = self._fmt(self.theme['code'], italic=True)
        self.rules.append((QRegularExpression(r'(`(.*?)`)'), code_format))

        # Links        
        link_text_format = self._fmt(self.theme['link_text'], underline=True)
        link_url_format = self._fmt(self.theme['link_url'], underline=True)
        self.rules.append((QRegularExpression(r'(\[(.*?)\]\((.*?)\))'), link_url_format))
        self.rules.append((QRegularExpression(r'(\[(.*?)\])'), link_text_format))

        # Frontmatter
        frontmatter_format = self._fmt(self.theme['frontmatter'], italic=True)
        self.in_frontmatter = False

        # Lists
        list_format = self._fmt(self.theme['heading'], italic=True)
        self.rules.append((QRegularExpression(r'^(\s*[-*+] .+)$'), list_format))
        self.rules.append((QRegularExpression(r'^(\s*\d+\. .+)$'), list_format))

    def _fmt(self, color, bold=False, italic=False, underline=False, strike=False):
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        if bold:
            fmt.setFontWeight(QFont.Weight.Bold)
        #fmt.setFontWeight(QTextCharFormat.fontWeight.Bold if bold else QTextCharFormat.fontWeight.Normal)
        fmt.setFontItalic(italic)
        fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SingleUnderline if underline else QTextCharFormat.UnderlineStyle.NoUnderline)
        fmt.setFontStrikeOut(strike)
        return fmt
    
    def highlightBlock(self, text):
        #spellchecker = SpellChecker()
        #super().highlightBlock(text)
        #print("2")
        
        #errors = spellchecker.check(text)
        #print("errors:", errors)
        
        #for err in errors:
            #start = err.offset
            #length = err.errorLength
            #length = err.error_length
            #self.setFormat(start, length, self.spell_format)

        # Frontmatter handling
        if text.strip() == '---':
            self.in_frontmatter = not self.in_frontmatter
            self.setFormat(0, len(text), self._fmt(self.theme['frontmatter']))
            return
        if self.in_frontmatter:
            self.setFormat(0, len(text), self._fmt(self.theme['frontmatter']))
            return

        # Normale regels
        for pattern, fmt in self.rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                match = it.next()
                start, length = match.capturedStart(1), match.capturedLength(1)
                self.setFormat(start, length, fmt)


