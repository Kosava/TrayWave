#!/usr/bin/env python3
"""
TrayWave - Main application entry point
"""
import sys
import os

# CRITICAL: Force Qt to use its own rendering instead of native menus
# This MUST be set BEFORE importing PyQt6
os.environ['QT_QPA_PLATFORMTHEME'] = ''
os.environ['QT_STYLE_OVERRIDE'] = 'Fusion'

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# FIXED: Use absolute imports from traywave package
from traywave.ui.tray_main import TrayWave


def main():
    """Main application entry point"""
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Force Qt style instead of native platform menus
    app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar, True)
    app.setQuitOnLastWindowClosed(False)
    
    # Create and show tray icon
    try:
        tray = TrayWave()
        print("✅ TrayWave started successfully!")
    except Exception as e:
        print(f"ERROR: Failed to create TrayWave: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()