import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTranslator
from gui.main_window import MainWindow
from utils.theme_manager import ThemeManager

def main():
    app = QApplication(sys.argv)
    
    # Imposta la traduzione italiana
    translator = QTranslator(app)
    if translator.load('qt_it', ':/qt/translations'):
        app.installTranslator(translator)
    
    # Forza la lingua italiana per i dialoghi standard
    app.setProperty('language', 'it')
    
    # Inizializza il gestore del tema
    theme_manager = ThemeManager()
    
    # Crea la finestra principale
    window = MainWindow(theme_manager)
    
    # Se c'è un file passato come argomento, aprilo
    if len(sys.argv) > 1:
        window.load_xml(sys.argv[1])
    
    window.show()
    
    # Applica il tema iniziale
    theme_manager.toggle_theme()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 