"""
Stations manager and configuration
"""
import json
import os
from typing import Dict, List, Tuple
from ..data.stations import DEFAULT_STATIONS

class StationsManager:
    """Manages radio stations and categories"""
    
    def __init__(self):
        self.config_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "..", "config", "stations.json"
        )
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        self.stations = self.load_stations()
    
    def load_stations(self) -> Dict[str, List[Tuple[str, str]]]:
        """Load stations from JSON file or use defaults"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return DEFAULT_STATIONS.copy()
        return DEFAULT_STATIONS.copy()
    
    def save_stations(self) -> bool:
        """Save stations to JSON file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.stations, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False
    
    def add_category(self, name: str) -> bool:
        """Add a new category"""
        if name and name not in self.stations:
            self.stations[name] = []
            return True
        return False
    
    def remove_category(self, name: str) -> bool:
        """Remove a category"""
        if name in self.stations:
            del self.stations[name]
            return True
        return False
    
    def add_station(self, category: str, name: str, url: str) -> bool:
        """Add a station to a category"""
        if category in self.stations and name and url:
            self.stations[category].append((name, url))
            return True
        return False
    
    def remove_station(self, category: str, index: int) -> bool:
        """Remove a station from a category"""
        if category in self.stations and 0 <= index < len(self.stations[category]):
            del self.stations[category][index]
            return True
        return False