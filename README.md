# VoxBox Desktop App

![VoxBox](https://img.shields.io/badge/VoxBox-TTS%20Desktop-purple)

Modern desktop text-to-speech application with TikTok and Microsoft Edge voices.

![image.png](attachment:355d060a-a757-1408-3c45-55370a8b7b9a:image.png)

## 🚀 Features

### 🎵 TikTok Voices (22 voices)
- **Standard Voices**: Female 1/2/3/4, Male 1/2, Male Lobby, Male Sunshine Soon
- **Character Voices**: Ghostface, Chewbacca, C-3PO, Stitch, Stormtrooper, Rocket
- **Special Voices**: Madam Leota, Ghost Host, Pirate
- **Musical/Singing**: Glorious, Dramatic, It Goes Up, Chipmunk, Alto

### 🗣️ Microsoft Edge Voices (6 voices)
- Jenny (Female, en-US)
- Aria (Female, en-US)
- Guy (Male, en-US)
- Davis (Male, en-US)
- Sonia (British Female, en-GB)
- Ryan (British Male, en-GB)

## 📦 Installation

### Option 1: Download Installer (Recommended)

1. Go to [Releases](https://github.com/[username]/voxbox/releases)
2. Download `VoxBox Setup 1.0.0.exe`
3. Run the installer
4. Launch VoxBox from Start Menu

### Option 2: Build from Source

#### Prerequisites
- Node.js 18+ and npm
- Python 3.10+
- Git

#### Steps

```bash
# Clone repository
git clone https://github.com/[username]/voxbox.git
cd voxbox

# Install Node dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt

# Run in development mode
npm run dev
```

## ⚙️ Configuration

### TikTok Session ID

TikTok voices require authentication via a session ID cookie:

1. **In VoxBox App**:
   - Click the **Settings** gear icon (top right)
   - Paste your TikTok session ID
   - Click **Save**
   - Restart the app

2. **Environment Variable** (alternative):
   ```bash
   # Windows PowerShell
   $env:TIKTOK_SESSION_ID="your_session_id_here"
   npm start

   # Linux/Mac
   export TIKTOK_SESSION_ID="your_session_id_here"
   npm start
   ```

#### How to Get TikTok Session ID

1. Open TikTok in your browser
2. Log in to your account
3. Open DevTools (F12)
4. Go to **Application** tab → **Cookies** → `https://www.tiktok.com`
5. Find the `sessionid` cookie
6. Copy its value

**Note**: The session ID is stored locally in the app's settings and never sent to external servers. It's only used for TikTok API authentication.

## 🛠️ Build and Package

### Create Windows Installer

```bash
npm run build:win
```

This creates a `.exe` installer in the `dist/` folder.

### Create Linux AppImage

```bash
npm run build:linux
```

### Create macOS DMG

```bash
npm run build:mac
```

### Build for All Platforms

```bash
npm run build:all
```

## 📱 Usage

1. **Enter Text**: Type or paste your text in the text area
2. **Select Voice**:
   - Click the **TikTok** or **Edge TTS** tab
   - Click on a voice card to select it
   - Selected voices highlight in purple/pink
3. **Generate**: Click the **Generate** button
4. **Listen/Download**:
   - **Play**: Listen to generated audio
   - **Download**: Save MP3 to your disk

## 🐛 Troubleshooting

### TikTok Voices Not Working

1. **Check Session ID**: Go to Settings and verify your session ID is saved
2. **Restart App**: After setting session ID, restart the app completely
3. **Session Expired**: TikTok session IDs expire. Get a fresh one from your browser
4. **Voice Unavailable**: Some TikTok voices may be disabled by Disney

### Edge Voices Work but TikTok Don't

Edge TTS uses Microsoft's free service and doesn't require authentication. If Edge works but TikTok doesn't:
- Your session ID may be expired
- TikTok may have rate-limited your account
- Check internet connection (TikTok API requires internet)

### Build Errors

**Electron Build Failures**:
- Ensure Node.js version is 18+
- Delete `node_modules` and `package-lock.json`, then run `npm install`

**Python Import Errors**:
- Install dependencies: `pip install -r requirements.txt`
- Use virtual environment: `python -m venv venv` and activate it

### Voice Shows "Invalid Voice" Error

- Voice may have been removed by TikTok
- Try different voices from the same category
- Update VoxBox to latest version for new voice mappings

## 🔒 Privacy & Security

- All TTS generation happens locally or via official APIs (TikTok/Edge)
- Session ID is stored locally in app settings (encrypted storage)
- No data is collected or sent to VoxBox developers
- Audio files are saved temporarily and cleaned up on app close

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- TikTok TTS API (community reverse-engineered)
- Microsoft Edge TTS Service
- Electron Framework
- All voice artists who created these amazing voices

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/[username]/voxbox/issues)
- **Discussions**: [GitHub Discussions](https://github.com/[username]/voxbox/discussions)

---

**Made with ❤️ for content creators**

*VoxBox is not affiliated with TikTok or Microsoft. This is a community project.*
