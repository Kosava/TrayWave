#!/usr/bin/env python3
"""
Run TrayWave directly from source
"""
import os
import sys

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print(f"🚀 Starting TrayWave from source...")
print(f"📁 Project root: {project_root}")

# Check for required packages
try:
    from PyQt6.QtWidgets import QApplication
    print("✓ PyQt6 is available")
except ImportError as e:
    print(f"❌ PyQt6 is not installed: {e}")
    print("Install it with: pip install PyQt6")
    sys.exit(1)

# Check if icons exist
icons_dir = os.path.join(project_root, "resources", "icons")
if not os.path.exists(icons_dir):
    print(f"⚠️ Icons directory not found: {icons_dir}")
    print("Creating icons directory...")
    os.makedirs(icons_dir, exist_ok=True)

# Check for icons
required_icons = ["traywave-playing.png", "traywave-stopped.png", "traywave-muted.png"]
missing_icons = []
for icon in required_icons:
    icon_path = os.path.join(icons_dir, icon)
    if not os.path.exists(icon_path):
        missing_icons.append(icon)

if missing_icons:
    print(f"⚠️ Missing icons: {missing_icons}")
    print("To create icons, run: python create_icons.py")
    print("⚠️ Continuing with fallback icons...")

try:
    from traywave.__main__ import main
    print("✓ TrayWave imported successfully")
    print("\n" + "="*50)
    print("Starting TrayWave...")
    print("="*50 + "\n")
    main()
except Exception as e:
    print(f"❌ Error starting TrayWave: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)