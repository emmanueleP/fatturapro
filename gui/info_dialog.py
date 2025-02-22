from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QTextBrowser, 
                           QPushButton, QDialogButtonBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class InfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Informazioni")
        self.setMinimumSize(500, 400)
        
        # Layout principale
        layout = QVBoxLayout(self)
        layout.setSpacing(20)  # Spaziatura macOS-style
        layout.setContentsMargins(20, 20, 20, 20)  # Margini macOS-style
        
        info_text = """
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial;
                line-height: 1.5;
                color: #333333;
            }
            h2 {
                font-size: 20px;
                font-weight: 500;
                margin-bottom: 15px;
                color: #000000;
            }
            h3 {
                font-size: 16px;
                font-weight: 500;
                margin-top: 20px;
                margin-bottom: 10px;
                color: #000000;
            }
            p {
                margin: 10px 0;
            }
            ul {
                margin: 10px 0;
                padding-left: 20px;
            }
            li {
                margin: 5px 0;
            }
            a {
                color: #0066cc;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
        <h2>FatturaPro - Visualizzatore Fatture Elettroniche</h2>
        <p>Un'applicazione per visualizzare, convertire in PDF e stampare fatture elettroniche in formato XML e P7M.</p>
        
        <h3>Funzionalità:</h3>
        <ul>
            <li>Apertura e visualizzazione di fatture elettroniche (XML, P7M)</li>
            <li>Conversione in PDF</li>
            <li>Stampa dei documenti</li>
            <li>Visualizzazione informazioni firma digitale per file P7M</li>
        </ul>
        
        <h3>Requisiti:</h3>
        <ul>
        Richiede macOS 13 o superiore con Apple Silicon.
        </ul>
        
        <h3>Repository GitHub:</h3>
        <p><a href="https://github.com/emmanueleP/fatturapro">https://github.com/emmanueleP/fatturapro</a></p>
        
        <h3>Copyright:</h3>
        <p>© 2025 Emmanuele Pani.</p>
        """
        
        # Browser con stile macOS
        info_browser = QTextBrowser()
        info_browser.setHtml(info_text)
        info_browser.setOpenExternalLinks(True)
        info_browser.setStyleSheet("""
            QTextBrowser {
                border: 1px solid #cccccc;
                border-radius: 8px;
                background-color: white;
                padding: 10px;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 14px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #a1a1a1;
                min-height: 30px;
                border-radius: 7px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #7d7d7d;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        
        # Pulsanti stile macOS
        button_box = QDialogButtonBox()
        close_button = QPushButton("Chiudi")
        close_button.setDefault(True)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 20px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #0069D9;
            }
            QPushButton:pressed {
                background-color: #0051A8;
            }
        """)
        button_box.addButton(close_button, QDialogButtonBox.ButtonRole.AcceptRole)
        button_box.accepted.connect(self.accept)
        
        # Aggiungi i widget al layout
        layout.addWidget(info_browser)
        layout.addWidget(button_box, alignment=Qt.AlignmentFlag.AlignRight) 