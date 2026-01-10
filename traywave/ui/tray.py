"""
Main tray icon and application
"""
import os
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import Qt, QTimer
from ..core.engine import AudioEngine
from ..core.stations import StationsManager
from ..ui.popups import VolumePopup
from ..ui.dialogs import SettingsDialog
from ..utils.geometry import is_mouse_in_tray_area

class TrayWave(QSystemTrayIcon):
    """Main system tray application"""
    
    def __init__(self):
        super().__init__()
        
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
        
        # Initial setup
        self._update_icon()
        self.setToolTip("TrayWave - Radio Player")
        
        # Build context menu
        self._build_menu()
        
        # Connect signals
        self.activated.connect(self.on_tray_activated)
        
        # Setup timers
        self.setup_timers()
        
        # Show tray icon
        self.show()
        
    def setup_timers(self):
        """Setup various timers"""
        # Tooltip update timer
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self._update_tooltip)
        self.status_timer.start(5000)  # Update every 5 seconds
        
        # Mouse tracking for scroll events
        self.mouse_timer = QTimer()
        self.mouse_timer.timeout.connect(self._check_mouse_position)
        self.mouse_timer.start(100)  # Check every 100ms
        
        self.last_scroll_time = 0
        self.is_mouse_in_tray = False
        
        # Install global event filter for scroll
        app = QApplication.instance()
        app.installEventFilter(self)
    
    def _build_menu(self):
        """Build the context menu"""
        self.menu = QMenu()
        
        # Now Playing header - EXTENDED VERSION
        if self.engine.current_station:
            header = self.menu.addAction(f"🎵 Now playing:")
            header.setEnabled(False)
            
            # Station info
            station_info = self.menu.addAction(f"    📻 {self.engine.current_station}")
            station_info.setEnabled(False)
            
            # Show song if available
            if self.now_playing_title:
                if self.now_playing_artist:
                    # Has both artist and title
                    song_line = self.menu.addAction(f"    🎵 {self.now_playing_artist} - {self.now_playing_title}")
                else:
                    # Only title
                    song_line = self.menu.addAction(f"    🎵 {self.now_playing_title}")
                song_line.setEnabled(False)
                # Add separator after song
                self.menu.addSeparator()
            else:
                # No song, just separator
                self.menu.addSeparator()
        else:
            # Nothing is playing
            self.menu.addSeparator()
        
        # Radio Categories
        for category, stations in self.stations_manager.stations.items():
            if stations:  # Only if category has stations
                self._add_category_menu(category, stations)
        
        self.menu.addSeparator()
        
        # Sleep Timer submenu
        sleep_menu = QMenu("Sleep timer ▶", self.menu)
        sleep_menu.addAction("15 minutes", lambda: self._set_sleep_timer(15))
        sleep_menu.addAction("30 minutes", lambda: self._set_sleep_timer(30))
        sleep_menu.addAction("45 minutes", lambda: self._set_sleep_timer(45))
        sleep_menu.addAction("60 minutes", lambda: self._set_sleep_timer(60))
        self.menu.addMenu(sleep_menu)
        
        self.menu.addSeparator()
        
        # Settings
        self.menu.addAction("Settings", self._open_settings)
        
        self.menu.addSeparator()
        
        # Controls
        self.menu.addAction("Stop", self.engine.stop)
        self.mute_action = self.menu.addAction("Mute", self._toggle_mute)
        
        # About item with separator above
        self.menu.addSeparator()
        self.menu.addAction("About", self._open_about)
        
        self.menu.addSeparator()
        self.menu.addAction("Quit", self._quit)
        
        self.setContextMenu(self.menu)
    
    def _add_category_menu(self, category: str, stations: list):
        """Add a category submenu"""
        category_menu = QMenu(f"{category} ▶", self.menu)
        for name, url in stations:
            category_menu.addAction(name, lambda u=url, n=name: self.engine.play(u, n))
        self.menu.addMenu(category_menu)
    
    def _rebuild_menu(self):
        """Rebuild the context menu (e.g., after station change)"""
        self._build_menu()
    
    def _open_settings(self):
        """Open settings dialog"""
        dialog = SettingsDialog(self.stations_manager, self.menu)
        if dialog.exec():
            self._rebuild_menu()
    
    def _open_about(self):
        """Open About dialog"""
        from ..ui.dialogs import AboutDialog
        dialog = AboutDialog(self.menu)
        dialog.exec()
    
    def _on_metadata_changed(self, artist: str, title: str):
        """Handle metadata (song) changes"""
        self.now_playing_artist = artist
        self.now_playing_title = title
        
        # Update tooltip
        self._update_tooltip()
        
        # Rebuild menu to show new song
        self._rebuild_menu()
    
    def _set_sleep_timer(self, minutes: int):
        """Set sleep timer"""
        # TODO: Implement sleep timer
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

    def _update_icon(self):
        """Update tray icon based on state"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(script_dir, "..", "..")
        
        if self.engine.is_muted():
            base_name = "traywave-muted"
            fallback = "audio-volume-muted"
        elif self.engine.is_playing():
            base_name = "traywave-playing"
            fallback = "audio-radio"
        else:
            base_name = "traywave-stopped"
            fallback = "audio-card"
        
        icon_loaded = False
        
        # Try SVG in resources/icons
        svg_path = os.path.join(project_root, "resources", "icons", f"{base_name}.svg")
        if os.path.exists(svg_path):
            icon = QIcon(svg_path)
            if not icon.isNull() and len(icon.availableSizes()) > 0:
                self.setIcon(icon)
                icon_loaded = True
        
        # Try PNG if SVG failed
        if not icon_loaded:
            png_path = os.path.join(project_root, "resources", "icons", f"{base_name}.png")
            if os.path.exists(png_path):
                icon = QIcon(png_path)
                if not icon.isNull():
                    self.setIcon(icon)
                    icon_loaded = True
        
        # Fallback to theme icon
        if not icon_loaded:
            self.setIcon(QIcon.fromTheme(fallback, QIcon.fromTheme("audio-radio")))
    
    def _update_tooltip(self):
        """Update tray tooltip - EXTENDED VERSION"""
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
            # Handle scroll in tray area (when popup is not visible)
            if self.is_mouse_in_tray and not self.popup.isVisible():
                # Debounce: max 100ms between scroll events
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

    def on_tray_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            # Left click - show volume popup
            self.popup.show_at_cursor()
            
        elif reason == QSystemTrayIcon.ActivationReason.MiddleClick:
            # Middle click - toggle mute
            self.engine.toggle_mute()