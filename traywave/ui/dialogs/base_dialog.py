"""
Base dialog classes with common functionality.
"""

import logging
import os
import sys
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import Qt

logger = logging.getLogger(__name__)


class BaseDialog(QDialog):
    """Base dialog with common functionality like window icon setting."""
    
    def _set_window_icon(self, icon_name="traywave-playing.png"):
        """Set window icon for dialog."""
        try:
            current_file = os.path.abspath(__file__)
            current_dir = os.path.dirname(current_file)
            
            icon_paths = [
                os.path.join(current_dir, "..", "..", "resources", "icons", icon_name),
                os.path.join(current_dir, "..", "..", "traywave", "resources", "icons", icon_name),
                os.path.join(current_dir, "..", "..", "..", "resources", "icons", icon_name),
                os.path.join(os.getcwd(), "resources", "icons", icon_name),
                os.path.join(os.getcwd(), "traywave", "resources", "icons", icon_name),
                f"/usr/share/traywave/icons/{icon_name}",
                f"/usr/local/share/traywave/icons/{icon_name}",
                os.path.join(os.getcwd(), icon_name),
            ]
            
            try:
                import traywave
                package_dir = os.path.dirname(traywave.__file__)
                icon_paths.append(os.path.join(package_dir, "resources", "icons", icon_name))
            except ImportError:
                pass
            
            for icon_path in icon_paths:
                abs_path = os.path.abspath(icon_path)
                if os.path.exists(abs_path):
                    icon = QIcon(abs_path)
                    if not icon.isNull():
                        self.setWindowIcon(icon)
                        logger.debug(f"Window icon set from: {abs_path}")
                        return True
                    else:
                        logger.debug(f"Icon file exists but could not load: {abs_path}")
            
            logger.debug(f"Icon '{icon_name}' not found, using fallback")
            return self._set_fallback_icon()
            
        except Exception as e:
            logger.debug(f"Error setting window icon: {e}")
            return self._set_fallback_icon()
    
    def _set_fallback_icon(self):
        """Set fallback icon."""
        try:
            icon = QIcon.fromTheme("audio-x-generic")
            if not icon.isNull():
                self.setWindowIcon(icon)
                return True
        except Exception:
            pass
        return False


class DialogWithIcon(BaseDialog):
    """Dialog with header containing icon and title."""
    
    def create_header(self, title_text, subtitle_text="", icon_size=48):
        """Create a dialog header with icon, title and subtitle."""
        layout = QVBoxLayout()
        
        header_layout = QVBoxLayout()
        header_layout.setSpacing(10)
        
        # Icon and title row
        icon_title_layout = QHBoxLayout()
        icon_title_layout.setSpacing(15)
        
        # Logo icon
        logo_label = QLabel()
        icon_path = self._find_local_icon("traywave-playing.png")
        
        if icon_path and os.path.exists(icon_path):
            try:
                logo_pixmap = QPixmap(icon_path)
                if not logo_pixmap.isNull():
                    scaled_pixmap = logo_pixmap.scaled(
                        icon_size, icon_size,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    logo_label.setPixmap(scaled_pixmap)
                    logo_label.setFixedSize(icon_size + 2, icon_size + 2)
            except Exception as e:
                print(f"⚠️ Error loading logo: {e}")
                self._set_fallback_logo(logo_label, icon_size)
        else:
            self._set_fallback_logo(logo_label, icon_size)
        
        icon_title_layout.addWidget(logo_label)
        
        # Title text
        title_container = QVBoxLayout()
        title = QLabel(title_text)
        title.setFont(QFont("", 18, QFont.Weight.Bold))
        
        if subtitle_text:
            subtitle = QLabel(subtitle_text)
            subtitle.setFont(QFont("", 10))
            subtitle.setStyleSheet("color: #6b7280;")
            title_container.addWidget(subtitle)
        
        title_container.addWidget(title)
        
        icon_title_layout.addLayout(title_container)
        icon_title_layout.addStretch()
        
        header_layout.addLayout(icon_title_layout)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("""
            QFrame {
                border: 1px solid #e5e7eb;
                margin: 10px 0px;
            }
        """)
        header_layout.addWidget(separator)
        
        layout.addLayout(header_layout)
        return layout
    
    def _find_local_icon(self, icon_name):
        """Find icon in local project folders."""
        try:
            current_file = os.path.abspath(__file__)
            current_dir = os.path.dirname(current_file)
            
            # 1. Prvo package folder
            package_path = os.path.join(current_dir, "..", "..", "resources", "icons", icon_name)
            if os.path.exists(package_path):
                return os.path.abspath(package_path)
            
            # 2. Root folder
            root_path = os.path.join(current_dir, "..", "..", "..", "resources", "icons", icon_name)
            if os.path.exists(root_path):
                return os.path.abspath(root_path)
            
            # 3. Working directory
            cwd = os.getcwd()
            cwd_path1 = os.path.join(cwd, "traywave", "resources", "icons", icon_name)
            if os.path.exists(cwd_path1):
                return os.path.abspath(cwd_path1)
            
            cwd_path2 = os.path.join(cwd, "resources", "icons", icon_name)
            if os.path.exists(cwd_path2):
                return os.path.abspath(cwd_path2)
            
        except Exception as e:
            print(f"⚠️ Error finding local icon: {e}")
        
        return None
    
    def _set_fallback_logo(self, label, size=48):
        """Set fallback logo."""
        label.setText("🎵")
        label.setFont(QFont("", size // 2))
        label.setFixedSize(size + 2, size + 2)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)