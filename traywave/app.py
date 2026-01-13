# app.py - PROMENJEN IMPORT
import sys
from PyQt6.QtWidgets import QApplication
from ui.tray import TrayWave


def main():
    app = QApplication(sys.argv)
    tray = TrayWave()
    tray.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()