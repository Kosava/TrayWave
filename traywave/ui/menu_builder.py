"""
Menu builder - constructs the tray menu with ZERO GAPS fix + COMBINED CSS
"""
from PyQt6.QtWidgets import QMenu, QWidgetAction, QApplication
from PyQt6.QtCore import Qt
from .widgets.menu_header import MenuHeader
from .styles.style_manager import StyleManager

MENU_WIDTH = 280


class MenuBuilder:
    """Builds and manages the tray menu structure"""
    
    def __init__(self, tray_app):
        self.tray = tray_app
        self.style_manager = StyleManager()
        self.menu_header = None
        self._css_cache = {}
    
    def _get_base_menu_css(self, theme: dict, theme_name: str = "") -> str:
        """Get base CSS that eliminates ALL gaps - uses theme colors (cached)"""
        cache_key = theme_name if theme_name else id(theme)
        if cache_key in self._css_cache:
            return self._css_cache[cache_key]
        
        menu_d = theme.get('menu', {})
        item = theme.get('item', {})
        separator = theme.get('separator', {})

        css = f"""
            QMenu {{
                background-color: {menu_d.get('background', 'palette(base)')};
                margin: 0px !important;
                padding: 0px !important;
                border: {menu_d.get('border', '1px solid palette(mid)')};
                border-radius: {menu_d.get('border_radius', '8px')};
                left: -1px;
            }}
            QMenu::item {{
                padding: {item.get('padding', '8px 16px')} !important;
                margin: 0px !important;
                border: none;
                border-radius: {item.get('border_radius', '4px')};
                color: {item.get('color', 'palette(text)')};
                font-size: {item.get('font_size', '13px')};
            }}
            QMenu::item:selected {{
                background: {item.get('hover_background', 'palette(highlight)')};
            }}
            QMenu::separator {{
                height: 1px !important;
                margin: 4px 0px !important;
                padding: 0px !important;
                background: {separator.get('background', 'palette(mid)')};
            }}
            QMenu::indicator, QMenu::icon {{
                width: 0px !important;
                height: 0px !important;
                margin: 0px !important;
                padding: 0px !important;
            }}
            QMenu::right-arrow {{
                margin: 0px !important;
                padding: 0px 4px 0px 0px !important;
            }}
        """

        self._css_cache[cache_key] = css
        return css

    def _apply_menu_fix(self, menu_obj: QMenu):
        """Helper to apply window flags and attributes to any menu/submenu"""
        menu_obj.setWindowFlags(
            Qt.WindowType.Popup | 
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.NoDropShadowWindowHint
        )
        menu_obj.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        menu_obj.setContentsMargins(0, 0, 0, 0)

    def build_menu(self, current_style: str) -> QMenu:
        """Build the complete menu with given style"""
        self._css_cache.clear()
        
        menu = QMenu()
        self._apply_menu_fix(menu)
        menu.setFixedWidth(MENU_WIDTH)
        # BEZ setMaximumHeight - glavni meni je uvijek kratak
        
        theme = self.style_manager.themes.get(current_style, {})
        menu.setStyleSheet(self._get_base_menu_css(theme, current_style))
        
        style = self.style_manager.get_style(current_style)
        
        self._add_header(menu, style, theme)
        menu.addSeparator()
        
        self._add_stations_submenu(menu, style)  # SVE stanice u jednom submeniju
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
        
        return menu

    def _add_header(self, menu: QMenu, style: dict, theme: dict):
        """Add header with proper text color from theme"""
        self.menu_header = MenuHeader()
        
        header_config = theme.get('header', {})
        text_color = header_config.get('text_color', 'white')
        background = header_config.get('background', 'transparent')
        padding = header_config.get('padding', '14px 16px')
        border_radius = header_config.get('border_radius', '0px')
        border_bottom = header_config.get('border_bottom', '')
        
        item_config = theme.get('item', {})
        item_color = item_config.get('color', 'palette(text)')
        
        print(f"🎨 Applying header theme:")
        print(f"   text_color: {text_color}")
        print(f"   item_color: {item_color}")
        print(f"   background: {background}")
        
        self.menu_header.apply_theme(
            background=background,
            text_color=text_color,
            padding=padding,
            border_radius=border_radius,
            border_bottom=border_bottom,
            item_color=item_color
        )
        
        self.menu_header.update_content(
            station=self.tray.engine.current_station,
            artist=self.tray.now_playing_artist,
            title=self.tray.now_playing_title
        )
        
        header_action = QWidgetAction(menu)
        header_action.setDefaultWidget(self.menu_header)
        menu.addAction(header_action)

    def _add_stations_submenu(self, menu: QMenu, style: dict):
        """Sve kategorije unutar jednog 'Stanice' submenija — glavni meni ostaje kratak"""
        theme = self.style_manager.themes.get(self.tray.current_style, {})
        current_style = self.tray.current_style
        
        stations_menu = QMenu("📻 Stanice ▶", menu)
        self._apply_menu_fix(stations_menu)
        stations_menu.setStyleSheet(self._get_base_menu_css(theme, current_style))
        stations_menu.setMinimumWidth(220)
        
        for category, stations in self.tray.stations_manager.stations.items():
            if stations:
                display_name = category[:20] + "..." if len(category) > 20 else category
                category_menu = QMenu(f"{display_name} ▶", stations_menu)
                self._apply_menu_fix(category_menu)
                category_menu.setStyleSheet(self._get_base_menu_css(theme, current_style))
                category_menu.setMinimumWidth(220)
                
                for name, url in stations:
                    display_station = name[:35] + "..." if len(name) > 35 else name
                    action = category_menu.addAction(
                        display_station,
                        lambda u=url, n=name: self.tray.engine.play(u, n)
                    )
                    action.setIconVisibleInMenu(False)
                
                stations_menu.addMenu(category_menu)
        
        menu.addMenu(stations_menu)

    def _add_style_submenu(self, menu: QMenu, style: dict, current_style: str):
        style_menu = QMenu("🎨 Change Style ▶", menu)
        self._apply_menu_fix(style_menu)
        
        theme = self.style_manager.themes.get(self.tray.current_style, {})
        style_menu.setStyleSheet(self._get_base_menu_css(theme, self.tray.current_style))
        
        for style_name in self.style_manager.get_theme_names():
            is_current = (style_name == current_style)
            display_name = self.style_manager.get_theme_display_name(style_name)
            action_text = f"{'✓ ' if is_current else ''}{display_name}"
            action = style_menu.addAction(
                action_text,
                lambda s=style_name: self.tray.change_menu_style(s)
            )
            action.setIconVisibleInMenu(False)
        
        menu.addMenu(style_menu)

    def _add_sleep_timer_submenu(self, menu: QMenu, style: dict):
        sleep_menu = QMenu("⏰ Sleep timer ▶", menu)
        self._apply_menu_fix(sleep_menu)
        
        theme = self.style_manager.themes.get(self.tray.current_style, {})
        sleep_menu.setStyleSheet(self._get_base_menu_css(theme, self.tray.current_style))
        
        for minutes in [15, 30, 45, 60]:
            action = sleep_menu.addAction(
                f"{minutes} minutes",
                lambda m=minutes: self.tray._set_sleep_timer(m)
            )
            action.setIconVisibleInMenu(False)
        
        sleep_menu.addSeparator()
        action = sleep_menu.addAction("⏹ Cancel sleep timer", self.tray._cancel_sleep_timer)
        action.setIconVisibleInMenu(False)
        
        menu.addMenu(sleep_menu)

    def _add_settings(self, menu: QMenu):
        action = menu.addAction("⚙️ Settings", self.tray._open_settings)
        action.setIconVisibleInMenu(False)

    def _add_controls(self, menu: QMenu):
        action = menu.addAction("Stop", self.tray.engine.stop)
        action.setIconVisibleInMenu(False)
        self.tray.mute_action = menu.addAction("Mute", self.tray._toggle_mute)
        self.tray.mute_action.setIconVisibleInMenu(False)

    def _add_about(self, menu: QMenu):
        action = menu.addAction("About", self.tray._open_about)
        action.setIconVisibleInMenu(False)

    def _add_quit(self, menu: QMenu):
        action = menu.addAction("Quit", self.tray._quit)
        action.setIconVisibleInMenu(False)

    def update_header(self, station=None, artist=None, title=None):
        """Update header content"""
        if self.menu_header:
            self.menu_header.update_content(station, artist, title)