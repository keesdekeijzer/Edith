from PyQt6.QtWidgets import QFormLayout, QLabel, QLineEdit, QMainWindow

class FrontmatterWindow(QMainWindow):
    def __init__(self, fm=None):
        super().__init__()
        self.fm = fm
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Frontmatter Window")
        self.setGeometry(100, 100, 800, 600)
        # Additional UI setup can be done here
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        for key, value in self.fm.items():
            field = QLineEdit(str(value))
            #field.editingFinished.connect(self._emit_change)
            self.fields[key] = field
            self.layout.addRow(QLabel(key), field)