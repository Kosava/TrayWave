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
        
        # Icon source tracking
        self._icon_source_logged = False
        
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
    
    def _find_icon_path(self, icon_name: str) -> str:
        """
        Find icon file path - works for both development and installed package
        Returns absolute path or None
        
        Search order (IMPORTANT - installed paths first!):
        1. Package resources (pip/AUR installed)
        2. System-wide paths (AUR installation)
        3. Development paths (running from source)
        """
        paths_to_check = []
        
        # 1. Try package resources FIRST (for installed package)
        try:
            from importlib.resources import files
            icon_path = str(files('traywave.resources.icons').joinpath(icon_name))
            paths_to_check.append(('Package resources', icon_path))
        except Exception:
            pass
        
        # 2. System-wide installation paths (AUR installs here)
        system_paths = [
            (f"/usr/share/traywave/icons/{icon_name}", 'System traywave'),
            (f"/usr/share/icons/hicolor/128x128/apps/{icon_name}", 'Hicolor 128x128'),
            (f"/usr/share/icons/hicolor/scalable/apps/{icon_name.replace('.png', '.svg')}", 'Hicolor scalable'),
            (f"/usr/local/share/traywave/icons/{icon_name}", 'Local traywave'),
        ]
        for path, desc in system_paths:
            paths_to_check.append((desc, path))
        
        # 3. Development paths (running from source) - LAST
        # From traywave/ui/tray.py go up to project root
        try:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
            paths_to_check.append(('Project root', os.path.join(project_root, 'resources', 'icons', icon_name)))
            
            # traywave/resources/icons/
            traywave_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            paths_to_check.append(('Traywave dev', os.path.join(traywave_dir, 'resources', 'icons', icon_name)))
        except Exception:
            pass
        
        # Check each path
        for source, path in paths_to_check:
            if os.path.exists(path):
                # Log source only once per session
                if not self._icon_source_logged:
                    print(f"✓ Loading icons from: {source}")
                    print(f"  Example: {path}")
                    self._icon_source_logged = True
                return path
        
        # Icon not found - show debug info
        print(f"✗ Icon not found: {icon_name}")
        print(f"  Searched {len(paths_to_check)} locations:")
        for source, path in paths_to_check[:5]:
            print(f"    [{source}] {path}")
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
        
        # Try PNG first
        icon_path = self._find_icon_path(icon_name)
        
        if icon_path:
            icon = QIcon(icon_path)
            if not icon.isNull():
                self.setIcon(icon)
                return
        
        # Try SVG version
        svg_name = icon_name.replace('.png', '.svg')
        svg_path = self._find_icon_path(svg_name)
        
        if svg_path:
            icon = QIcon(svg_path)
            if not icon.isNull():
                self.setIcon(icon)
                return
        
        # Final fallback to theme icon
        if not self._icon_source_logged:
            print(f"⚠ Using system theme icon: {fallback}")
        self.setIcon(QIcon.fromTheme(fallback, QIcon.fromTheme("audio-radio")))
    
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
        
        # Now Playing header
        if self.engine.current_station:
            header = self.menu.addAction(f"🎵 Now playing:")
            header.setEnabled(False)
            
            # Station info
            station_info = self.menu.addAction(f"    📻 {self.engine.current_station}")
            station_info.setEnabled(False)
            
            # Show song if available
            if self.now_playing_title:
                if self.now_playing_artist:
                    song_line = self.menu.addAction(f"    🎵 {self.now_playing_artist} - {self.now_playing_title}")
                else:
                    song_line = self.menu.addAction(f"    🎵 {self.now_playing_title}")
                song_line.setEnabled(False)
                self.menu.addSeparator()
            else:
                self.menu.addSeparator()
        else:
            self.menu.addSeparator()
        
        # Radio Categories
        for category, stations in self.stations_manager.stations.items():
            if stations:
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
        
        # About
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
        """Rebuild the context menu"""
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
        self._update_tooltip()
        self._rebuild_menu()
    
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

    def on_tray_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.popup.show_at_cursor()
        elif reason == QSystemTrayIcon.ActivationReason.MiddleClick:
            self.engine.toggle_mute()