# traywave/__main__.py
import sys
import os

# Dodaj trenutni folder u Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication

def main():
    # Import tek kada je sve spremno
    from ui.tray import TrayWave
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    tray = TrayWave()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()