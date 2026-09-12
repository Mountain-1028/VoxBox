import sys
import json
import asyncio
import base64
from pathlib import Path
from typing import List, Dict

# TikTok API
TIKTOK_API = "https://api16-normal-useast1a.tiktokv.com/media/api/text/speech/invoke/"
TIKTOK_UA = "com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)"

# Voice catalog
VOICES = {
    "tt:f1": {"name": "Female 1", "id": "en_us_001", "type": "tiktok"},
    "tt:f2": {"name": "Female 2", "id": "en_us_002", "type": "tiktok"},
    "tt:f3": {"name": "Female 3", "id": "en_us_006", "type": "tiktok"},
    "tt:f4": {"name": "Female 4", "id": "en_us_007", "type": "tiktok"},
    "tt:m1": {"name": "Male 1", "id": "en_us_009", "type": "tiktok"},
    "tt:m2": {"name": "Male 2", "id": "en_us_010", "type": "tiktok"},
    "tt:m3": {"name": "Male Lobby", "id": "en_male_m03_lobby", "type": "tiktok"},
    "tt:m4": {"name": "Male Sunshine", "id": "en_male_m03_sunshine_soon", "type": "tiktok"},
    "tt:ghostface": {"name": "Ghostface", "id": "en_us_ghostface", "type": "tiktok"},
    "tt:chewbacca": {"name": "Chewbacca", "id": "en_us_chewbacca", "type": "tiktok"},
    "tt:c3po": {"name": "C-3PO", "id": "en_us_c3po", "type": "tiktok"},
    "tt:stitch": {"name": "Stitch", "id": "en_us_stitch", "type": "tiktok"},
    "tt:stormtrooper": {"name": "Stormtrooper", "id": "en_us_stormtrooper", "type": "tiktok"},
    "tt:rocket": {"name": "Rocket", "id": "en_us_rocket", "type": "tiktok"},
    "tt:madam_leota": {"name": "Madam Leota", "id": "en_female_madam_leota", "type": "tiktok"},
    "tt:ghost_host": {"name": "Ghost Host", "id": "en_male_ghosthost", "type": "tiktok"},
    "tt:pirate": {"name": "Pirate", "id": "en_male_pirate", "type": "tiktok"},
    "tt:glorious": {"name": "Glorious", "id": "en_female_ht_f08_glorious", "type": "tiktok"},
    "tt:dramatic": {"name": "Dramatic", "id": "en_female_ht_f08_wonderful_world", "type": "tiktok"},
    "tt:itgoesup": {"name": "It Goes Up", "id": "en_male_sing_funny_it_goes_up", "type": "tiktok"},
    "tt:chipmunk": {"name": "Chipmunk", "id": "en_male_m2_xhxs_m03_silly", "type": "tiktok"},
    "tt:alto": {"name": "Alto", "id": "en_female_f08_salut_damour", "type": "tiktok"},
    "edge:jenny": {"name": "Jenny (Female)", "id": "en-US-JennyNeural", "type": "edge"},
    "edge:aria": {"name": "Aria (Female)", "id": "en-US-AriaNeural", "type": "edge"},
    "edge:guy": {"name": "Guy (Male)", "id": "en-US-GuyNeural", "type": "edge"},
    "edge:davis": {"name": "Davis (Male)", "id": "en-US-DavisNeural", "type": "edge"},
    "edge:sonia": {"name": "Sonia (British Female)", "id": "en-GB-SoniaNeural", "type": "edge"},
    "edge:ryan": {"name": "Ryan (British Male)", "id": "en-GB-RyanNeural", "type": "edge"},
}


def load_session_id() -> str:
    """Load TikTok session ID from .env or environment."""
    import os
    # Check environment first
    env_val = os.environ.get("TIKTOK_SESSION_ID", "").strip()
    if env_val:
        return env_val
    # Check .env file
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line.startswith("TIKTOK_SESSION_ID=") and "your_" not in line:
                return line.split("=", 1)[1].strip()
    return ""


def list_voices() -> List[Dict]:
    """Return list of available voices."""
    voices = []
    for key, info in VOICES.items():
        voices.append({
            "key": key,
            "name": info["name"],
            "id": info["id"],
            "type": info["type"],
        })
    return voices


def generate_tts(text: str, voice_key: str, output_path: str) -> str:
    """Generate TTS audio and return path to output file."""
    if voice_key not in VOICES:
        raise ValueError(f"Unknown voice: {voice_key}")

    info = VOICES[voice_key]

    if info["type"] == "tiktok":
        return _generate_tiktok(text, info["id"], output_path)
    elif info["type"] == "edge":
        return _generate_edge(text, info["id"], output_path)
    else:
        raise ValueError(f"Unknown voice type: {info['type']}")


def _generate_tiktok(text: str, voice_id: str, output_path: str) -> str:
    """Generate via TikTok API."""
    import requests

    session_id = load_session_id()
    if not session_id:
        raise ValueError(
            "TikTok session ID not set. "
            "Set TIKTOK_SESSION_ID in environment or .env file."
        )

    encoded = text.replace("+", "plus").replace(" ", "+").replace("&", "and")
    url = f"{TIKTOK_API}?text_speaker={voice_id}&req_text={encoded}&speaker_map_type=0&aid=1233"
    cookie_val = f"sessionid={session_id}; sid_tt={session_id}; odin_tt="

    resp = requests.post(
        url,
        headers={
            "User-Agent": TIKTOK_UA,
            "Cookie": cookie_val,
            "Accept-Encoding": "gzip,deflate,compress",
        },
        timeout=30,
    )

    data = resp.json()
    status = data.get("status_code", 1)

    if status != 0:
        errors = {1: "Session ID invalid", 2: "Text too long", 4: "Invalid voice", 5: "No session ID"}
        raise Exception(errors.get(status, data.get("message", "Unknown error")))

    v_str = data.get("data", {}).get("v_str")
    if not v_str:
        raise Exception("No audio data returned")

    audio_bytes = base64.b64decode(v_str)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    return output_path


def _generate_edge(text: str, voice_id: str, output_path: str) -> str:
    """Generate via Edge TTS."""
    import edge_tts
    import asyncio

    async def _run():
        comm = edge_tts.Communicate(text, voice_id)
        chunks = []
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                chunks.append(chunk["data"])
        return b"".join(chunks)

    audio_bytes = asyncio.run(_run())
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    return output_path


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: tts_server.py <list_voices|generate> [args...]"}))
        sys.exit(1)

    command = sys.argv[1]

    if command == "list_voices":
        print(json.dumps(list_voices()))
    elif command == "generate":
        if len(sys.argv) < 5:
            print(json.dumps({"error": "Usage: tts_server.py generate <text> <voice> <output_path>"}))
            sys.exit(1)
        text = sys.argv[2]
        voice_key = sys.argv[3]
        output_path = sys.argv[4]
        try:
            generate_tts(text, voice_key, output_path)
            print(json.dumps({"success": True, "path": output_path}))
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)
    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
