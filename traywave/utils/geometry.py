"""
Geometry and positioning utilities
"""
from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QApplication

def is_mouse_in_tray_area(tray_height: int = 60) -> bool:
    """
    Check if mouse is in the tray/notification area at bottom of screen
    
    Args:
        tray_height: Height of tray area to check (in pixels)
    
    Returns: True if mouse is in tray area
    """
    pos = QCursor.pos()
    screen = QApplication.screenAt(pos)
    
    if not screen:
        return False
    
    screen_geo = screen.geometry()
    
    # Check if mouse is in bottom tray area
    return (
        pos.x() >= screen_geo.left() and 
        pos.x() <= screen_geo.right() and
        pos.y() >= screen_geo.bottom() - tray_height and
        pos.y() <= screen_geo.bottom()
    )
