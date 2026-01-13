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
        ("Lola Radio", "https://streaming.tdiradio.com/radiolola.mp3"),
        ("TDI Radio", "http://streaming.tdiradio.com:8000/tdiradio"),
        ("Play", "http://stream.playradio.rs:8001/play.aac"),
        ("Radio S3 Južni", "https://stream.radios.rs:9038/;*.mp3"),
        ("Karolina", "http://streaming.karolina.rs:8000/karolina"),
        ("Radio Nostalgija", "http://nostalgie128.streaming.rs:9250/"),
    ],

    # ============ DANCE ============
    "Dance": [
        ("Dance Wave!", "http://onair.dancewave.online:8080/dance.mp3"),
        ("Intense Radio - We love Dance #HQ# FLAC", "http://secure.live-streams.nl/flac.ogg"),
        ("Intense Radio - We love Dance 256k", "http://intenseradio.live-streams.nl:8000/main"),
        ("EuroDance 90 radio", "https://stream-eurodance90.fr/radio/8000/128.mp3?1627933323"),
        ("Ibiza Global Radio", "http://cdn-peer022.streaming-pro.com:8024/ibizaglobalradio.mp3"),
        ("Chocolate FM", "http://streaming5.elitecomunicacion.es:8082/live.mp3"),
        ("Radio Stereocittà", "http://onair11.xdevel.com:8134/;stream.mp3"),
        ("1000 HITS 80s", "http://c2.auracast.net:8048/stream"),
        ("Sunshine Live - Die 90er", "http://sunsl.streamabc.net/sunsl-90er-mp3-192-9697679?sABC=6961o89n%230%234313or3p195706q13n90589o7061s597%23fgernz.fhafuvar-yvir.qr&aw_0_1st.playerid=stream.sunshine-live.de&amsparams=playerid:stream.sunshine-live.de;skey:1768011930"),
        ("Fun Radio", "http://streamer-04.rtl.fr/fun-1-44-128"),
    ],

    # ============ TECHNO & TRANCE ============
    "Techno & Trance": [
        ("Deep House Lounge", "http://198.15.94.34:8006/stream"),
        ("Intense Radio - We love Dance #HQ# FLAC", "http://secure.live-streams.nl/flac.ogg"),
        ("Radio Schizoid - Dub Techno", "http://94.130.113.214:8000/dubtechno"),
        ("TranceBase.FM - AAC HD 256k", "http://listener2.aachd.tb-group.fm:80/trb-hd.aac"),
        ("TechnoBase.FM", "http://lw2.mp3.tb-group.fm/tb.mp3"),
        ("Dance Wave!", "http://onair.dancewave.online:8080/dance.mp3"),
        ("Intense Radio - We love Dance #HQ# FLAC", "http://secure.live-streams.nl/flac.ogg"),
        ("Radio Schizoid - Progressive Psychedelic Trance", "http://94.130.113.214:8000/prog"),
        ("TranceBase.FM - AAC HD 256k", "http://listener2.aachd.tb-group.fm:80/trb-hd.aac"),
        ("1.FM - Amsterdam Trance Radio", "http://strm112.1.fm/atr_mobile_mp3"),
    ],

    # ============ HIP HOP ============
    "Hip Hop": [
        ("Rap/Hip Hop", "http://185.32.188.17:8097/stream"),
        ("- 0 N - Indie on Radio", "https://0n-indie.radionetz.de/0n-indie.mp3"),
        ("deutschrap", "http://deutschrap.stream.laut.fm/deutschrap?t302=2026-01-10_08-13-38&uuid=bf3474b3-b64a-441c-9056-2a22013c1bdd"),
        ("# TOP 100 CLUB CHARTS - DANCE & DJ MIX RADIO - 24 HOURS NON-STOP MUSIC @ TikTok Hits, Ibiza House, Sunset Lounge, Melodic Music, EDM, Deep House, Dance Music, Techno & Hypertechno, Rave Charts, Top 40 Charts, Latin, Reggaeton Music, Moombahton, Urban Hits, HipHop, Party & Clubbing Radio, Trending Chartmusic, R&B, Urban, Mixtape - & LIVE DJ SET ", "https://rautemusik.stream25.radiohost.de/breakz?ref=radiobrowser-top100-clubcharts&upd-meta&upd-scheme=https&_art=dD0xNzY3OTk3NTQ1JmQ9ZmVmNDQ2MzAxNDYzNjkyYzQxNmM"),
        (".100 Hip hop and RNB FM", "https://ice64.securenetsystems.net/LFTM"),
        ("Top Urbano", "https://radio.dominiserver.com/proxy/topurbano?mp=/stream"),
        ("Studio 92 (92.5 FM Lima)", "https://us-b4-p-e-pb13-audio.cdn.mdstrm.com/live-audio-aw/5fada553978fe1080e3ac5ea?aid=5faaeb72f92d7b07dfe10181&pid=GCeuRKXQJAe8pvMxLzLm5dGPXiV8ufGI&sid=EGIFKd6TIDucZpfYHwMKaiPPtY2iq7o8&uid=AT3UUEUthOMyaoe40Fq0IOYuBc2bqZ6K&es=us-b4-p-e-pb13-audio.cdn.mdstrm.com&ote=1768138006758&ot=_R6YM57HZIl_8x2eRnd98A&proto=https&pz=us&cP=128000&awCollectionId=5faaeb72f92d7b07dfe10181&liveId=5fada553978fe1080e3ac5ea&listenerId=AT3UUEUthOMyaoe40Fq0IOYuBc2bqZ6K"),
        ("Virgin Radio Romania", "https://astreaming.edi.ro:8443/VirginRadio_aac"),
        ("All Underground Hip Hop Radio", "http://n06.radiojar.com/c1912tk5rtzuv?rj-ttl=5&rj-tok=AAABm6eVK_8ARYQ9EuMuxV72Mg"),
        ("181.FM - Old School HipHop/RnB", "http://listen.181fm.com/181-oldschool_128k.mp3"),
    ],

    # ============ ROCK ============
    "Rock": [
        ("Rockabilly-radio.net", "http://lin3.ash.fast-serv.com:6026/stream_96"),
        ("Radio Caroline", "http://78.129.202.200:8040/;"),
        ("Big R Radio - 80s Metal FM", "http://bigrradio.cdnstream1.com/5186_128"),
        ("RTL2", "http://streamer-04.rtl.fr/rtl2-1-44-128"),
        ("Virgin Radio Classic Rock", "http://icy.unitedradio.it/VirginRockClassics.mp3"),
        ("Hard Rock Heaven", "http://hydra.cdnstream.com/1521_128"),
        ("1LIVE", "http://d111.rndfnk.com/ard/wdr/1live/live/mp3/128/stream.mp3?cid=01FBRZTS1K1TCD4KA2YZ1ND8X3&sid=383ini3vXB4dIp4U3LOvef4nJvE&token=zZnWzDd3fNPrHIgHskAdZagqxHFy7GvIJYb1oCacZ-k&tvf=hnvLGfNliRhkMTExLnJuZGZuay5jb20"),
        ("Antyradio", "https://n-4-2.dcs.redcdn.pl/sc/o2/Eurozet/live/antyradio.livx?audio=5"),
        ("Rock Antenne", "http://s5-webradio.rockantenne.de/rockantenne"),
        ("TMM 1", "https://listen-msmn.sharp-stream.com/nme1.mp3"),
    ],

    # ============ JAZZ ============
    "Jazz": [
        ("Classic Vinyl HD", "https://icecast.walmradio.com:8443/classic"),
        ("Adroit Jazz Underground", "https://icecast.walmradio.com:8443/jazz"),
        ("101 SMOOTH JAZZ", "http://jking.cdnstream1.com/b22139_128mp3"),
        ("Deep House Lounge", "http://198.15.94.34:8006/stream"),
        ("Jazz Radio Blues", "http://jazzblues.ice.infomaniak.ch/jazzblues-high.mp3"),
        ("Adroit Jazz Underground HD Opus", "https://icecast.walmradio.com:8443/jazz_opus"),
        ("Jazz Radio", "http://jazzradio.ice.infomaniak.ch/jazzradio-high.mp3"),
        ("Classic Vinyl HD Opus", "https://icecast.walmradio.com:8443/classic_opus"),
        ("Classic Vinyl HD", "https://icecast.walmradio.com:8443/classic"),
        ("Antena 1 São Paulo, SP (ZYD823 94,7 MHz FM) [aac]", "http://antena1.newradio.it/stream?ext=.mp3"),
    ],

    # ============ POP ============
    "Pop": [
        ("RMF FM", "http://195.150.20.9/RMFFM48"),
        ("Radio Caroline", "http://78.129.202.200:8040/;"),
        (" Radio Navahang", "https://navairan.com/;stream.nsv"),
        ("Synthetic FM The New Italo generation sound", "https://mediaserv38.live-streams.nl:18030/stream"),
        ("EuroDance 90 radio", "https://stream-eurodance90.fr/radio/8000/128.mp3?1627933323"),
        ("RTL2", "http://streamer-04.rtl.fr/rtl2-1-44-128"),
        ("Capital FM London", "http://media-ice.musicradio.com/CapitalMP3"),
        ("Radio 105 Network", "http://icecast.unitedradio.it/Radio105.mp3"),
        ("Hits 1 Algérie", "https://radio12.pro-fhi.net/listen/whmnrlow/stream"),
        ("Heart 80s", "https://media-ssl.musicradio.com/Heart80sMP3"),
    ],

    # ============ CLASSICAL ============
    "Classical": [
        ("WALM 2 HD", "https://icecast.walmradio.com:8443/walm2"),
        ("parsa", "http://parsa.icdndhcp.com:18000/stream"),
        ("WALM 2 HD Opus", "https://icecast.walmradio.com:8443/walm2_opus"),
        ("Classic FM UK", "http://ice-the.musicradio.com/ClassicFMMP3"),
        ("Your Classical - Relax", "http://relax.stream.publicradio.org/relax.mp3"),
        ("caltexmusic", "http://n03.radiojar.com/cp13r2cpn3quv?rj-ttl=5&rj-tok=AAABm6f0MvkAl57PAP9olzjqiw"),
        ("Mosaique FM", "https://radio.mosaiquefm.net/mosalive"),
        ("Jazz Radio Classic Jazz", "http://jazz-wr01.ice.infomaniak.ch/jazz-wr01-128.mp3"),
        ("إذاعة القرآن الكريم", "http://n03.radiojar.com/0tpy1h0kxtzuv?rj-ttl=5&rj-tok=AAABm6llo20AGv811MUq9vd5oQ"),
        ("Rai Radio 3", "http://icecdn-19d24861e90342cc8decb03c24c8a419.msvdn.net/icecastRelay/S56630579/yEbkcBtIoSwd/icecast"),
    ],

    # ============ CHILL & LOFI ============
    "Chill & Lofi": [
        ("ABC Lounge Radio", "https://eu1.fastcast4u.com/proxy/kpmxz?mp=/1"),
        ("Antenne Bayern - Chillout", "http://s5-webradio.antenne.de/chillout"),
        ("Smooth Chill", "https://media-ssl.musicradio.com/ChillMP3"),
        ("1.FM - Chillout Lounge Radio", "http://strm112.1.fm/chilloutlounge_mobile_mp3"),
        ("Costa Del Mar - Chillout (AAC 96kbps)", "http://stream.cdm-chillout.com:8020/stream-AAC-Chill"),
        ("Café del Mar", "https://streams.radio.co/se1a320b47/listen"),
        ("REGGAE CHILL CAFE", "https://maggie.torontocast.com:2020/stream/reggaechillcafe"),
        ("- 0 N - Smooth Jazz on Radio", "https://0n-smoothjazz.radionetz.de/0n-smoothjazz.aac"),
        ("- 0 N - Chillout on Radio", "https://0n-chillout.radionetz.de/0n-chillout.aac"),
        ("Costa del Mar - Chill Out", "http://stream.cdm-chillout.com:8020/stream-mp3-Chill"),
    ],

    # ============ ELECTRONIC ============
    "Electronic": [
        ("Dance Wave!", "http://onair.dancewave.online:8080/dance.mp3"),
        ("Deep House Lounge", "http://198.15.94.34:8006/stream"),
        ("Frisky", "http://stream2.friskyradio.com/frisky_mp3_hi"),
        ("Intense Radio - We love Dance 256k", "http://intenseradio.live-streams.nl:8000/main"),
        ("Synthetic FM The New Italo generation sound", "https://mediaserv38.live-streams.nl:18030/stream"),
        ("Deep House Radio", "http://62.210.105.16:7000/stream"),
        ("EuroDance 90 radio", "https://stream-eurodance90.fr/radio/8000/128.mp3?1627933323"),
        ("Ibiza Global Radio", "http://cdn-peer022.streaming-pro.com:8024/ibizaglobalradio.mp3"),
        ("Synthetic FM - The radio for the Synth lovers", "https://mediaserv38.live-streams.nl:18040/live"),
        ("Radio Meuh", "http://radiomeuh.ice.infomaniak.ch/radiomeuh-128.mp3"),
    ],

}


class StationsManager(QObject):
    """Menadžer za radio stanice sa perzistencijom"""
    
    # ⭐ KLJUČNA ISPRAVKA - DEFINICIJA SIGNALA ⭐
    # Signal koji se emituje kada se stanice promene
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
                # Zadrži default stanice
                self.stations = DEFAULT_STATIONS.copy()
    
    def save_stations(self):
        """Sačuvaj stanice u fajl"""
        os.makedirs(self.config_dir, exist_ok=True)
        try:
            with open(self.stations_file, 'w', encoding='utf-8') as f:
                json.dump(self.stations, f, indent=2, ensure_ascii=False)
            # Emituj signal nakon čuvanja
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
        # Proveri duplikate
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
            self.stations_changed.emit()  # Emituj signal
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