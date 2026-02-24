"""
Main tray icon application
"""
import logging
import os
import sys
import json
from PyQt6.QtWidgets import QSystemTrayIcon, QApplication
from PyQt6.QtGui import QIcon, QCursor, QShortcut, QKeySequence
from PyQt6.QtCore import Qt, QTimer, QPoint, QRect

logger = logging.getLogger(__name__)

# Fixed imports - use absolute imports from traywave package
from traywave.core.engine import AudioEngine
from traywave.core.stations import StationsManager
from traywave.ui.popups import VolumePopup
# PROMENJENO: Sada import iz dialogs foldera
from traywave.ui.dialogs import StyleSettingsDialog, AboutDialog  # OVO SE MENJA!
from traywave.utils.geometry import is_mouse_in_tray_area
from traywave.ui.menu_builder import MenuBuilder
from traywave.ui.menu_positioning import MenuPositioner


class TrayWave(QSystemTrayIcon):
    """Main system tray application"""
    
    def __init__(self):
        super().__init__()
        
        # Force Qt style rendering
        app = QApplication.instance()
        if app:
            app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar, True)
        
        # Core components
        self.stations_manager = StationsManager()
        self.engine = AudioEngine()
        self.popup = VolumePopup(self.engine)
        
        # Menu builder
        self.menu_builder = MenuBuilder(self)
        
        # Setup callbacks
        self.engine.on_icon_changed(self._update_icon)
        self.engine.on_station_changed(self._rebuild_menu)
        self.engine.on_metadata_changed(self._on_metadata_changed)
        self.engine.on_sleep_timer_changed(self._on_sleep_timer_changed)
        
        # Poveži signal za promenu stanica
        self.stations_manager.stations_changed.connect(self._rebuild_menu)
        
        # Current playback state
        self.now_playing_artist = None
        self.now_playing_title = None
        
        # Sleep timer state
        self.sleep_timer_active = False
        self.sleep_minutes_left = 0
        self.sleep_quit_on_expire = False
        
        # Style management
        self.config_file = os.path.expanduser("~/.traywave_style.json")
        self.current_style = self._load_style()
        self.menu = None
        self.mute_action = None
        
        # Initial setup
        self._update_icon()
        self.setToolTip("TrayWave - Radio Player\nLeft click: Menu | Middle/Double click: Volume")
        
        # Build menu
        self._rebuild_menu()
        
        # Connect activation signal
        self.activated.connect(self._on_tray_activated)
        
        # Keyboard shortcut for menu
        self.menu_shortcut = QShortcut(QKeySequence("Ctrl+M"), None)
        self.menu_shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.menu_shortcut.activated.connect(self._show_menu)
        
        # Setup timers
        self._setup_timers()
        
        # Show tray icon
        self.show()
    
    # ============ Configuration ============
    
    def _load_style(self) -> str:
        """Load saved style from config"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('style', 'teal')
        except (json.JSONDecodeError, OSError, KeyError) as e:
            logger.warning(f"Ne mogu učitati style config: {e}")
        return 'teal'
    
    def _save_style(self, style_name: str):
        """Save style to config"""
        try:
            fd = os.open(self.config_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, 'w') as f:
                json.dump({'style': style_name}, f)
        except OSError as e:
            logger.warning(f"Ne mogu sačuvati style config: {e}")
    
    # ============ Menu Management ============
    
    def _rebuild_menu(self):
        """Rebuild the menu completely"""
        # Zaštita od re-entrant poziva (processEvents() može triggerovati signal ponovo)
        if getattr(self, '_rebuilding_menu', False):
            return
        self._rebuilding_menu = True
        try:
            self._do_rebuild_menu()
        finally:
            self._rebuilding_menu = False
    
    def _do_rebuild_menu(self):
        """Actual menu rebuild logic"""
        logger.debug(f"Rebuilding menu with style: {self.current_style}")
        
        # Cleanup old menu
        if self.menu:
            try:
                self.menu.hide()
                self.menu.clear()
                self.menu.deleteLater()
                self.menu = None
            except Exception as e:
                logger.warning(f"Error deleting menu: {e}")
        
        # Build new menu
        self.menu = self.menu_builder.build_menu(self.current_style)
        
        # Primijeni temu na volume popup
        theme = self.menu_builder.style_manager.themes.get(self.current_style, {})
        self.popup.apply_theme(theme)
        
        # Postavi minimalni context meni za desni klik (Stop, Mute, Quit)
        self.setContextMenu(self._build_context_menu(theme))
        
        logger.debug("Menu rebuilt")
    
    def _build_context_menu(self, theme: dict):
        """Minimalni context meni za desni klik - prati aktivnu temu"""
        from PyQt6.QtWidgets import QMenu
        from PyQt6.QtCore import Qt
        
        menu = QMenu()
        menu.setWindowFlags(
            Qt.WindowType.Popup |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.NoDropShadowWindowHint
        )
        menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Primijeni CSS iz teme
        menu_d = theme.get('menu', {})
        item = theme.get('item', {})
        separator = theme.get('separator', {})
        
        css = f"""
            QMenu {{
                background-color: {menu_d.get('background', 'palette(base)')};
                margin: 0px;
                padding: 4px;
                border: {menu_d.get('border', '1px solid palette(mid)')};
                border-radius: {menu_d.get('border_radius', '8px')};
            }}
            QMenu::item {{
                padding: {item.get('padding', '8px 16px')};
                margin: 0px;
                border-radius: {item.get('border_radius', '4px')};
                color: {item.get('color', 'palette(text)')};
                font-size: {item.get('font_size', '13px')};
            }}
            QMenu::item:selected {{
                background: {item.get('hover_background', 'palette(highlight)')};
            }}
            QMenu::separator {{
                height: 1px;
                margin: 4px 0px;
                background: {separator.get('background', 'palette(mid)')};
            }}
            QMenu::indicator, QMenu::icon {{
                width: 0px; height: 0px; margin: 0px; padding: 0px;
            }}
        """
        menu.setStyleSheet(css)
        
        stop_action = menu.addAction("⏹ Stop", self.engine.stop)
        stop_action.setIconVisibleInMenu(False)
        
        mute_text = "🔇 Unmute" if self.engine.is_muted() else "🔈 Mute"
        mute_action = menu.addAction(mute_text, self._toggle_mute)
        mute_action.setIconVisibleInMenu(False)
        
        menu.addSeparator()
        
        quit_action = menu.addAction("⏻ Quit", self._quit)
        quit_action.setIconVisibleInMenu(False)
        
        return menu

    def change_menu_style(self, style_name: str):
        """Change menu style"""
        if style_name == self.current_style:
            return
        
        old_style = self.current_style
        self.current_style = style_name
        self._save_style(style_name)
        
        logger.debug(f"Changing style: '{old_style}' -> '{style_name}'")
        
        # Check if menu is visible
        menu_was_visible = self.menu and self.menu.isVisible()
        if menu_was_visible:
            self.menu.hide()
            QApplication.processEvents()
        
        # Rebuild menu
        self._rebuild_menu()
        
        # Show notification
        display_name = self.menu_builder.style_manager.get_theme_display_name(style_name)
        self.showMessage(
            "Style Changed",
            f"✓ {display_name}",
            QSystemTrayIcon.MessageIcon.Information,
            1000
        )
        
        # Reopen if it was visible
        if menu_was_visible:
            QTimer.singleShot(100, self._show_menu)
        
        logger.debug("Style change complete")
    
    def _get_tray_position(self):
        """Get tray icon position - WORKAROUND za Linux gde geometry() ne radi"""
        logger.debug("Getting tray position...")
        
        # Prvo probaj standardnu geometriju
        tray_geo = self.geometry()
        logger.debug(f"Standard geometry(): {tray_geo}")
        
        # Ako nije validna, koristi cursor poziciju kao workaround
        if not tray_geo.isValid() or tray_geo.width() == 0 or tray_geo.height() == 0:
            logger.debug("Invalid tray geometry, using cursor position")
            cursor_pos = QCursor.pos()
            
            # Na Linux-u, tray je obično u donjem desnom uglu
            screen = QApplication.primaryScreen()
            screen_geo = screen.availableGeometry()
            
            # Kreiraj estimiranu tray geometriju
            tray_width = 32  # Tipična širina tray ikone
            tray_height = 32  # Tipična visina
            
            # Ako je cursor u donjem delu ekrana, koristi cursor
            if cursor_pos.y() > screen_geo.height() * 0.7:
                logger.debug("Using cursor position (in bottom area)")
                x = cursor_pos.x() - tray_width // 2
                y = screen_geo.bottom() - tray_height - 5
            else:
                # Inače, koristi donji desni ugao
                logger.debug("Using bottom-right corner")
                x = screen_geo.right() - tray_width - 5
                y = screen_geo.bottom() - tray_height - 5
            
            tray_geo = QRect(x, y, tray_width, tray_height)
        
        logger.debug(f"Final tray position: {tray_geo}")
        return tray_geo
    
    def _show_menu(self):
        """Show menu at appropriate position"""
        if not self.menu:
            logger.warning("No menu to show!")
            return
        
        # Dobij poziciju tray ikone
        tray_geo = self._get_tray_position()
        
        # Dobij stvarnu visinu menija
        # adjustSize() forsira Qt da izračuna layout prije sizeHint()
        self.menu.adjustSize()
        menu_height = self.menu.sizeHint().height()
        # Sanity check - pri prvom pozivu Qt može vratiti preveliku vrijednost
        screen = QApplication.primaryScreen()
        if screen:
            max_h = screen.availableGeometry().height() - 100
            if menu_height > max_h:
                menu_height = max_h
        logger.debug(f"Menu height: {menu_height}px")
        
        # Izračunaj poziciju menija koristeći stvarnu visinu
        position = MenuPositioner.calculate_position(tray_geo, menu_height)
        
        logger.debug(f"Showing menu at: {position}")
        
        
        # Prikaži meni
        self.menu.popup(position)
        
        # Fokusiraj meni
        self.menu.setFocus()
    
    # ============ Icon Management ============
    
    def _find_icon_path(self, icon_name: str) -> str:
        """Find icon file path - prioritizuj lokalne development resurse"""
        paths_to_check = []
        
        # 1. Prvo proveri lokalne development resurse (najvažnije za development)
        try:
            # Dobij base direktorijum gde se nalazi ovaj fajl
            current_file_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Različite moguće lokacije u development okruženju
            dev_paths = [
                # Lokacija kada se pokreće iz traywave/ui/ foldera
                os.path.join(current_file_dir, "..", "..", "resources", "icons", icon_name),
                # Lokacija kada se pokreće iz root foldera projekta
                os.path.join(os.getcwd(), "resources", "icons", icon_name),
                # Lokacija kada se pokreće preko run.py iz root foldera
                os.path.join(os.path.dirname(sys.argv[0]), "resources", "icons", icon_name),
                # Apsolutna putanja za development (zameni /home/alen sa tvojom putanjom)
                os.path.expanduser(f"~/traywave/resources/icons/{icon_name}"),
            ]
            
            for dev_path in dev_paths:
                dev_path = os.path.abspath(dev_path)
                if os.path.exists(dev_path):
                    paths_to_check.append(('DEVELOPMENT resources', dev_path))
                    logger.debug(f"Found development path: {dev_path}")
        except Exception as e:
            logger.debug(f"Error checking development paths: {e}")
        
        # 2. Proveri user .local folder
        user_local_path = os.path.expanduser(f"~/.local/share/traywave/icons/{icon_name}")
        if os.path.exists(user_local_path):
            paths_to_check.append(('User local', user_local_path))
        
        # 3. Package resources (za instaliranu verziju)
        try:
            from importlib.resources import files
            pkg_path = str(files('traywave.resources.icons').joinpath(icon_name))
            paths_to_check.append(('Package resources', pkg_path))
        except Exception as e:
            # Ovo je ok za development
            pass
        
        # 4. Sistemske lokacije (samo kao fallback)
        system_paths = [
            (f"/usr/share/traywave/icons/{icon_name}", 'System traywave'),
            (f"/usr/share/icons/hicolor/128x128/apps/{icon_name}", 'Hicolor 128x128'),
            (f"/usr/local/share/traywave/icons/{icon_name}", 'Local traywave'),
        ]
        paths_to_check.extend(system_paths)
        
        # Proveri sve putanje
        for source, path in paths_to_check:
            if os.path.exists(path):
                # Proveri da li je PNG fajl validan
                if path.lower().endswith('.png'):
                    try:
                        from PyQt6.QtGui import QPixmap
                        pixmap = QPixmap(path)
                        if pixmap.isNull():
                            logger.debug(f"PNG file exists but is invalid/corrupted: {path}")
                            continue
                    except Exception:
                        pass
                logger.debug(f"Using icon from: {source} ({path})")
                return path
        
        # Ako ništa nije pronađeno
        logger.warning(f"Icon {icon_name!r} not found in any location")
        
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
                logger.debug(f"Tray icon {icon_name!r} loaded")
                return
            else:
                logger.warning(f"Icon {icon_name!r} at {icon_path} failed to load")
        
        # Fallback to theme icon
        fallback_icon = QIcon.fromTheme(fallback, QIcon.fromTheme("audio-radio"))
        self.setIcon(fallback_icon)
        logger.debug(f"Using fallback theme icon: {fallback}")
        
        # Ako koristimo fallback, probaj da kreiraš ikonicu
        self._try_create_icons()
    
    def _try_create_icons(self):
        """Try to create icons if they don't exist"""
        logger.debug("Attempting to create missing icons...")
        
        # Proveri da li resources folder postoji
        resources_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "resources", "icons")
        os.makedirs(resources_dir, exist_ok=True)
        
        # Proveri koje ikonice nedostaju
        required_icons = ["traywave-playing.png", "traywave-stopped.png", "traywave-muted.png"]
        missing_icons = []
        
        for icon in required_icons:
            icon_path = os.path.join(resources_dir, icon)
            if not os.path.exists(icon_path):
                missing_icons.append(icon)
        
        if missing_icons:
            logger.warning(f"Missing icons: {missing_icons}")
            logger.warning("Run: python create_icons.py in project root to generate icons")
        else:
            logger.debug("All icons exist in resources folder")
    
    # ============ Timers ============
    
    def _setup_timers(self):
        """Setup various timers"""
        # Status update timer
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self._update_tooltip)
        self.status_timer.start(5000)
        
        # Mouse position timer
        self.mouse_timer = QTimer()
        self.mouse_timer.timeout.connect(self._check_mouse_position)
        self.mouse_timer.start(100)
        
        self.last_scroll_time = 0
        self.is_mouse_in_tray = False
        
        # Install event filter for scroll
        app = QApplication.instance()
        app.installEventFilter(self)
    
    def _check_mouse_position(self):
        """Check if mouse is in tray area"""
        self.is_mouse_in_tray = is_mouse_in_tray_area(70)
    
    # ============ SLEEP TIMER HANDLING ============
    
    def _on_sleep_timer_changed(self, is_active: bool, minutes_left: int):
        """Handle sleep timer changes from engine"""
        logger.debug(f"Sleep timer changed: active={is_active}, minutes_left={minutes_left}")
        self.sleep_timer_active = is_active
        self.sleep_minutes_left = minutes_left
        self._update_tooltip()
    
    # ============ Event Handlers ============
    
    def _on_tray_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            # Left click - show menu
            self._show_menu()
        elif reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            # Double click - volume popup
            self.popup.show_at_cursor()
        elif reason == QSystemTrayIcon.ActivationReason.MiddleClick:
            # Middle click - volume popup
            self.popup.show_at_cursor()
    
    def eventFilter(self, obj, event):
        """Global event filter for scroll events"""
        if event.type() == event.Type.Wheel:
            if self.is_mouse_in_tray and not self.popup.isVisible():
                import time as _time
                current_time = int(_time.monotonic() * 1000)
                if current_time - self.last_scroll_time > 100:
                    self.last_scroll_time = current_time
                    
                    delta = 5 if event.angleDelta().y() > 0 else -5
                    self.engine.change_volume(delta)
                    return True
        return False
    
    def _on_metadata_changed(self, artist: str, title: str):
        """Handle metadata changes"""
        self.now_playing_artist = artist
        self.now_playing_title = title
        self._update_tooltip()
        
        # Update menu header
        if self.menu_builder.menu_header:
            self.menu_builder.update_header(
                station=self.engine.current_station,
                artist=artist,
                title=title
            )
    
    # ============ UI Actions ============
    
    def _open_settings(self):
        """Open settings dialog"""
        if self.menu and self.menu.isVisible():
            self.menu.close()
        
        dialog = StyleSettingsDialog(self.stations_manager, self, self.menu)
        # Poveži signal za direktno osvežavanje
        dialog.stations_modified.connect(self._rebuild_menu)
        dialog.exec()
    
    def _open_about(self):
        """Open about dialog"""
        dialog = AboutDialog(self.menu)
        dialog.exec()
    
    def _set_sleep_timer(self, minutes: int):
        """Set sleep timer from tray menu"""
        logger.debug(f"Setting sleep timer: {minutes} minutes")
        self.engine.set_sleep_timer(minutes, False)
        
        # Prikaži notifikaciju
        self.showMessage(
            "Sleep Timer",
            f"⏰ Radio will stop in {minutes} minutes",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )
    
    def _cancel_sleep_timer(self):
        """Cancel active sleep timer"""
        logger.debug("Cancelling sleep timer")
        self.engine.cancel_sleep_timer()
        
        # Prikaži notifikaciju
        self.showMessage(
            "Sleep Timer",
            "❌ Sleep timer cancelled",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )
    
    def _toggle_mute(self):
        """Toggle mute"""
        is_muted = self.engine.toggle_mute()
        if self.mute_action:
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
        
        # Dodaj sleep timer info ako postoji
        if self.sleep_timer_active and self.sleep_minutes_left > 0:
            status += f"\n⏰ Sleep timer: {self.sleep_minutes_left} min left"
        
        vol = self.engine.get_volume()
        muted = " (Muted)" if self.engine.is_muted() else ""
        self.setToolTip(f"TrayWave\n{status}\nVolume: {vol}%{muted}")
    
    def _quit(self):
        """Quit application"""
        self.engine.stop()
        QApplication.quit()