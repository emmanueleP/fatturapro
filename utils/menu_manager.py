from PyQt6.QtWidgets import QMenu, QMenuBar

class MenuManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.menu_bar = QMenuBar(main_window)

        self.create_file_menu()
        self.create_services_menu()
        self.create_settings_menu()
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
    