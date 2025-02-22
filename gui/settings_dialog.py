from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QGroupBox)
from PyQt6.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, theme_manager, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Impostazioni")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Gruppo Tema
        theme_group = QGroupBox("Tema Applicazione")
        theme_layout = QHBoxLayout()
        
        theme_label = QLabel("Tema:")
        self.theme_button = QPushButton(
            "Tema Scuro" if self.theme_manager.dark_mode else "Tema Chiaro"
        )
        self.theme_button.clicked.connect(self.toggle_theme)
        self.theme_button.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                background-color: #4a90e2;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_button)
        theme_group.setLayout(theme_layout)
        
        # Pulsante Chiudi
        close_button = QPushButton("Chiudi")
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                background-color: #e0e0e0;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        
        layout.addWidget(theme_group)
        layout.addStretch()
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight)
        
    def toggle_theme(self):
        self.theme_manager.toggle_theme()
        self.theme_button.setText(
            "Tema Scuro" if self.theme_manager.dark_mode else "Tema Chiaro"
        ) 