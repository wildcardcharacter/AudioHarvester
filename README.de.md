# AudioHarvester

**Sprachen:** [English](README.md) | [Deutsch](README.de.md)

<p align="center">
  <img src="assets/icons/audioharvester.png" width="140" alt="AudioHarvester-Logo">
</p>

<h1 align="center">AudioHarvester</h1>

<p align="center">
  <strong>Ein moderner Audio-Downloader für Linux mit yt-dlp, ffmpeg und PyQt6.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.5.5-blue" alt="Version">
  <img src="https://img.shields.io/badge/platform-Linux-orange" alt="Plattform">
  <img src="https://img.shields.io/badge/Debian-13-A81D33?logo=debian" alt="Debian">
  <img src="https://img.shields.io/badge/language-Python-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PyQt6-GUI-41CD52?logo=qt" alt="PyQt6">
  <img src="https://img.shields.io/badge/yt--dlp-Latest-red" alt="yt-dlp">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="Lizenz">
  <img src="https://img.shields.io/badge/status-Stable-success" alt="Status">
</p>

<p align="center">
  YouTube • Audio • MP3 • Opus • M4A • Open Source • Debian • XFCE
</p>

---

## 📸 Vorschau

<p align="center">
  <img src="assets/img/deu_main-window.png" width="600" alt="AudioHarvester-Hauptfenster auf Deutsch">
</p>

---

## ✨ Funktionen

* 🎵 Audio von YouTube herunterladen
* 🎧 Unterstützung für MP3, Opus und M4A
* 🎚 Audioqualität auswählen
* 🖼 Coverbilder einbetten
* 📝 Metadaten automatisch übernehmen
* 📃 Ganze Playlists herunterladen
* 🎯 Einzelne Titel aus Playlists herunterladen
* 📥 Mehrere Downloads nacheinander in einer Warteschlange verarbeiten
* 📊 Status pro Warteschlangeneintrag und erneuter Versuch fehlgeschlagener Downloads
* 🔗 Mehrere URLs eingeben, eine pro Zeile
* 🏷 Eigene Dateinamenvorlagen mit yt-dlp-Feldern
* ⏹ Laufende Downloads abbrechen
* 📜 Download-Verlauf
* 🗂 Verlauf verwalten
* 📁 Eigenen Zielordner festlegen
* ⚙ Einstellungen speichern
* 🌍 Deutsche und englische Oberfläche, in den Einstellungen wählbar
* 🎛 Format, Qualität, Sprache und Coverbild in den Einstellungen festlegen
* ⌄ Menü mit Informationen, Rechtlichem und Changelog
* 📖 Integrierte Changelog-Anzeige
* ⚖ Integrierte rechtliche Hinweise
* 🔍 yt-dlp automatisch erkennen
* 🔄 Updates über GitHub Releases suchen und installieren
* 📦 Als Debian-Paket installierbar
* 🖥 Eintrag im XFCE-Anwendungsmenü
* 🧩 Modularer Programmaufbau

---

## 🖼 Bildschirmfotos

### Deutsch

<p align="center">
  <img src="assets/img/deu_main-window.png" width="520" alt="AudioHarvester-Hauptfenster auf Deutsch">
</p>

### Englisch

<p align="center">
  <img src="assets/img/eng_main-window.png" width="520" alt="AudioHarvester-Hauptfenster auf Englisch">
</p>

---

## 📦 Installation

### Debian-Paket

Lade die aktuelle Version von der [GitHub-Releases-Seite](https://github.com/wildcardcharacter/AudioHarvester/releases/latest) herunter.

```bash
sudo apt install ./audioharvester_1.5.5_all.deb
```

AudioHarvester starten:

```bash
audioharvester
```

---

## 🚀 Aus dem Quellcode starten

Repository klonen:

```bash
git clone https://github.com/wildcardcharacter/AudioHarvester.git
cd AudioHarvester
```

Benötigte Abhängigkeiten installieren:

```bash
pip install PyQt6 markdown
```

**yt-dlp** installieren (empfohlen):

```bash
pipx install yt-dlp
```

Installation prüfen:

```bash
which yt-dlp
yt-dlp --version
```

**ffmpeg** über die Paketverwaltung deiner Linux-Distribution installieren.

Programm starten:

```bash
python3 src/main.py
```

## ⚙ AudioHarvester verwenden

Füge eine oder mehrere YouTube-URLs in das URL-Feld ein, jeweils eine pro Zeile. Wähle **Zur Warteschlange hinzufügen** und dann **Warteschlange starten**, um die Links nacheinander abzuarbeiten. Bei Playlist-Links kannst du wählen, ob die ganze Playlist oder nur der ausgewählte Titel heruntergeladen werden soll.

Jeder Eintrag zeigt an, ob er wartet, gerade heruntergeladen wird, abgeschlossen ist oder fehlgeschlagen ist. Mit **Fehlgeschlagene erneut versuchen** kannst du fehlgeschlagene Downloads erneut einreihen. Die aktuelle URL und der Fortschritt werden im Aktionsbereich angezeigt. Das Protokoll lässt sich bei Bedarf ein- und ausblenden.

Über das Menü **Einstellungen** kannst du Sprache, Audioformat, Qualität und Einbettung des Coverbilds ändern. Diese Einstellungen werden automatisch gespeichert.

Das Dateinamenfeld unterstützt yt-dlp-Vorlagen. Mit `%(artist)s - %(title)s` werden zum Beispiel Interpret und Titel verwendet. Standardmäßig lautet die Vorlage `%(title)s`.

Das Menü **Mehr** enthält die Dialoge für Informationen, Rechtliches und Changelog.

### Updates

Klicke oben im Fenster auf **Updates prüfen**, um auf GitHub nach einer neueren Version zu suchen. AudioHarvester zeigt die Versionshinweise an. Wenn das Programm als Debian-Paket installiert wurde, kann es das Update herunterladen und installieren. Dafür ist eine Systemauthentifizierung erforderlich. Alternativ kannst du die Release-Seite öffnen und das Paket manuell installieren.

---

## ⚙ Voraussetzungen

* Linux
* Python 3.10 oder neuer
* PyQt6
* Python-Markdown
* yt-dlp
* ffmpeg

---

## 📖 Changelog

Alle Änderungen stehen in **CHANGELOG.md**.

AudioHarvester enthält außerdem eine integrierte Markdown-Anzeige für das Changelog.

---

## 🗺 Roadmap

Geplante Funktionen:

* 📦 AppImage-Paket
* 📦 Flatpak-Paket
* 🚀 Veröffentlichung auf Flathub
* 🤖 Build-Workflow mit GitHub Actions
* 🎨 Verbesserungen am Design
* 🔊 Weitere Audioformate

Die vollständige Roadmap steht in **TODO.md**.

---

## 🤝 Mitwirken

Fehlerberichte, Funktionswünsche und Pull Requests sind willkommen.

Wenn du einen Fehler findest oder eine Idee hast, kannst du gern ein Issue eröffnen.

---

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

Weitere Informationen stehen in **LICENSE**.

---

## 👤 Autor

**Markus**

🌐 Website  
https://wildcardcharacter.github.io

💻 GitHub  
https://github.com/wildcardcharacter

☕ Projekt unterstützen  
https://buymeacoffee.com/wildcardcharacter
