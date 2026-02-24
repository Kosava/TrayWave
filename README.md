# TrayWave 🎧

**TrayWave** is a lightweight, modern **system tray internet radio player for Linux**.

It is designed with a *tray‑first* philosophy:
- no main window
- instant access from the system tray
- minimal UI with practical audio controls

TrayWave focuses on simplicity, responsiveness, and low system impact while providing a comfortable way to listen to internet radio.

---

## ✨ Features

- 📻 Internet radio playback (any stream URL)
- 🧭 System tray application (no main window)
- 🔊 Vertical volume popup slider
- 🖱️ Mouse wheel volume control directly on tray icon
- 🔇 Middle‑click mute / unmute
- 🎨 Tray icon states: playing / muted / stopped
- 📂 Radio stations organized by categories
- 🧾 Stations stored in editable JSON configuration
- ⚙️ Settings dialog for managing stations and categories
- 💤 Sleep timer 

---

## 🖥️ Supported environments

TrayWave works on **Linux desktop environments with system tray support**, including but not limited to:

- KDE Plasma
- Xfce
- LXQt
- other DEs providing a standard system tray

> Note: mouse middle‑click and wheel behavior may vary slightly depending on the desktop environment.

---

## 📸 Screenshots

### Tray menu with station categories
![Tray menu](screenshots/tray-menu.png)

### Volume popup
![Volume popup](screenshots/volume-popup.png)


---

## 📦 Project structure

```
TrayWave/
├── config
│   ├── stations.json
│   └── traywave_stations.json
├── MANIFEST.in
├── packaging
│   └── traywave.desktop
├── pyproject.toml
├── README.md
├── requirements.txt
├── resources
│   └── icons
├── screenshots
│   ├── tray-menu.jpg
│   └── volume-popup.jpg
├── traywave
│   ├── app.py
│   ├── core
│   ├── data
│   ├── __init__.py
│   ├── __pycache__
│   ├── resources
│   ├── ui
│   └── utils
└── traywave_pystray.py
```

---

## 🚀 Installation & usage

### Requirements

- Python **3.10+**
- PyQt6
- Qt Multimedia (FFmpeg backend)
- PipeWire or PulseAudio

Install dependencies:

```bash
pip install -r requirements.txt
```

Run TrayWave:

```bash
python main.py
```

The application will appear as an icon in the system tray.

---

## 🎛️ Controls

| Action | Result |
|------|--------|
| Left click on tray icon | Show volume popup |
| Mouse wheel on tray icon | Increase / decrease volume |
| Middle click on tray icon | Mute / unmute |
| Right click on tray icon | Station menu / quit |

---

## 📁 Station configuration

Stations are stored in:

```
config/stations.json
```

Example:

```json
{
  "Electronic": [
    {
      "name": "Groove Salad",
      "url": "http://ice1.somafm.com/groovesalad-128-mp3"
    }
  ],
  "Rock": []
}
```

Changes take effect on the next application start.

---

## 🧠 Resource usage

TrayWave is designed to be lightweight:

- CPU usage: near zero when idle
- Memory usage: approximately **40–80 MB PSS** during playback

> Some system monitors may display higher values due to shared Qt libraries.

---

## 🛣️ Roadmap

- [ ] Sleep timer
- [ ] Remember last played station
- [ ] Light / Dark tray icon switching
- [ ] Autostart support
- [ ] Optional C++ audio backend (long‑term)

---

## 📜 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

## 👤 Author

**Košava**

---

## 💡 Philosophy

TrayWave is inspired by classic Linux tray radio tools, but aims to be:

- more modular
- more responsive
- focused on real‑world tray usability

No clutter. No unnecessary windows. Just music — directly from the tray.

🎶 Enjoy!

