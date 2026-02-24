"""
Popup widgets (volume popup, etc.) - prati aktivnu temu
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor, QPainter, QColor, QPainterPath
from traywave.core.engine import AudioEngine


class VolumePopup(QWidget):
    """Popup volume control - prati aktivnu temu"""

    def __init__(self, engine: AudioEngine):
        super().__init__()
        self.engine = engine
        self._theme = {}

        self.setup_ui()
        self.setup_timer()

    def setup_ui(self):
        self.setWindowFlags(
            Qt.WindowType.Popup |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(64, 200)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 14, 12, 14)
        layout.setSpacing(8)

        # Procenat volumena
        self.label = QLabel("50")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFixedHeight(26)

        # Slider
        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setRange(0, 100)
        self.slider.setValue(self.engine.get_volume())
        self.slider.valueChanged.connect(self._on_slider_changed)

        layout.addWidget(self.label)
        layout.addWidget(self.slider, 1, Qt.AlignmentFlag.AlignHCenter)

        self.engine.on_volume_changed(self.update_slider)

        # Primijeni default temu odmah
        self._apply_theme_css()

    def apply_theme(self, theme: dict):
        """Primijeni boje iz aktivne teme"""
        self._theme = theme
        self._apply_theme_css()

    def _apply_theme_css(self):
        menu = self._theme.get('menu', {})
        header = self._theme.get('header', {})
        item = self._theme.get('item', {})
        separator = self._theme.get('separator', {})

        bg = menu.get('background', 'rgba(30, 30, 30, 0.97)')
        accent = header.get('background', '#06b6d4')
        text_color = item.get('color', '#f0f0f0')
        border_color = separator.get('background', 'rgba(255,255,255,0.15)')
        border_radius = menu.get('border_radius', '14px')

        # Tamna/svijetla pozadina za groove
        groove_bg = self._darken_or_lighten(bg)

        self.setStyleSheet(f"""
            QWidget#volumePopup {{
                background: transparent;
            }}
            QLabel {{
                font-size: 13px;
                font-weight: bold;
                color: {text_color};
                background: transparent;
            }}
            QSlider::groove:vertical {{
                width: 6px;
                background: {groove_bg};
                border-radius: 3px;
            }}
            QSlider::sub-page:vertical {{
                background: {groove_bg};
                border-radius: 3px;
            }}
            QSlider::add-page:vertical {{
                background: {accent};
                border-radius: 3px;
            }}
            QSlider::handle:vertical {{
                width: 18px;
                height: 18px;
                background: {accent};
                border: 2px solid {bg};
                border-radius: 9px;
                margin: 0 -6px;
            }}
            QSlider::handle:vertical:hover {{
                border: 2px solid {text_color};
            }}
        """)
        self.setObjectName("volumePopup")

    def _darken_or_lighten(self, bg_color: str) -> str:
        """Vraća kontrastnu boju za groove (tamnija ili svjetlija od pozadine)"""
        # Proba parsiranja rgba/rgb
        try:
            s = bg_color.strip()
            if s.startswith('rgba(') or s.startswith('rgb('):
                parts = s.split('(')[1].split(')')[0].split(',')
                r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
                brightness = (r * 299 + g * 587 + b * 114) / 1000
                if brightness > 128:
                    return f"rgba({max(r-40,0)},{max(g-40,0)},{max(b-40,0)},0.5)"
                else:
                    return f"rgba({min(r+60,255)},{min(g+60,255)},{min(b+60,255)},0.4)"
            elif s.startswith('#') and len(s) in (7, 9):
                r = int(s[1:3], 16)
                g = int(s[3:5], 16)
                b = int(s[5:7], 16)
                brightness = (r * 299 + g * 587 + b * 114) / 1000
                if brightness > 128:
                    return f"rgba({max(r-40,0)},{max(g-40,0)},{max(b-40,0)},0.5)"
                else:
                    return f"rgba({min(r+60,255)},{min(g+60,255)},{min(b+60,255)},0.4)"
        except Exception:
            pass
        return "rgba(128, 128, 128, 0.35)"

    def paintEvent(self, event):
        """Crtanje zaobljene pozadine s blagim shadow efektom"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        menu = self._theme.get('menu', {})
        bg_str = menu.get('background', 'rgba(30, 30, 30, 0.97)')
        radius_str = menu.get('border_radius', '14px')
        separator = self._theme.get('separator', {})
        border_str = menu.get('border', '')

        # Parsiranje border-radiusa
        try:
            radius = float(radius_str.replace('px', '').strip())
        except Exception:
            radius = 14.0

        # Blagi shadow
        shadow_color = QColor(0, 0, 0, 40)
        for i in range(3):
            shadow_path = QPainterPath()
            shadow_path.addRoundedRect(2 + i, 2 + i, self.width() - 4, self.height() - 4, radius, radius)
            painter.fillPath(shadow_path, shadow_color)

        # Pozadina
        bg_color = self._parse_color(bg_str, QColor(30, 30, 30, 247))
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width() - 2, self.height() - 2, radius, radius)
        painter.fillPath(path, bg_color)

        # Border
        if border_str:
            try:
                border_color_str = border_str.split('solid')[-1].strip() if 'solid' in border_str else ''
                if border_color_str:
                    border_color = self._parse_color(border_color_str, QColor(128, 128, 128, 80))
                    from PyQt6.QtGui import QPen
                    painter.setPen(QPen(border_color, 1))
                    painter.drawPath(path)
            except Exception:
                pass

        painter.end()

    def _parse_color(self, color_str: str, fallback: QColor) -> QColor:
        """Parsira CSS color string u QColor"""
        try:
            s = color_str.strip()
            if s.startswith('rgba('):
                parts = s[5:-1].split(',')
                r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
                a = int(float(parts[3]) * 255) if len(parts) > 3 else 255
                return QColor(r, g, b, a)
            elif s.startswith('rgb('):
                parts = s[4:-1].split(',')
                return QColor(int(parts[0]), int(parts[1]), int(parts[2]))
            elif s.startswith('#'):
                c = QColor(s[:7])
                if len(s) == 9:
                    c.setAlpha(int(s[7:9], 16))
                return c
        except Exception:
            pass
        return fallback

    def setup_timer(self):
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide)
        self.hide_timer.setInterval(3000)

    def _on_slider_changed(self, value: int):
        self.engine.set_volume(value)
        self.label.setText(str(value))
        self.hide_timer.start()

    def update_slider(self, value: int):
        self.slider.blockSignals(True)
        self.slider.setValue(value)
        self.label.setText(str(value))
        self.slider.blockSignals(False)

    def showEvent(self, event):
        super().showEvent(event)
        self.hide_timer.start()

    def wheelEvent(self, event):
        delta = 5 if event.angleDelta().y() > 0 else -5
        self.engine.change_volume(delta)
        self.hide_timer.start()
        event.accept()

    def mousePressEvent(self, event):
        if not self.slider.geometry().contains(event.pos()):
            self.hide()
        super().mousePressEvent(event)

    def enterEvent(self, event):
        self.hide_timer.stop()

    def leaveEvent(self, event):
        self.hide_timer.start()

    def show_at_cursor(self):
        """Prikaži popup pozicioniran iznad tray ikone"""
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