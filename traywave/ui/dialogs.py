"""
Dialog windows (settings, etc.)
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QListWidget, QPushButton, QMessageBox, QInputDialog,
    QFrame
)
from PyQt6.QtCore import Qt
from ..core.stations import StationsManager

class SettingsDialog(QDialog):
    """Dialog for managing stations and categories"""
    
    def __init__(self, stations_manager: StationsManager, parent=None):
        super().__init__(parent)
        self.manager = stations_manager
        self.setWindowTitle("TrayWave Settings")
        self.setMinimumSize(600, 400)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize dialog UI"""
        layout = QHBoxLayout(self)
        
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
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        right_layout.addWidget(close_btn)
        
        self.load_categories()
    
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
        version = QLabel("Version: 0.1.2")
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