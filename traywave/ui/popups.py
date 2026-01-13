"""
VARIJANTA 1: STATIČNA PLAVA BOJA
Popup widgets (volume popup, etc.)
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QApplication
from traywave.core.engine import AudioEngine

class VolumePopup(QWidget):
    """Popup volume control widget - Static Blue Color"""
    
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
        
        self.setFixedSize(50, 180)
        self.setStyleSheet("""
            QWidget {
                background-color: palette(window);
                border: 1px solid palette(mid);
                border-radius: 4px;
            }
            QSlider::groove:vertical {
                width: 6px;
                background: #9E9E9E;
                border-radius: 3px;
            }
            QSlider::sub-page:vertical {
                background: #9E9E9E;
                border-radius: 3px;
            }
            QSlider::add-page:vertical {
                background: #2196F3;
                border-radius: 3px;
            }
            QSlider::handle:vertical {
                height: 20px;
                width: 20px;
                background: #1976D2;
                border: 2px solid white;
                border-radius: 10px;
                margin: 0 -7px;
            }
            QLabel {
                font-size: 16pt;
                font-weight: bold;
                color: palette(text);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(7, 7, 7, 7)
        layout.setSpacing(6)
        
        self.label = QLabel("50")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFixedHeight(30)
        
        layout.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setRange(0, 100)
        self.slider.setValue(self.engine.get_volume())
        self.slider.valueChanged.connect(self._on_slider_changed)
        
        layout.addWidget(self.slider, 0, Qt.AlignmentFlag.AlignHCenter)
        
        self.engine.on_volume_changed(self.update_slider)
        
    def setup_timer(self):
        """Setup auto-hide timer"""
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide)
        self.hide_timer.setInterval(3000)

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
            
            x = cursor_pos.x() - self.width() // 2
            
            if cursor_pos.y() > geo.bottom() - 100:
                y = cursor_pos.y() - self.height() - 10
            else:
                y = cursor_pos.y() + 10
            
            x = max(geo.left() + 5, min(x, geo.right() - self.width() - 5))
            y = max(geo.top() + 5, min(y, geo.bottom() - self.height() - 5))
            
            self.move(x, y)
        else:
            self.move(cursor_pos.x() - self.width() // 2, cursor_pos.y() - self.height() - 10)
        
        self.show()
        self.raise_()
        self.activateWindow()
