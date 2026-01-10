"""
Audio engine and playback management - SA REQUESTS METADATA READER
"""
from PyQt6.QtCore import QUrl, QTimer, pyqtSignal, QObject, QThread
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaMetaData
from typing import Callable, List
import json
import os
import re
import struct
from pathlib import Path

# Pokušaj importovati requests
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("⚠️  'requests' biblioteka nije instalirana. Metadata neće raditi za FLAC/OGG.")
    print("Instaliraj sa: pip install requests")


class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.default_config = {
            "show_song_info": True,
            "volume": 50,
            "muted": False,
            "last_station": None
        }
        self.config = self._load_config()
    
    def _get_config_dir(self) -> str:
        """Get configuration directory path"""
        config_dir = os.path.join(Path.home(), ".config", "traywave")
        os.makedirs(config_dir, exist_ok=True)
        return config_dir
    
    def _load_config(self) -> dict:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    for key, value in self.default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
        except Exception:
            pass
        return self.default_config.copy()
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception:
            pass
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        """Set configuration value"""
        self.config[key] = value
        self.save_config()
    
    def get_show_song_info(self) -> bool:
        """Get whether to show song info"""
        return self.config.get("show_song_info", True)
    
    def set_show_song_info(self, value: bool):
        """Set whether to show song info"""
        self.config["show_song_info"] = value
        self.save_config()


class MetadataWorker(QThread):
    """Worker thread koji čita ICY metadata u pozadini"""
    
    metadata_found = pyqtSignal(str, str)  # artist, title
    
    def __init__(self):
        super().__init__()
        self.url = None
        self.running = False
        self.last_title = None
    
    def set_url(self, url: str):
        """Postavi URL za čitanje"""
        self.url = url
        self.last_title = None
    
    def stop(self):
        """Zaustavi worker"""
        self.running = False
    
    def run(self):
        """Glavna petlja worker thread-a"""
        if not HAS_REQUESTS or not self.url:
            return
        
        self.running = True
        
        try:
            # Napravi request sa ICY-MetaData headerom
            headers = {
                'Icy-MetaData': '1',
                'User-Agent': 'TrayWave/1.0'
            }
            
            response = requests.get(
                self.url, 
                headers=headers, 
                stream=True,
                timeout=10
            )
            
            # Izvuci metaint iz headera
            metaint = None
            if 'icy-metaint' in response.headers:
                try:
                    metaint = int(response.headers['icy-metaint'])
                    print(f"📡 ICY metaint: {metaint}")
                except:
                    pass
            
            if not metaint:
                print("⚠️  Stream ne podržava ICY metadata")
                return
            
            # Čitaj stream i parsiraj metadata
            buffer = b''
            bytes_until_metadata = metaint
            
            for chunk in response.iter_content(chunk_size=4096):
                if not self.running:
                    break
                
                buffer += chunk
                
                while len(buffer) >= bytes_until_metadata:
                    # Preskoči audio podatke
                    buffer = buffer[bytes_until_metadata:]
                    
                    if len(buffer) < 1:
                        break
                    
                    # Pročitaj metadata length (prvi bajt * 16)
                    meta_length = buffer[0] * 16
                    buffer = buffer[1:]
                    
                    if meta_length > 0:
                        if len(buffer) >= meta_length:
                            # Izvuci metadata
                            meta_bytes = buffer[:meta_length]
                            buffer = buffer[meta_length:]
                            
                            # Dekodiraj metadata
                            try:
                                meta_string = meta_bytes.decode('utf-8', errors='ignore').strip('\x00')
                                self._parse_metadata(meta_string)
                            except:
                                pass
                            
                            bytes_until_metadata = metaint
                        else:
                            # Nedovoljno podataka, sačekaj još
                            bytes_until_metadata = 0
                            break
                    else:
                        bytes_until_metadata = metaint
        
        except Exception as e:
            print(f"❌ Metadata worker greška: {e}")
    
    def _parse_metadata(self, meta_string: str):
        """Parsiraj metadata string"""
        try:
            # Traži StreamTitle
            match = re.search(r"StreamTitle='([^']*)'", meta_string)
            if match:
                title = match.group(1).strip()
                
                if title and title != self.last_title:
                    self.last_title = title
                    
                    # Podeli na artist i title
                    if ' - ' in title:
                        parts = title.split(' - ', 1)
                        artist = parts[0].strip()
                        song = parts[1].strip()
                        print(f"🎵 Metadata: {artist} - {song}")
                        self.metadata_found.emit(artist, song)
                    elif ': ' in title:
                        parts = title.split(': ', 1)
                        artist = parts[0].strip()
                        song = parts[1].strip()
                        print(f"🎵 Metadata: {artist} - {song}")
                        self.metadata_found.emit(artist, song)
                    else:
                        print(f"🎵 Metadata: {title}")
                        self.metadata_found.emit("", title)
        except Exception as e:
            print(f"Parse error: {e}")


class AudioEngine(QObject):
    """Handles audio playback and volume control"""
    
    metadata_changed = pyqtSignal(str, str)
    
    def __init__(self):
        super().__init__()
        
        self.config = ConfigManager()
        self.audio = QAudioOutput()
        
        volume = self.config.get("volume", 50)
        self.audio.setVolume(volume / 100)
        
        muted = self.config.get("muted", False)
        self.audio.setMuted(muted)
        self._muted = muted

        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio)

        self._volume_before_mute = volume
        self._volume_changed_callbacks: List[Callable] = []
        self._icon_changed_callbacks: List[Callable] = []
        self._station_changed_callbacks: List[Callable] = []
        self._metadata_callbacks: List[Callable] = []
        
        self.current_station = None
        self.current_bitrate = "128 kbps"
        self.current_song = None
        self.current_artist = None
        self.current_url = None
        
        # Metadata worker za sve streamove
        self.metadata_worker = MetadataWorker()
        self.metadata_worker.metadata_found.connect(self._on_worker_metadata)
        
        # Flag da li koristimo worker ili PyQt metadata
        self.use_worker = False
        
        self.player.playbackStateChanged.connect(self._on_playback_changed)
        self.player.metaDataChanged.connect(self._on_qt_metadata_changed)
        
        # Fallback timer
        self.metadata_timer = QTimer()
        self.metadata_timer.timeout.connect(self._check_metadata)
        self.metadata_timer.setInterval(5000)

    def play(self, url: str, station_name: str, bitrate: str = "128 kbps"):
        """Play a radio stream"""
        self.current_url = url
        
        # Zaustavi prethodni worker
        if self.metadata_worker.isRunning():
            self.metadata_worker.stop()
            self.metadata_worker.wait(1000)
        
        # Odluči koji sistem koristiti
        # Za FLAC/OGG ili ako PyQt ne radi dobro, koristi worker
        if HAS_REQUESTS and ('.flac' in url.lower() or '.ogg' in url.lower() or 'flac' in bitrate.lower()):
            self.use_worker = True
            print(f"🎵 Koristim requests metadata worker za: {station_name}")
            self.metadata_worker.set_url(url)
            self.metadata_worker.start()
            self.metadata_timer.stop()
        else:
            self.use_worker = False
            self.metadata_timer.start()
        
        self.player.setSource(QUrl(url))
        self.player.play()
        self.current_station = station_name
        self.current_bitrate = bitrate
        self.current_song = None
        self.current_artist = None
        
        self.config.set("last_station", {
            "name": station_name,
            "url": url,
            "bitrate": bitrate
        })
        
        if self._muted:
            self._muted = False
            self.audio.setMuted(False)
            
        self._notify_icon_changed()
        self._notify_station_changed()

    def stop(self):
        """Stop playback"""
        self.player.stop()
        
        # Zaustavi worker
        if self.metadata_worker.isRunning():
            self.metadata_worker.stop()
            self.metadata_worker.wait(1000)
        
        self.current_station = None
        self.current_song = None
        self.current_artist = None
        self.current_url = None
        self.use_worker = False
        self.metadata_timer.stop()
        self._notify_icon_changed()
        self._notify_station_changed()
        self._notify_metadata_changed(None, None)

    def set_volume(self, value: int):
        """Set volume (0-100)"""
        value = max(0, min(100, value))
        self.audio.setVolume(value / 100)
        
        if not self._muted:
            self._volume_before_mute = value
        
        self.config.set("volume", value)
        self._notify_volume_changed(value)

    def change_volume(self, delta: int):
        """Change volume by delta"""
        v = int(self.audio.volume() * 100)
        self.set_volume(v + delta)

    def toggle_mute(self) -> bool:
        """Toggle mute state"""
        self._muted = not self._muted
        
        if self._muted:
            self._volume_before_mute = self.get_volume()
            self.audio.setMuted(True)
        else:
            self.audio.setMuted(False)
            self.set_volume(self._volume_before_mute)
        
        self.config.set("muted", self._muted)
        self._notify_icon_changed()
        return self._muted

    def get_volume(self) -> int:
        """Get current volume (0-100)"""
        return int(self.audio.volume() * 100)
    
    def is_playing(self) -> bool:
        """Check if audio is playing"""
        return self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState
    
    def is_muted(self) -> bool:
        """Check if audio is muted"""
        return self._muted
    
    def get_show_song_info(self) -> bool:
        """Get whether to show song info"""
        return self.config.get_show_song_info()
    
    def set_show_song_info(self, value: bool):
        """Set whether to show song info"""
        self.config.set_show_song_info(value)
    
    def get_last_station(self):
        """Get last played station"""
        return self.config.get("last_station")

    def _parse_metadata(self, metadata: str):
        """Parse StreamTitle metadata"""
        if not metadata:
            return None, None
        
        metadata = metadata.strip()
        
        if metadata.startswith("StreamTitle='") and metadata.endswith("';"):
            metadata = metadata[13:-2]
        
        if " - " in metadata:
            parts = metadata.split(" - ", 1)
            return parts[0].strip(), parts[1].strip()
        elif ": " in metadata:
            parts = metadata.split(": ", 1)
            return parts[0].strip(), parts[1].strip()
        else:
            return None, metadata

    def _on_worker_metadata(self, artist: str, title: str):
        """Callback kada worker pronađe metadata"""
        if artist != self.current_artist or title != self.current_song:
            self.current_artist = artist if artist else None
            self.current_song = title if title else None
            self._notify_metadata_changed(artist, title)

    def _on_qt_metadata_changed(self):
        """Handle metadata changes from QMediaPlayer - samo za non-FLAC"""
        if self.use_worker:
            return
        
        try:
            metadata = self.player.metaData()
            if not metadata:
                return
            
            title_value = None
            
            try:
                title_value = metadata.stringValue(QMediaMetaData.Key.Title)
            except:
                return
            
            if title_value and isinstance(title_value, str) and len(title_value) > 0:
                artist, title = self._parse_metadata(title_value)
                if artist != self.current_artist or title != self.current_song:
                    self.current_artist = artist
                    self.current_song = title
                    self._notify_metadata_changed(artist, title)
        
        except Exception:
            pass

    def _check_metadata(self):
        """Manual check for metadata (fallback)"""
        if self.is_playing() and not self.use_worker:
            self._on_qt_metadata_changed()

    def on_volume_changed(self, callback: Callable):
        self._volume_changed_callbacks.append(callback)

    def on_icon_changed(self, callback: Callable):
        self._icon_changed_callbacks.append(callback)
    
    def on_station_changed(self, callback: Callable):
        self._station_changed_callbacks.append(callback)
    
    def on_metadata_changed(self, callback: Callable):
        """Register callback for metadata changes"""
        self._metadata_callbacks.append(callback)

    def _notify_volume_changed(self, value: int):
        for callback in self._volume_changed_callbacks:
            callback(value)
    
    def _notify_icon_changed(self):
        for callback in self._icon_changed_callbacks:
            callback()
    
    def _notify_station_changed(self):
        for callback in self._station_changed_callbacks:
            callback()
    
    def _notify_metadata_changed(self, artist: str, title: str):
        """Notify all metadata callbacks"""
        try:
            self.metadata_changed.emit(artist or "", title or "")
        except:
            pass
        for callback in self._metadata_callbacks:
            try:
                callback(artist, title)
            except:
                pass
    
    def _on_playback_changed(self, state):
        self._notify_icon_changed()