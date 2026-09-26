from PyQt6.QtWidgets import QFormLayout, QVBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QWidget, QDialog

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
        self.form_layout = QFormLayout()
        #self.setLayout(self.layout)

        for key, value in self.fm.items():
            #print(f"Adding field for key: {key}, value: {value}")
            field = QLineEdit(str(value))
            field.editingFinished.connect(self._emit_change)
            self.fields[key] = field
            self.form_layout.addRow(QLabel(key), field)

        self.button_layout = QVBoxLayout()
        #button_layout.addWidget(QPushButton("Submit"))
        #button_layout.addWidget(QPushButton("Cancel"))

        self.label2 = QLabel("")
        self.knop2 = QPushButton("Change ID (Ctrl+S)")
        self.knop2.setShortcut("Ctrl+S")
        self.knop2.clicked.connect(self.change_ok)
        #self.button_layout.addRow(self.label2, self.knop2)
        self.button_layout.addWidget(self.knop2)

        self.label3 = QLabel("")
        self.knop3 = QPushButton("Add Subtitle (Alt+S)")
        self.knop3.setShortcut("Alt+S")
        self.knop3.clicked.connect(self.add_subtitle)
        #self.button_layout.addRow(self.label3, self.knop3)
        self.button_layout.addWidget(self.knop3)

        self.label = QLabel("Save and Close:")
        self.knop = QPushButton("OK")
        self.knop.clicked.connect(self.ok)
        #self.button_layout.addRow(self.label, self.knop)
        self.button_layout.addWidget(self.knop)

        self.knop.setStyleSheet("""    
                QPushButton {        
                background-color: #3498db;        
                color: white;        
                border: none;        
                border-radius: 6px;        
                padding: 8px 16px;    }
                QPushButton:hover {        
                background-color: #2980b9;    }
                QPushButton:pressed {        
                background-color: #1f618d;    }
                """)

        self.knop2.setStyleSheet("""    
                QPushButton {        
                background-color: #3498db;        
                color: white;        
                border: none;        
                border-radius: 6px;        
                padding: 8px 16px;    }
                QPushButton:hover {        
                background-color: #2980b9;    }
                QPushButton:pressed {        
                background-color: #1f618d;    }
                """)

        self.knop3.setStyleSheet("""    
                QPushButton {        
                background-color: #3498db;        
                color: white;        
                border: none;        
                border-radius: 6px;        
                padding: 8px 16px;    }
                QPushButton:hover {        
                background-color: #2980b9;    }
                QPushButton:pressed {        
                background-color: #1f618d;    }
                """)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

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

    def change_ok(self):
        """Handle the Change ID button click."""
        self.fields['author'].setText(self.fields['author'].text().strip().replace(".", " ").replace(":", " ").replace(";", " ").replace("/", "_"))  # Ensure no leading/trailing whitespace
        self.fields['title'].setText(self.fields['title'].text().strip().replace(".", " ").replace(":", " - ").replace(";", " ").replace("/", "_"))
        new_id = self.fields['author'].text() + "_" + self.fields['title'].text()
        new_id = new_id.replace("/", "_")
        self.fields['identifier'].setText(new_id)  # Change the identifier field to a new value
        self.resultaat = self.get_form_data()  # Store the current form data
        self.accept()  # Close the dialog and return QDialog.Accepted

    def add_subtitle(self):
        #print("fields:", self.fields)
        self.fields['subtitle'] = QLineEdit(str(""))
        self.form_layout.addRow(QLabel('subtitle'), QLineEdit(str("")))
        self.resultaat = self.get_form_data()
        self.accept()
