# AudioHarvester

<p align="center">
  <img src="icons/audioharvester.png" width="140" alt="AudioHarvester Logo">
</p>

<h1 align="center">AudioHarvester</h1>

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

## 📸 Preview

<p align="center">
  <img src="screenshots/download-completed.png" width="700" alt="AudioHarvester Preview">
</p>

---

## ✨ Features

* 🎵 Download audio from YouTube
* 🎧 MP3, Opus and M4A support
* 🎚 Audio quality selection
* 🖼 Embed cover artwork
* 📝 Automatic metadata support
* 📃 Download complete playlists
* 🎯 Download only the selected track from playlists
* ⏹ Cancel running downloads
* 📜 Download history
* 🗂 History management
* 📁 Custom output directory
* ⚙ Saved settings
* 📖 Integrated changelog viewer
* ⚖ Integrated legal information
* 🔍 Automatic yt-dlp detection
* 📦 Installable Debian package
* 🖥 XFCE application menu integration
* 🧩 Modular project architecture

---

## 🖼 Screenshots

### Main Window

<p align="center">
  <img src="screenshots/main-window.png" width="520" alt="Main Window">
</p>

### Playlist Detection

<p align="center">
  <img src="screenshots/playlist-detection.png" width="520" alt="Playlist Detection">
</p>

### About Dialog

<p align="center">
  <img src="screenshots/about-dialog.png" width="520" alt="About Dialog">
</p>

### Legal Notice

<p align="center">
  <img src="screenshots/legal-dialog.png" width="520" alt="Legal Notice">
</p>

---

## 📦 Installation

### Debian Package

Download the latest release from the GitHub Releases page.

```bash
sudo apt install ./audioharvester_0.9.6_all.deb
```

Start AudioHarvester:

```bash
audioharvester
```

---

## 🚀 Run from Source

Clone the repository:

```bash
git clone https://github.com/wildcardcharacter/AudioHarvester.git
cd AudioHarvester
```

Install the required dependencies:

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

Run the application:

```bash
python3 src/main.py
```

---

## ⚙ Requirements

* Linux
* Python 3.10 or newer
* PyQt6
* Python-Markdown
* yt-dlp
* ffmpeg

---

## 📖 Changelog

All changes are documented in **CHANGELOG.md**.

AudioHarvester also includes an integrated Markdown-based changelog viewer.

---

## 🗺 Roadmap

Planned features:

* 🌍 English user interface
* 📦 AppImage package
* 📦 Flatpak package
* 🚀 Flathub release
* 🤖 GitHub Actions build workflow
* 🎨 Theme improvements
* 🔊 Additional audio formats

See **TODO.md** for the complete roadmap.

---

## 🤝 Contributing

Bug reports, feature requests and pull requests are always welcome.

If you find a bug or have an idea for a new feature, feel free to open an issue.

---

## 📄 License

This project is licensed under the MIT License.

See **LICENSE.txt** for more information.

---

## 👤 Author

**Markus**

🌐 Website
https://wildcardcharacter.github.io

💻 GitHub
https://github.com/wildcardcharacter

☕ Support the project
https://buymeacoffee.com/wildcardcharacter
