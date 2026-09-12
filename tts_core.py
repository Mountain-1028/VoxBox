import asyncio
import edge_tts
import httpx
import base64
from pathlib import Path
from typing import List, Dict
import os

TTS_TIKTOK_API_URL = "https://api16-normal-useast1a.tiktokv.com/media/api/text/speech/invoke/"
TTS_TIKTOK_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.tiktok.com/',
    'Origin': 'https://www.tiktok.com',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
}

# TikTok voice mapping (key -> display name -> actual voice ID)
TIKTOK_VOICES = {
    'ghostface': {'name': 'Ghostface', 'id': 'en_us_ghostface'},
    'chewbacca': {'name': 'Chewbacca', 'id': 'en_us_chewbacca'},
    'c3po': {'name': 'C3PO', 'id': 'en_us_c3po'},
    'stitch': {'name': 'Stitch', 'id': 'en_us_stitch'},
    'stormtrooper': {'name': 'Stormtrooper', 'id': 'en_us_stormtrooper'},
    'rocket': {'name': 'Rocket', 'id': 'en_us_rocket'},
    'madam_leota': {'name': 'Madam Leota', 'id': 'en_female_madam_leota'},
    'ghost_host': {'name': 'Ghost Host', 'id': 'en_male_ghosthost'},
    'pirate': {'name': 'Pirate', 'id': 'en_male_pirate'},
    'glorious': {'name': 'Glorious', 'id': 'en_female_ht_f08_glorious'},
    'wonderful_world': {'name': 'It Goes Up', 'id': 'en_female_ht_f08_wonderful_world'},
    'sunshine_soon': {'name': 'Sunshine Soon', 'id': 'en_male_m03_sunshine_soon'},
    'warmy_breeze': {'name': 'Warmy Breeze', 'id': 'en_female_f08_warmy_breeze'},
    'handsome_boi': {'name': 'Handsome Boi', 'id': 'en_male_m03_handsome_boi'},
    'tricky': {'name': 'Tricky', 'id': 'en_male_funny'},
    'narrator': {'name': 'Narrator', 'id': 'en_male_narration'},
}

# Edge voices
EDGE_VOICES = {
    'jenny': {'name': 'Jenny', 'id': 'en-US-JennyNeural', 'gender': 'Female'},
    'guy': {'name': 'Guy', 'id': 'en-US-GuyNeural', 'gender': 'Male'},
    'aria': {'name': 'Aria', 'id': 'en-US-AriaNeural', 'gender': 'Female'},
    'davis': {'name': 'Davis', 'id': 'en-US-DavisNeural', 'gender': 'Male'},
    'tony': {'name': 'Tony', 'id': 'en-US-TonyNeural', 'gender': 'Male'},
    'sara': {'name': 'Sara', 'id': 'en-US-SaraNeural', 'gender': 'Female'},
}

async def generate_tiktok_tts(text: str, voice_key: str, output_path: str) -> str:
    """Generate TTS audio using TikTok API"""
    session_id = os.getenv('TIKTOK_SESSION_ID')
    if not session_id:
        raise ValueError("TIKTOK_SESSION_ID environment variable not set")
    
    if voice_key not in TIKTOK_VOICES:
        raise ValueError(f"Invalid TikTok voice: {voice_key}")
    
    voice_id = TIKTOK_VOICES[voice_key]['id']
    
    encoded_text = text.replace(' ', '+')
    url = f"{TTS_TIKTOK_API_URL}?text_speaker={voice_id}&req_text={encoded_text}&speaker_map_type=0"
    
    headers = {
        **TTS_TIKTOK_HEADERS,
        'Cookie': f'sessionid={session_id}; sid_tt={session_id}; odin_tt='
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, timeout=30.0)
        data = response.json()
    
    if 'data' in data and 'v_str' in data['data']:
        audio_data = base64.b64decode(data['data']['v_str'])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(audio_data)
        return str(output_path)
    else:
        raise Exception(f"TikTok API error: {data.get('message', 'Unknown error')}")

async def generate_edge_tts(text: str, voice_key: str, output_path: str) -> str:
    """Generate TTS audio using Edge TTS"""
    if voice_key not in EDGE_VOICES:
        raise ValueError(f"Invalid Edge voice: {voice_key}")
    
    voice_id = EDGE_VOICES[voice_key]['id']
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    communicate = edge_tts.Communicate(text, voice_id)
    await communicate.save(str(output_path))
    
    return str(output_path)

def get_all_voices() -> List[Dict]:
    """Get list of all available voices"""
    voices = []
    
    # Add TikTok voices
    for key, voice in TIKTOK_VOICES.items():
        voices.append({
            'key': f"tiktok:{key}",
            'id': voice['id'],
            'name': voice['name'],
            'type': 'tiktok'
        })
    
    # Add Edge voices
    for key, voice in EDGE_VOICES.items():
        voices.append({
            'key': f"edge:{key}",
            'id': voice['id'],
            'name': voice['name'],
            'type': 'edge',
            'gender': voice['gender']
        })
    
    return voices

async def generate_tts(text: str, voice_key: str, output_path: str) -> str:
    """Generate TTS audio based on voice type"""
    output_path = Path(output_path)
    
    if voice_key.startswith('tiktok:'):
        voice = voice_key.split(':', 1)[1]
        return await generate_tiktok_tts(text, voice, output_path)
    elif voice_key.startswith('edge:'):
        voice = voice_key.split(':', 1)[1]
        return await generate_edge_tts(text, voice, output_path)
    else:
        raise ValueError(f"Unknown voice type: {voice_key}")
