from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QLabel
import yaml
import re

class FrontmatterPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QFormLayout
        self.fields = {}
        self.current_data = {}

    def load_frontmatter(self, text):
        """Extract YAML frontmatter and populate fields."""
        match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
        if not match:
            #self.clear_panel()
            return
        
        yaml_text = match.group(1)
        try:
            data = yaml.safe_load(yaml_text) or {}
        except Exception:
            self.clear_panel()
            return
        
    def _populate_fields(self, data):
        # Clear old fields
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.fields = {}

        for key, value in data.items():
            field = QLineEdit(str(value))
            field.editingFinished.connect(self._emit_change)
            self.fields[key] = field
            self.layout.addRow(QLabel(key), field)

    def _emit_change(self):
        """Called when a field is edited"""
        updated = {k: f.next() for k, f in self.fields.items()}
        self.parent().update_frontmatter_from_panel(updated)

    def clear_panel(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.fields = {}
        self.current_data = {}
