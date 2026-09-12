const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');
const os = require('os');

let mainWindow;
let tempDir = path.join(os.tmpdir(), 'voxbox');

// Create temp directory if it doesn't exist
if (!fs.existsSync(tempDir)) {
    fs.mkdirSync(tempDir, { recursive: true });
}

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1000,
        height: 700,
        minWidth: 800,
        minHeight: 600,
        title: 'VoxBox',
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js')
        },
        icon: path.join(__dirname, 'icons/icon.png')
    });

    mainWindow.loadFile(path.join(__dirname, 'ui/index.html'));

    // Open DevTools in development
    if (process.argv.includes('--dev')) {
        mainWindow.webContents.openDevTools();
    }
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    // Clean up temp files
    if (fs.existsSync(tempDir)) {
        fs.rmSync(tempDir, { recursive: true, force: true });
    }
    
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

// IPC Handlers
ipcMain.handle('list-voices', async () => {
    return new Promise((resolve, reject) => {
        const serverPath = path.join(__dirname, 'tts_server.py');
        exec(`python "${serverPath}" list_voices`, (error, stdout, stderr) => {
            if (error) {
                reject(new Error(`Failed to list voices: ${error.message}`));
                return;
            }
            
            try {
                const voices = JSON.parse(stdout);
                resolve(voices);
            } catch (e) {
                reject(new Error(`Failed to parse voice data: ${e.message}`));
            }
        });
    });
});

ipcMain.handle('generate-tts', async (event, text, voice, outputName) => {
    return new Promise((resolve, reject) => {
        const serverPath = path.join(__dirname, 'tts_server.py');
        const outputPath = path.join(tempDir, outputName);
        
        const command = `python "${serverPath}" generate "${text}" "${voice}" "${outputPath}"`;
        
        // Inject TikTok session ID from settings into environment
        const settings = loadSettings();
        const env = { ...process.env };
        if (settings.tiktokSessionId) {
            env.TIKTOK_SESSION_ID = settings.tiktokSessionId;
        }
        
        exec(command, { env }, (error, stdout, stderr) => {
            if (error) {
                reject(new Error(`Failed to generate TTS: ${error.message}\n${stderr}`));
                return;
            }
            
            if (stderr) {
                console.error('Python stderr:', stderr);
            }
            
            try {
                const result = JSON.parse(stdout);
                if (result.success) {
                    resolve({ success: true, path: outputPath });
                } else {
                    reject(new Error(result.error || 'Unknown error'));
                }
            } catch (e) {
                reject(new Error(`Failed to parse result: ${e.message}`));
            }
        });
    });
});

// Settings file path
const settingsPath = path.join(app.getPath('userData'), 'settings.json');

function loadSettings() {
    try {
        if (fs.existsSync(settingsPath)) {
            const data = fs.readFileSync(settingsPath, 'utf8');
            return JSON.parse(data);
        }
    } catch (error) {
        console.error('Error loading settings:', error);
    }
    return {};
}

function saveSettings(settings) {
    try {
        const dir = path.dirname(settingsPath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }
        fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2), 'utf8');
        return true;
    } catch (error) {
        console.error('Error saving settings:', error);
        return false;
    }
}

ipcMain.handle('get-settings', async () => {
    return loadSettings();
});

ipcMain.handle('save-settings', async (event, settings) => {
    return saveSettings(settings);
});
