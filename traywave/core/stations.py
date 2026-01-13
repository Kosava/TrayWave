"""
Radio stanice iz Radio Browser API (radio-browser.info)
Auto-generisano sa verifikovanim stream-ovima
"""
from PyQt6.QtCore import QObject, pyqtSignal
import json
import os
from typing import Dict, List, Tuple

DEFAULT_STATIONS = {
    # ============ EX-YU ============
    "EX-YU": [
        ("Cool Radio", "http://176.9.30.66/cool64"),
        ("OK radio", "https://sslstream.okradio.net/;?type=http&nocache=8804"),
        ("Hit FM Radio Beograd", "http://streaming.hitfm.rs:8000/hit"),
        ("Naxi Radio", "http://naxi48.streaming.rs:9180/"),
        ("Naxi Radio", "http://naxi128.streaming.rs:9150/"),
        ("TDI Radio", "http://streaming.tdiradio.com:8000/tdiradio"),
        ("Play", "http://stream.playradio.rs:8001/play.aac"),
        ("Radio S3 Južni", "https://stream.radios.rs:9038/;*.mp3"),
        ("Karolina", "http://streaming.karolina.rs:8000/karolina"),
        ("Radio Nostalgija", "http://nostalgie128.streaming.rs:9250/"),
    ],
    "Dance": [
        ("Dance Wave!", "http://onair.dancewave.online:8080/dance.mp3"),
        ("Intense Radio - We love Dance #HQ# FLAC", "http://secure.live-streams.nl/flac.ogg"),
    ],
    "Rock": [
        ("Radio Caroline", "http://78.129.202.200:8040/;"),
    ],
}


class StationsManager(QObject):
    """Menadžer za radio stanice sa perzistencijom"""
    
    # OBAVEZNO - definicija signala NA NIVOU KLASE
    stations_changed = pyqtSignal()
    
    def __init__(self, config_dir=None):
        super().__init__()
        self.config_dir = config_dir or os.path.expanduser("~/.config/traywave")
        self.stations_file = os.path.join(self.config_dir, "stations.json")
        self.stations = DEFAULT_STATIONS.copy()
        self.load_stations()
    
    def load_stations(self):
        """Učitaj stanice iz fajla"""
        if os.path.exists(self.stations_file):
            try:
                with open(self.stations_file, 'r', encoding='utf-8') as f:
                    loaded_stations = json.load(f)
                    if loaded_stations:
                        self.stations = loaded_stations
            except Exception as e:
                print(f"Greška pri učitavanju stanica: {e}")
                self.stations = DEFAULT_STATIONS.copy()
    
    def save_stations(self):
        """Sačuvaj stanice u fajl"""
        os.makedirs(self.config_dir, exist_ok=True)
        try:
            with open(self.stations_file, 'w', encoding='utf-8') as f:
                json.dump(self.stations, f, indent=2, ensure_ascii=False)
            self.stations_changed.emit()
            return True
        except Exception as e:
            print(f"Greška pri čuvanju stanica: {e}")
            return False
    
    def add_category(self, name: str) -> bool:
        """Dodaj novu kategoriju"""
        if name in self.stations:
            return False
        self.stations[name] = []
        return True
    
    def remove_category(self, name: str) -> bool:
        """Ukloni kategoriju"""
        if name not in self.stations:
            return False
        del self.stations[name]
        return True
    
    def add_station(self, category: str, name: str, url: str) -> bool:
        """Dodaj stanicu u kategoriju"""
        if category not in self.stations:
            return False
        for existing_name, existing_url in self.stations[category]:
            if existing_name == name or existing_url == url:
                return False
        self.stations[category].append((name, url))
        return True
    
    def remove_station(self, category: str, index: int) -> bool:
        """Ukloni stanicu iz kategorije"""
        if category not in self.stations:
            return False
        if index < 0 or index >= len(self.stations[category]):
            return False
        self.stations[category].pop(index)
        return True
    
    def refresh_stations(self):
        """Osveži stanice sa diska"""
        try:
            self.load_stations()
            self.stations_changed.emit()
            return True
        except Exception as e:
            print(f"Greška pri osvežavanju stanica: {e}")
            return False
    
    def get_categories(self) -> List[str]:
        """Dobij listu imena kategorija"""
        return list(self.stations.keys())
    
    def get_stations(self, category: str) -> List[Tuple[str, str]]:
        """Dobij stanice za kategoriju"""
        return self.stations.get(category, [])
