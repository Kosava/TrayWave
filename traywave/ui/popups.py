"""
Popup widgets (volume popup, etc.)
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor
from ..core.engine import AudioEngine
from ..utils.geometry import center_popup_near_cursor

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
        
        self.setFixedSize(40, 160)
        self.setStyleSheet("""
            QWidget {
                background-color: palette(window);
                border: 1px solid palette(mid);
                border-radius: 3px;
            }
            QSlider::groove:vertical {
                width: 6px;
                background: palette(dark);
                border-radius: 3px;
            }
            QSlider::handle:vertical {
                height: 16px;
                background: palette(highlight);
                border-radius: 8px;
                margin: 0 -5px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        
        self.label = QLabel("50%")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setRange(0, 100)
        self.slider.setValue(self.engine.get_volume())
        self.slider.valueChanged.connect(self._on_slider_changed)
        
        layout.addWidget(self.slider)
        
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
        self.label.setText(f"{value}%")
        self.hide_timer.start()

    def update_slider(self, value: int):
        """Update slider from external volume change"""
        self.slider.blockSignals(True)
        self.slider.setValue(value)
        self.label.setText(f"{value}%")
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
        """Show popup positioned near cursor"""
        pos = center_popup_near_cursor(self.width(), self.height())
        self.move(pos)
        self.show()
        self.raise_()
        self.activateWindow()