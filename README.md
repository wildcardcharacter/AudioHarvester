# AudioHarvester

AudioHarvester is a lightweight Linux desktop application for downloading audio from YouTube using **yt-dlp** and **ffmpeg**.

Built with **Python** and **PyQt6**.

## Features

* MP3, Opus and M4A support
* Audio quality selection
* Embedded cover artwork
* Metadata support
* Playlist downloads
* Download entire playlists or a single track
* Download cancellation
* Download history
* History management
* Custom output directory
* Saved settings
* XFCE menu integration
* Installable DEB package
* Automatic yt-dlp detection
* Integrated changelog viewer
* Tooltips and GUI improvements

## Screenshots

### Main Window

![Main Window](screenshots/main-window.png)

### Legal Notice

![Legal Notice](screenshots/legal-dialog.png)

### About Dialog

![About Dialog](screenshots/about-dialog.png)

## Requirements

* Python 3.10+
* PyQt6
* Python-Markdown
* yt-dlp
* ffmpeg

## Installation

### Option 1: Install the DEB Package

Download the latest `.deb` package from the GitHub Releases page.

Install it with:

```bash
sudo apt install ./audioharvester_0.9.6_all.deb
```

After installation, AudioHarvester can be started from the application menu or with:

```bash
audioharvester
```

### Uninstall

Remove AudioHarvester:

```bash
sudo apt remove audioharvester
```

Remove AudioHarvester including package configuration:

```bash
sudo apt purge audioharvester
```

User settings are stored in:

```text
~/.config/audioharvester/
```

and can be removed manually if desired.

### Option 2: Run from Source

Clone the repository:

```bash
git clone https://github.com/wildcardcharacter/AudioHarvester.git
cd AudioHarvester
```

Install dependencies:

```bash
pip install PyQt6
```

Install Markdown support:

```bash
sudo apt install python3-markdown
```

Install yt-dlp:

```bash
pipx install yt-dlp
```

or:

```bash
pip install -U yt-dlp
```

Install ffmpeg using your distribution's package manager.

## Run

```bash
python3 src/main.py
```

## Changelog Viewer

AudioHarvester includes an integrated changelog viewer.

The application reads the project's `CHANGELOG.md` file and renders it using Markdown formatting directly inside the GUI.

## Notes

AudioHarvester automatically searches for yt-dlp in common installation locations, including:

```text
~/.local/bin/yt-dlp
```

## Legal Notice

AudioHarvester is intended for downloading content that you are legally allowed to access and store.

Users are responsible for complying with local laws, copyright regulations, and the terms of service of the platforms they use.

## Version

Current release: **v0.9.6**

## Author

Markus

Website:

https://wildcardcharacter.github.io

Support development:

https://buymeacoffee.com/wildcardcharacter

## License

MIT License
