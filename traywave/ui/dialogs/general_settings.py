"""
General settings tab for sleep timer and other preferences.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QCheckBox, QSpinBox, QGroupBox
)
from PyQt6.QtCore import Qt


class GeneralSettingsTab(QWidget):
    """General settings tab with sleep timer and other preferences."""
    
    def __init__(self, tray_wave):
        super().__init__()
        self.tray_wave = tray_wave
        self.init_ui()
        self.load_sleep_timer_state()
    
    def init_ui(self):
        """Initialize general settings UI."""
        layout = QVBoxLayout(self)
        
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
        
        # Apply styles
        self.setStyleSheet("""
            QGroupBox {
                border: 2px solid #e5e7eb;
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 15px;
                background-color: white;
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
    
    def _update_sleep_controls(self, state):
        """Enable/disable sleep timer controls based on checkbox."""
        enabled = (state == Qt.CheckState.Checked.value)
        self.sleep_minutes_spin.setEnabled(enabled)
        self.sleep_quit_check.setEnabled(enabled)
    
    def load_sleep_timer_state(self):
        """Load current sleep timer state from engine."""
        sleep_info = self.tray_wave.engine.get_sleep_timer_info()
        if sleep_info and sleep_info["active"]:
            self.sleep_enable.setChecked(True)
            self.sleep_minutes_spin.setValue(sleep_info["minutes_set"])
            self.sleep_quit_check.setChecked(sleep_info["quit_on_expire"])
            self._update_sleep_controls(Qt.CheckState.Checked.value)
    
    def apply_settings(self):
        """Apply sleep timer settings to engine."""
        if self.sleep_enable.isChecked():
            minutes = self.sleep_minutes_spin.value()
            quit_app = self.sleep_quit_check.isChecked()
            self.tray_wave.engine.set_sleep_timer(minutes, quit_app)
            print(f"⏰ Sleep timer set: {minutes} min, quit: {quit_app}")
        else:
            self.tray_wave.engine.cancel_sleep_timer()
            print("⏰ Sleep timer disabled")