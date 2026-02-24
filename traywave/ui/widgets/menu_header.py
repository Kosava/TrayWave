"""
Menu header widget - FANCY VERSION with gradients and shadows
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class MenuHeader(QWidget):
    """Header widget for tray menu - fancy styled with gradients"""
    
    def __init__(self):
        super().__init__()
        self._text_color = "white"
        self._background = "#06b6d4"
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize UI"""
        self.setFixedHeight(90)
        self.setContentsMargins(0, 0, 0, 0)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(2)
        
        # Naziv stanice — manji, diskretni tekst
        self.station_label = QLabel("🎵 TrayWave Radio")
        self.station_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.station_label.setWordWrap(False)
        
        # Artist — veći, bold
        self.artist_label = QLabel("")
        self.artist_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.artist_label.setWordWrap(False)
        
        # Song title — veći, italic
        self.now_playing = QLabel("No station playing")
        self.now_playing.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.now_playing.setWordWrap(False)
        
        layout.addWidget(self.station_label)
        layout.addWidget(self.artist_label)
        layout.addWidget(self.now_playing)
    
    def apply_theme(self, background: str, text_color: str, padding: str, 
                    border_radius: str, border_bottom: str, item_color: str = None):
        """Apply complete theme to header with fancy styling"""
        # Koristimo item_color ako je prosleđen, inače text_color
        self._text_color = item_color if item_color else text_color
        self._background = background
        
        # Kreiramo gradient efekat
        # Uzimamo base boju i pravimo svetliju i tamniju varijantu
        gradient_style = self._create_gradient_style(background, border_radius, border_bottom)
        
        self.setStyleSheet(gradient_style)
        self._update_label_styles()
    
    def _create_gradient_style(self, base_color: str, border_radius: str, border_bottom: str) -> str:
        """Create subtle gradient style"""
        # Suptilniji gradient - samo 8% razlike
        gradient = f"""
            MenuHeader {{
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 {base_color},
                    stop:1 {self._darken_color(base_color, 0.08)}
                );
                border-radius: {border_radius};
                {f'border-bottom: {border_bottom};' if border_bottom else ''}
                padding: 0px;
            }}
        """
        return gradient
    
    def _darken_color(self, color: str, factor: float) -> str:
        """Darken a hex color by factor (0.0 to 1.0)"""
        # Ako je hex color
        if color.startswith('#') and len(color) == 7:
            try:
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
                
                r = int(r * (1 - factor))
                g = int(g * (1 - factor))
                b = int(b * (1 - factor))
                
                return f"#{r:02x}{g:02x}{b:02x}"
            except:
                pass
        
        # Fallback
        return color
    
    def _update_label_styles(self):
        """Update label styles"""
        # Naziv stanice — mali, diskretni
        self.station_label.setStyleSheet(f"""
            QLabel {{
                font-size: 10px;
                color: {self._text_color};
                background: transparent;
                padding: 0px;
                opacity: 0.75;
            }}
        """)
        
        # Artist — bold, veći
        self.artist_label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                font-weight: bold;
                color: {self._text_color};
                background: transparent;
                padding: 0px;
            }}
        """)
        
        # Song title — italic, malo manji od artista
        self.now_playing.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                font-style: italic;
                color: {self._text_color};
                background: transparent;
                padding: 0px;
            }}
        """)
    
    def update_content(self, station=None, artist=None, title=None):
        """Update header content"""
        if station:
            display_station = station[:32] + "..." if len(station) > 32 else station
            self.station_label.setText(f"🎵 {display_station}")
            
            if artist:
                display_artist = artist[:28] + "..." if len(artist) > 28 else artist
                self.artist_label.setText(display_artist)
            else:
                self.artist_label.setText("")
            
            if title:
                display_title = title[:30] + "..." if len(title) > 30 else title
                self.now_playing.setText(f"♪ {display_title}")
            elif artist:
                self.now_playing.setText("")
            else:
                self.now_playing.setText("♪ Now playing...")
        else:
            self.station_label.setText("🎵 TrayWave Radio")
            self.artist_label.setText("")
            self.now_playing.setText("No station playing")
        
        self._update_label_styles()