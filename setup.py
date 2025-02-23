from setuptools import setup

APP = ['main.py']
DATA_FILES = [
    ('assets', ['assets/main.png']),
    ('utils', ['utils/invoice_parser.py', 'utils/p7m_handler.py', 'utils/theme_manager.py']),
    ('gui', ['gui/main_window.py', 'gui/info_dialog.py', 'gui/settings_dialog.py']),
    ('bin', ['bin/wkhtmltopdf'])
]
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'assets/icona.icns',
    'plist': {
        'CFBundleName': 'FatturaPro',
        'CFBundleDisplayName': 'FatturaPro',
        'CFBundleGetInfoString': "Visualizzatore Fatture Elettroniche",
        'CFBundleIdentifier': "com.emmanuele.fatturapro",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': "© 2025 Emmanuele Pani",
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': "13.0.0",
        'LSApplicationCategoryType': 'public.app-category.business',
        'PyRuntimeLocations': ['/Library/Frameworks/Python.framework/Versions/3.12/bin/python3']
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 