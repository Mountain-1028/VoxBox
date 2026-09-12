from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
import asyncio
from pathlib import Path
from tts_core import get_all_voices, generate_tts

app = Flask(__name__)
CORS(app)

@app.route('/api/voices', methods=['GET'])
def api_get_voices():
    """Get list of available voices"""
    voices = get_all_voices()
    return jsonify(voices)

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """Generate TTS audio"""
    data = request.json
    text = data.get('text')
    voice_key = data.get('voice')
    
    if not text or not voice_key:
        return jsonify({'error': 'Missing text or voice parameter'}), 400
    
    # Create temporary file for audio
    temp_dir = Path(tempfile.gettempdir()) / 'voxbox'
    temp_dir.mkdir(exist_ok=True)
    temp_file = temp_dir / f'{voice_key.replace(":", "_")}_{hash(text)}.mp3'
    
    try:
        # Run async TTS generation
        audio_path = asyncio.run(generate_tts(text, voice_key, temp_file))
        
        # Return the audio file
        return send_file(audio_path, mimetype='audio/mpeg')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
