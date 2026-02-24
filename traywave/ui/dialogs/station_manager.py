"""
Station management dialogs and widgets - REFINED DESIGN
"""

import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QListWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QWidget,
    QLineEdit, QComboBox, QMessageBox, QInputDialog,
    QHeaderView, QAbstractItemView, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from .base_dialog import BaseDialog
from ..icons import get_icon, get_pixmap

_ICON_SIZE = 20  # px pro ikone u dijalozima


class EditStationDialog(BaseDialog):
    """Dialog for editing a station - REFINED."""
    
    def __init__(self, station_name, station_url, category, all_categories, parent=None):
        super().__init__(parent)
        self.station_name = station_name
        self.station_url = station_url
        self.category = category
        self.all_categories = all_categories
        
        self.setWindowTitle("Edit Station")
        self.setFixedSize(520, 380)
        
        self.init_ui()
        self._set_window_icon()
    
    def init_ui(self):
        """Initialize edit dialog UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)
        
        # Title with icon - MODERNIZOVANO
        title_layout = QHBoxLayout()
        title_layout.setSpacing(12)
        
        icon_label = QLabel()
        icon_label.setPixmap(get_pixmap("edit", 24))
        icon_label.setFixedSize(40, 40)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #06b6d4, stop:1 #0891b2);
            border-radius: 8px;
            padding: 8px;
        """)
        title_layout.addWidget(icon_label)
        
        title_container = QVBoxLayout()
        title_container.setSpacing(2)
        
        title = QLabel("Edit Station")
        title.setFont(QFont("", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #1f2937;")
        
        subtitle = QLabel("Modify station details")
        subtitle.setFont(QFont("", 9))
        subtitle.setStyleSheet("color: #9ca3af;")
        
        title_container.addWidget(title)
        title_container.addWidget(subtitle)
        
        title_layout.addLayout(title_container)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        # Separator - TANKI I ELEGANTAN
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 transparent, stop:0.5 #e5e7eb, stop:1 transparent);
            height: 1px;
            border: none;
            margin: 8px 0;
        """)
        layout.addWidget(separator)
        
        # Station Name - LEPŠI INPUT
        name_layout = QVBoxLayout()
        name_layout.setSpacing(6)
        
        name_label = QLabel("Station Name")
        name_label.setFont(QFont("", 10, QFont.Weight.DemiBold))
        name_label.setStyleSheet("color: #374151;")
        
        self.name_input = QLineEdit()
        self.name_input.setText(self.station_name)
        self.name_input.setPlaceholderText("Enter station name...")
        self.name_input.setMinimumHeight(38)
        
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # Stream URL - LEPŠI INPUT
        url_layout = QVBoxLayout()
        url_layout.setSpacing(6)
        
        url_label = QLabel("Stream URL")
        url_label.setFont(QFont("", 10, QFont.Weight.DemiBold))
        url_label.setStyleSheet("color: #374151;")
        
        self.url_input = QLineEdit()
        self.url_input.setText(self.station_url)
        self.url_input.setPlaceholderText("https://stream.example.com/radio")
        self.url_input.setMinimumHeight(38)
        
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)
        
        # Category - LEPŠI DROPDOWN
        category_layout = QVBoxLayout()
        category_layout.setSpacing(6)
        
        category_label = QLabel("Category")
        category_label.setFont(QFont("", 10, QFont.Weight.DemiBold))
        category_label.setStyleSheet("color: #374151;")
        
        self.category_combo = QComboBox()
        self.category_combo.addItems(self.all_categories)
        self.category_combo.setMinimumHeight(38)
        
        # Set current category
        index = self.category_combo.findText(self.category)
        if index >= 0:
            self.category_combo.setCurrentIndex(index)
        
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)
        layout.addLayout(category_layout)
        
        layout.addStretch()
        
        # Buttons - MODERNIZOVANI
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedSize(100, 38)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("Save")
        save_btn.setIcon(get_icon("save", _ICON_SIZE))
        save_btn.setFixedSize(100, 38)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self.validate_and_accept)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addLayout(button_layout)
        
        # MODERNIZOVAN STYLESHEET
        self.setStyleSheet("""
            QDialog {
                background-color: #f9fafb;
            }
            QLabel {
                color: #374151;
                background-color: transparent;
            }
            QLineEdit {
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 11px;
                background-color: white;
                color: #1f2937;
            }
            QLineEdit:focus {
                border-color: #06b6d4;
                background-color: #f0f9ff;
                outline: none;
            }
            QLineEdit:hover {
                border-color: #d1d5db;
            }
            QComboBox {
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 11px;
                background-color: white;
                color: #1f2937;
            }
            QComboBox:focus {
                border-color: #06b6d4;
                background-color: #f0f9ff;
            }
            QComboBox:hover {
                border-color: #d1d5db;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6b7280;
                margin-right: 10px;
            }
            QComboBox:hover::down-arrow {
                border-top-color: #06b6d4;
            }
            QPushButton {
                background-color: #f3f4f6;
                color: #374151;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #e5e7eb;
                border-color: #d1d5db;
            }
            QPushButton:pressed {
                background-color: #d1d5db;
            }
            QPushButton#save_btn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #06b6d4, stop:1 #0891b2);
                color: white;
                border: none;
            }
            QPushButton#save_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0891b2, stop:1 #0e7490);
            }
        """)
        
        save_btn.setObjectName("save_btn")
        
        # Connect Enter key
        self.name_input.returnPressed.connect(save_btn.click)
        self.url_input.returnPressed.connect(save_btn.click)
    
    def validate_and_accept(self):
        """Validate inputs before accepting."""
        name = self.name_input.text().strip()
        url = self.url_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Error", "Station name cannot be empty!")
            self.name_input.setFocus()
            return
        
        if not url:
            QMessageBox.warning(self, "Error", "Stream URL cannot be empty!")
            self.url_input.setFocus()
            return
        
        if not url.startswith(('http://', 'https://')):
            QMessageBox.warning(self, "Error", "URL must start with http:// or https://")
            self.url_input.setFocus()
            return
        
        self.accept()
    
    def get_values(self):
        """Get edited values."""
        return {
            'name': self.name_input.text().strip(),
            'url': self.url_input.text().strip(),
            'category': self.category_combo.currentText()
        }


class StationTableWidget(QTableWidget):
    """Custom table widget for displaying stations - REFINED."""
    
    station_selected = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_table()
    
    def setup_table(self):
        """Configure table appearance and behavior."""
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Station Name", "Stream URL"])
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # MODERNIZOVAN STIL
        self.setStyleSheet("""
            QTableWidget {
                border: 2px solid #e5e7eb;
                border-radius: 10px;
                background-color: white;
                gridline-color: #f3f4f6;
                font-size: 11px;
                selection-background-color: #dbeafe;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #06b6d4, stop:1 #0891b2);
                color: white;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-right: 1px solid rgba(255,255,255,0.1);
                font-size: 11px;
            }
            QHeaderView::section:first {
                border-top-left-radius: 8px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 8px;
                border-right: none;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f3f4f6;
            }
            QTableWidget::item:selected {
                background-color: #dbeafe;
                color: #0c4a6e;
            }
            QTableWidget::item:hover {
                background-color: #f0f9ff;
            }
            QTableWidget QTableCornerButton::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #06b6d4, stop:1 #0891b2);
                border: none;
                border-top-left-radius: 8px;
            }
        """)
        
        # Configure headers
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
        # Set row height
        self.verticalHeader().setDefaultSectionSize(36)
        self.verticalHeader().hide()  # Sakrij vertikalni header
        
        # Connect signals
        self.cellClicked.connect(self._on_cell_clicked)
    
    def _on_cell_clicked(self, row, column):
        """Handle cell click and emit station_selected signal."""
        self.station_selected.emit(row)
    
    def load_stations(self, stations):
        """Load stations into the table."""
        self.setRowCount(len(stations))
        
        for row, (name, url) in enumerate(stations):
            # Station name
            name_item = QTableWidgetItem(name)
            name_item.setData(Qt.ItemDataRole.UserRole, (name, url))
            name_item.setFont(QFont("", 10, QFont.Weight.DemiBold))
            self.setItem(row, 0, name_item)
            
            # Stream URL
            display_url = url if len(url) <= 50 else url[:47] + "..."
            url_item = QTableWidgetItem(display_url)
            url_item.setToolTip(url)
            url_item.setData(Qt.ItemDataRole.UserRole, url)
            url_item.setForeground(Qt.GlobalColor.darkGray)
            self.setItem(row, 1, url_item)


class StationManagerTab(QWidget):
    """Tab widget for managing stations and categories - REFINED."""
    
    def __init__(self, stations_manager, settings_dialog):
        super().__init__()
        self.manager = stations_manager
        self.settings_dialog = settings_dialog
        self.current_category = None
        self.current_station_index = -1
        
        self.init_ui()
        self.load_categories()
    
    def init_ui(self):
        """Initialize the station manager tab UI."""
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # ===== LEFT SIDE - Categories =====
        left_container = QWidget()
        left_container.setMaximumWidth(220)
        left_layout = QVBoxLayout(left_container)
        left_layout.setSpacing(10)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header sa ikonom
        cat_header = QHBoxLayout()
        cat_header.setSpacing(8)
        
        cat_icon = QLabel()
        cat_icon.setPixmap(get_pixmap("folder", 20))
        cat_icon.setFixedSize(24, 24)
        
        cat_label = QLabel("Categories")
        cat_label.setFont(QFont("", 12, QFont.Weight.Bold))
        cat_label.setStyleSheet("color: #1f2937;")
        
        cat_header.addWidget(cat_icon)
        cat_header.addWidget(cat_label)
        cat_header.addStretch()
        left_layout.addLayout(cat_header)
        
        # Categories list
        self.categories_list = QListWidget()
        self.categories_list.currentItemChanged.connect(self.on_category_selected)
        left_layout.addWidget(self.categories_list)
        
        # Category buttons
        cat_buttons_layout = QHBoxLayout()
        cat_buttons_layout.setSpacing(6)
        
        self.add_cat_btn = QPushButton()
        self.add_cat_btn.setIcon(get_icon("add", _ICON_SIZE))
        self.add_cat_btn.setToolTip("Add Category")
        self.add_cat_btn.clicked.connect(self.add_category)
        self.add_cat_btn.setFixedSize(32, 32)
        
        self.remove_cat_btn = QPushButton()
        self.remove_cat_btn.setIcon(get_icon("delete", _ICON_SIZE))
        self.remove_cat_btn.setToolTip("Remove Category")
        self.remove_cat_btn.clicked.connect(self.remove_category)
        self.remove_cat_btn.setFixedSize(32, 32)
        
        cat_buttons_layout.addWidget(self.add_cat_btn)
        cat_buttons_layout.addWidget(self.remove_cat_btn)
        cat_buttons_layout.addStretch()
        left_layout.addLayout(cat_buttons_layout)
        
        # ===== RIGHT SIDE - Stations =====
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setSpacing(10)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header sa ikonom
        sta_header = QHBoxLayout()
        sta_header.setSpacing(8)
        
        sta_icon = QLabel()
        sta_icon.setPixmap(get_pixmap("radio", 20))
        sta_icon.setFixedSize(24, 24)
        
        sta_label = QLabel("Stations")
        sta_label.setFont(QFont("", 12, QFont.Weight.Bold))
        sta_label.setStyleSheet("color: #1f2937;")
        
        sta_header.addWidget(sta_icon)
        sta_header.addWidget(sta_label)
        sta_header.addStretch()
        right_layout.addLayout(sta_header)
        
        # Station table
        self.stations_table = StationTableWidget()
        self.stations_table.station_selected.connect(self.on_station_selected)
        self.stations_table.cellDoubleClicked.connect(self.edit_station)
        right_layout.addWidget(self.stations_table)
        
        # Station buttons
        station_buttons_layout = QHBoxLayout()
        station_buttons_layout.setSpacing(8)
        
        self.add_station_btn = QPushButton("Add")
        self.add_station_btn.setIcon(get_icon("add", _ICON_SIZE))
        self.add_station_btn.clicked.connect(self.add_station)
        self.add_station_btn.setFixedHeight(36)
        self.add_station_btn.setMinimumWidth(80)
        
        self.edit_station_btn = QPushButton("Edit")
        self.edit_station_btn.setIcon(get_icon("edit", _ICON_SIZE))
        self.edit_station_btn.clicked.connect(self.edit_station)
        self.edit_station_btn.setFixedHeight(36)
        self.edit_station_btn.setMinimumWidth(80)
        self.edit_station_btn.setEnabled(False)
        
        self.remove_station_btn = QPushButton("Remove")
        self.remove_station_btn.setIcon(get_icon("delete", _ICON_SIZE))
        self.remove_station_btn.clicked.connect(self.remove_station)
        self.remove_station_btn.setFixedHeight(36)
        self.remove_station_btn.setMinimumWidth(80)
        self.remove_station_btn.setEnabled(False)
        
        station_buttons_layout.addWidget(self.add_station_btn)
        station_buttons_layout.addWidget(self.edit_station_btn)
        station_buttons_layout.addWidget(self.remove_station_btn)
        station_buttons_layout.addStretch()
        right_layout.addLayout(station_buttons_layout)
        
        # Add both sides
        main_layout.addWidget(left_container)
        main_layout.addWidget(right_container, 1)
        
        # MODERNIZOVANI STILOVI
        button_style = """
            QPushButton {
                background-color: white;
                color: #374151;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #f9fafb;
                border-color: #06b6d4;
                color: #06b6d4;
            }
            QPushButton:pressed {
                background-color: #f3f4f6;
            }
            QPushButton:disabled {
                background-color: #f9fafb;
                color: #d1d5db;
                border-color: #f3f4f6;
            }
        """
        
        icon_button_style = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #06b6d4, stop:1 #0891b2);
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0891b2, stop:1 #0e7490);
            }
            QPushButton:pressed {
                background: #0e7490;
            }
        """
        
        self.add_cat_btn.setStyleSheet(icon_button_style)
        self.remove_cat_btn.setStyleSheet(icon_button_style)
        self.add_station_btn.setStyleSheet(button_style)
        self.edit_station_btn.setStyleSheet(button_style)
        self.remove_station_btn.setStyleSheet(button_style)
        
        # Categories list style
        self.categories_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #e5e7eb;
                border-radius: 10px;
                background-color: white;
                font-size: 11px;
                padding: 4px;
            }
            QListWidget::item {
                padding: 10px 12px;
                border-radius: 6px;
                margin: 2px 0;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #06b6d4, stop:1 #0891b2);
                color: white;
                font-weight: bold;
            }
            QListWidget::item:hover {
                background-color: #f0f9ff;
            }
        """)
    
    # ===== CATEGORY METHODS =====
    
    def load_categories(self):
        """Load categories into list."""
        self.categories_list.clear()
        categories = list(self.manager.stations.keys())
        
        for category in categories:
            self.categories_list.addItem(category)
        
        if self.categories_list.count() > 0:
            self.categories_list.setCurrentRow(0)
            self.on_category_selected(self.categories_list.currentItem(), None)
    
    def on_category_selected(self, current, previous):
        """Load stations for selected category."""
        if not current:
            self.current_category = None
            self.stations_table.setRowCount(0)
            return
        
        self.current_category = current.text()
        stations = self.manager.stations.get(self.current_category, [])
        self.stations_table.load_stations(stations)
        
        self.current_station_index = -1
        self.update_button_states()
    
    def on_station_selected(self, row):
        """Handle station selection."""
        self.current_station_index = row
        self.update_button_states()
    
    def update_button_states(self):
        """Update button states."""
        has_selection = self.current_station_index >= 0
        self.edit_station_btn.setEnabled(has_selection)
        self.remove_station_btn.setEnabled(has_selection)
    
    # ===== CRUD OPERATIONS =====
    
    def add_category(self):
        """Add new category."""
        name, ok = QInputDialog.getText(
            self.settings_dialog, 
            "Add Category", 
            "Category name:",
            QLineEdit.EchoMode.Normal,
            ""
        )
        
        if ok and name:
            name = name.strip()
            if name:
                if self.manager.add_category(name):
                    self.manager.save_stations()
                    self.load_categories()
                else:
                    QMessageBox.warning(self.settings_dialog, "Error", 
                                       "Category already exists!")
    
    def remove_category(self):
        """Remove selected category."""
        current = self.categories_list.currentItem()
        if not current:
            return
        
        category = current.text()
        
        reply = QMessageBox.question(
            self.settings_dialog, 
            "Confirm Removal", 
            f"Remove '{category}' and all its stations?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.manager.remove_category(category):
                self.manager.save_stations()
                self.load_categories()
    
    def add_station(self):
        """Add new station."""
        if not self.current_category:
            QMessageBox.warning(self.settings_dialog, "Error", 
                               "Please select a category first!")
            return
        
        all_categories = list(self.manager.stations.keys())
        dialog = EditStationDialog("", "", self.current_category, all_categories, 
                                 self.settings_dialog)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            values = dialog.get_values()
            
            if values['category'] != self.current_category:
                if self.manager.add_station(values['category'], values['name'], values['url']):
                    self.manager.save_stations()
                    self.load_categories()
                    index = self.categories_list.findItems(values['category'], 
                                                          Qt.MatchFlag.MatchExactly)
                    if index:
                        self.categories_list.setCurrentItem(index[0])
            else:
                if self.manager.add_station(self.current_category, values['name'], values['url']):
                    self.manager.save_stations()
                    self.on_category_selected(self.categories_list.currentItem(), None)
    
    def edit_station(self):
        """Edit selected station."""
        if self.current_station_index < 0 or not self.current_category:
            return
        
        name_item = self.stations_table.item(self.current_station_index, 0)
        url_item = self.stations_table.item(self.current_station_index, 1)
        
        if not name_item or not url_item:
            return
        
        current_name = name_item.data(Qt.ItemDataRole.UserRole)[0]
        current_url = url_item.data(Qt.ItemDataRole.UserRole)
        
        all_categories = list(self.manager.stations.keys())
        dialog = EditStationDialog(current_name, current_url, self.current_category, 
                                 all_categories, self.settings_dialog)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            values = dialog.get_values()
            
            if (values['name'] == current_name and 
                values['url'] == current_url and 
                values['category'] == self.current_category):
                return
            
            if values['category'] != self.current_category:
                self.manager.remove_station_by_name(self.current_category, current_name)
                self.manager.add_station(values['category'], values['name'], values['url'])
            else:
                self.manager.update_station(
                    self.current_category, 
                    self.current_station_index, 
                    values['name'], 
                    values['url']
                )
            
            self.manager.save_stations()
            
            if values['category'] != self.current_category:
                self.load_categories()
                index = self.categories_list.findItems(values['category'], 
                                                      Qt.MatchFlag.MatchExactly)
                if index:
                    self.categories_list.setCurrentItem(index[0])
            else:
                self.on_category_selected(self.categories_list.currentItem(), None)
    
    def remove_station(self):
        """Remove selected station."""
        if self.current_station_index < 0 or not self.current_category:
            return
        
        name_item = self.stations_table.item(self.current_station_index, 0)
        if not name_item:
            return
        
        station_name = name_item.text()
        
        reply = QMessageBox.question(
            self.settings_dialog, 
            "Confirm Removal", 
            f"Remove '{station_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.manager.remove_station(self.current_category, self.current_station_index):
                self.manager.save_stations()
                
                # Ako je kategorija automatski obrisana (bila prazna), osvježi cijelu listu
                if self.current_category not in self.manager.stations:
                    self.load_categories()
                else:
                    self.on_category_selected(self.categories_list.currentItem(), None)