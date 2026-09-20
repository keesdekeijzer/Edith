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
            QMenuBar::item:selected {
                background: #444;
            }
        """
