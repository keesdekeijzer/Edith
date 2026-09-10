from PyQt6.QtWidgets import QFormLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QWidget, QDialog

class FrontmatterWindow(QDialog):
    def __init__(self, fm=None):
        super().__init__()
        self.fm = fm
        self.fields = {}
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle("Frontmatter Window")
        self.setGeometry(100, 100, 800, 600)
        # Additional UI setup can be done here
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        for key, value in self.fm.items():
            #print(f"Adding field for key: {key}, value: {value}")
            field = QLineEdit(str(value))
            field.editingFinished.connect(self._emit_change)
            self.fields[key] = field
            self.layout.addRow(QLabel(key), field)

        self.label = QLabel("Save and Close:")
        self.knop = QPushButton("OK")
        self.knop.clicked.connect(self.ok)
        self.layout.addRow(self.label, self.knop)

        #print("FrontmatterWindow initialized with fields:", self.fields)   
        self.print_gegevens() 

    def get_form_data(self):
        """Return the current data from the form fields."""
        return {key: field.text() for key, field in self.fields.items()}

    def _emit_change(self):
        """Called when a field is edited"""
        updated = {k: f.text() for k, f in self.fields.items()}
        #print("Form data updated:", updated)
        # Here you would typically emit a signal or call a method to update the frontmatter in the main application

    def haal_gegevens(self):
        """Retrieve the current data from the form fields."""
        #print("Retrieving form data...")
        return self.get_form_data()

    def print_gegevens(self):
        """Print the current data from the form fields."""
        #print("Current form data:", self.get_form_data())
        #print("FrontmatterWindow class defined with methods: initUI and get_form_data")
        gegevens = self.haal_gegevens()
        #print("Retrieved form data:", gegevens)

    def ok(self):
        """Handle the OK button click."""
        #print("OK button clicked. Current form data:", self.get_form_data())
        self.resultaat = self.get_form_data()  # Store the current form data
        self.accept()  # Close the dialog and return QDialog.Accepted
