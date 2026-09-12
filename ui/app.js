document.addEventListener('DOMContentLoaded', () => {
    const textInput = document.getElementById('text-input');
    const charCount = document.getElementById('char-count');
    const voiceTabs = document.querySelectorAll('.tab-btn');
    const voiceGrids = {
        tiktok: document.getElementById('tiktok-voices'),
        edge: document.getElementById('edge-voices')
    };
    const generateBtn = document.getElementById('generate-btn');
    const playBtn = document.getElementById('play-btn');
    const downloadBtn = document.getElementById('download-btn');
    const status = document.getElementById('status');

    let voices = [];
    let selectedVoice = null;
    let currentTab = 'tiktok';
    let generatedAudioPath = null;

    // Update character count
    textInput.addEventListener('input', () => {
        charCount.textContent = textInput.value.length;
    });

    // Tab switching
    voiceTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            voiceTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            currentTab = tab.dataset.tab;
            Object.values(voiceGrids).forEach(grid => grid.style.display = 'none');
            voiceGrids[currentTab].style.display = 'grid';
        });
    });

    // Load voices
    async function loadVoices() {
        try {
            voices = await window.voxbox.listVoices();
            renderVoices();
        } catch (error) {
            showStatus(`Error loading voices: ${error.message}`, 'error');
        }
    }

    // Render voice cards
    function renderVoices() {
        const tiktokVoices = voices.filter(v => v.type === 'tiktok');
        const edgeVoices = voices.filter(v => v.type === 'edge');

        voiceGrids.tiktok.innerHTML = tiktokVoices.map(voice => `
            <div class="voice-card" data-key="${voice.key}">
                <div class="voice-name">${voice.name}</div>
            </div>
        `).join('');

        voiceGrids.edge.innerHTML = edgeVoices.map(voice => `
            <div class="voice-card" data-key="${voice.key}">
                <div class="voice-name">${voice.name}</div>
            </div>
        `).join('');

        // Add click handlers
        document.querySelectorAll('.voice-card').forEach(card => {
            card.addEventListener('click', () => {
                document.querySelectorAll('.voice-card').forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
                selectedVoice = card.dataset.key;
            });
        });
    }

    // Generate TTS
    generateBtn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        
        if (!text) {
            showStatus('Please enter some text', 'error');
            return;
        }

        if (!selectedVoice) {
            showStatus('Please select a voice', 'error');
            return;
        }

        // Show loading state
        generateBtn.disabled = true;
        generateBtn.querySelector('.btn-text').style.display = 'none';
        generateBtn.querySelector('.btn-loader').style.display = 'inline';
        
        try {
            const outputName = `voxbox_${Date.now()}.mp3`;
            const result = await window.voxbox.generateTTS(text, selectedVoice, outputName);
            
            if (result.success) {
                generatedAudioPath = result.path;
                playBtn.disabled = false;
                downloadBtn.disabled = false;
                showStatus('Audio generated successfully!', 'success');
            }
        } catch (error) {
            showStatus(`Error: ${error.message}`, 'error');
        } finally {
            generateBtn.disabled = false;
            generateBtn.querySelector('.btn-text').style.display = 'inline';
            generateBtn.querySelector('.btn-loader').style.display = 'none';
        }
    });

    // Play audio
    playBtn.addEventListener('click', () => {
        if (generatedAudioPath) {
            const audio = new Audio(`file://${generatedAudioPath}`);
            audio.play().catch(err => {
                showStatus(`Error playing audio: ${err.message}`, 'error');
            });
        }
    });

    // Download audio
    downloadBtn.addEventListener('click', async () => {
        if (generatedAudioPath) {
            const blob = await fetch(`file://${generatedAudioPath}`).then(r => r.blob());
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `voxbox_${Date.now()}.mp3`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
    });

    // Show status message
    function showStatus(message, type) {
        status.textContent = message;
        status.className = `status show ${type}`;
        
        if (type === 'success') {
            setTimeout(() => {
                status.classList.remove('show');
            }, 3000);
        }
    }

    // Settings modal
    const settingsBtn = document.getElementById('settings-btn');
    const settingsModal = document.getElementById('settings-modal');
    const closeSettings = document.getElementById('close-settings');
    const toggleVisibility = document.getElementById('toggle-visibility');
    const sessionIdInput = document.getElementById('session-id-input');
    const saveSettingsBtn = document.getElementById('save-settings');

    settingsBtn.addEventListener('click', () => {
        loadSettings();
        settingsModal.classList.add('show');
    });

    closeSettings.addEventListener('click', () => {
        settingsModal.classList.remove('show');
    });

    settingsModal.addEventListener('click', (e) => {
        if (e.target === settingsModal) {
            settingsModal.classList.remove('show');
        }
    });

    toggleVisibility.addEventListener('click', () => {
        if (sessionIdInput.type === 'password') {
            sessionIdInput.type = 'text';
            toggleVisibility.textContent = '🔒';
        } else {
            sessionIdInput.type = 'password';
            toggleVisibility.textContent = '👁️';
        }
    });

    saveSettingsBtn.addEventListener('click', async () => {
        const sessionId = sessionIdInput.value.trim();
        const success = await window.voxbox.saveSettings({ tiktokSessionId: sessionId });
        if (success) {
            showStatus('Settings saved! TikTok voices will use this session ID.', 'success');
            settingsModal.classList.remove('show');
        } else {
            showStatus('Failed to save settings.', 'error');
        }
    });

    async function loadSettings() {
        try {
            const settings = await window.voxbox.getSettings();
            sessionIdInput.value = (settings && settings.tiktokSessionId) || '';
        } catch (error) {
            console.error('Error loading settings:', error);
        }
    }

    // Initialize
    loadVoices();
});
