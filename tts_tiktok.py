import os
import sys
import json
import httpx
import base64
from pathlib import Path

# TikTok session ID - user should set this
SESSION_ID = os.environ.get('TIKTOK_SESSION_ID', '')

# Voice catalog with actual TikTok API IDs
VOICES = {
    'tt:ghostface': {'name': 'Ghostface', 'id': 'en_us_ghostface', 'type': 'tiktok'},
    'tt:chewbacca': {'name': 'Chewbacca', 'id': 'en_us_chewbacca', 'type': 'tiktok'},
    'tt:c3po': {'name': 'C-3PO', 'id': 'en_us_c3po', 'type': 'tiktok'},
    'tt:stitch': {'name': 'Stitch', 'id': 'en_us_stitch', 'type': 'tiktok'},
    'tt:stormtrooper': {'name': 'Stormtrooper', 'id': 'en_us_stormtrooper', 'type': 'tiktok'},
    'tt:rocket': {'name': 'Rocket', 'id': 'en_us_rocket', 'type': 'tiktok'},
    'tt:madam_leota': {'name': 'Madam Leota', 'id': 'en_female_madam_leota', 'type': 'tiktok'},
    'tt:ghosthost': {'name': 'Ghost Host', 'id': 'en_male_ghosthost', 'type': 'tiktok'},
    'tt:pirate': {'name': 'Pirate', 'id': 'en_male_pirate', 'type': 'tiktok'},
    'tt:glorious': {'name': 'Glorious', 'id': 'en_female_ht_f08_glorious', 'type': 'tiktok'},
    'tt:dramatic': {'name': 'Dramatic', 'id': 'en_female_ht_f08_wonderful_world', 'type': 'tiktok'},
    'tt:itgoesup': {'name': 'It Goes Up', 'id': 'en_male_sing_funny_it_goes_up', 'type': 'tiktok'},
    'tt:chipmunk': {'name': 'Chipmunk', 'id': 'en_male_m2_xhxs_m03_silly', 'type': 'tiktok'},
    'tt:alto': {'name': 'Alto', 'id': 'en_female_f08_salut_damour', 'type': 'tiktok'},
    'edge:jenny': {'name': 'Jenny', 'id': 'en-US-JennyNeural', 'type': 'edge'},
    'edge:aria': {'name': 'Aria', 'id': 'en-US-AriaNeural', 'type': 'edge'},
    'edge:guy': {'name': 'Guy', 'id': 'en-US-GuyNeural', 'type': 'edge'},
    'edge:davis': {'name': 'Davis', 'id': 'en-US-DavisNeural', 'type': 'edge'},
    'edge:sonia': {'name': 'Sonia', 'id': 'en-GB-SoniaNeural', 'type': 'edge'},
    'edge:ryan': {'name': 'Ryan', 'id': 'en-GB-RyanNeural', 'type': 'edge'},
}

def generate_tiktok_tts(text: str, voice_id: str, output_path: str) -> str:
    """Generate TTS audio using TikTok API"""
    if not SESSION_ID:
        raise ValueError("TikTok session ID not set. Set TIKTOK_SESSION_ID environment variable.")

    voice = VOICES.get(voice_id, {})
    api_voice_id = voice.get('id')

    if not api_voice_id:
        raise ValueError(f"Invalid voice: {voice_id}")

    encoded_text = text.replace('+', '%2B').replace(' ', '+')
    url = f"https://api22-normal-c-useast2a.tiktokv.com/media/api/text/speech/invoke/?text_speaker={api_voice_id}&req_text={encoded_text}&speaker_map_type=0"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Cookie': f'sessionid={SESSION_ID}; sid_tt={SESSION_ID}; odin_tt=',
    }

    response = httpx.post(url, headers=headers, timeout=30.0)
    response.raise_for_status()
    data = response.json()

    if data.get('status_code') != 0:
        raise Exception(f"TikTok API error: {data.get('message', 'Unknown error')}")

    audio_data = data.get('data', {}).get('v_str', '')
    if not audio_data:
        raise Exception("No audio data returned")

    audio_bytes = base64.b64decode(audio_data)

    with open(output_path, 'wb') as f:
        f.write(audio_bytes)

    return output_path

def get_tiktok_voices():
    """Get list of available TikTok voices"""
    return [v for k, v in VOICES.items() if v['type'] == 'tiktok']
