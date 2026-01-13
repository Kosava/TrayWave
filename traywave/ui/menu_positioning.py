"""
Menu positioning utilities
"""
from PyQt6.QtCore import QPoint, QRect
from PyQt6.QtWidgets import QApplication


class MenuPositioner:
    """Handles menu positioning near tray icon"""
    
    ESTIMATED_MENU_HEIGHT = 800
    ESTIMATED_MENU_WIDTH = 280
    SCREEN_MARGIN = 10
    
    @staticmethod
    def calculate_position(tray_geometry: QRect) -> QPoint:
        """
        Calculate optimal menu position near tray icon
        
        Args:
            tray_geometry: QRect of tray icon geometry
            
        Returns:
            QPoint for menu position
        """
        screen = QApplication.primaryScreen()
        screen_geo = screen.availableGeometry()
        
        if tray_geometry.isValid() and tray_geometry.y() >= 0:
            # Valid tray geometry - position near it
            return MenuPositioner._position_near_tray(tray_geometry, screen_geo)
        else:
            # No valid tray geometry - use corner
            return MenuPositioner._position_at_corner(screen_geo)
    
    @staticmethod
    def _position_near_tray(tray_geo: QRect, screen_geo: QRect) -> QPoint:
        """Position menu near tray icon"""
        x = tray_geo.x()
        y = tray_geo.y()
        
        # Vertical positioning
        # If tray is in bottom half of screen, show menu above it
        if y > screen_geo.height() / 2:
            y = tray_geo.top() - MenuPositioner.ESTIMATED_MENU_HEIGHT - 5
        else:
            y = tray_geo.bottom() + 5
        
        # Horizontal positioning
        # If tray is in right half of screen, align menu to right edge
        if x > screen_geo.width() / 2:
            x = tray_geo.right() - MenuPositioner.ESTIMATED_MENU_WIDTH
        
        # Ensure menu stays on screen
        return MenuPositioner._clamp_to_screen(x, y, screen_geo)
    
    @staticmethod
    def _position_at_corner(screen_geo: QRect) -> QPoint:
        """Position menu at bottom-right corner (typical tray location)"""
        x = screen_geo.right() - MenuPositioner.ESTIMATED_MENU_WIDTH - MenuPositioner.SCREEN_MARGIN
        y = screen_geo.bottom() - MenuPositioner.ESTIMATED_MENU_HEIGHT - MenuPositioner.SCREEN_MARGIN
        
        return MenuPositioner._clamp_to_screen(x, y, screen_geo)
    
    @staticmethod
    def _clamp_to_screen(x: int, y: int, screen_geo: QRect) -> QPoint:
        """Ensure position is within screen bounds"""
        margin = MenuPositioner.SCREEN_MARGIN
        
        # Clamp X
        if x < screen_geo.left():
            x = screen_geo.left() + margin
        if x + MenuPositioner.ESTIMATED_MENU_WIDTH > screen_geo.right():
            x = screen_geo.right() - MenuPositioner.ESTIMATED_MENU_WIDTH - margin
        
        # Clamp Y
        if y < screen_geo.top():
            y = screen_geo.top() + margin
        if y + MenuPositioner.ESTIMATED_MENU_HEIGHT > screen_geo.bottom():
            y = screen_geo.bottom() - MenuPositioner.ESTIMATED_MENU_HEIGHT - margin
        
        return QPoint(x, y)