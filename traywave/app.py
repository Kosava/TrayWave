from traywave.ui.tray import TrayWave
from PyQt6.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    tray = TrayWave()
    tray.show()
    sys.exit(app.exec())
