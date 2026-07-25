import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLineEdit, QLabel, QScrollArea
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QIcon





class HelpWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help Window")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Edith Help")

        content = """
<h1>Help Content</h1>
<p>This is the help content for the Markdown Editor.</p>
"""

        # Create a central widget and set layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.perform_search)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        # Create a scroll area for the help content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        # Create a web view to display help content
        self.web_view = QWebEngineView()
        self.scroll_area.setWidget(self.web_view)   
        self.load_help_content(content)

        print("Help window initialized")


    def perform_search(self):
        query = self.search_input.text()
        if query:
            # For demonstration, we will just load a local HTML file with the search query.
            # In a real application, you would implement actual search functionality here.
            help_file_path = os.path.join(os.path.dirname(__file__), "help_content.html")
            if os.path.exists(help_file_path):
                self.web_view.load(QUrl.fromLocalFile(help_file_path))
            else:
                self.web_view.setHtml(f"<h1>No help content found for '{query}'</h1>")
        else:
            self.web_view.setHtml("<h1>Please enter a search query.</h1>")

    def load_help_content(self, content):
        self.web_view.setHtml(content)

    def closeEvent(self, event):        
        # Clean up the web view and other resources       
        self.setParent(None)
        self.deleteLater()
        self.web_view = None
        super().closeEvent(event)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HelpWindow()
    window.show()
    sys.exit(app.exec())
