"""
Style manager - loads themes and generates CSS
"""
import json
import os
from typing import Dict, Any
from pathlib import Path


class StyleManager:
    """Manages menu themes and CSS generation"""
    
    def __init__(self):
        self.themes = self._load_themes()
        self._cache = {}  # Cache generated CSS
    
    def _load_themes(self) -> Dict[str, Any]:
        """Load themes from JSON file"""
        # Try multiple paths for themes.json
        paths_to_try = [
            # Package resources
            self._get_package_resource_path(),
            # Development path
            Path(__file__).parent / "themes.json",
            # Installed path
            Path("/usr/share/traywave/themes.json"),
        ]
        
        for path in paths_to_try:
            if path and path.exists():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        themes = json.load(f)
                        print(f"✓ Loaded themes from: {path}")
                        return themes
                except Exception as e:
                    print(f"⚠️  Failed to load themes from {path}: {e}")
        
        # Fallback to empty dict
        print("⚠️  No themes.json found, using fallback")
        return self._get_fallback_theme()
    
    def _get_package_resource_path(self):
        """Try to get themes.json from package resources"""
        try:
            from importlib.resources import files
            return files('traywave.ui.tray.styles').joinpath('themes.json')
        except Exception:
            return None
    
    def _get_fallback_theme(self) -> Dict[str, Any]:
        """Fallback theme if JSON loading fails"""
        return {
            "teal": {
                "name": "🌊 Teal",
                "menu": {
                    "background": "rgba(255, 255, 255, 0.98)",
                    "border_radius": "14px",
                    "padding": "10px",
                    "border": "1px solid rgba(6, 182, 212, 0.2)"
                },
                "item": {
                    "padding": "10px 16px",
                    "border_radius": "8px",
                    "color": "#0f172a",
                    "font_size": "13px",
                    "margin": "2px 0px",
                    "hover_background": "rgba(6, 182, 212, 0.1)"
                },
                "separator": {
                    "height": "1px",
                    "background": "rgba(6, 182, 212, 0.3)",
                    "margin": "10px 0px"
                },
                "header": {
                    "background": "#06b6d4",
                    "padding": "14px 16px",
                    "text_color": "white"
                }
            }
        }
    
    def get_theme_names(self) -> list:
        """Get list of all available theme names"""
        return list(self.themes.keys())
    
    def get_theme_display_name(self, theme_name: str) -> str:
        """Get display name for a theme"""
        return self.themes.get(theme_name, {}).get('name', theme_name)
    
    def get_style(self, theme_name: str) -> Dict[str, str]:
        """Get CSS stylesheets for a theme"""
        # Check cache first
        if theme_name in self._cache:
            return self._cache[theme_name]
        
        theme = self.themes.get(theme_name)
        if not theme:
            print(f"⚠️  Theme '{theme_name}' not found, using 'teal'")
            theme = self.themes.get('teal', list(self.themes.values())[0])
        
        # Generate CSS
        result = {
            'name': theme.get('name', theme_name),
            'css': self._generate_menu_css(theme),
            'header_css': self._generate_header_css(theme)
        }
        
        # Cache it
        self._cache[theme_name] = result
        return result
    
    def _generate_menu_css(self, theme: Dict[str, Any]) -> str:
        """Generate menu CSS from theme definition"""
        menu = theme.get('menu', {})
        item = theme.get('item', {})
        separator = theme.get('separator', {})
        
        css = f"""
            QMenu {{
                background-color: {menu.get('background', 'white')};
                border-radius: {menu.get('border_radius', '8px')};
                padding: {menu.get('padding', '8px')};
                border: {menu.get('border', '1px solid #e0e0e0')};
            }}
            QMenu::item {{
                padding: {item.get('padding', '10px 16px')};
                border-radius: {item.get('border_radius', '4px')};
                color: {item.get('color', '#000000')};
                font-size: {item.get('font_size', '13px')};
                margin: {item.get('margin', '2px 0px')};
            }}
            QMenu::item:selected {{
                background: {item.get('hover_background', 'rgba(0, 0, 0, 0.1)')};
            }}
            QMenu::separator {{
                height: {separator.get('height', '1px')};
                background: {separator.get('background', 'rgba(0, 0, 0, 0.1)')};
                margin: {separator.get('margin', '8px 0px')};
            }}
        """
        return css
    
    def _generate_header_css(self, theme: Dict[str, Any]) -> str:
        """Generate header CSS from theme definition"""
        header = theme.get('header', {})
        
        css = f"""
            QWidget {{
                background: {header.get('background', 'transparent')};
        """
        
        if 'border_radius' in header:
            css += f"        border-radius: {header['border_radius']};\n"
        if 'border_bottom' in header:
            css += f"        border-bottom: {header['border_bottom']};\n"
        
        css += f"""        padding: {header.get('padding', '12px 16px')};
            }}
            QLabel {{
                color: {header.get('text_color', 'black')};
                background: transparent;
            }}
        """
        return css
    
    def reload_themes(self):
        """Reload themes from file (useful for development)"""
        self._cache.clear()
        self.themes = self._load_themes()
    
    def get_all_styles(self) -> Dict[str, Dict[str, str]]:
        """Get all styles as dict (for compatibility)"""
        return {
            name: self.get_style(name)
            for name in self.get_theme_names()
        }