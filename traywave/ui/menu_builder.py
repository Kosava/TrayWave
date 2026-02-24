"""
Menu builder - constructs the tray menu with ZERO GAPS fix + COMBINED CSS
SVG ikone za sve stavke menija - kompatibilnost sa Debian/LMDE.
"""
import logging
from PyQt6.QtWidgets import QMenu, QWidgetAction, QApplication
from PyQt6.QtCore import Qt
from .widgets.menu_header import MenuHeader
from .styles.style_manager import StyleManager
from .icons import get_icon, get_category_icon, get_theme_icon

logger = logging.getLogger(__name__)

MENU_WIDTH = 280
ICON_SIZE = 18  # px, za sve stavke menija


class MenuBuilder:
    """Builds and manages the tray menu structure"""

    def __init__(self, tray_app):
        self.tray = tray_app
        self.style_manager = StyleManager()
        self.menu_header = None
        self._css_cache = {}

    # ── CSS ──────────────────────────────────────────────────────────────────

    def _get_base_menu_css(self, theme: dict, theme_name: str = "") -> str:
        """Get base CSS - uses theme colors (cached by theme name)."""
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
            QMenu::icon {{
                padding-left: 4px;
            }}
            QMenu::indicator {{
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

    # ── HELPERS ──────────────────────────────────────────────────────────────

    def _apply_menu_fix(self, menu_obj: QMenu):
        """Apply window flags and attributes to any menu/submenu."""
        menu_obj.setWindowFlags(
            Qt.WindowType.Popup |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.NoDropShadowWindowHint
        )
        menu_obj.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        menu_obj.setContentsMargins(0, 0, 0, 0)

    def _add_action(self, menu: QMenu, text: str, callback, icon_name: str = "") -> object:
        """Add a menu action with optional SVG icon."""
        action = menu.addAction(text, callback)
        if icon_name:
            action.setIcon(get_icon(icon_name, ICON_SIZE))
            action.setIconVisibleInMenu(True)
        else:
            action.setIconVisibleInMenu(False)
        return action

    # ── BUILD ─────────────────────────────────────────────────────────────────

    def build_menu(self, current_style: str) -> QMenu:
        """Build the complete menu with given style."""
        self._css_cache.clear()

        menu = QMenu()
        self._apply_menu_fix(menu)
        menu.setFixedWidth(MENU_WIDTH)

        theme = self.style_manager.themes.get(current_style, {})
        menu.setStyleSheet(self._get_base_menu_css(theme, current_style))

        style = self.style_manager.get_style(current_style)

        self._add_header(menu, style, theme)
        menu.addSeparator()

        self._add_stations_submenu(menu, style)
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

    # ── SEKCIJE ──────────────────────────────────────────────────────────────

    def _add_header(self, menu: QMenu, style: dict, theme: dict):
        """Add header widget."""
        self.menu_header = MenuHeader()

        header_config = theme.get('header', {})
        item_config = theme.get('item', {})

        self.menu_header.apply_theme(
            background=header_config.get('background', 'transparent'),
            text_color=header_config.get('text_color', 'white'),
            padding=header_config.get('padding', '14px 16px'),
            border_radius=header_config.get('border_radius', '0px'),
            border_bottom=header_config.get('border_bottom', ''),
            item_color=item_config.get('color', 'palette(text)')
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
        """All categories inside a single 'Stations' submenu."""
        theme = self.style_manager.themes.get(self.tray.current_style, {})
        current_style = self.tray.current_style

        stations_menu = QMenu("Stations", menu)
        stations_menu.setIcon(get_icon("radio", ICON_SIZE))
        self._apply_menu_fix(stations_menu)
        stations_menu.setStyleSheet(self._get_base_menu_css(theme, current_style))
        stations_menu.setMinimumWidth(220)

        for category, stations in self.tray.stations_manager.stations.items():
            if not stations:
                continue

            # Skrati ime za prikaz u meniju (bez emoji - oni su u ikoni)
            display_name = _strip_emoji_prefix(category)
            if len(display_name) > 25:
                display_name = display_name[:24] + "…"

            category_menu = QMenu(display_name, stations_menu)
            category_menu.setIcon(get_category_icon(category, ICON_SIZE))
            self._apply_menu_fix(category_menu)
            category_menu.setStyleSheet(self._get_base_menu_css(theme, current_style))
            category_menu.setMinimumWidth(220)

            for name, url in stations:
                display_station = name[:40] + "…" if len(name) > 40 else name
                action = category_menu.addAction(
                    display_station,
                    lambda u=url, n=name: self.tray.engine.play(u, n)
                )
                action.setIconVisibleInMenu(False)

            stations_menu.addMenu(category_menu)

        menu.addMenu(stations_menu)

    def _add_style_submenu(self, menu: QMenu, style: dict, current_style: str):
        """Theme/style picker submenu."""
        style_menu = QMenu("Change Style", menu)
        style_menu.setIcon(get_icon("palette", ICON_SIZE))
        self._apply_menu_fix(style_menu)

        theme = self.style_manager.themes.get(self.tray.current_style, {})
        style_menu.setStyleSheet(self._get_base_menu_css(theme, self.tray.current_style))

        for style_name in self.style_manager.get_theme_names():
            is_current = (style_name == current_style)
            display_name = self.style_manager.get_theme_display_name(style_name)
            # Ukloni emoji iz display_name jer imamo SVG ikonu
            display_name_clean = _strip_emoji_prefix(display_name)
            action_text = ("✓  " if is_current else "") + display_name_clean
            action = style_menu.addAction(
                action_text,
                lambda s=style_name: self.tray.change_menu_style(s)
            )
            action.setIcon(get_theme_icon(style_name, ICON_SIZE))
            action.setIconVisibleInMenu(True)

        menu.addMenu(style_menu)

    def _add_sleep_timer_submenu(self, menu: QMenu, style: dict):
        """Sleep timer submenu."""
        sleep_menu = QMenu("Sleep Timer", menu)
        sleep_menu.setIcon(get_icon("sleep", ICON_SIZE))
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
        self._add_action(sleep_menu, "Cancel Sleep Timer",
                         self.tray._cancel_sleep_timer, "cancel")

        menu.addMenu(sleep_menu)

    def _add_settings(self, menu: QMenu):
        self._add_action(menu, "Settings", self.tray._open_settings, "settings")

    def _add_controls(self, menu: QMenu):
        self._add_action(menu, "Stop", self.tray.engine.stop, "stop")
        self.tray.mute_action = self._add_action(
            menu, "Mute", self.tray._toggle_mute, "mute"
        )

    def _add_about(self, menu: QMenu):
        self._add_action(menu, "About", self.tray._open_about, "about")

    def _add_quit(self, menu: QMenu):
        self._add_action(menu, "Quit", self.tray._quit, "power")

    def update_header(self, station=None, artist=None, title=None):
        """Update header content."""
        if self.menu_header:
            self.menu_header.update_content(station, artist, title)

    def update_mute_action(self, is_muted: bool):
        """Update mute action icon and text."""
        if self.tray.mute_action:
            if is_muted:
                self.tray.mute_action.setText("Unmute")
                self.tray.mute_action.setIcon(get_icon("volume", ICON_SIZE))
            else:
                self.tray.mute_action.setText("Mute")
                self.tray.mute_action.setIcon(get_icon("mute", ICON_SIZE))


# ── UTILITIES ─────────────────────────────────────────────────────────────────

def _strip_emoji_prefix(text: str) -> str:
    """
    Ukloni emoji i flag sekvence sa početka stringa.
    Npr: '🎸 Rock' → 'Rock', '🇷🇸 EX-YU' → 'EX-YU', '❄️ Nord' → 'Nord'
    """
    import re
    # Ukloni vodeće emoji/flag karaktere i whitespace
    stripped = re.sub(
        r'^[\U0001F000-\U0001FFFF\U00002600-\U000027FF\U00002B00-\U00002BFF'
        r'\U0001F1E0-\U0001F1FF\uFE0F\u20E3\u200D]+\s*',
        '', text
    ).strip()
    return stripped if stripped else text