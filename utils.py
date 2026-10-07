import hashlib
import re
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QFont
#from PyQt6.QtWidgets import QApplication, QPushButton
import sys



def slugify(text):
    # Unieke maar stabiele ID
    base = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    h = hashlib.md5(text.encode()).hexdigest()[:6]
    return f"{base}-{h}"

def icon_from_text(text: str, size: int = 32) -> QIcon:    
    pixmap = QPixmap(size, size)    
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)    
    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
    font = QFont("Segoe UI Symbol")    
    font.setPixelSize(26)    
    painter.setFont(font)    
    painter.setPen(Qt.GlobalColor.black)
    painter.drawText(        
        QRect(0, 0, size, size),        
        Qt.AlignmentFlag.AlignCenter,        
        text,    
        )    
    
    painter.end()
    return QIcon(pixmap)