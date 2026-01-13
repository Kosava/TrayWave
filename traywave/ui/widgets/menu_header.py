"""
Menu header widget
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont


class MenuHeader(QWidget):
    """Custom header widget for the tray menu"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        # Set maximum width to prevent menu stretching
        self.setMaximumWidth(280)
        
        # Now playing label
        self.now_playing_label = QLabel("♪ Now playing:")
        self.now_playing_label.setFont(QFont("", 9, QFont.Weight.Bold))
        self.now_playing_label.setWordWrap(True)
        
        # Station label
        self.station_label = QLabel("📻 TrayWave")
        self.station_label.setFont(QFont("", 11, QFont.Weight.DemiBold))
        self.station_label.setWordWrap(True)
        
        # Song label
        self.song_label = QLabel("")
        self.song_label.setFont(QFont("", 10))
        self.song_label.setVisible(False)
        self.song_label.setWordWrap(True)
        
        layout.addWidget(self.now_playing_label)
        layout.addWidget(self.station_label)
        layout.addWidget(self.song_label)
    
    def update_content(self, station=None, artist=None, title=None):
        """Update header content with current playback info"""
        # Update station
        if station:
            self.station_label.setText(f"📻 {station}")
            self.station_label.setVisible(True)
        else:
            self.station_label.setText("📻 TrayWave")
        
        # Update song info
        if title:
            if artist:
                self.song_label.setText(f"🎵 {artist} - {title}")
            else:
                self.song_label.setText(f"🎵 {title}")
            self.song_label.setVisible(True)
        else:
            self.song_label.setVisible(False)
    
    def clear(self):
        """Clear all content"""
        self.station_label.setText("📻 TrayWave")
        self.song_label.setText("")
        self.song_label.setVisible(False)