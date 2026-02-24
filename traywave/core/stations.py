"""
Stations manager for TrayWave
"""

import json
import os
from typing import Dict, List, Tuple
from PyQt6.QtCore import QObject, pyqtSignal


class StationsManager(QObject):
    """Manages radio stations and categories"""

    stations_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.stations_file = os.path.expanduser("~/.traywave_stations.json")
        self.stations: Dict[str, List[Tuple[str, str]]] = {}
        self.load_stations()

    def load_stations(self) -> bool:
        """Load stations from JSON file"""

        # ================= DEFAULT STATIONS =================

        default_stations: Dict[str, List[Tuple[str, str]]] = {
            "🇷🇸 EX-YU": [
                ("Cool Radio", "http://176.9.30.66/cool64"),
                ("OK radio", "https://sslstream.okradio.net/;?type=http&nocache=8804"),
                ("Hit FM Radio Beograd", "http://streaming.hitfm.rs:8000/hit"),
                ("Naxi Radio", "http://naxi48.streaming.rs:9180/"),
                ("Radio Lola", "https://streaming.tdiradio.com/radiolola.mp3"),
                ("TDI Radio", "http://streaming.tdiradio.com:8000/tdiradio"),
                ("Play", "http://stream.playradio.rs:8001/play.aac"),
                ("Radio S3 Južni", "https://stream.radios.rs:9038/;*.mp3"),
                ("Karolina", "http://streaming.karolina.rs:8000/karolina"),
                ("Extra FM", "http://streams.extrafm.hr:8110/;")
            ],

            "🎸 Rock": [
                ("Hit FM (UKraine) - 128kb/s", "http://195.95.206.17/HitFM"),
                ("Rockabilly-radio.net", "http://lin3.ash.fast-serv.com:6026/stream_96"),
                ("Radio Caroline", "http://78.129.202.200:8040/;"),
                ("Big R Radio - 80s Metal FM", "http://bigrradio.cdnstream1.com/5186_128"),
                ("RTL2", "http://streaming.radio.rtl2.fr/rtl2-1-44-128"),
                ("Virgin Radio Classic Rock", "http://icy.unitedradio.it/VirginRockClassics.mp3"),
                ("Hard Rock Heaven", "http://hydra.cdnstream.com/1521_128"),
                ("1LIVE", "http://wdr-1live-live.icecast.wdr.de/wdr/1live/live/mp3/128/stream.mp3"),
                ("Radio ROKS Ballads", "http://online.radioroks.ua/RadioROKS_Ballads_HD"),
                ("Antyradio", "https://n-4-2.dcs.redcdn.pl/sc/o2/Eurozet/live/antyradio.livx?audio=5")
            ],

            "🎵 Pop": [
                ("Hit FM (UKraine) - 128kb/s", "http://195.95.206.17/HitFM"),
                ("RMF FM", "http://195.150.20.9/RMFFM48"),
                ("Radio Caroline", "http://78.129.202.200:8040/;"),
                ("Radio Navahang", "https://navairan.com/;stream.nsv"),
                ("EuroDance 90 radio", "https://stream-eurodance90.fr/radio/8000/128.mp3?1627933323"),
                ("RTL2", "http://streaming.radio.rtl2.fr/rtl2-1-44-128"),
                ("Capital FM London", "http://media-ice.musicradio.com/CapitalMP3"),
                ("Хіт FM Сучасні хіти", "http://online.hitfm.ua/HitFM_Top"),
                ("Hits 1 Algérie", "https://radio12.pro-fhi.net/listen/whmnrlow/stream"),
                ("Radio 105 Network", "http://icecast.unitedradio.it/Radio105.mp3")
            ],

            "🎤 Hip Hop & R&B": [
                ("Rap/Hip Hop", "http://185.32.188.17:8097/stream"),
                ("- 0 N - Indie on Radio", "https://0n-indie.radionetz.de/0n-indie.mp3"),
                ("deutschrap", "http://stream.laut.fm/deutschrap"),
                ("# TOP 100 CLUB CHARTS - DANCE & DJ MIX RADIO - 24 HOURS NON-STOP MUSIC @ TikTok Hits, Ibiza House, Sunset Lounge, Melodic Music, EDM, Deep House, Dance Music, Techno & Hypertechno, Rave Charts, Top 40 Charts, Latin, Reggaeton Music, Moombahton, Urban Hits, HipHop, Party & Clubbing Radio, Trending Chartmusic, R&B, Urban, Mixtape - & LIVE DJ SET", "https://breakz-2012-high.rautemusik.fm/?ref=radiobrowser-top100-clubcharts"),
                ("BBC Radio 6 Music", "http://as-hls-ww-live.akamaized.net/pool_81827798/live/ww/bbc_6music/bbc_6music.isml/bbc_6music-audio%3d320000.norewind.m3u8"),
                (".100 Hip hop and RNB FM", "https://ice64.securenetsystems.net/LFTM"),
                ("Top Urbano", "https://radio.dominiserver.com/proxy/topurbano?mp=/stream"),
                ("Studio 92 (92.5 FM Lima)", "https://mdstrm.com/audio/5fada553978fe1080e3ac5ea/icecast.audio"),
                ("Virgin Radio Romania", "https://astreaming.edi.ro:8443/VirginRadio_aac"),
                ("All Underground Hip Hop Radio", "http://stream.radiojar.com/c1912tk5rtzuv")
            ],

            "🎹 Jazz": [
                ("Classic Vinyl HD", "https://icecast.walmradio.com:8443/classic"),
                ("Adroit Jazz Underground", "https://icecast.walmradio.com:8443/jazz"),
                ("101 SMOOTH JAZZ", "http://jking.cdnstream1.com/b22139_128mp3"),
                ("Deep House Lounge", "http://198.15.94.34:8006/stream"),
                ("Jazz Radio Blues", "http://jazzblues.ice.infomaniak.ch/jazzblues-high.mp3"),
                ("Adroit Jazz Underground HD Opus", "https://icecast.walmradio.com:8443/jazz_opus"),
                ("Jazz Radio", "http://jazzradio.ice.infomaniak.ch/jazzradio-high.mp3"),
                ("Classic Vinyl HD Opus", "https://icecast.walmradio.com:8443/classic_opus"),
                ("Classic Vinyl HD", "https://icecast.walmradio.com:8443/classic"),
                ("SomaFM Secret Agent (128k MP3)", "https://ice6.somafm.com/secretagent-128-mp3")
            ],

            "🎻 Classical": [
                ("WALM 2 HD", "https://icecast.walmradio.com:8443/walm2"),
                ("parsa", "http://parsa.icdndhcp.com:18000/stream"),
                ("WALM 2 HD Opus", "https://icecast.walmradio.com:8443/walm2_opus"),
                ("Classic FM UK", "http://ice-the.musicradio.com/ClassicFMMP3"),
                ("Your Classical - Relax", "http://relax.stream.publicradio.org/relax.mp3"),
                ("caltexmusic", "http://n13.radiojar.com/cp13r2cpn3quv?rj-ttl=5&rj-tok=AAABeB5OHJQA07FIiDdZAZNHWw"),
                ("Mosaique FM", "https://radio.mosaiquefm.net/mosalive"),
                ("Jazz Radio Classic Jazz", "http://jazz-wr01.ice.infomaniak.ch/jazz-wr01-128.mp3"),
                ("إذاعة القرآن الكريم", "http://stream.radiojar.com/0tpy1h0kxtzuv"),
                ("Rai Radio 3", "http://icestreaming.rai.it/3.mp3")
            ],

            "💃 Dance": [
                ("Dance Wave!", "https://dancewave.online/dance.mp3"),
                ("Hit FM (UKraine) - 128kb/s", "http://195.95.206.17/HitFM"),
                ("Dance Wave Retro!", "https://retro.dancewave.online/retrodance.mp3"),
                ("Intense Radio - We love Dance #HQ# FLAC", "http://secure.live-streams.nl/flac.ogg"),
                ("Intense Radio - We love Dance 256k", "http://intenseradio.live-streams.nl:8000/main"),
                ("EuroDance 90 radio", "https://stream-eurodance90.fr/radio/8000/128.mp3?1627933323"),
                ("Ibiza Global Radio", "http://ibizaglobalradio.streaming-pro.com:8024/"),
                ("Chocolate FM", "http://streaming5.elitecomunicacion.es:8082/live.mp3"),
                ("Radio Stereocittà", "http://onair11.xdevel.com:8134/;stream.mp3"),
                ("1000 HITS 80s", "http://c2.auracast.net:8048/stream")
            ],

            "🌀 Trance": [
                ("Dance Wave!", "https://dancewave.online/dance.mp3"),
                ("Intense Radio - We love Dance #HQ# FLAC", "http://secure.live-streams.nl/flac.ogg"),
                ("Intense Radio - We love Dance 256k", "http://intenseradio.live-streams.nl:8000/main"),
                ("Radio Schizoid - Progressive Psychedelic Trance", "http://94.130.113.214:8000/prog"),
                ("TranceBase.FM - AAC HD 256k", "http://listen.trancebase.fm/tunein-aac-hd-pls"),
                ("1.FM - Amsterdam Trance Radio", "http://strm112.1.fm/atr_mobile_mp3"),
                ("Sunshine Live", "http://stream.sunshine-live.de/live/mp3-192/stream.sunshine-live.de/"),
                ("Trance Athena", "http://cast.streams.ovh:8008/stream"),
                ("Kane FM", "http://stream.kanefm.com:1037/;stream"),
                ("Dance Wave!", "https://dancewave.online/dance.ogg")
            ],

            "🛸 Electronic": [
                ("Dance Wave!", "https://dancewave.online/dance.mp3"),
                ("Deep House Lounge", "http://198.15.94.34:8006/stream"),
                ("Frisky", "http://stream2.friskyradio.com/frisky_mp3_hi"),
                ("Intense Radio - We love Dance 256k", "http://intenseradio.live-streams.nl:8000/main"),
                ("Deep House Radio", "http://62.210.105.16:7000/stream"),
                ("EuroDance 90 radio", "https://stream-eurodance90.fr/radio/8000/128.mp3?1627933323"),
                ("Ibiza Global Radio", "http://ibizaglobalradio.streaming-pro.com:8024/"),
                ("Radio Meuh", "http://radiomeuh.ice.infomaniak.ch/radiomeuh-128.mp3"),
                ("Sunshine Live - Die 90er", "http://stream.sunshine-live.de/90er/mp3-192/stream.sunshine-live.de"),
                ("SomaFM Space Station Soma (128k AAC)", "https://ice5.somafm.com/spacestation-128-aac")
            ],

            "❄️ Chillout": [
                ("SomaFM Groove Salad (128k MP3)", "https://ice5.somafm.com/groovesalad-128-mp3"),
                ("ABC Lounge Radio", "https://eu1.fastcast4u.com/proxy/kpmxz?mp=/1"),
                ("Antenne Bayern - Chillout", "http://mp3channels.webradio.antenne.de/chillout"),
                ("Smooth Chill", "https://media-ssl.musicradio.com/ChillMP3"),
                ("1.FM - Chillout Lounge Radio", "http://strm112.1.fm/chilloutlounge_mobile_mp3"),
                ("Chilltrax", "http://server1.chilltrax.com:9000/"),
                ("Costa Del Mar - Chillout (AAC 96kbps)", "http://stream.cdm-chillout.com:8020/stream-AAC-Chill"),
                ("Café del Mar", "https://streams.radio.co/se1a320b47/listen"),
                ("REGGAE CHILL CAFE", "https://maggie.torontocast.com:2020/stream/reggaechillcafe"),
                ("dinamo.fm sleep", "http://channels.dinamo.fm/sleep-mp3")
            ],

            "🌍 World Music": [
                ("RFI Monde", "http://live02.rfi.fr/rfimonde-64.mp3"),
                ("RFI-Afrique", "http://live02.rfi.fr/rfiafrique-96k.mp3"),
                ("Radio Nova", "http://novazz.ice.infomaniak.ch/novazz-128.mp3"),
                ("Radio Mojdeh - Iranian Farsi/Persian Christian music and talk", "https://ic2326.c1261.fastserv.com/rm128"),
                ("Radio FM", "https://icecast.stv.livebox.sk/fm_128.mp3"),
                ("1.FM - Cafe Radio", "http://strm112.1.fm/caferadio_mobile_mp3"),
                ("Nostalgie New York", "http://c32.radioboss.fm:8139/stream"),
                ("RFI Monde", "http://live02.rfi.fr/rfimonde-96k.mp3"),
                ("Radyo Voyage", "http://voyagewmp.radyotvonline.com/;stream.mp3"),
                ("WDR COSMO", "http://wdr-cosmo-live.icecast.wdr.de/wdr/cosmo/live/mp3/128/stream.mp3")
            ],

            "🤠 Country": [
                (".977 Country", "http://26343.live.streamtheworld.com/977_COUNTRY_SC"),
                ("Radio Caroline", "http://78.129.202.200:8040/;"),
                ("181.FM - Highway 181", "http://listen.181fm.com/181-highway_128k.mp3"),
                ("1.FM - Absolute Country Hits Radio", "http://strm112.1.fm/acountry_mobile_mp3"),
                ("Country Radio", "http://icecast2.play.cz:8000/country128aac"),
                ("1.FM - Classic Country Radio", "http://strm112.1.fm/ccountry_mobile_mp3"),
                ("Classic Country", "http://185.33.21.112/ccountry_mobile_mp3"),
                ("RequestRadio เพื่อชีวิต", "https://cast.requestradio.in.th:830/stream/"),
                ("181.FM - 80's Country", "http://listen.181fm.com/181-80scountry_128k.mp3"),
                ("Irish Country Music Radio", "http://46.28.49.164:7502/")
            ],

            "🎷 Blues": [
                ("Jazz Radio Blues", "http://jazzblues.ice.infomaniak.ch/jazzblues-high.mp3"),
                ("Blues Radio", "http://cast3.radiohost.ovh:8352/"),
                ("1.FM - Blues Radio", "http://strm112.1.fm/blues_mobile_mp3"),
                ("181.FM - True Blues", "http://listen.181fm.com/181-blues_128k.mp3"),
                ("# RdMix Classic Rock 70s 80s 90s", "https://cast1.torontocast.com:4610/stream"),
                ("Exclusively Elvis Presley", "http://streaming.exclusive.radio/er/elvispresley/icecast.audio"),
                ("Radiostorm - Oldies 104", "http://streaming.live365.com/b09584_64aac"),
                ("70 80 90 Vibrazioni Rock Radio", "https://maggie.torontocast.com:2020/stream/vibrazionirockradio"),
                ("JR Radio", "http://stream.zeno.fm/pdkt234k698uv.mp3"),
                ("BBC Radio 6 Music", "http://as-hls-ww-live.akamaized.net/pool_81827798/live/ww/bbc_6music/bbc_6music.isml/bbc_6music-audio%3d320000.norewind.m3u8")
            ],

            "🤘 Metal": [
                ("Big R Radio - 80s Metal FM", "http://bigrradio.cdnstream1.com/5186_128"),
                ("Hard Rock Heaven", "http://hydra.cdnstream.com/1521_128"),
                ("Rock Antenne - Heavy Metal", "http://mp3channels.webradio.rockantenne.de/heavy-metal"),
                ("Antyradio", "https://n-4-2.dcs.redcdn.pl/sc/o2/Eurozet/live/antyradio.livx?audio=5"),
                ("La Grosse Radio Métal", "http://hd.lagrosseradio.info/lagrosseradio-metal-192.mp3"),
                ("Radio Beat", "http://icecast2.play.cz/radiobeat128.mp3"),
                ("ChroniX Radio Metalcore", "http://usa17.fastcast4u.com:5508/stream"),
                ("SomaFM Metal Detector (128k AAC)", "https://ice4.somafm.com/metal-128-aac"),
                ("Radiónica (HJYM 99.1 Bogotá) RTVC", "http://shoutcast.rtvc.gov.co:8010/;"),
                ("Best Of Rock.FM Alternative Rock", "https://bestofrockfm.stream.vip/altrock/mp3-256/bestofrock.fm/")
            ],

            "🎺 Reggae": [
                ("Chocolate FM", "http://streaming5.elitecomunicacion.es:8082/live.mp3"),
                ("La Grosse Radio Reggae", "http://hd.lagrosseradio.info/lagrosseradio-reggae-192.mp3"),
                ("Chocolate FM [calidad móvil-low bandwidth]", "http://streaming5.elitecomunicacion.es:8082/live32.aac"),
                ("Latina Reggaeton", "http://latinareggaeton.ice.infomaniak.ch/latinareggaeton.mp3"),
                ("SABROSITA Ciudad de México - 590 AM - XEPH-AM - NRM Comunicaciones - Ciudad de México", "https://playerservices.streamtheworld.com/api/livestream-redirect/XEPHAMAAC.aac"),
                ("Kane FM", "http://stream.kanefm.com:1037/;stream"),
                ("REGGAE CHILL CAFE", "https://maggie.torontocast.com:2020/stream/reggaechillcafe"),
                ("Reggae Radio Rastamusic.com", "http://origin-rastamusic.streamguys1.com/rastamusic.mp3"),
                ("Cuban Flow Radio", "http://nap.casthost.net:9194/stream.mp3"),
                ("La Mega (Medellín) 92.9 FM", "https://us-b4-p-e-qg12-audio.cdn.mdstrm.com/live-audio-aw/632cb48f613bac0856b931ab")
            ],

            "📰 News & Talk": [
                ("BBC World Service", "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service"),
                ("Iran International", "https://radio.iraninternational.app/iintl_c"),
                ("RFE/RL Radio Farda", "http://rfe21.akacast.akamaistream.net/7/751/437779/v1/ibb.akacast.akamaistream.net/rfe21"),
                ("iraninternational", "https://radio.iraninternational.app/iintl_c"),
                ("RFI Afrique", "http://live02.rfi.fr/rfiafrique-64.mp3"),
                ("RFI Monde", "http://live02.rfi.fr/rfimonde-64.mp3"),
                ("RFI-Afrique", "http://live02.rfi.fr/rfiafrique-96k.mp3"),
                ("Rai Radio 1", "http://icestreaming.rai.it/1.mp3"),
                ("Радио НВ", "http://91.218.212.84:8000/radionv.mp3"),
                ("Radio 24 il sole 24 ore", "http://shoutcast2.radio24.it:8000/;")
            ],

            "🎬 Soundtracks": [
                ("1.FM - Movie Soundtrack", "http://strm112.1.fm/moviesoundtracks_mobile_mp3"),
                ("Retro PC GAME MUSIC Streaming Radio", "http://gyusyabu.ddo.jp:8000/"),
                ("80s Soundtracks Radio", "http://uk5.internet-radio.com:8256/;"),
                ("Hit Radio FFH - Soundtrack", "http://mp3.ffh.de/ffhchannels/hqsoundtrack.mp3"),
                ("Cinemix", "http://94.23.51.96:8001"),
                ("- 0 N - Movies on Radio", "https://0n-movies.radionetz.de/0n-movies.mp3"),
                ("Cinemix", "https://kathy.torontocast.com:1825/stream"),
                ("COOLFM Filmzenék", "https://mediagw.e-tiger.net/stream/zc01?ver=753658"),
                ("Klassik Radio - Klassik Dreams", "http://stream.klassikradio.de/dreams/mp3-128/"),
                ("StreamingSoundtracks.com Hi", "http://hi5.streamingsoundtracks.com/")
            ],

            "🕺 House": [
                ("Dance Wave!", "https://dancewave.online/dance.mp3"),
                ("Deep House Lounge", "http://198.15.94.34:8006/stream"),
                ("Intense Radio - We love Dance #HQ# FLAC", "http://secure.live-streams.nl/flac.ogg"),
                ("Intense Radio - We love Dance 256k", "http://intenseradio.live-streams.nl:8000/main"),
                ("Ibiza Global Radio", "http://ibizaglobalradio.streaming-pro.com:8024/"),
                ("1.FM - Deep House Radio", "http://strm112.1.fm/deephouse_mobile_mp3"),
                ("Deep House Radio - Bucharest Romania", "http://live.dancemusic.ro:7000/stream"),
                ("ORBITAL", "http://centova.radios.pt:8401/;listen.pls"),
                ("Los 40 Dance", "http://playerservices.streamtheworld.com/api/livestream-redirect/LOS40_DANCE_SC"),
                ("Kane FM", "http://stream.kanefm.com:1037/;stream")
            ],

            "🌿 Ambient": [
                ("Ambient Sleeping Pill", "http://radio.stereoscenic.com/asp-h"),
                ("SomaFM Groove Salad (128k MP3)", "https://ice5.somafm.com/groovesalad-128-mp3"),
                ("SomaFM Secret Agent (128k MP3)", "https://ice6.somafm.com/secretagent-128-mp3"),
                ("Cryosleep", "http://streams.echoesofbluemars.org:8000/cryosleep"),
                ("SomaFM Space Station Soma (128k AAC)", "https://ice5.somafm.com/spacestation-128-aac"),
                ("ABC Lounge Radio", "https://eu1.fastcast4u.com/proxy/kpmxz?mp=/1"),
                ("Total instrumental", "http://stream.laut.fm/total-instrumental"),
                ("dinamo.fm sleep", "http://channels.dinamo.fm/sleep-mp3"),
                ("- 0 N - Chillout on Radio", "https://0n-chillout.radionetz.de/0n-chillout.aac"),
                ("SomaFM Drone Zone (128k MP3)", "https://ice4.somafm.com/dronezone-128-mp3")
            ],

            "🎙️ Podcasts": [
                ("Radio Vibration", "https://vibration.ice.infomaniak.ch/vibration-high.mp3"),
                ("DANCEable Radio", "http://s9.myradiostream.com:35944/;"),
                ("Jupiter Broadcasting Live", "http://n09.radiojar.com/0uk94cu0xrquv"),
                ("Rádio Lisboa", "http://radiolisboa.ddns.net:8080/stream/1/"),
                ("LA Talk Radio", "https://securestreams2.autopo.st:1185/;stream/1"),
                ("No Agenda Show Stream (pls)", "https://listen.noagendastream.com/noagenda"),
                ("ToXoRs minimalRADIO (320k)", "http://95.216.245.239:8000/stream/1/"),
                ("Radio Ritmo 97.3 FM", "https://azura1.bitstreaming.net/listen/radio_ritmo/radio.aac"),
                ("Netlabel.org (Germany)", "https://netlabelorg.stream.laut.fm/netlabel_org"),
                ("AudioBook Radio Audio Book Radio", "https://audiobookradio.out.airtime.pro/audiobookradio_a")
            ],

            "🏆 Top 40": [
                (".977 Hitz", "http://18863.live.streamtheworld.com/977_HITS_SC"),
                ("Radio 105 Network", "http://icecast.unitedradio.it/Radio105.mp3"),
                ("LOS 40 Principales España", "https://playerservices.streamtheworld.com/api/livestream-redirect/Los40.mp3"),
                ("1LIVE", "http://wdr-1live-live.icecast.wdr.de/wdr/1live/live/mp3/128/stream.mp3"),
                ("Chocolate FM", "http://streaming5.elitecomunicacion.es:8082/live.mp3"),
                ("Antenne Bayern", "http://mp3channels.webradio.antenne.de/antenne"),
                ("Los 40 Principales México", "http://27063.live.streamtheworld.com/LOS40_MEXICO_SC"),
                ("Clouds FM", "http://eu6.fastcast4u.com:5306/;"),
                ("Chocolate FM [calidad móvil-low bandwidth]", "http://streaming5.elitecomunicacion.es:8082/live32.aac"),
                ("Pro FM", "http://edge126.rdsnet.ro:84/profm/profm.mp3")
            ]

        }
        # ================= LOAD LOGIC =================

        try:
            if os.path.exists(self.stations_file):
                with open(self.stations_file, "r", encoding="utf-8") as f:
                    loaded_data = json.load(f)

                self.stations = {}
                for category, stations_list in loaded_data.items():
                    formatted = []
                    for s in stations_list:
                        if isinstance(s, dict) and "name" in s and "url" in s:
                            formatted.append((s["name"], s["url"]))
                    if formatted:
                        self.stations[category] = formatted

                return True

            self.stations = default_stations
            self.save_stations()
            return True

        except Exception as e:
            print(f"Error loading stations: {e}")
            self.stations = default_stations
            return False

    def save_stations(self) -> bool:
        try:
            os.makedirs(os.path.dirname(self.stations_file), exist_ok=True)

            json_data = {
                cat: [{"name": n, "url": u} for n, u in lst]
                for cat, lst in self.stations.items()
            }

            with open(self.stations_file, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)

            self.stations_changed.emit()
            return True

        except Exception as e:
            print(f"Error saving stations: {e}")
            return False

    def get_categories(self) -> List[str]:
        return list(self.stations.keys())

    def get_stations_in_category(self, category: str) -> List[Tuple[str, str]]:
        return self.stations.get(category, [])

    def get_all_stations(self) -> Dict[str, List[Tuple[str, str]]]:
        return self.stations.copy()