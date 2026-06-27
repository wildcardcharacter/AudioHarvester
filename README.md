# AudioHarvester

<p align="center">
  <img src="icons/audioharvester.png" width="140" alt="AudioHarvester Logo">
</p>

<p align="center">
  <strong>A modern Linux audio downloader powered by yt-dlp, ffmpeg and PyQt6.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.9.6-blue" alt="Version">
  <img src="https://img.shields.io/badge/platform-Linux-orange" alt="Platform">
  <img src="https://img.shields.io/badge/Debian-13-A81D33?logo=debian" alt="Debian">
  <img src="https://img.shields.io/badge/language-Python-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PyQt6-GUI-41CD52?logo=qt" alt="PyQt6">
  <img src="https://img.shields.io/badge/yt--dlp-Latest-red" alt="yt-dlp">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/status-Stable-success" alt="Status">
</p>

<p align="center">
  YouTube • Audio • MP3 • Opus • M4A • Open Source • Debian • XFCE
</p>

---

## About

AudioHarvester is a modern desktop application for Linux that allows you to download high-quality audio from YouTube using **yt-dlp** and **ffmpeg**.

Built with **Python** and **PyQt6**, it offers an intuitive graphical interface for downloading individual tracks or complete playlists while automatically converting them into your preferred audio format.

---

## Features

- 🎵 MP3, Opus and M4A support
- 🎚 Audio quality selection
- 🖼 Embedded cover artwork
- 📝 Automatic metadata support
- 📃 Playlist downloads
- 🎧 Download single tracks or complete playlists
- ⏹ Cancel running downloads
- 📜 Download history
- 🗂 History management
- 📁 Custom output directory
- ⚙ Saved settings
- 📖 Integrated changelog viewer
- ⚖ Integrated legal information
- 🔍 Automatic yt-dlp detection
- 📦 Installable DEB package
- 🖥 XFCE application menu integration
- 🧩 Modular project architecture

---

## Screenshots

### Main Window

![Main Window](screenshots/main-window.png)

### About Dialog

![About Dialog](screenshots/about-dialog.png)

### Legal Dialog

![Legal Dialog](screenshots/legal-dialog.png)

---

## Installation

### Install the DEB package

Download the latest release from GitHub.

```bash
sudo apt install ./audioharvester_0.9.6_all.deb
```

Launch the application:

```bash
audioharvester
```

---

## Run from Source

Clone the repository:

```bash
git clone https://github.com/wildcardcharacter/AudioHarvester.git
cd AudioHarvester
```

Install the required Python package:

```bash
pip install PyQt6 markdown
```

Install **yt-dlp** (recommended):

```bash
pipx install yt-dlp
```

Verify the installation:

```bash
which yt-dlp
yt-dlp --version
```

Install **ffmpeg** using your distribution's package manager.

Run AudioHarvester:

```bash
python3 src/main.py
```

---

## Requirements

- Linux
- Python 3.10+
- PyQt6
- Python-Markdown
- yt-dlp
- ffmpeg

---

## Changelog

AudioHarvester includes an integrated Markdown-based changelog viewer.

All changes are documented in:

```
CHANGELOG.md
```

---

## Roadmap

Planned features for future releases:

- 🌍 English user interface
- 📦 AppImage support
- 📦 Flatpak package
- 🚀 Flathub release
- 🤖 GitHub Actions build workflow
- 🎨 Additional themes
- 🔊 More audio formats

---

## License

This project is licensed under the MIT License.

See the **LICENSE.txt** file for details.

---

## Author

**Markus**

GitHub:

https://github.com/wildcardcharacter

Website:

https://wildcardcharacter.github.io

Support the project:

https://buymeacoffee.com/wildcardcharacter