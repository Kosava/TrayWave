"""
Popup widgets (volume popup, etc.)
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QApplication
from ..core.engine import AudioEngine

class VolumePopup(QWidget):
    """Popup volume control widget"""
    
    def __init__(self, engine: AudioEngine):
        super().__init__()
        self.engine = engine
        
        self.setup_ui()
        self.setup_timer()
        
    def setup_ui(self):
        """Initialize UI components"""
        self.setWindowFlags(
            Qt.WindowType.Popup | 
            Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        
        # Kompaktnija veličina
        self.setFixedSize(50, 180)
        self.setStyleSheet("""
            QWidget {
                background-color: palette(window);
                border: 2px solid palette(mid);
                border-radius: 4px;
            }
            QSlider::groove:vertical {
                width: 4px;
                background: palette(dark);
                border-radius: 2px;
            }
            QSlider::handle:vertical {
                height: 14px;
                background: palette(highlight);
                border-radius: 7px;
                margin: 0 -5px;
            }
            QLabel {
                font-size: 14pt;
                font-weight: bold;
                color: palette(text);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(7, 7, 7, 7)
        layout.setSpacing(6)
        
        # Minimalistička labela
        self.label = QLabel("50")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFixedHeight(30)
        
        layout.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setRange(0, 100)
        self.slider.setValue(self.engine.get_volume())
        self.slider.valueChanged.connect(self._on_slider_changed)
        
        layout.addWidget(self.slider, 0, Qt.AlignmentFlag.AlignHCenter)
        
        # Connect engine volume changes to slider
        self.engine.on_volume_changed(self.update_slider)
        
    def setup_timer(self):
        """Setup auto-hide timer"""
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide)
        self.hide_timer.setInterval(3000)  # 3 seconds

    def _on_slider_changed(self, value: int):
        """Handle slider value change"""
        self.engine.set_volume(value)
        self.label.setText(f"{value}")
        self.hide_timer.start()

    def update_slider(self, value: int):
        """Update slider from external volume change"""
        self.slider.blockSignals(True)
        self.slider.setValue(value)
        self.label.setText(f"{value}")
        self.slider.blockSignals(False)

    def showEvent(self, event):
        """Start hide timer when shown"""
        super().showEvent(event)
        self.hide_timer.start()
        
    def wheelEvent(self, event):
        """Handle mouse wheel scroll"""
        delta = 5 if event.angleDelta().y() > 0 else -5
        self.engine.change_volume(delta)
        self.hide_timer.start()
        event.accept()

    def mousePressEvent(self, event):
        """Hide when clicking outside slider"""
        if not self.slider.geometry().contains(event.pos()):
            self.hide()
        super().mousePressEvent(event)
    
    def enterEvent(self, event):
        """Pause hide timer when mouse enters"""
        self.hide_timer.stop()
        
    def leaveEvent(self, event):
        """Resume hide timer when mouse leaves"""
        self.hide_timer.start()
    
    def show_at_cursor(self):
        """Show popup positioned near tray icon"""
        cursor_pos = QCursor.pos()
        screen = QApplication.screenAt(cursor_pos)
        
        if screen:
            geo = screen.availableGeometry()
            
            # Centriraj horizontalno u odnosu na kursor
            x = cursor_pos.x() - self.width() // 2
            
            # Proveri da li je kursor u donjem delu ekrana (tray area)
            if cursor_pos.y() > geo.bottom() - 100:
                # Kursor je blizu panela - prikaži popup iznad
                y = cursor_pos.y() - self.height() - 10
            else:
                # Kursor je negde drugde - prikaži popup ispod
                y = cursor_pos.y() + 10
            
            # Drži popup unutar ekrana
            x = max(geo.left() + 5, min(x, geo.right() - self.width() - 5))
            y = max(geo.top() + 5, min(y, geo.bottom() - self.height() - 5))
            
            self.move(x, y)
        else:
            # Fallback: jednostavno pozicioniranje
            self.move(cursor_pos.x() - self.width() // 2, cursor_pos.y() - self.height() - 10)
        
        self.show()
        self.raise_()
        self.activateWindow()
