"""
About dialog for TrayWave.
"""

import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame
)
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt
from .base_dialog import BaseDialog, DialogWithIcon


class AboutDialog(DialogWithIcon):
    """About dialog."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About TrayWave")
        self.setFixedSize(400, 500)
        self.setModal(True)
        
        # OBAVEZNO: Postavi ikonu
        self._set_window_icon("traywave-playing.png")
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize about dialog UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # Logo/Title
        title_layout = QHBoxLayout()
        
        # Logo icon - koristimo BaseDialog metodu
        logo_label = QLabel()
        
        # Pronađi ikonu koristeći nasljeđenu metodu iz BaseDialog
        icon_path = self._find_local_icon("traywave-playing.png")
        
        if icon_path and os.path.exists(icon_path):
            try:
                pixmap = QPixmap(icon_path)
                if not pixmap.isNull():
                    scaled = pixmap.scaled(64, 64, 
                                         Qt.AspectRatioMode.KeepAspectRatio,
                                         Qt.TransformationMode.SmoothTransformation)
                    logo_label.setPixmap(scaled)
                    print(f"✅ Logo loaded from: {icon_path}")
                else:
                    self._set_fallback_logo(logo_label)
            except Exception as e:
                print(f"⚠️ Error loading logo: {e}")
                self._set_fallback_logo(logo_label)
        else:
            self._set_fallback_logo(logo_label)
        
        logo_label.setFixedSize(70, 70)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(logo_label)
        
        # Title text
        title_container = QVBoxLayout()
        title = QLabel("TrayWave")
        title.setFont(QFont("", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #06b6d4;")
        
        subtitle = QLabel("Radio player for your system tray")
        subtitle.setFont(QFont("", 10))
        subtitle.setStyleSheet("color: #6b7280;")
        
        title_container.addWidget(title)
        title_container.addWidget(subtitle)
        title_layout.addLayout(title_container)
        
        layout.addLayout(title_layout)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("border: 1px solid #e5e7eb; margin: 15px 0px;")
        layout.addWidget(separator)
        
        # Info text
        info_text = """
        <div style="font-size: 11px; color: #374151; line-height: 1.6;">
        <p><b>Version:</b> 0.2.0</p>
        <p><b>Description:</b> A modern system tray radio player with support for multiple stations and custom styles.</p>
        <p><b>Features:</b></p>
        <ul>
            <li>🎵 Stream online radio stations</li>
            <li>🎨 Customizable menu styles</li>
            <li>⚡ Sleep timer functionality</li>
            <li>🔔 Song notifications</li>
            <li>📻 Station management</li>
        </ul>
        <p><b>Keyboard Shortcuts:</b></p>
        <ul>
            <li>Ctrl+M: Open/Close menu</li>
            <li>Mouse wheel over tray: Adjust volume</li>
            <li>Double/Middle click: Volume control</li>
        </ul>
        <p><b>GitHub:</b> <a href="https://github.com/yourusername/traywave">github.com/yourusername/traywave</a></p>
        </div>
        """
        
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setTextFormat(Qt.TextFormat.RichText)
        info_label.setOpenExternalLinks(True)
        layout.addWidget(info_label)
        
        # License info
        license_label = QLabel("© 2024 TrayWave. Released under MIT License.")
        license_label.setFont(QFont("", 8))
        license_label.setStyleSheet("color: #9ca3af; margin-top: 15px;")
        license_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(license_label)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.setFixedSize(120, 35)
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #06b6d4;
                color: white;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0891b2;
            }
        """)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Set dialog style
        self.setStyleSheet("""
            QDialog {
                background-color: #fafafa;
            }
            QLabel {
                background-color: transparent;
            }
        """)