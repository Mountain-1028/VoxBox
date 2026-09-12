# VoxBox

A desktop text-to-speech application with TikTok & Edge voices.

## Features

- **TikTok Voices**: 15 authentic TikTok voices including character voices
- **Edge TTS**: High-quality Microsoft Edge neural voices
- **Modern UI**: Clean, intuitive interface with dark theme
- **Local Processing**: All TTS generation happens locally
- **Free to Use**: No API keys required for Edge TTS

## Installation

### Windows

1. Download the latest release from [Releases](https://github.com/yourusername/voxbox/releases)
2. Run `VoxBox Setup.exe`
3. Launch VoxBox from Start Menu

### Build from Source

```bash
git clone https://github.com/yourusername/voxbox.git
cd voxbox
npm install
python -m pip install edge-tts
npm start
```

### Build Distributable

```bash
npm run build:all
# Check dist/ for platform-specific installers
```

## Usage

1. Enter text in the text area
2. Select a voice from TikTok or Edge TTS tabs
3. Click "Generate" to create audio
4. Click "Play" to listen or "Download" to save

## Environment Variables

For TikTok voices, you need to set your session ID:

**Windows (PowerShell)**:
```powershell
$env:TIKTOK_SESSION_ID="your_session_id_here"
npm start
```

**Windows (CMD)**:
```cmd
set TIKTOK_SESSION_ID=your_session_id_here
npm start
```

**Linux/Mac**:
```bash
export TIKTOK_SESSION_ID="your_session_id_here"
npm start
```

### Getting Your TikTok Session ID

1. Open TikTok in Chrome/Firefox
2. Open Developer Tools (F12)
3. Go to Application/Storage tab
4. Find cookies for tiktok.com
5. Copy the value of `sessionid` cookie

**Note**: Session IDs expire. If you get authentication errors, get a fresh session ID.

## Development

```bash
# Run in development mode
npm start

# Lint code
npm run lint

# Build for all platforms
npm run build:all

# Build for current platform only
npm run build:linux
npm run build:win
npm run build:mac
```

## Tech Stack

- **Electron**: Cross-platform desktop app
- **Python**: TTS backend
- **edge-tts**: Microsoft Edge TTS
- **TikTok API**: TikTok TTS voices

## License

MIT

## Disclaimer

This project is for educational purposes. TikTok voices are accessed through their API and may be subject to change. Respect TikTok's terms of service and copyright.
