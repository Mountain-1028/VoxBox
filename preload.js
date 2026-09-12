const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('voxbox', {
    listVoices: () => ipcRenderer.invoke('list-voices'),
    generateTTS: (text, voice, outputName) => 
        ipcRenderer.invoke('generate-tts', text, voice, outputName)
});
