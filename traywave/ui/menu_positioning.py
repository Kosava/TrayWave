"""
Menu positioning utilities - uses actual menu height for correct positioning
"""
from PyQt6.QtCore import QPoint, QRect
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QCursor

from .menu_builder import MENU_WIDTH


class MenuPositioner:
    """Handles menu positioning - smart positioning for tray icons"""
    
    @staticmethod
    def calculate_position(tray_geometry: QRect, menu_height: int = 500) -> QPoint:
        """
        Position menu intelligently based on tray icon position.
        menu_height: stvarna visina menija (iz menu.sizeHint().height())
        """
        cursor_pos = QCursor.pos()
        
        screen = QApplication.screenAt(cursor_pos)
        if not screen:
            screen = QApplication.primaryScreen()
        
        screen_geo = screen.availableGeometry()
        
        # Ograniči visinu menija na visinu ekrana
        menu_height = min(menu_height, screen_geo.height() - 50)
        
        distance_from_right = screen_geo.right() - cursor_pos.x()
        distance_from_bottom = screen_geo.bottom() - cursor_pos.y()
        
        if distance_from_bottom < 150:
            # Tray je na dnu - meni ide TAČNO iznad taskbara (zalijepljen za dno)
            y = screen_geo.bottom() - menu_height
            
            if distance_from_right < 400:
                # Donji desni ugao - poravnat desno
                x = screen_geo.right() - MENU_WIDTH
            else:
                # Dno, ali ne desni ugao - centriraj na kursor
                x = cursor_pos.x() - MENU_WIDTH // 2
        
        elif distance_from_right < 200:
            # Desna ivica, nije dno
            x = screen_geo.right() - MENU_WIDTH
            y = cursor_pos.y() - menu_height // 2
        
        else:
            # Default: centriraj na kursor
            x = cursor_pos.x() - MENU_WIDTH // 2
            if cursor_pos.y() > screen_geo.height() / 2:
                y = cursor_pos.y() - menu_height - 10
            else:
                y = cursor_pos.y() + 10
        
        # Ograniči da ne izlazi van ekrana
        x = max(screen_geo.left(), min(x, screen_geo.right() - MENU_WIDTH))
        y = max(screen_geo.top(), min(y, screen_geo.bottom() - menu_height))
        
        return QPoint(x, y)