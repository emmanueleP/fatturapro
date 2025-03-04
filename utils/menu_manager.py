from PyQt6.QtWidgets import QMenu, QMenuBar
import os

class MenuManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.menu_bar = QMenuBar(main_window)

        self.create_file_menu()
        self.create_services_menu()
        self.create_settings_menu()
        self.create_history_menu()
        self.create_help_menu()

    def create_file_menu(self):
        file_menu = QMenu("File", self.main_window)
        self.menu_bar.addMenu(file_menu)

        # Azioni per il menu File
        open_action = file_menu.addAction("Apri fattura")
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.main_window.open_invoice)

        save_pdf_action = file_menu.addAction("Salva come PDF")
        save_pdf_action.setShortcut("Ctrl+S")
        save_pdf_action.triggered.connect(self.main_window.save_as_pdf)

        print_action = file_menu.addAction("Stampa")
        print_action.setShortcut("Ctrl+P")
        print_action.triggered.connect(self.main_window.print_invoice)

        file_menu.addSeparator()

    def create_services_menu(self):
        services_menu = QMenu("Servizi", self.main_window)
        self.menu_bar.addMenu(services_menu)

    def create_settings_menu(self):
        settings_menu = QMenu("Impostazioni", self.main_window)
        self.menu_bar.addMenu(settings_menu)

        settings_action = settings_menu.addAction("Apri impostazioni")
        settings_action.triggered.connect(self.main_window.show_settings)
    
    def create_history_menu(self):
        self.history_menu = QMenu("Cronologia", self.main_window)
        self.menu_bar.addMenu(self.history_menu)
        
        # Aggiungi azione per pulire la cronologia
        clear_history_action = self.history_menu.addAction("Pulisci cronologia")
        clear_history_action.triggered.connect(self.clear_history)
        self.history_menu.addSeparator()
        
        # Carica e mostra i file recenti
        self.update_recent_files()

    def update_recent_files(self):
        # Rimuovi le vecchie azioni dei file recenti
        for action in self.history_menu.actions()[2:]:  # Salta "Pulisci" e separatore
            self.history_menu.removeAction(action)
            
        # Carica i file recenti dalle impostazioni
        recent_files = self.main_window.settings.value("recent_files", [])
        
        if recent_files:
            for file_path in recent_files:
                action = self.history_menu.addAction(os.path.basename(file_path))
                action.setData(file_path)
                action.triggered.connect(lambda checked, path=file_path: 
                                      self.main_window.open_recent_file(path))
        else:
            no_files_action = self.history_menu.addAction("Nessun file recente")
            no_files_action.setEnabled(False)

    def clear_history(self):
        self.main_window.settings.setValue("recent_files", [])
        self.update_recent_files()

    def create_help_menu(self):
        help_menu = QMenu("Aiuto", self.main_window)
        self.menu_bar.addMenu(help_menu)

        # Azioni per il menu Aiuto
        info_action = help_menu.addAction("Informazioni")
        info_action.triggered.connect(self.main_window.show_info)

        manual_action = help_menu.addAction("Manuale")
        manual_action.triggered.connect(self.main_window.show_manual)

    def get_menu_bar(self):
        return self.menu_bar 
    