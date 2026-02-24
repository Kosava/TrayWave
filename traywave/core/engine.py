"""
Audio engine and playback management - SA REQUESTS METADATA READER
"""
from PyQt6.QtCore import QUrl, QTimer, pyqtSignal, QObject, QThread
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaMetaData
from typing import Callable, List
import json
import logging
import os
import re
import stat
import time
from pathlib import Path

logger = logging.getLogger(__name__)

# Pokušaj importovati requests
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    logger.warning("'requests' biblioteka nije instalirana. Metadata neće raditi za FLAC/OGG. Instaliraj sa: pip install requests")


class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.default_config = {
            "show_song_info": True,
            "volume": 50,
            "muted": False,
            "last_station": None,
            "sleep_minutes": 0,  # Dodato za sleep timer
            "sleep_quit_on_expire": False  # Dodato za sleep timer
        }
        self.config = self._load_config()
    
    def _get_config_dir(self) -> str:
        """Get configuration directory path"""
        config_dir = os.path.join(Path.home(), ".config", "traywave")
        os.makedirs(config_dir, exist_ok=True)
        os.chmod(config_dir, stat.S_IRWXU)  # 700 — samo vlasnik
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
        except json.JSONDecodeError as e:
            logger.warning(f"Config fajl je oštećen, koristim default vrijednosti: {e}")
        except OSError as e:
            logger.warning(f"Ne mogu pročitati config fajl: {e}")
        return self.default_config.copy()
    
    def save_config(self):
        """Save configuration to file"""
        try:
            fd = os.open(self.config_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, 'w') as f:
                json.dump(self.config, f, indent=2)
        except OSError as e:
            logger.error(f"Ne mogu sačuvati config: {e}")
    
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
    
    def get_sleep_timer(self):
        """Get sleep timer settings"""
        return {
            "minutes": self.config.get("sleep_minutes", 0),
            "quit_on_expire": self.config.get("sleep_quit_on_expire", False)
        }
    
    def set_sleep_timer(self, minutes: int, quit_on_expire: bool):
        """Set sleep timer settings"""
        self.config["sleep_minutes"] = minutes
        self.config["sleep_quit_on_expire"] = quit_on_expire
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
        self.requestInterruption()
    
    def run(self):
        """Glavna petlja worker thread-a"""
        if not HAS_REQUESTS or not self.url:
            return
        
        self.running = True
        logger.debug(f"MetadataWorker started for: {self.url}")
        
        while self.running and not self.isInterruptionRequested():
            response = None
            try:
                headers = {
                    'Icy-MetaData': '1',
                    'User-Agent': 'Mozilla/5.0 TrayWave/1.0'
                }
                
                response = requests.get(
                    self.url,
                    headers=headers,
                    stream=True,
                    timeout=15
                )
                
                # Postavi socket timeout da spriječimo blokirajući read()
                try:
                    sock = response.raw._fp.fp.raw._sock
                    sock.settimeout(5.0)
                except Exception:
                    pass
                
                metaint = None
                if 'icy-metaint' in response.headers:
                    try:
                        metaint = int(response.headers['icy-metaint'])
                        logger.debug(f"ICY metaint: {metaint}")
                    except (ValueError, TypeError):
                        pass
                
                if not metaint:
                    logger.debug("Nema icy-metaint, koristim polling fallback")
                    self._poll_metadata_fallback(response)
                    response = None  # fallback zatvara response sam
                    return
                
                # Čitanje ICY stream-a: audio bajti → 1 bajt dužine → metadata blok
                while self.running and not self.isInterruptionRequested():
                    audio = response.raw.read(metaint)
                    if not audio or len(audio) < metaint:
                        logger.debug("Stream prekinut, rekonektovanje...")
                        break
                    
                    length_byte = response.raw.read(1)
                    if not length_byte:
                        break
                    meta_length = length_byte[0] * 16
                    
                    if meta_length > 0:
                        meta_bytes = response.raw.read(meta_length)
                        if meta_bytes:
                            try:
                                meta_string = meta_bytes.decode('utf-8', errors='ignore').strip('\x00')
                                logger.debug(f"Raw metadata: {meta_string[:80]}")
                                self._parse_metadata(meta_string)
                            except Exception as e:
                                logger.debug(f"Parse error: {e}")
                
            except Exception as e:
                logger.debug(f"Metadata worker greška: {e}")
            finally:
                if response is not None:
                    try:
                        response.close()
                    except Exception:
                        pass
                    
            # Kratka pauza prije rekonektovanja (100ms koraci za brzi izlaz)
            for _ in range(30):
                if not self.running or self.isInterruptionRequested():
                    break
                time.sleep(0.1)
    
    def _poll_metadata_fallback(self, initial_response):
        """Fallback za streamove bez icy-metaint: polling svakih 15s"""
        
        # Provjeri headere prvog responsa
        self._check_headers_for_title(initial_response.headers)
        # Pročitaj prvih 4KB i traži StreamTitle u body-u
        try:
            chunk = b''
            for c in initial_response.iter_content(chunk_size=1024):
                chunk += c
                if len(chunk) >= 4096:
                    break
            text = chunk.decode('utf-8', errors='ignore')
            m = re.search(r"StreamTitle='([^']*)'", text)
            if m and m.group(1).strip():
                self._parse_metadata(text)
        except Exception:
            pass
        try:
            initial_response.close()
        except Exception:
            pass
        
        # Polling svakih 15s (u 100ms koracima za brzi izlaz)
        while self.running and not self.isInterruptionRequested():
            for _ in range(150):  # 15s = 150 x 100ms
                if not self.running or self.isInterruptionRequested():
                    return
                time.sleep(0.1)
            if not self.running or self.isInterruptionRequested():
                break
            try:
                r = requests.get(
                    self.url,
                    headers={'Icy-MetaData': '1', 'User-Agent': 'TrayWave/1.0'},
                    stream=True,
                    timeout=8
                )
                self._check_headers_for_title(r.headers)
                try:
                    chunk = b''
                    for c in r.iter_content(chunk_size=1024):
                        chunk += c
                        if len(chunk) >= 4096:
                            break
                    text = chunk.decode('utf-8', errors='ignore')
                    if "StreamTitle='" in text:
                        self._parse_metadata(text)
                except Exception:
                    pass
                try:
                    r.close()
                except Exception:
                    pass
            except Exception as e:
                logger.debug(f"Polling fallback greška: {e}")

    def _check_headers_for_title(self, headers):
        """Izvuci StreamTitle iz HTTP response headera"""
        for key in headers:
            if key.lower() in ('streamtitle', 'x-current-song'):
                val = headers[key].strip()
                if val and val != self.last_title:
                    self.last_title = val
                    if ' - ' in val:
                        parts = val.split(' - ', 1)
                        self.metadata_found.emit(parts[0].strip(), parts[1].strip())
                    else:
                        self.metadata_found.emit('', val)
                return

    def _sanitize_metadata(self, text: str, max_len: int = 200) -> str:
        """Sanitize metadata string — ukloni kontrolne karaktere i ograniči dužinu"""
        if not text:
            return ""
        # Ukloni kontrolne karaktere (osim tab/newline koji su benign)
        cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
        return cleaned[:max_len].strip()

    def _parse_metadata(self, meta_string: str):
        """Parsiraj metadata string"""
        try:
            # Traži StreamTitle
            match = re.search(r"StreamTitle='([^']*)'", meta_string)
            if match:
                raw_title = match.group(1)
                title = self._sanitize_metadata(raw_title)

                if title and title != self.last_title:
                    self.last_title = title
                    logger.debug(f"Worker parsed: '{title}'")

                    # Podeli na artist i title
                    if ' - ' in title:
                        parts = title.split(' - ', 1)
                        artist = parts[0].strip()
                        song = parts[1].strip()
                        logger.debug(f"Metadata: {artist} - {song}")
                        self.metadata_found.emit(artist, song)
                    elif ': ' in title:
                        parts = title.split(': ', 1)
                        artist = parts[0].strip()
                        song = parts[1].strip()
                        logger.debug(f"Metadata: {artist} - {song}")
                        self.metadata_found.emit(artist, song)
                    else:
                        logger.debug(f"Metadata: {title}")
                        self.metadata_found.emit("", title)
        except Exception as e:
            logger.debug(f"Parse error: {e}")


class AudioEngine(QObject):
    """Handles audio playback and volume control"""
    
    metadata_changed = pyqtSignal(str, str)
    sleep_timer_changed = pyqtSignal(bool, int)  # is_active, minutes_left
    
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
        
        # Sleep timer
        self.sleep_timer = None
        self.sleep_minutes = 0
        self.sleep_quit_on_expire = False
        
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
        
        # Timer za update sleep timer display-a (pokreće se samo kad je sleep aktivan)
        self.sleep_update_timer = QTimer()
        self.sleep_update_timer.timeout.connect(self._update_sleep_display)

    # === SLEEP TIMER METODE ===
    
    def set_sleep_timer(self, minutes: int, quit_on_expire: bool = False):
        """Set sleep timer to stop playback after X minutes"""
        # Cancel existing timer
        self.cancel_sleep_timer()
        
        if minutes > 0:
            self.sleep_minutes = minutes
            self.sleep_quit_on_expire = quit_on_expire
            
            self.sleep_timer = QTimer()
            self.sleep_timer.setSingleShot(True)
            self.sleep_timer.timeout.connect(self._on_sleep_timeout)
            self.sleep_timer.start(minutes * 60 * 1000)  # min → ms
            
            # Pokreni display update timer
            self.sleep_update_timer.start(60000)  # Svaki minut
            
            # Sačuvaj u config
            self.config.set_sleep_timer(minutes, quit_on_expire)
            
            logger.debug(f"Sleep timer set: {minutes} min, quit: {quit_on_expire}")
            self.sleep_timer_changed.emit(True, minutes)
    
    def cancel_sleep_timer(self):
        """Cancel existing sleep timer"""
        if self.sleep_timer:
            self.sleep_timer.stop()
            self.sleep_timer = None
        
        self.sleep_update_timer.stop()
        
        self.sleep_minutes = 0
        self.sleep_quit_on_expire = False
        
        # Sačuvaj u config
        self.config.set_sleep_timer(0, False)
        
        logger.debug("Sleep timer cancelled")
        self.sleep_timer_changed.emit(False, 0)
    
    def get_sleep_timer_info(self):
        """Get sleep timer info"""
        if not self.sleep_timer:
            return {
                "active": False,
                "minutes_set": 0,
                "minutes_left": 0,
                "quit_on_expire": False
            }
        
        minutes_left = 0
        if self.sleep_timer:
            remaining_ms = self.sleep_timer.remainingTime()
            minutes_left = max(0, remaining_ms // 60000)
        
        return {
            "active": self.sleep_timer is not None,
            "minutes_set": self.sleep_minutes,
            "minutes_left": minutes_left,
            "quit_on_expire": self.sleep_quit_on_expire
        }
    
    def _on_sleep_timeout(self):
        """Handle sleep timer expiration"""
        logger.debug("Sleep timer expired")
        
        # Stop playback
        self.stop()
        
        # Emit signal da je timer završen
        self.sleep_timer_changed.emit(False, 0)
        
        # Reset timer
        self.sleep_timer = None
        self.sleep_minutes = 0
    
    def _update_sleep_display(self):
        """Update sleep timer display (called every minute)"""
        if self.sleep_timer:
            remaining_ms = self.sleep_timer.remainingTime()
            minutes_left = max(0, remaining_ms // 60000)
            if minutes_left > 0:
                self.sleep_timer_changed.emit(True, minutes_left)

    # === OSTALE METODE ===
    
    def play(self, url: str, station_name: str, bitrate: str = "128 kbps"):
        """Play a radio stream"""
        self.current_url = url
        
        # Zaustavi prethodni worker
        if self.metadata_worker.isRunning():
            self.metadata_worker.stop()
            self.metadata_worker.wait(1000)
        
        # Koristi worker za sve HTTP streamove - QMediaPlayer ne čita ICY metadata pouzdano
        if HAS_REQUESTS and (url.startswith('http://') or url.startswith('https://')):
            self.use_worker = True
            logger.debug(f"MetadataWorker started for: {station_name}")
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

    def _split_artist_title(self, metadata: str):
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
        logger.debug(f"Worker metadata: artist='{artist}' title='{title}'")
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
            except Exception:
                return
            
            if title_value and isinstance(title_value, str) and len(title_value) > 0:
                artist, title = self._split_artist_title(title_value)
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

    # === CALLBACK METODE ===
    
    def on_volume_changed(self, callback: Callable):
        self._volume_changed_callbacks.append(callback)

    def on_icon_changed(self, callback: Callable):
        self._icon_changed_callbacks.append(callback)
    
    def on_station_changed(self, callback: Callable):
        self._station_changed_callbacks.append(callback)
    
    def on_metadata_changed(self, callback: Callable):
        """Register callback for metadata changes via signal"""
        self.metadata_changed.connect(callback)
    
    def on_sleep_timer_changed(self, callback: Callable):
        """Register callback for sleep timer changes"""
        self.sleep_timer_changed.connect(callback)

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
        """Notify all metadata listeners via signal"""
        try:
            self.metadata_changed.emit(artist or "", title or "")
        except Exception:
            pass
    
    def _on_playback_changed(self, state):
        self._notify_icon_changed()