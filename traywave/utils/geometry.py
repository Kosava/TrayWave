"""
Geometry and positioning utilities
"""
from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QApplication

def center_popup_near_cursor(popup_width: int, popup_height: int) -> QPoint:
    """
    Calculate position to center a popup near the cursor at bottom of screen
    Returns: QPoint with x, y coordinates
    """
    cursor_pos = QCursor.pos()
    screen = QApplication.screenAt(cursor_pos)
    
    if not screen:
        return cursor_pos
    
    geo = screen.availableGeometry()
    
    # Center horizontally relative to cursor
    x = cursor_pos.x() - popup_width // 2
    
    # Position at bottom of screen
    y = geo.bottom() - popup_height - 10
    
    # Keep within screen bounds
    x = max(geo.left() + 5, min(x, geo.right() - popup_width - 5))
    y = max(geo.top() + 5, min(y, geo.bottom() - popup_height - 5))
    
    return QPoint(x, y)

def is_mouse_in_tray_area(tray_height: int = 60) -> bool:
    """
    Check if mouse is in the tray/notification area at bottom of screen
    tray_height: height of tray area to check (in pixels)
    """
    pos = QCursor.pos()
    screen = QApplication.screenAt(pos)
    
    if not screen:
        return False
    
    screen_geo = screen.geometry()
    
    return (
        pos.x() >= screen_geo.left() and 
        pos.x() <= screen_geo.right() and
        pos.y() >= screen_geo.bottom() - tray_height and
        pos.y() <= screen_geo.bottom()
    )