"""
Main tray icon and application with modern styled menu
"""
import os
import json
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication, QWidgetAction, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QIcon, QCursor, QFont
from PyQt6.QtCore import Qt, QTimer, QPoint
from ..core.engine import AudioEngine
from ..core.stations import StationsManager
from ..ui.popups import VolumePopup
from ..ui.dialogs import StyleSettingsDialog
from ..utils.geometry import is_mouse_in_tray_area

class MenuStyles:
    """Style definitions for the tray menu"""
    
    STYLES = {
        'teal': {
            'name': '🌊 Teal',
            'css': """
                QMenu {
                    background-color: rgba(255, 255, 255, 0.98);
                    border-radius: 14px;
                    padding: 10px;
                    border: 1px solid rgba(6, 182, 212, 0.2);
                }
                QMenu::item {
                    padding: 10px 16px;
                    border-radius: 8px;
                    color: #0f172a;
                    font-size: 13px;
                    margin: 2px 0px;
                }
                QMenu::item:selected {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(6, 182, 212, 0.1),
                        stop:1 rgba(8, 145, 178, 0.15));
                }
                QMenu::separator {
                    height: 1px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 transparent,
                        stop:0.5 rgba(6, 182, 212, 0.3),
                        stop:1 transparent);
                    margin: 10px 0px;
                }
            """,
            'header_css': """
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #06b6d4,
                        stop:1 #0891b2);
                    border-radius: 10px;
                    padding: 14px 16px;
                }
                QLabel {
                    color: white;
                    background: transparent;
                }
            """
        },
        'macos': {
            'name': '🍎 macOS',
            'css': """
                QMenu {
                    background-color: rgba(255, 255, 255, 0.95);
                    border-radius: 12px;
                    padding: 8px;
                    border: 1px solid rgba(0, 0, 0, 0.1);
                }
                QMenu::item {
                    padding: 8px 16px;
                    border-radius: 6px;
                    color: #1d1d1f;
                    font-size: 13px;
                    margin: 2px 0px;
                }
                QMenu::item:selected {
                    background-color: rgba(0, 0, 0, 0.06);
                }
                QMenu::separator {
                    height: 1px;
                    background-color: rgba(0, 0, 0, 0.08);
                    margin: 8px 0px;
                }
            """,
            'header_css': """
                QWidget {
                    background-color: transparent;
                    border-bottom: 1px solid rgba(0, 0, 0, 0.08);
                    padding: 12px 16px;
                }
                QLabel {
                    color: #1d1d1f;
                    background: transparent;
                }
            """
        },
        'win11': {
            'name': '🪟 Windows 11',
            'css': """
                QMenu {
                    background-color: rgba(243, 243, 243, 0.9);
                    border-radius: 8px;
                    padding: 4px;
                    border: 1px solid rgba(0, 0, 0, 0.08);
                }
                QMenu::item {
                    padding: 10px 16px;
                    border-radius: 4px;
                    color: #323130;
                    font-size: 13px;
                    margin: 1px 0px;
                }
                QMenu::item:selected {
                    background-color: rgba(0, 0, 0, 0.05);
                }
                QMenu::separator {
                    height: 1px;
                    background-color: rgba(0, 0, 0, 0.06);
                    margin: 4px 0px;
                }
            """,
            'header_css': """
                QWidget {
                    background-color: transparent;
                    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
                    padding: 12px 16px;
                }
                QLabel {
                    color: #323130;
                    background: transparent;
                }
            """
        },
        'material': {
            'name': '🎨 Material',
            'css': """
                QMenu {
                    background-color: white;
                    border-radius: 4px;
                    padding: 8px 0px;
                    border: none;
                }
                QMenu::item {
                    padding: 12px 16px;
                    color: rgba(0, 0, 0, 0.87);
                    font-size: 14px;
                }
                QMenu::item:selected {
                    background-color: rgba(0, 0, 0, 0.04);
                }
                QMenu::separator {
                    height: 1px;
                    background-color: rgba(0, 0, 0, 0.12);
                    margin: 8px 0px;
                }
            """,
            'header_css': """
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #667eea,
                        stop:1 #764ba2);
                    padding: 16px 16px 12px 16px;
                }
                QLabel {
                    color: white;
                    background: transparent;
                }
            """
        },
        'minimal': {
            'name': '⚫ Minimal',
            'css': """
                QMenu {
                    background-color: #2a2a2a;
                    border-radius: 12px;
                    padding: 12px;
                    border: 1px solid rgba(255, 255, 255, 0.15);
                }
                QMenu::item {
                    padding: 10px 12px;
                    border-radius: 6px;
                    color: rgba(255, 255, 255, 0.95);
                    font-size: 13px;
                    margin: 2px 0px;
                }
                QMenu::item:selected {
                    background-color: rgba(255, 255, 255, 0.12);
                }
                QMenu::separator {
                    height: 1px;
                    background-color: rgba(255, 255, 255, 0.1);
                    margin: 10px 0px;
                }
            """,
            'header_css': """
                QWidget {
                    background-color: #1a1a1a;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                    padding: 12px 12px 16px 12px;
                    border-radius: 8px;
                }
                QLabel {
                    color: white;
                    background: transparent;
                }
            """
        },
        'rosegold': {
            'name': '🌸 Rose Gold',
            'css': """
                QMenu {
                    background-color: #ffe4e1;
                    padding: 12px;
                    border: 2px solid #ffb6c1;
                }
                QMenu::item {
                    padding: 11px 16px;
                    color: #8b4789;
                    font-size: 13px;
                    margin: 2px 0px;
                }
                QMenu::item:selected {
                    background-color: #ffc0cb;
                }
                QMenu::separator {
                    height: 1px;
                    background-color: #ffb6c1;
                    margin: 10px 0px;
                }
            """,
            'header_css': """
                QWidget {
                    background-color: #ff69b4;
                    padding: 14px 16px;
                }
                QLabel {
                    color: white;
                    background: transparent;
                }
            """
        },
        'ocean': {
            'name': '🌊 Ocean Blue',
            'css': """
                QMenu {
                    background-color: #e0f2f7;
                    padding: 12px;
                    border: 2px solid #4fc3f7;
                }
                QMenu::item {
                    padding: 11px 16px;
                    color: #01579b;
                    font-size: 13px;
                    margin: 2px 0px;
                }
                QMenu::item:selected {
                    background-color: #81d4fa;
                }
                QMenu::separator {
                    height: 1px;
                    background-color: #4fc3f7;
                    margin: 10px 0px;
                }
            """,
            'header_css': """
                QWidget {
                    background-color: #0277bd;
                    padding: 14px 16px;
                }
                QLabel {
                    color: white;
                    background: transparent;
                }
            """
        },
        'forest': {
            'name': '🌲 Forest Green',
            'css': """
                QMenu {
                    background-color: #e8f5e9;
                    padding: 12px;
                    border: 2px solid #66bb6a;
                }
                QMenu::item {
                    padding: 11px 16px;
                    color: #1b5e20;
                    font-size: 13px;
                    margin: 2px 0px;
                }
                QMenu::item:selected {
                    background-color: #a5d6a7;
                }
                QMenu::separator {
                    height: 1px;
                    background-color: #66bb6a;
                    margin: 10px 0px;
                }
            """,
            'header_css': """
                QWidget {
                    background-color: #388e3c;
                    padding: 14px 16px;
                }
                QLabel {
                    color: white;
                    background: transparent;
                }
            """
        },
        'sunset': {
            'name': '🌅 Sunset Orange',
            'css': """
                QMenu {
                    background-color: #fff3e0;
                    padding: 12px;
                    border: 2px solid #ffb74d;
                }
                QMenu::item {
                    padding: 11px 16px;
                    color: #e65100;
                    font-size: 13px;
                    margin: 2px 0px;
                }
                QMenu::item:selected {
                    background-color: #ffcc80;
                }
                QMenu::separator {
                    height: 1px;
                    background-color: #ffb74d;
                    margin: 10px 0px;
                }
            """,
            'header_css': """
                QWidget {
                    background-color: #f57c00;
                    padding: 14px 16px;
                }
                QLabel {
                    color: white;
                    background: transparent;
                }
            """
        },
        'lavender': {
            'name': '💜 Lavender Dream',
            'css': """
                QMenu {
                    background-color: #f3e5f5;
                    padding: 12px;
                    border: 2px solid #ba68c8;
                }
                QMenu::item {
                    padding: 11px 16px;
                    color: #4a148c;
                    font-size: 13px;
                    margin: 2px 0px;
                }
                QMenu::item:selected {
                    background-color: #ce93d8;
                }
                QMenu::separator {
                    height: 1px;
                    background-color: #ba68c8;
                    margin: 10px 0px;
                }
            """,
            'header_css': """
                QWidget {
                    background-color: #7b1fa2;
                    padding: 14px 16px;
                }
                QLabel {
                    color: white;
                    background: transparent;
                }
            """
        },
        'midnight': {
            'name': '🌙 Midnight Blue',
            'css': """
                QMenu {
                    background-color: #1a237e;
                    padding: 12px;
                    border: 2px solid #5c6bc0;
                }
                QMenu::item {
                    padding: 11px 16px;
                    color: #e8eaf6;
                    font-size: 13px;
                    margin: 2px 0px;
                }
                QMenu::item:selected {
                    background-color: #3949ab;
                }
                QMenu::separator {
                    height: 1px;
                    background-color: #5c6bc0;
                    margin: 10px 0px;
                }
            """,
            'header_css': """
                QWidget {
                    background-color: #0d47a1;
                    padding: 14px 16px;
                }
                QLabel {
                    color: white;
                    background: transparent;
                }
            """
        }
    }

class MenuHeader(QWidget):
    """Custom header widget for the menu"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        # Set maximum width to prevent menu stretching
        self.setMaximumWidth(280)
        
        self.now_playing_label = QLabel("♪ Now playing:")
        self.now_playing_label.setFont(QFont("", 9, QFont.Weight.Bold))
        self.now_playing_label.setWordWrap(True)
        
        self.station_label = QLabel("📻 TrayWave")
        self.station_label.setFont(QFont("", 11, QFont.Weight.DemiBold))
        self.station_label.setWordWrap(True)
        
        self.song_label = QLabel("")
        self.song_label.setFont(QFont("", 10))
        self.song_label.setVisible(False)
        self.song_label.setWordWrap(True)
        
        layout.addWidget(self.now_playing_label)
        layout.addWidget(self.station_label)
        layout.addWidget(self.song_label)
    
    def update_content(self, station=None, artist=None, title=None):
        """Update header content"""
        if station:
            self.station_label.setText(f"📻 {station}")
            self.station_label.setVisible(True)
        else:
            self.station_label.setText("📻 TrayWave")
        
        if title:
            if artist:
                self.song_label.setText(f"🎵 {artist} - {title}")
            else:
                self.song_label.setText(f"🎵 {title}")
            self.song_label.setVisible(True)
        else:
            self.song_label.setVisible(False)

class TrayWave(QSystemTrayIcon):
    """Main system tray application"""
    
    def __init__(self):
        super().__init__()
        
        # Force Qt style rendering instead of native menus
        app = QApplication.instance()
        if app:
            app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar, True)
        
        self.stations_manager = StationsManager()
        self.engine = AudioEngine()
        self.popup = VolumePopup(self.engine)
        
        # Setup callbacks
        self.engine.on_icon_changed(self._update_icon)
        self.engine.on_station_changed(self._rebuild_menu)
        self.engine.on_metadata_changed(self._on_metadata_changed)
        
        # Song display variables
        self.now_playing_artist = None
        self.now_playing_title = None
        
        # Icon source tracking
        self._icon_source_logged = False
        
        # Menu style management
        self.config_file = os.path.expanduser("~/.traywave_style.json")
        self.current_style = self._load_style()
        self.menu_header = None
        self.menu = None
        self._menu_visible = False  # Track if menu is currently visible
        
        # Initial setup
        self._update_icon()
        self.setToolTip("TrayWave - Radio Player\nLeft click: Menu | Middle/Double click: Volume")
        
        # DON'T set context menu - we'll show it manually!
        # self.setContextMenu(None)
        
        # Build context menu
        self._build_menu()
        
        # Connect signals - override right-click behavior
        self.activated.connect(self.on_tray_activated)
        
        # Add context menu action manually since right-click doesn't work
        # User can double-click OR use keyboard shortcut
        from PyQt6.QtGui import QShortcut, QKeySequence
        self.menu_shortcut = QShortcut(QKeySequence("Ctrl+M"), None)
        self.menu_shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.menu_shortcut.activated.connect(self._show_custom_menu)
        
        # WORKAROUND: Monitor for right-clicks manually since Context event doesn't fire
        self._right_click_timer = QTimer()
        self._right_click_timer.timeout.connect(self._check_for_menu_request)
        self._right_click_timer.start(50)  # Check every 50ms
        self._last_trigger_time = 0
        
        # Setup timers
        self.setup_timers()
        
        # Show tray icon
        self.show()
    
    def _load_style(self):
        """Load saved style from config"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('style', 'teal')
        except:
            pass
        return 'teal'
    
    def _save_style(self, style_name):
        """Save style to config"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump({'style': style_name}, f)
        except:
            pass
    
    def change_menu_style(self, style_name):
        """Change menu style - NUCLEAR OPTION: Complete rebuild"""
        if style_name in MenuStyles.STYLES:
            old_style = self.current_style
            self.current_style = style_name
            self._save_style(style_name)
            
            print(f"\n🎨 CHANGING STYLE: '{old_style}' → '{style_name}'")
            
            # ALWAYS do complete rebuild - stylesheet updates don't work visually
            menu_was_visible = False
            if self.menu and self.menu.isVisible():
                print("   📋 Menu is visible, will reopen after rebuild")
                menu_was_visible = True
                self.menu.hide()
                QApplication.processEvents()
            
            # Complete rebuild
            print("   🔥 NUCLEAR REBUILD: Destroying and recreating menu...")
            self._rebuild_menu()
            
            # Show notification
            self.showMessage(
                "Style Changed",
                f"✓ {MenuStyles.STYLES[style_name]['name']}",
                QSystemTrayIcon.MessageIcon.Information,
                1000
            )
            
            # Reopen menu if it was visible
            if menu_was_visible:
                print("   🔄 Reopening menu with new style...")
                QTimer.singleShot(100, self._show_menu_at_cursor)
            
            print(f"   ✅ Style change complete!")
    
    def _find_icon_path(self, icon_name: str) -> str:
        """Find icon file path - works for both development and installed package"""
        paths_to_check = []
        
        # 1. Try package resources FIRST
        try:
            from importlib.resources import files
            icon_path = str(files('traywave.resources.icons').joinpath(icon_name))
            paths_to_check.append(('Package resources', icon_path))
        except Exception:
            pass
        
        # 2. System-wide installation paths
        system_paths = [
            (f"/usr/share/traywave/icons/{icon_name}", 'System traywave'),
            (f"/usr/share/icons/hicolor/128x128/apps/{icon_name}", 'Hicolor 128x128'),
            (f"/usr/share/icons/hicolor/scalable/apps/{icon_name.replace('.png', '.svg')}", 'Hicolor scalable'),
            (f"/usr/local/share/traywave/icons/{icon_name}", 'Local traywave'),
        ]
        for path, desc in system_paths:
            paths_to_check.append((desc, path))
        
        # 3. Development paths
        try:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
            paths_to_check.append(('Project root', os.path.join(project_root, 'resources', 'icons', icon_name)))
            
            traywave_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            paths_to_check.append(('Traywave dev', os.path.join(traywave_dir, 'resources', 'icons', icon_name)))
        except Exception:
            pass
        
        # Check each path
        for source, path in paths_to_check:
            if os.path.exists(path):
                if not self._icon_source_logged:
                    print(f"✓ Loading icons from: {source}")
                    self._icon_source_logged = True
                return path
        
        return None
    
    def _update_icon(self):
        """Update tray icon based on state"""
        if self.engine.is_muted():
            icon_name = "traywave-muted.png"
            fallback = "audio-volume-muted"
        elif self.engine.is_playing():
            icon_name = "traywave-playing.png"
            fallback = "audio-radio"
        else:
            icon_name = "traywave-stopped.png"
            fallback = "audio-card"
        
        icon_path = self._find_icon_path(icon_name)
        
        if icon_path:
            icon = QIcon(icon_path)
            if not icon.isNull():
                self.setIcon(icon)
                return
        
        svg_name = icon_name.replace('.png', '.svg')
        svg_path = self._find_icon_path(svg_name)
        
        if svg_path:
            icon = QIcon(svg_path)
            if not icon.isNull():
                self.setIcon(icon)
                return
        
        self.setIcon(QIcon.fromTheme(fallback, QIcon.fromTheme("audio-radio")))
    
    def setup_timers(self):
        """Setup various timers"""
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self._update_tooltip)
        self.status_timer.start(5000)
        
        self.mouse_timer = QTimer()
        self.mouse_timer.timeout.connect(self._check_mouse_position)
        self.mouse_timer.start(100)
        
        self.last_scroll_time = 0
        self.is_mouse_in_tray = False
        
        app = QApplication.instance()
        app.installEventFilter(self)
    
    def _build_menu(self):
        """Build the context menu with modern styling AS STANDALONE POPUP"""
        print(f"🎨 Building menu with style: {self.current_style}")
        
        # Create COMPLETELY NEW menu object AS POPUP WINDOW
        self.menu = QMenu()
        
        # CRITICAL: Make it a standalone popup, NOT a context menu
        self.menu.setWindowFlags(
            Qt.WindowType.Popup | 
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.NoDropShadowWindowHint
        )
        
        # Set fixed width to prevent stretching
        self.menu.setFixedWidth(280)
        
        # Get and apply current style
        style = MenuStyles.STYLES.get(self.current_style, MenuStyles.STYLES['teal'])
        print(f"📝 Applying CSS for: {style['name']}")
        self.menu.setStyleSheet(style['css'])
        
        # Debug: Print first 100 chars of CSS
        css_preview = style['css'].replace('\n', ' ').replace('  ', ' ')[:100]
        print(f"   CSS preview: {css_preview}...")
        
        # Add custom header
        self.menu_header = MenuHeader()
        self.menu_header.update_content(
            station=self.engine.current_station,
            artist=self.now_playing_artist,
            title=self.now_playing_title
        )
        self.menu_header.setStyleSheet(style['header_css'])
        
        header_action = QWidgetAction(self.menu)
        header_action.setDefaultWidget(self.menu_header)
        self.menu.addAction(header_action)
        print(f"   ✓ Added header")
        
        self.menu.addSeparator()
        
        # Radio Categories
        category_count = 0
        for category, stations in self.stations_manager.stations.items():
            if stations:
                self._add_category_menu(category, stations)
                category_count += 1
        print(f"   ✓ Added {category_count} radio categories")
        
        self.menu.addSeparator()
        
        # Style selector submenu with proper styling
        style_menu = QMenu("🎨 Change Style ▶", self.menu)
        style_menu.setStyleSheet(style['css'])  # Apply same style!
        style_menu.setFixedWidth(200)
        
        for style_key, style_info in MenuStyles.STYLES.items():
            is_current = (style_key == self.current_style)
            action_text = f"{'✓ ' if is_current else ''}{style_info['name']}"
            style_menu.addAction(action_text, lambda s=style_key: self.change_menu_style(s))
        self.menu.addMenu(style_menu)
        print(f"   ✓ Added style selector")
        
        # Sleep Timer submenu with proper styling
        sleep_menu = QMenu("⏰ Sleep timer ▶", self.menu)
        sleep_menu.setStyleSheet(style['css'])  # Apply same style!
        sleep_menu.setFixedWidth(180)
        
        sleep_menu.addAction("15 minutes", lambda: self._set_sleep_timer(15))
        sleep_menu.addAction("30 minutes", lambda: self._set_sleep_timer(30))
        sleep_menu.addAction("45 minutes", lambda: self._set_sleep_timer(45))
        sleep_menu.addAction("60 minutes", lambda: self._set_sleep_timer(60))
        self.menu.addMenu(sleep_menu)
        print(f"   ✓ Added sleep timer")
        
        self.menu.addSeparator()
        
        # Settings
        self.menu.addAction("⚙️ Settings", self._open_settings)
        print(f"   ✓ Added settings")
        
        self.menu.addSeparator()
        
        # Controls
        self.menu.addAction("Stop", self.engine.stop)
        self.mute_action = self.menu.addAction("Mute", self._toggle_mute)
        print(f"   ✓ Added controls")
        
        # About
        self.menu.addSeparator()
        self.menu.addAction("About", self._open_about)
        print(f"   ✓ Added about")
        
        self.menu.addSeparator()
        self.menu.addAction("Quit", self._quit)
        print(f"   ✓ Added quit")
        
        # DON'T use setContextMenu! Show manually with popup()
        # self.setContextMenu(self.menu)
        
        # Connect menu signals
        self.menu.aboutToShow.connect(self._on_menu_about_to_show)
        self.menu.aboutToHide.connect(self._on_menu_about_to_hide)
        
        total_actions = len(self.menu.actions())
        print(f"   ✅ Menu built with {total_actions} total actions (standalone popup mode)")
    
    def _on_menu_about_to_show(self):
        """Menu is about to show"""
        self._menu_visible = True
        print("📋 Menu showing...")
    
    def _on_menu_about_to_hide(self):
        """Menu is about to hide"""
        self._menu_visible = False
        print("📋 Menu hiding...")
    
    def _add_category_menu(self, category: str, stations: list):
        """Add a category submenu with proper styling"""
        # Shorten category name if too long
        display_name = category[:20] + "..." if len(category) > 20 else category
        category_menu = QMenu(f"{display_name} ▶", self.menu)
        
        # CRITICAL: Apply same stylesheet to submenu!
        style = MenuStyles.STYLES.get(self.current_style, MenuStyles.STYLES['teal'])
        category_menu.setStyleSheet(style['css'])
        
        # Set reasonable width for submenus
        category_menu.setMinimumWidth(220)
        category_menu.setMaximumWidth(300)
        
        for name, url in stations:
            # Shorten station names if too long
            display_station = name[:35] + "..." if len(name) > 35 else name
            category_menu.addAction(display_station, lambda u=url, n=name: self.engine.play(u, n))
        
        self.menu.addMenu(category_menu)
    
    def _rebuild_menu(self):
        """Rebuild the context menu - COMPLETELY destroy and recreate"""
        print(f"\n🔄 Rebuilding menu with style: {self.current_style}")
        
        # Delete old menu completely
        if self.menu:
            try:
                # Disconnect ALL signals
                try:
                    self.menu.aboutToShow.disconnect()
                    self.menu.aboutToHide.disconnect()
                except:
                    pass
                
                # Hide it
                self.menu.hide()
                
                # Clear all actions
                self.menu.clear()
                
                # Destroy the widget completely
                self.menu.deleteLater()
                self.menu = None
                self.menu_header = None
                
                # FORCE event processing
                QApplication.processEvents()
                
            except Exception as e:
                print(f"⚠️ Error deleting menu: {e}")
        
        # Build completely NEW menu object
        self._build_menu()
        
        print(f"✅ Menu rebuilt with NEW style: {self.current_style}")
    
    def _show_menu_at_cursor(self):
        """Show menu at cursor position"""
        if self.menu:
            self.menu.popup(QCursor.pos())
    
    def _open_settings(self):
        """Open settings dialog"""
        print(f"\n⚙️ Opening settings dialog...")
        
        # Close menu before opening settings
        if self.menu and self.menu.isVisible():
            self.menu.close()
        
        dialog = StyleSettingsDialog(self.stations_manager, self, self.menu)
        
        # Connect to dialog close event
        dialog.finished.connect(self._on_settings_closed)
        
        dialog.exec()
    
    def _on_settings_closed(self, result):
        """Handle settings dialog close"""
        print(f"Settings dialog closed, result: {result}")
        
        # Menu will automatically show again when user clicks tray icon
    
    def _open_about(self):
        """Open About dialog"""
        from ..ui.dialogs import AboutDialog
        dialog = AboutDialog(self.menu)
        dialog.exec()
    
    def _on_metadata_changed(self, artist: str, title: str):
        """Handle metadata (song) changes"""
        self.now_playing_artist = artist
        self.now_playing_title = title
        self._update_tooltip()
        
        # Update header if menu exists
        if self.menu_header:
            self.menu_header.update_content(
                station=self.engine.current_station,
                artist=artist,
                title=title
            )
    
    def _set_sleep_timer(self, minutes: int):
        """Set sleep timer"""
        self.showMessage(
            "Sleep Timer",
            f"Sleep timer set for {minutes} minutes (not implemented yet)",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )

    def _toggle_mute(self):
        """Toggle mute and update menu text"""
        is_muted = self.engine.toggle_mute()
        self.mute_action.setText("Unmute" if is_muted else "Mute")

    def _update_tooltip(self):
        """Update tray tooltip"""
        if self.engine.current_station:
            if self.now_playing_title:
                if self.now_playing_artist:
                    song_info = f"{self.now_playing_artist} - {self.now_playing_title}"
                else:
                    song_info = self.now_playing_title
                status = f"Playing: {self.engine.current_station}\n{song_info}"
            else:
                status = f"Playing: {self.engine.current_station}"
        else:
            status = "Stopped"
        
        vol = self.engine.get_volume()
        muted = " (Muted)" if self.engine.is_muted() else ""
        self.setToolTip(f"TrayWave\n{status}\nVolume: {vol}%{muted}")

    def _check_mouse_position(self):
        """Check if mouse is in tray area for scroll events"""
        self.is_mouse_in_tray = is_mouse_in_tray_area(70)

    def eventFilter(self, obj, event):
        """Global event filter for scroll events"""
        if event.type() == event.Type.Wheel:
            if self.is_mouse_in_tray and not self.popup.isVisible():
                current_time = QTimer.currentTime().msec()
                if current_time - self.last_scroll_time > 100:
                    self.last_scroll_time = current_time
                    
                    if event.angleDelta().y() > 0:
                        self.engine.change_volume(+5)
                    else:
                        self.engine.change_volume(-5)
                    return True
        return False

    def _quit(self):
        """Clean quit application"""
        self.engine.stop()
        QApplication.quit()

    def _check_for_menu_request(self):
        """Check if user wants to open menu (workaround for missing Context event)"""
        # This is a backup - we'll use keyboard shortcut or double-click
        pass
    
    def on_tray_activated(self, reason):
        """Handle tray icon activation"""
        print(f"\n🖱️ Tray activated with reason: {reason} ({reason.name})")
        
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            # Left click - show STYLED MENU
            print("   → Left click: showing STYLED MENU")
            self._show_custom_menu()
        elif reason == QSystemTrayIcon.ActivationReason.Context:
            # Right click - show menu (doesn't fire on your system, but just in case)
            print("   → Right click (Context): showing STYLED MENU")
            self._show_custom_menu()
        elif reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            # Double click - show volume popup
            print("   → Double click: showing volume popup")
            self.popup.show_at_cursor()
        elif reason == QSystemTrayIcon.ActivationReason.MiddleClick:
            # Middle click - show volume popup
            print("   → Middle click: showing volume popup")
            self.popup.show_at_cursor()
        elif reason == QSystemTrayIcon.ActivationReason.Unknown:
            print("   → Unknown activation")
        else:
            print(f"   → Unhandled reason: {reason}")
    
    def _show_custom_menu(self):
        """Show our custom styled menu near tray icon"""
        if self.menu:
            action_count = len(self.menu.actions())
            
            print(f"\n   📋 SHOWING CUSTOM MENU:")
            print(f"      Total actions: {action_count}")
            
            # Calculate position near tray icon (usually bottom-right)
            screen = QApplication.primaryScreen()
            screen_geo = screen.availableGeometry()
            
            # Get tray icon geometry if available
            tray_geo = self.geometry()
            
            # Estimate menu size (since sizeHint() isn't reliable before show)
            estimated_height = 800  # Conservative estimate for full menu
            estimated_width = 280   # Our fixed width
            
            if tray_geo.isValid() and tray_geo.y() >= 0:
                # Position menu near tray icon
                x = tray_geo.x()
                y = tray_geo.y()
                
                # Adjust based on tray position
                # If tray is at bottom, show menu above it
                if y > screen_geo.height() / 2:
                    y = tray_geo.top() - estimated_height - 5
                else:
                    y = tray_geo.bottom() + 5
                
                # If tray is at right, align menu to right edge
                if x > screen_geo.width() / 2:
                    x = tray_geo.right() - estimated_width
                
                print(f"      Tray position: {tray_geo}")
                print(f"      Menu position: ({x}, {y})")
            else:
                # Fallback: bottom-right corner (typical tray location)
                x = screen_geo.right() - estimated_width - 10
                y = screen_geo.bottom() - estimated_height - 10
                
                print(f"      Tray geometry invalid ({tray_geo}), using corner: ({x}, {y})")
            
            # Ensure menu is FULLY on screen with conservative margins
            if x < screen_geo.left():
                x = screen_geo.left() + 10
            if y < screen_geo.top():
                y = screen_geo.top() + 10
            if x + estimated_width > screen_geo.right():
                x = screen_geo.right() - estimated_width - 10
            if y + estimated_height > screen_geo.bottom():
                y = screen_geo.bottom() - estimated_height - 10
            
            print(f"      Final position (after bounds check): ({x}, {y})")
            
            # Show menu at calculated position
            self.menu.popup(QPoint(x, y))
            
            print(f"      Menu visible: {self.menu.isVisible()}")
            
        else:
            print("   ⚠️ Menu is None!")