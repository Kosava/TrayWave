#!/usr/bin/env python3
"""
TrayWave - System tray radio player
"""
import sys
from PyQt6.QtWidgets import QApplication
from traywave.ui.tray import TrayWave

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("TrayWave")
    app.setQuitOnLastWindowClosed(False)
    
    tray = TrayWave()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()