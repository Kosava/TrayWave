#!/usr/bin/env python3
"""
TrayWave launcher - Corrected for actual structure
"""
import sys
import os

# CRITICAL: Force Qt to use its own rendering instead of native menus
# This MUST be set BEFORE importing PyQt6
os.environ['QT_QPA_PLATFORMTHEME'] = ''
os.environ['QT_STYLE_OVERRIDE'] = 'Fusion'

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

def main():
    """Main application entry point"""
    # Import TrayWave from actual location: traywave/ui/tray_main.py
    try:
        from traywave.ui.tray_main import TrayWave
    except ModuleNotFoundError as e:
        print(f"ERROR: Cannot import TrayWave: {e}")
        print(f"\nCurrent directory: {os.getcwd()}")
        print(f"Project root: {project_root}")
        print(f"\nPython path:")
        for p in sys.path:
            print(f"  - {p}")
        
        # Check if files exist
        tray_main_path = os.path.join(project_root, "traywave", "ui", "tray_main.py")
        print(f"\nChecking for tray_main.py at: {tray_main_path}")
        print(f"Exists: {os.path.exists(tray_main_path)}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR during import: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
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