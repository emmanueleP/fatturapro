from PyQt6.QtWidgets import QApplication

class ThemeManager:
    def __init__(self):
        self.dark_mode = False
        self.dark_stylesheet = """
            QMainWindow, QWidget, QDialog {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QPushButton {
                background-color: #404040;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QMenuBar {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QMenuBar::item:selected {
                background-color: #404040;
            }
            QMenu {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #555555;
            }
            QMenu::item:selected {
                background-color: #404040;
            }
            QTextBrowser {
                background-color: #363636;
                color: #ffffff;
                border: 1px solid #555555;
            }
            /* Il viewer della fattura mantiene sempre lo sfondo bianco */
            QMainWindow QTextEdit {
                background-color: white;
                color: black;
            }
        """
        
        self.light_stylesheet = """
            QMainWindow, QWidget, QDialog {
                background-color: #ffffff;
                color: #000000;
            }
            QPushButton {
                background-color: #f0f0f0;
                color: #000000;
                border: 1px solid #cccccc;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QMenuBar {
                background-color: #f0f0f0;
            }
            QMenuBar::item:selected {
                background-color: #e0e0e0;
            }
            QMenu {
                background-color: #ffffff;
                border: 1px solid #cccccc;
            }
            QMenu::item:selected {
                background-color: #e0e0e0;
            }
            QTextBrowser {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #cccccc;
            }
            /* Il viewer della fattura mantiene sempre lo sfondo bianco */
            QMainWindow QTextEdit {
                background-color: white;
                color: black;
            }
        """
        
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        QApplication.instance().setStyleSheet(
            self.dark_stylesheet if self.dark_mode else self.light_stylesheet
        ) 