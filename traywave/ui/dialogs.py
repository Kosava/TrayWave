"""
Dialog windows (settings, style picker, about, etc.)
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QListWidget, QPushButton, QMessageBox, QInputDialog,
    QFrame, QTabWidget, QWidget, QScrollArea, QGroupBox, QCheckBox, QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from traywave.core.stations import StationsManager

class StylePreviewWidget(QWidget):
    """Preview widget showing menu style"""
    
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
        
        # Title - konzistentan font i poravnanje
        title = QLabel(style_data.get('name', style_name))
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Preview container - fiksna veličina za sve
        preview = QWidget()
        preview.setFixedHeight(150)
        preview.setFixedWidth(250)
        
        # Apply mini version of the style
        mini_style = self._create_mini_style()
        preview.setStyleSheet(mini_style)
        
        preview_layout = QVBoxLayout(preview)
        preview_layout.setContentsMargins(8, 8, 8, 8)
        preview_layout.setSpacing(3)
        
        # Add sample items - SVI ISTI
        # Koristi proper Unicode karakter za muzičku notu
        sample_items = ["♫ Now playing", "EX-YU ▶", "Dance ▶", "Settings", "Quit"]
        for text in sample_items:
            item = QLabel(text)
            # CSS će biti primenjen preko parent widget-a
            preview_layout.addWidget(item)
        
        # Dodaj stretch da svi budu isti
        preview_layout.addStretch()
        
        layout.addWidget(preview)
        
        # Apply initial border style
        self._update_style()
    
    def _create_mini_style(self):
        """Create a simplified version of the style for preview"""
        # KONZISTENTAN PREVIEW ZA SVE - samo border i boje se razlikuju
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
        # --- NOVE TEME ---
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
        """Update widget style based on state"""
        if self.is_selected:
            # SELEKTOVAN - jak efekat: border + jak glow + svetlija pozadina
            border_color = "#06b6d4"
            border_width = "4px"  # Još deblji border
            bg_color = "#f0f9ff"  # Dosta svetlija plava pozadina
            # Jači glow efekat sa više prozirnosti i većim rasponom
            glow_effect = """
                box-shadow: 
                    0 0 0 3px rgba(6, 182, 212, 0.1),
                    0 0 20px 5px rgba(6, 182, 212, 0.25),
                    0 0 30px 8px rgba(6, 182, 212, 0.15);
            """
        elif self.is_hovered:
            # HOVER - umereni efekat
            border_color = "#06b6d4"
            border_width = "2px"
            bg_color = "white"
            glow_effect = ""
        else:
            # NORMAL - neutralni stil
            border_color = "#e5e7eb"
            border_width = "2px"
            bg_color = "#f9fafb"  # Veoma blaga siva pozadina
            glow_effect = ""
        
        # Postavi glavni stil
        self.setStyleSheet(f"""
            QWidget {{
                border: {border_width} solid {border_color};
                border-radius: 14px;
                background-color: {bg_color};
                {glow_effect}
                padding: 2px;
            }}
        """)
    
    def enterEvent(self, event):
        """Handle mouse enter"""
        self.is_hovered = True
        if not self.is_selected:
            self._update_style()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Handle mouse leave"""
        self.is_hovered = False
        if not self.is_selected:
            self._update_style()
        super().leaveEvent(event)
    
    def set_selected(self, selected):
        """Highlight as selected"""
        self.is_selected = selected
        self._update_style()


class StyleSettingsDialog(QDialog):
    """Combined Settings dialog with tabs for Stations and Appearance"""
    
    # Signal koji se emituje kada se stanice promene
    stations_modified = pyqtSignal()
    
    def __init__(self, stations_manager: StationsManager, tray_wave, parent=None):
        super().__init__(parent)
        self.manager = stations_manager
        self.tray_wave = tray_wave
        self.selected_style = tray_wave.current_style
        self.style_widgets = {}
        
        self.setWindowTitle("TrayWave Settings")
        self.setMinimumSize(900, 650)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog UI with tabs"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("⚙️ TrayWave Settings")
        title.setFont(QFont("", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Tab widget
        tabs = QTabWidget()
        tabs.addTab(self._create_stations_tab(), "📻 Stations")
        tabs.addTab(self._create_appearance_tab(), "🎨 Appearance")
        tabs.addTab(self._create_general_tab(), "🔧 General")
        layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
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
        
        close_btn = QPushButton("Close")
        close_btn.setFixedSize(120, 40)
        close_btn.clicked.connect(self.accept)  # Zatvori bez promena
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
            QGroupBox {
                border: 2px solid #e5e7eb;
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 5px 15px;
                color: #1f2937;
            }
            QCheckBox {
                font-size: 11px;
                color: #374151;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #d1d5db;
            }
            QCheckBox::indicator:checked {
                background-color: #06b6d4;
                border-color: #06b6d4;
            }
            QSpinBox {
                font-size: 11px;
                padding: 4px;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                background-color: white;
            }
            QSpinBox:hover {
                border-color: #9ca3af;
            }
        """)
    
    def _create_stations_tab(self):
        """Create stations management tab"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # Left side - categories
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Categories:"))
        
        self.categories_list = QListWidget()
        self.categories_list.currentItemChanged.connect(self.on_category_selected)
        left_layout.addWidget(self.categories_list)
        
        cat_buttons = QHBoxLayout()
        add_cat_btn = QPushButton("Add Category")
        add_cat_btn.clicked.connect(self.add_category)
        remove_cat_btn = QPushButton("Remove Category")
        remove_cat_btn.clicked.connect(self.remove_category)
        cat_buttons.addWidget(add_cat_btn)
        cat_buttons.addWidget(remove_cat_btn)
        left_layout.addLayout(cat_buttons)
        
        # Right side - stations
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Stations:"))
        
        self.stations_list = QListWidget()
        right_layout.addWidget(self.stations_list)
        
        station_buttons = QHBoxLayout()
        add_station_btn = QPushButton("Add Station")
        add_station_btn.clicked.connect(self.add_station)
        remove_station_btn = QPushButton("Remove Station")
        remove_station_btn.clicked.connect(self.remove_station)
        station_buttons.addWidget(add_station_btn)
        station_buttons.addWidget(remove_station_btn)
        right_layout.addLayout(station_buttons)
        
        # Combine layouts
        layout.addLayout(left_layout, 1)
        layout.addLayout(right_layout, 2)
        
        self.load_categories()
        
        return widget
    
    def _create_appearance_tab(self):
        """Create appearance/style selection tab"""
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
        
        # FIXED: Import StyleManager to get themes
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
        
        # FIXED: Popuni poslednji red praznim widget-ima da bi sve bile poravnate
        if row_layout and row_layout.count() < 3:
            for _ in range(3 - row_layout.count()):
                spacer = QWidget()
                spacer.setFixedSize(280, 200)  # iste dimenzije kao preview widget
                row_layout.addWidget(spacer)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        return widget
    
    def _handle_preview_click(self, style_name, event):
        """Handle preview widget click"""
        print(f"🖱️ Preview clicked: {style_name}")
        self.select_style(style_name)
    
    def _create_general_tab(self):
        """Create general settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # General Settings group
        general_group = QGroupBox("General Settings")
        general_layout = QVBoxLayout(general_group)
        
        self.autostart_check = QCheckBox("Launch at system startup")
        self.notifications_check = QCheckBox("Show notifications on track change")
        self.minimize_check = QCheckBox("Minimize to tray on close")
        
        general_layout.addWidget(self.autostart_check)
        general_layout.addWidget(self.notifications_check)
        general_layout.addWidget(self.minimize_check)
        
        layout.addWidget(general_group)
        
        # Sleep Timer group
        sleep_group = QGroupBox("Sleep Timer")
        sleep_layout = QVBoxLayout(sleep_group)
        
        self.sleep_enable = QCheckBox("Enable sleep timer")
        
        # Minutes input
        minutes_layout = QHBoxLayout()
        minutes_layout.addWidget(QLabel("Stop playback after:"))
        self.sleep_minutes_spin = QSpinBox()
        self.sleep_minutes_spin.setRange(1, 480)  # Do 8 sati
        self.sleep_minutes_spin.setSuffix(" min")
        self.sleep_minutes_spin.setValue(60)
        self.sleep_minutes_spin.setEnabled(False)
        minutes_layout.addWidget(self.sleep_minutes_spin)
        minutes_layout.addStretch()
        
        # Quit option
        self.sleep_quit_check = QCheckBox("Quit application when timer expires")
        self.sleep_quit_check.setEnabled(False)
        
        # Connect checkbox to enable/disable inputs
        self.sleep_enable.stateChanged.connect(self._update_sleep_controls)
        
        sleep_layout.addWidget(self.sleep_enable)
        sleep_layout.addLayout(minutes_layout)
        sleep_layout.addWidget(self.sleep_quit_check)
        
        layout.addWidget(sleep_group)
        layout.addStretch()
        
        # Load current sleep timer state from engine
        self._load_sleep_timer_state()
        
        return widget
    
    def _update_sleep_controls(self, state):
        """Enable/disable sleep timer controls based on checkbox"""
        enabled = (state == Qt.CheckState.Checked.value)
        self.sleep_minutes_spin.setEnabled(enabled)
        self.sleep_quit_check.setEnabled(enabled)
    
    def _load_sleep_timer_state(self):
        """Load current sleep timer state from engine"""
        sleep_info = self.tray_wave.engine.get_sleep_timer_info()
        if sleep_info and sleep_info["active"]:
            self.sleep_enable.setChecked(True)
            self.sleep_minutes_spin.setValue(sleep_info["minutes_set"])
            self.sleep_quit_check.setChecked(sleep_info["quit_on_expire"])
            self._update_sleep_controls(Qt.CheckState.Checked.value)
    
    def select_style(self, style_name):
        """Select a style"""
        print(f"🎯 Selecting style: {style_name}")
        self.selected_style = style_name
        
        # Update visual selection
        for name, widget in self.style_widgets.items():
            widget.set_selected(name == style_name)
    
    def apply_settings(self):
        """Apply the selected settings"""
        print(f"🔄 Applying style: {self.selected_style}")
        
        # Apply style
        if self.selected_style != self.tray_wave.current_style:
            print(f"🔄 Style will change from '{self.tray_wave.current_style}' to '{self.selected_style}'")
            self.tray_wave.change_menu_style(self.selected_style)
        else:
            # OSVEŽI MENU ČAK I AKO SE NIJE PROMENILA TEMA
            # (u slučaju da su se dodale stanice)
            self.tray_wave._rebuild_menu()
        
        # Apply sleep timer settings
        if self.sleep_enable.isChecked():
            minutes = self.sleep_minutes_spin.value()
            quit_app = self.sleep_quit_check.isChecked()
            self.tray_wave.engine.set_sleep_timer(minutes, quit_app)
            print(f"⏰ Sleep timer set: {minutes} min, quit: {quit_app}")
        else:
            self.tray_wave.engine.cancel_sleep_timer()
            print("⏰ Sleep timer disabled")
        
        # EMITUJ SIGNAL DA SU STANICE PROMENJENE
        self.stations_modified.emit()
        
        # Zatvori dialog nakon Apply
        self.accept()
        print(f"✅ Settings applied, dialog closed")
    
    def load_categories(self):
        """Load categories into list"""
        self.categories_list.clear()
        for category in self.manager.stations.keys():
            self.categories_list.addItem(category)
        if self.categories_list.count() > 0:
            self.categories_list.setCurrentRow(0)
    
    def on_category_selected(self, current, previous):
        """Load stations for selected category"""
        self.stations_list.clear()
        if current:
            category = current.text()
            for name, url in self.manager.stations.get(category, []):
                self.stations_list.addItem(f"{name} - {url}")
    
    def add_category(self):
        """Add new category"""
        name, ok = QInputDialog.getText(self, "Add Category", "Category name:")
        if ok and name:
            if self.manager.add_category(name):
                self.manager.save_stations()
                self.load_categories()
            else:
                QMessageBox.warning(self, "Error", "Category already exists or invalid name!")
    
    def remove_category(self):
        """Remove selected category"""
        current = self.categories_list.currentItem()
        if current:
            reply = QMessageBox.question(
                self, "Confirm", 
                f"Remove category '{current.text()}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.manager.remove_category(current.text())
                self.manager.save_stations()
                self.load_categories()
    
    def add_station(self):
        """Add new station to selected category"""
        current_cat = self.categories_list.currentItem()
        if not current_cat:
            QMessageBox.warning(self, "Error", "Select a category first!")
            return
        
        name, ok = QInputDialog.getText(self, "Add Station", "Station name:")
        if not ok or not name:
            return
        
        url, ok = QInputDialog.getText(self, "Add Station", "Station URL:")
        if ok and url:
            category = current_cat.text()
            if self.manager.add_station(category, name, url):
                self.manager.save_stations()
                self.on_category_selected(current_cat, None)
            else:
                QMessageBox.warning(self, "Error", "Failed to add station!")
    
    def remove_station(self):
        """Remove selected station"""
        current_cat = self.categories_list.currentItem()
        current_station = self.stations_list.currentRow()
        
        if current_cat and current_station >= 0:
            reply = QMessageBox.question(
                self, "Confirm",
                "Remove this station?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                category = current_cat.text()
                if self.manager.remove_station(category, current_station):
                    self.manager.save_stations()
                    self.on_category_selected(current_cat, None)


class AboutDialog(QDialog):
    """About dialog for TrayWave"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About TrayWave")
        self.setMinimumSize(400, 300)
        self.setMaximumSize(450, 350)
        self.init_ui()
    
    def init_ui(self):
        """Initialize About dialog UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("TrayWave")
        title_font = title.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Version
        version = QLabel("Version: 0.1.3")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        # Description
        desc = QLabel("A lightweight radio player for system tray")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Author
        author = QLabel("© 2026 Košava")
        author.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(author)
        
        # GitHub link
        github = QLabel('<a href="https://github.com/Kosava/traywave">https://github.com/Kosava/traywave</a>')
        github.setOpenExternalLinks(True)
        github.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(github)
        
        # License
        license_label = QLabel("MIT License")
        license_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(license_label)
        
        # Spacer
        layout.addStretch()
        
        # Close button
        button_layout = QHBoxLayout()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        close_btn.setFixedWidth(100)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)