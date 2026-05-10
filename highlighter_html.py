from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt6.QtCore import QRegularExpression


class HtmlHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        self.rules = []

        # Tags: <div>, </div>, <br>, <img ...>
        tag_format = QTextCharFormat()
        tag_format.setForeground(QColor("#569CD6"))
        self.rules.append((QRegularExpression(r"</?[a-zA-Z][a-zA-Z0-9:-]*"), tag_format))
        self.rules.append((QRegularExpression(r">"), tag_format))

        # Attributes: class=, id=, href=, src=
        attr_format = QTextCharFormat()
        attr_format.setForeground(QColor("#9CDCFE"))
        self.rules.append((QRegularExpression(r"\b[a-zA-Z_:][a-zA-Z0-9_:.-]*(?=\=)"), attr_format))

        # Attribute values: "..."
        value_format = QTextCharFormat()
        value_format.setForeground(QColor("#CE9178"))
        self.rules.append((QRegularExpression(r"\"[^\"]*\""), value_format))
        self.rules.append((QRegularExpression(r"'[^']*'"), value_format))

        # Comments: <!-- ... -->
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))
        self.comment_format = comment_format

        self.comment_start = QRegularExpression(r"<!--")
        self.comment_end = QRegularExpression(r"-->")

    def highlightBlock(self, text: str):
        # Simple rules
        for pattern, fmt in self.rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                m = it.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), fmt)

        # Multiline comments
        self.setCurrentBlockState(0)

        start = 0
        if self.previousBlockState() != 1:
            m = self.comment_start.match(text)
            start = m.capturedStart() if m.hasMatch() else -1
        else:
            start = 0

        while start >= 0:
            m_end = self.comment_end.match(text, start)
            if m_end.hasMatch():
                end = m_end.capturedEnd()
                length = end - start
                self.setFormat(start, length, self.comment_format)
                start = self.comment_start.match(text, end).capturedStart()
            else:
                self.setFormat(start, len(text) - start, self.comment_format)
                self.setCurrentBlockState(1)
                break


            