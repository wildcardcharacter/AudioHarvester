# Changelog

All notable changes to AudioHarvester are documented here.

## 1.0.0

### New features

- Added a download queue that processes links one after another.
- Added per-link queue status and retry for failed downloads.
- Added support for entering several URLs at once, one URL per line.
- Added customizable yt-dlp filename templates.
- Added German and English interface languages. The selected language is saved.
- Added a settings dropdown for language, audio format, quality, and cover art embedding.
- Added a **More** dropdown for About, legal information, and the changelog.

### Interface and documentation

- Reorganized the main window around downloads, the output folder, controls, and history.
- Added a collapsible log and clearer display of the active download.
- Updated the About dialog to describe the current features in German and English.
- Updated the README and roadmap for the 1.0 feature set.

## 0.9.6

### User interface

- Added an integrated Markdown changelog viewer.
- Added tooltips and icons for common actions.
- Improved button labels, spacing, and visual consistency.

### Code and documentation

- Moved the About, changelog, legal notice, and download worker into separate modules.
- Added automatic yt-dlp detection with local and system-wide fallbacks.
- Updated project documentation and added a `.gitignore` file.

## 0.9.5

### Packaging

- Added a Debian package, desktop launcher, application icon, and menu integration.
- Added `build-deb.sh` with automatic version detection.

### Improvements

- Removed the hardcoded yt-dlp path and improved detection across Linux systems.
- Updated project structure and documentation.

## 0.9

First public release.

- Added MP3, Opus, and M4A audio formats with quality selection.
- Added optional cover art and metadata embedding.
- Added playlist downloads with a choice between the full playlist and one track.
- Added download cancellation, history management, and a custom output folder.
- Added saved settings and XFCE menu integration.

