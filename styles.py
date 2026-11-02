# styles

toolbar_style = """
QToolBar {
    background: transparent;              /* let palette/theme show through */
    border: none;
    spacing: 6px;
}
QToolButton {
    background-color: lightblue;
    border: solid 1px silver;
    padding: 6px;
    color: black;
}
QToolButton:hover {
    background-color: rgba(120, 120, 120, 40);
}
QToolButton:checked {
    background-color: rgba(120, 120, 120, 70);
}
"""

menuBar_style = """
            QMenuBar {
                background: #2b2b2b;
                color: #e6e6e6;
                border-bottom: 1px solid #444;
                padding: 5px;
            }
            QMenuBar::item {
                padding: 5px 10px;
                border: 1px solid transparent;
            }

            QMenuBar::item:hover {
                background-color: #3a3a3a;
                color: white;
            }

            QMenuBar::item:selected {
                background-color: #3a3a3a;
                color: white;
            }
        """

zoekveld_style = """
QLineEdit {
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 4px 8px;
}
QLineEdit:focus {
    border-color: #66afe9;
    outline: none;
}
"""

dark_mode_style = """
QWidget {
    background-color: #2b2b2b;
    color: #e6e6e6;
}
QPushButton {
    background-color: #444;
    color: #e6e6e6;
    border: 1px solid #555;
    padding: 5px 10px;
}
QPushButton:hover {
    background-color: #555;
}
QPushButton:pressed {
    background-color: #666;
}
QLineEdit {
    background-color: #3a3a3a;
    color: #e6e6e6;
    border: 1px solid #555;
    padding: 4px 8px;
}
QLineEdit:focus {
    border-color: #66afe9;
    outline: none;
}
QMenuBar {
    background-color: #2b2b2b;
    color: #e6e6e6;
    border-bottom: 1px solid #444;
}
QMenuBar::item {
    padding: 5px 10px;
    border: 1px solid transparent;
}
QMenuBar::item:hover {
    background-color: #3a3a3a;
    color: white;
}
QMenuBar::item:selected {
    background-color: #3a3a3a;
    color: white;
}
QMenu {
    background-color: #2b2b2b;
    color: #e6e6e6;
    border: 1px solid #444;
}
QMenu::item {
    padding: 5px 10px;
}
QMenu::item:selected {
    background-color: #3a3a3a;
    color: white;
}
QToolBar {
    background-color: #2b2b2b;
    border: none;
    spacing: 6px;
}
QToolButton {
    background-color: #444;
    color: #e6e6e6;
    border: solid 1px #555;
    padding: 6px;
}
QToolButton:hover {
    background-color: #555;
}
QToolButton:checked {
    background-color: #666;
}
QStatusBar {
    background-color: #2b2b2b;
    color: #e6e6e6;
    border-top: 1px solid #444;
}
QStatusBar QLabel {
    color: #e6e6e6;
}
"""

blue_mode_style = """
background-color: #0000AA;
color: #FFFFFF;
QWidget{
    background-color: #0000AA;
    color: #FFFFFF;
    }
QPlainTextEdit{  
    background-color: #000BFF;
    color: #FFFFFF;
    }
QMenuBar{
    background-color: #0000AA;
    color: #FFFFFF;
}
QMenu{
    background-color: #0000AA;
    color: #FFFFFF;
}
QStatusBar{
    background-color: #0000AA;
    color: #FFFFFF;
}
QToolBar{
    background-color: #0000AA;
    color: #FFFFFF;
}
QToolBar QToolButton{
    background-color: #0000AA;
    color: #FFFFFF;
}
QToolbar QToolButton:hover{
    background-color: #000BFF;
    color: #FFFFFF;
}
QToolBar QToolButton:checked{
    background-color: #000BFF;
    color: #FFFFFF;
}
QToolBar QToolButton:pressed{
    background-color: #000BFF;
    color: #FFFFFF;
}
QToolBar QToolButton:focus{
    background-color: #000BFF;
    color: #FFFFFF;
}
QLabel{
    background-color: #0000AA;
    color: #FFFFFF;
}
QPushButton{
    background-color: #0000AA;
    color: #FFFFFF;
}
QLineEdit{
    background-color: #0000AA;
    color: #FFFFFF;
}
QCheckBox{
    background-color: #0000AA;
    color: #FFFFFF;
}
QScrollBar{
    background-color: #0000AA;
    color: #FFFFFF;
}
QHeaderView::section{
    background-color: #0000AA;
    color: #FFFFFF;
}
QTreeView{
    background-color: #0000AA;
    color: #FFFFFF;
}
QTableView{
    background-color: #0000AA;
    color: #FFFFFF;
}
QTabWidget::pane{
    background-color: #0000AA;
    color: #FFFFFF;
}
QTabBar::tab{
    background-color: #0000AA;
    color: #FFFFFF;
}
QTabBar::tab:selected{
    background-color: #000BFF;
    color: #FFFFFF;
}
QScrollBar::handle{
    background-color: #000BFF;
    color: #FFFFFF;
}
QScrollBar::add-line, QScrollBar::sub-line{
    background-color: #0000AA;
    color: #FFFFFF;
}
QScrollBar::add-page, QScrollBar::sub-page{
    background-color: #0000AA;
    color: #FFFFFF;
}
QMenuBar::item:selected{
    background-color: #000BFF;
    color: #FFFFFF;
}
QMenu::item:selected{
    background-color: #000BFF;
    color: #FFFFFF;
}
QStatusBar::item:selected{
    background-color: #000BFF;
    color: #FFFFFF;
}
QLabel::item:selected{
    background-color: #000BFF;
    color: #FFFFFF;
}
QPushButton::item:selected{
    background-color: #000BFF;
    color: #FFFFFF;
}
QLineEdit::item:selected{
    background-color: #000BFF;
    color: #FFFFFF;
}
QCheckBox::item:selected{
    background-color: #000BFF;
    color: #FFFFFF;
}
QScrollBar::handle:selected{
    background-color: #000BFF;
    color: #FFFFFF;
}
"""