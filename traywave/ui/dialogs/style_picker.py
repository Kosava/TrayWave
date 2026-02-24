"""
Style picker dialog and preview widget.
"""

import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QWidget,
    QPushButton, QScrollArea, QFrame, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QIcon
from .base_dialog import DialogWithIcon
from .station_manager import StationManagerTab
from .general_settings import GeneralSettingsTab


class StylePreviewWidget(QWidget):
    """Preview widget showing menu style."""
    
    def __init__(self, style_name, style_data, parent=None):
        super().__init__(parent)
        self.style_name = style_name
        self.style_data = style_data
        self.is_selected = False
        self.is_hovered = False
        
        self.setFixedSize(280, 200)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)
        
        # Title
        title = QLabel(style_data.get('name', style_name))
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Preview container
        preview = QWidget()
        preview.setFixedHeight(150)
        preview.setFixedWidth(250)
        
        # Apply mini version of the style
        mini_style = self._create_mini_style()
        preview.setStyleSheet(mini_style)
        
        preview_layout = QVBoxLayout(preview)
        preview_layout.setContentsMargins(8, 8, 8, 8)
        preview_layout.setSpacing(3)
        
        # Add sample items
        sample_items = ["♫ Now playing", "EX-YU ▶", "Dance ▶", "Settings", "Quit"]
        for text in sample_items:
            item = QLabel(text)
            preview_layout.addWidget(item)
        
        preview_layout.addStretch()
        layout.addWidget(preview)
        
        # Apply initial border style
        self._update_style()
    
    def _create_mini_style(self):
        """Create a simplified version of the style for preview."""
        if 'teal' in self.style_name.lower():
            return """
                QWidget {
                    background-color: rgba(255, 255, 255, 0.98);
                    border-radius: 8px;
                    border: 1px solid rgba(6, 182, 212, 0.2);
                }
                QLabel {
                    color: #0f172a;
                    font-size: 11px;
                    padding: 6px;
                    border-radius: 4px;
                }
                QLabel:hover {
                    background-color: rgba(6, 182, 212, 0.1);
                }
            """
        elif 'macos' in self.style_name.lower():
            return """
                QWidget {
                    background-color: rgba(255, 255, 255, 0.95);
                    border-radius: 8px;
                    border: 1px solid rgba(0, 0, 0, 0.1);
                }
                QLabel {
                    color: #1d1d1f;
                    font-size: 11px;
                    padding: 6px;
                    border-radius: 4px;
                }
                QLabel:hover {
                    background-color: rgba(0, 0, 0, 0.05);
                }
            """
        elif 'win11' in self.style_name.lower() or 'windows' in self.style_name.lower():
            return """
                QWidget {
                    background-color: rgba(243, 243, 243, 0.95);
                    border-radius: 6px;
                    border: 1px solid rgba(0, 0, 0, 0.08);
                }
                QLabel {
                    color: #323130;
                    font-size: 11px;
                    padding: 6px;
                    border-radius: 4px;
                }
                QLabel:hover {
                    background-color: rgba(0, 0, 0, 0.04);
                }
            """
        elif 'material' in self.style_name.lower():
            return """
                QWidget {
                    background-color: white;
                    border-radius: 4px;
                    border: 1px solid #e0e0e0;
                }
                QLabel {
                    color: rgba(0, 0, 0, 0.87);
                    font-size: 11px;
                    padding: 6px;
                    border-radius: 4px;
                }
                QLabel:hover {
                    background-color: rgba(0, 0, 0, 0.04);
                }
            """
        elif 'minimal' in self.style_name.lower():
            return """
                QWidget {
                    background-color: #1a1a1a;
                    border-radius: 12px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }
                QLabel {
                    color: rgba(255, 255, 255, 0.9);
                    font-size: 11px;
                    padding: 6px;
                    border-radius: 4px;
                }
                QLabel:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                }
            """
        elif 'rosegold' in self.style_name.lower() or 'rose gold' in self.style_name.lower():
            return """
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #fdfcfb, stop:1 #fef5f1);
                    border-radius: 12px;
                    border: 1px solid rgba(240, 147, 251, 0.3);
                }
                QLabel {
                    color: #4a1942;
                    font-size: 11px;
                    padding: 6px;
                    border-radius: 4px;
                }
                QLabel:hover {
                    background-color: rgba(240, 147, 251, 0.1);
                }
            """
        elif 'forest' in self.style_name.lower() or 'green' in self.style_name.lower():
            return """
                QWidget {
                    background-color: rgba(245, 251, 242, 0.95);
                    border-radius: 8px;
                    border: 1px solid rgba(76, 175, 80, 0.2);
                }
                QLabel {
                    color: #1b5e20;
                    font-size: 11px;
                    padding: 6px;
                    border-radius: 4px;
                }
                QLabel:hover {
                    background-color: rgba(76, 175, 80, 0.1);
                }
            """
        elif 'lavender' in self.style_name.lower():
            return """
                QWidget {
                    background-color: rgba(250, 245, 255, 0.95);
                    border-radius: 8px;
                    border: 1px solid rgba(186, 104, 200, 0.2);
                }
                QLabel {
                    color: #4a148c;
                    font-size: 11px;
                    padding: 6px;
                    border-radius: 4px;
                }
                QLabel:hover {
                    background-color: rgba(186, 104, 200, 0.1);
                }
            """
        elif 'sunset' in self.style_name.lower() or 'orange' in self.style_name.lower():
            return """
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #fff8e1, stop:1 #ffecb3);
                    border-radius: 8px;
                    border: 1px solid rgba(255, 152, 0, 0.2);
                }
                QLabel {
                    color: #e65100;
                    font-size: 11px;
                    padding: 6px;
                    border-radius: 4px;
                }
                QLabel:hover {
                    background-color: rgba(255, 152, 0, 0.1);
                }
            """
        elif 'midnight' in self.style_name.lower() or 'blue' in self.style_name.lower():
            return """
                QWidget {
                    background-color: #0d1b2a;
                    border-radius: 8px;
                    border: 1px solid rgba(66, 135, 245, 0.3);
                }
                QLabel {
                    color: #e0e1dd;
                    font-size: 11px;
                    padding: 6px;
                    border-radius: 4px;
                }
                QLabel:hover {
                    background-color: rgba(66, 135, 245, 0.1);
                }
            """
        elif 'ocean' in self.style_name.lower():
            return """
                QWidget {
                    background-color: rgba(227, 242, 253, 0.95);
                    border-radius: 8px;
                    border: 1px solid rgba(33, 150, 243, 0.2);
                }
                QLabel {
                    color: #0d47a1;
                    font-size: 11px;
                    padding: 6px;
                    border-radius: 4px;
                }
                QLabel:hover {
                    background-color: rgba(33, 150, 243, 0.1);
                }
            """
        elif 'nord' in self.style_name.lower():
            return """
                QWidget {
                    background-color: #2e3440;
                    border-radius: 8px;
                    border: 1px solid #3b4252;
                }
                QLabel {
                    color: #d8dee9;
                    font-size: 11px;
                    padding: 6px;
                    border-radius: 4px;
                }
                QLabel:hover {
                    background-color: #3b4252;
                }
            """
        elif 'solarized' in self.style_name.lower():
            return """
                QWidget {
                    background-color: #002b36;
                    border-radius: 8px;
                    border: 1px solid #073642;
                }
                QLabel {
                    color: #839496;
                    font-size: 11px;
                    padding: 6px;
                    border-radius: 4px;
                }
                QLabel:hover {
                    background-color: #073642;
                }
            """
        elif 'cyberpunk' in self.style_name.lower():
            return """
                QWidget {
                    background-color: #0a0a0f;
                    border-radius: 8px;
                    border: 2px solid #ff00ff;
                }
                QLabel {
                    color: #00ffff;
                    font-size: 11px;
                    padding: 6px;
                    border-radius: 4px;
                }
                QLabel:hover {
                    background-color: rgba(255, 0, 255, 0.2);
                }
            """
        elif 'dracula' in self.style_name.lower():
            return """
                QWidget {
                    background-color: #282a36;
                    border-radius: 8px;
                    border: 1px solid #44475a;
                }
                QLabel {
                    color: #f8f8f2;
                    font-size: 11px;
                    padding: 6px;
                    border-radius: 4px;
                }
                QLabel:hover {
                    background-color: #44475a;
                }
            """
        elif 'monokai' in self.style_name.lower():
            return """
                QWidget {
                    background-color: #272822;
                    border-radius: 8px;
                    border: 1px solid #3e3d32;
                }
                QLabel {
                    color: #f8f8f2;
                    font-size: 11px;
                    padding: 6px;
                    border-radius: 4px;
                }
                QLabel:hover {
                    background-color: #3e3d32;
                }
            """
        elif 'gruvbox' in self.style_name.lower():
            return """
                QWidget {
                    background-color: #282828;
                    border-radius: 8px;
                    border: 1px solid #3c3836;
                }
                QLabel {
                    color: #ebdbb2;
                    font-size: 11px;
                    padding: 6px;
                    border-radius: 4px;
                }
                QLabel:hover {
                    background-color: #3c3836;
                }
            """
        elif 'catppuccin' in self.style_name.lower() or 'mocha' in self.style_name.lower():
            return """
                QWidget {
                    background-color: #1e1e2e;
                    border-radius: 8px;
                    border: 1px solid #313244;
                }
                QLabel {
                    color: #cdd6f4;
                    font-size: 11px;
                    padding: 6px;
                    border-radius: 4px;
                }
                QLabel:hover {
                    background-color: #313244;
                }
            """
        elif 'tokyonight' in self.style_name.lower() or 'tokyo' in self.style_name.lower():
            return """
                QWidget {
                    background-color: #1a1b26;
                    border-radius: 8px;
                    border: 1px solid #24283b;
                }
                QLabel {
                    color: #a9b1d6;
                    font-size: 11px;
                    padding: 6px;
                    border-radius: 4px;
                }
                QLabel:hover {
                    background-color: #24283b;
                }
            """
        # Default za sve ostale
        return """
            QWidget {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 8px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
            QLabel {
                color: #333333;
                font-size: 11px;
                padding: 6px;
                border-radius: 4px;
            }
            QLabel:hover {
                background-color: rgba(0, 0, 0, 0.05);
            }
        """
    
    def _update_style(self):
        """Update widget style based on state."""
        if self.is_selected:
            # Deblja granica + plava pozadina simulira "glow" efekat
            # (PyQt6 ne podržava box-shadow)
            self.setStyleSheet("""
                QWidget {
                    border: 3px solid #06b6d4;
                    border-radius: 14px;
                    background-color: #e0f7fa;
                    padding: 2px;
                }
            """)
        elif self.is_hovered:
            self.setStyleSheet("""
                QWidget {
                    border: 2px solid #06b6d4;
                    border-radius: 14px;
                    background-color: white;
                    padding: 2px;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    border: 2px solid #e5e7eb;
                    border-radius: 14px;
                    background-color: #f9fafb;
                    padding: 2px;
                }
            """)
    
    def enterEvent(self, event):
        """Handle mouse enter."""
        self.is_hovered = True
        if not self.is_selected:
            self._update_style()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Handle mouse leave."""
        self.is_hovered = False
        if not self.is_selected:
            self._update_style()
        super().leaveEvent(event)
    
    def set_selected(self, selected):
        """Highlight as selected."""
        self.is_selected = selected
        self._update_style()


class StyleSettingsDialog(DialogWithIcon):
    """Combined Settings dialog with tabs for Stations and Appearance."""
    
    # Signal koji se emituje kada se stanice promene
    stations_modified = pyqtSignal()
    
    def __init__(self, stations_manager, tray_wave, parent=None):
        super().__init__(parent)
        self.manager = stations_manager
        self.tray_wave = tray_wave
        self.selected_style = tray_wave.current_style
        self.style_widgets = {}
        
        self.setWindowTitle("TrayWave Settings")
        self.setMinimumSize(1000, 700)
        
        self._set_window_icon()
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog UI with tabs."""
        from PyQt6.QtWidgets import QHBoxLayout
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Header sa logom
        header = self.create_header(
            "⚙️ TrayWave Settings",
            "Radio player for your system tray"
        )
        layout.addLayout(header)
        
        # Tab widget - importovani iz drugih modula
        tabs = QTabWidget()
        tabs.addTab(StationManagerTab(self.manager, self), "📻 Stations")
        tabs.addTab(self._create_appearance_tab(), "🎨 Appearance")
        tabs.addTab(GeneralSettingsTab(self.tray_wave), "🔧 General")
        layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.setFixedSize(120, 40)
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #e5e7eb;
                color: #374151;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d1d5db;
            }
        """)
        
        apply_btn = QPushButton("Apply")
        apply_btn.setFont(QFont("", 10, QFont.Weight.Bold))
        apply_btn.setFixedSize(120, 40)
        apply_btn.clicked.connect(self.apply_settings)
        apply_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #06b6d4, stop:1 #0891b2);
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0891b2, stop:1 #0e7490);
            }
        """)
        
        button_layout.addWidget(close_btn)
        button_layout.addWidget(apply_btn)
        layout.addLayout(button_layout)
        
        # Set dialog style
        self.setStyleSheet("""
            QDialog {
                background-color: #fafafa;
            }
            QTabWidget::pane {
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                padding: 10px 20px;
                margin-right: 5px;
                background-color: #e5e7eb;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #06b6d4;
                font-weight: bold;
            }
        """)
    
    def _create_appearance_tab(self):
        """Create appearance/style selection tab."""
        from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        style_label = QLabel("Choose Menu Style:")
        style_label.setFont(QFont("", 12, QFont.Weight.Bold))
        layout.addWidget(style_label)
        
        # Scroll area for style previews
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Import StyleManager to get themes
        from traywave.ui.styles.style_manager import StyleManager
        style_manager = StyleManager()
        
        # Create style preview grid
        row_layout = None
        theme_names = style_manager.get_theme_names()
        
        for i, style_name in enumerate(theme_names):
            if i % 3 == 0:
                row_layout = QHBoxLayout()
                row_layout.setSpacing(15)
                scroll_layout.addLayout(row_layout)
            
            # Get style data for preview
            style_data = {'name': style_manager.get_theme_display_name(style_name)}
            preview = StylePreviewWidget(style_name, style_data)
            
            # Create a closure to capture the current style_name
            def create_click_handler(s):
                return lambda event: self._handle_preview_click(s, event)
            
            preview.mousePressEvent = create_click_handler(style_name)
            
            # Postavi selektovanje na osnovu trenutnog stila
            is_selected = (style_name == self.selected_style)
            preview.set_selected(is_selected)
            
            self.style_widgets[style_name] = preview
            row_layout.addWidget(preview)
        
        # Popuni poslednji red praznim widget-ima
        if row_layout and row_layout.count() < 3:
            for _ in range(3 - row_layout.count()):
                spacer = QWidget()
                spacer.setFixedSize(280, 200)
                row_layout.addWidget(spacer)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        return widget
    
    def _handle_preview_click(self, style_name, event):
        """Handle preview widget click."""
        print(f"🖱️ Preview clicked: {style_name}")
        self.select_style(style_name)
    
    def select_style(self, style_name):
        """Select a style."""
        print(f"🎯 Selecting style: {style_name}")
        self.selected_style = style_name
        
        # Update visual selection
        for name, widget in self.style_widgets.items():
            widget.set_selected(name == style_name)
    
    def apply_settings(self):
        """Apply the selected settings."""
        print(f"🔄 Applying style: {self.selected_style}")
        
        # Apply style
        if self.selected_style != self.tray_wave.current_style:
            print(f"🔄 Style will change from '{self.tray_wave.current_style}' to '{self.selected_style}'")
            self.tray_wave.change_menu_style(self.selected_style)
        else:
            # OSVEŽI MENU ČAK I AKO SE NIJE PROMENILA TEMA
            self.tray_wave._rebuild_menu()
        
        # EMITUJ SIGNAL DA SU STANICE PROMENJENE
        self.stations_modified.emit()
        
        # Zatvori dialog nakon Apply
        self.accept()
        print(f"✅ Settings applied, dialog closed")