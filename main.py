import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow
from utils.theme_manager import ThemeManager

def main():
    app = QApplication(sys.argv)
    
    # Inizializza il gestore del tema
    theme_manager = ThemeManager()
    
    # Crea e mostra la finestra principale passando il theme_manager
    window = MainWindow(theme_manager)
    window.show()
    
    # Applica il tema iniziale
    theme_manager.toggle_theme()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 