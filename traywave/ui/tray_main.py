"""
Main tray icon application
"""
import os
import json
from PyQt6.QtWidgets import QSystemTrayIcon, QApplication
from PyQt6.QtGui import QIcon, QCursor, QShortcut, QKeySequence
from PyQt6.QtCore import Qt, QTimer

# Fixed imports - use absolute imports from traywave package
from traywave.core.engine import AudioEngine
from traywave.core.stations import StationsManager
from traywave.ui.popups import VolumePopup
from traywave.ui.dialogs import StyleSettingsDialog, AboutDialog
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
        
        # Icon tracking
        self._icon_source_logged = False
        
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
        except:
            pass
        return 'teal'
    
    def _save_style(self, style_name: str):
        """Save style to config"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump({'style': style_name}, f)
        except:
            pass
    
    # ============ Menu Management ============
    
    def _rebuild_menu(self):
        """Rebuild the menu completely"""
        print(f"\n🔄 Rebuilding menu with style: {self.current_style}")
        
        # Cleanup old menu
        if self.menu:
            try:
                self.menu.hide()
                self.menu.clear()
                self.menu.deleteLater()
                self.menu = None
                QApplication.processEvents()
            except Exception as e:
                print(f"⚠️  Error deleting menu: {e}")
        
        # Build new menu
        self.menu = self.menu_builder.build_menu(self.current_style)
        
        # Connect menu signals
        self.menu.aboutToShow.connect(lambda: print("📋 Menu showing..."))
        self.menu.aboutToHide.connect(lambda: print("📋 Menu hiding..."))
        
        print(f"✅ Menu rebuilt")
    
    def change_menu_style(self, style_name: str):
        """Change menu style"""
        if style_name == self.current_style:
            return
        
        old_style = self.current_style
        self.current_style = style_name
        self._save_style(style_name)
        
        print(f"\n🎨 CHANGING STYLE: '{old_style}' → '{style_name}'")
        
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
        
        print(f"   ✅ Style change complete!")
    
    def _show_menu(self):
        """Show menu at appropriate position"""
        if not self.menu:
            return
        
        position = MenuPositioner.calculate_position(self.geometry())
        
        print(f"\n📋 Showing menu at: {position}")
        self.menu.popup(position)
    
    # ============ Icon Management ============
    
    def _find_icon_path(self, icon_name: str) -> str:
        """Find icon file path"""
        paths_to_check = []
        
        # Package resources
        try:
            from importlib.resources import files
            icon_path = str(files('traywave.resources.icons').joinpath(icon_name))
            paths_to_check.append(('Package resources', icon_path))
        except Exception:
            pass
        
        # System paths
        system_paths = [
            (f"/usr/share/traywave/icons/{icon_name}", 'System traywave'),
            (f"/usr/share/icons/hicolor/128x128/apps/{icon_name}", 'Hicolor 128x128'),
            (f"/usr/local/share/traywave/icons/{icon_name}", 'Local traywave'),
        ]
        paths_to_check.extend(system_paths)
        
        # Development paths
        try:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            paths_to_check.append(('Project root', os.path.join(project_root, 'resources', 'icons', icon_name)))
        except Exception:
            pass
        
        # Check paths
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
        
        # Fallback to theme icon
        self.setIcon(QIcon.fromTheme(fallback, QIcon.fromTheme("audio-radio")))
    
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
        print(f"⏰ Sleep timer changed: active={is_active}, minutes_left={minutes_left}")
        self.sleep_timer_active = is_active
        self.sleep_minutes_left = minutes_left
        self._update_tooltip()
    
    # ============ Event Handlers ============
    
    def _on_tray_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            # Left click - show menu
            self._show_menu()
        elif reason == QSystemTrayIcon.ActivationReason.Context:
            # Right click - show menu
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
                current_time = QTimer.currentTime().msec()
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
        print(f"⏰ Setting sleep timer: {minutes} minutes")
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
        print("⏰ Cancelling sleep timer")
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