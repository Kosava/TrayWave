"""
Dialog windows module for TrayWave.
"""

from .base_dialog import BaseDialog, DialogWithIcon
from .style_picker import StyleSettingsDialog, StylePreviewWidget
from .station_manager import EditStationDialog, StationTableWidget, StationManagerTab
from .about_dialog import AboutDialog
from .general_settings import GeneralSettingsTab

__all__ = [
    'BaseDialog',
    'DialogWithIcon',
    'StyleSettingsDialog',
    'StylePreviewWidget',
    'EditStationDialog',
    'StationTableWidget',
    'StationManagerTab',
    'AboutDialog',
    'GeneralSettingsTab',
]