"""
Menu builder - constructs the tray menu
"""
from PyQt6.QtWidgets import QMenu, QWidgetAction
from PyQt6.QtCore import Qt
from .widgets.menu_header import MenuHeader
from .styles.style_manager import StyleManager


class MenuBuilder:
    """Builds and manages the tray menu structure"""
    
    def __init__(self, tray_app):
        self.tray = tray_app
        self.style_manager = StyleManager()
        self.menu_header = None
    
    def build_menu(self, current_style: str) -> QMenu:
        """Build the complete menu with given style"""
        print(f"🎨 Building menu with style: {current_style}")
        
        # Create new menu
        menu = QMenu()
        
        # Set as standalone popup
        menu.setWindowFlags(
            Qt.WindowType.Popup | 
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.NoDropShadowWindowHint
        )
        menu.setFixedWidth(280)
        
        # Apply style
        style = self.style_manager.get_style(current_style)
        menu.setStyleSheet(style['css'])
        
        # Build menu structure
        self._add_header(menu, style)
        menu.addSeparator()
        
        self._add_radio_categories(menu, style)
        menu.addSeparator()
        
        self._add_style_submenu(menu, style, current_style)
        self._add_sleep_timer_submenu(menu, style)
        menu.addSeparator()
        
        self._add_settings(menu)
        menu.addSeparator()
        
        self._add_controls(menu)
        menu.addSeparator()
        
        self._add_about(menu)
        menu.addSeparator()
        
        self._add_quit(menu)
        
        print(f"   ✅ Menu built with {len(menu.actions())} actions")
        return menu
    
    def _add_header(self, menu: QMenu, style: dict):
        """Add custom header widget"""
        self.menu_header = MenuHeader()
        self.menu_header.update_content(
            station=self.tray.engine.current_station,
            artist=self.tray.now_playing_artist,
            title=self.tray.now_playing_title
        )
        self.menu_header.setStyleSheet(style['header_css'])
        
        header_action = QWidgetAction(menu)
        header_action.setDefaultWidget(self.menu_header)
        menu.addAction(header_action)
    
    def _add_radio_categories(self, menu: QMenu, style: dict):
        """Add radio station categories"""
        for category, stations in self.tray.stations_manager.stations.items():
            if stations:
                self._add_category_submenu(menu, category, stations, style)
    
    def _add_category_submenu(self, menu: QMenu, category: str, stations: list, style: dict):
        """Add a single category submenu"""
        # Shorten category name if too long
        display_name = category[:20] + "..." if len(category) > 20 else category
        category_menu = QMenu(f"{display_name} ▶", menu)
        
        # Apply same style to submenu
        category_menu.setStyleSheet(style['css'])
        category_menu.setMinimumWidth(220)
        category_menu.setMaximumWidth(300)
        
        # Add stations
        for name, url in stations:
            display_station = name[:35] + "..." if len(name) > 35 else name
            category_menu.addAction(
                display_station, 
                lambda u=url, n=name: self.tray.engine.play(u, n)
            )
        
        menu.addMenu(category_menu)
    
    def _add_style_submenu(self, menu: QMenu, style: dict, current_style: str):
        """Add style selector submenu"""
        style_menu = QMenu("🎨 Change Style ▶", menu)
        style_menu.setStyleSheet(style['css'])
        style_menu.setFixedWidth(200)
        
        for style_name in self.style_manager.get_theme_names():
            is_current = (style_name == current_style)
            display_name = self.style_manager.get_theme_display_name(style_name)
            action_text = f"{'✓ ' if is_current else ''}{display_name}"
            style_menu.addAction(
                action_text, 
                lambda s=style_name: self.tray.change_menu_style(s)
            )
        
        menu.addMenu(style_menu)
    
    def _add_sleep_timer_submenu(self, menu: QMenu, style: dict):
        """Add sleep timer submenu"""
        sleep_menu = QMenu("⏰ Sleep timer ▶", menu)
        sleep_menu.setStyleSheet(style['css'])
        sleep_menu.setFixedWidth(180)
        
        # Add timer options
        for minutes in [15, 30, 45, 60]:
            sleep_menu.addAction(
                f"{minutes} minutes", 
                lambda m=minutes: self.tray._set_sleep_timer(m)
            )
        
        sleep_menu.addSeparator()
        
        # Add cancel option
        sleep_menu.addAction(
            "❌ Cancel sleep timer",
            self.tray._cancel_sleep_timer
        )
        
        menu.addMenu(sleep_menu)
    
    def _add_settings(self, menu: QMenu):
        """Add settings action"""
        menu.addAction("⚙️ Settings", self.tray._open_settings)
    
    def _add_controls(self, menu: QMenu):
        """Add playback controls"""
        menu.addAction("Stop", self.tray.engine.stop)
        self.tray.mute_action = menu.addAction("Mute", self.tray._toggle_mute)
    
    def _add_about(self, menu: QMenu):
        """Add about action"""
        menu.addAction("About", self.tray._open_about)
    
    def _add_quit(self, menu: QMenu):
        """Add quit action"""
        menu.addAction("Quit", self.tray._quit)
    
    def update_header(self, station=None, artist=None, title=None):
        """Update menu header content"""
        if self.menu_header:
            self.menu_header.update_content(station, artist, title)