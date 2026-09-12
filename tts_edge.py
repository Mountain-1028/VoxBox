import edge_tts
import asyncio
import os

async def generate_edge_tts(text: str, voice: str, output_path: str):
    """Generate TTS audio using Edge TTS"""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    return output_path

def get_edge_voices():
    """Get list of available Edge TTS voices"""
    return [
        {
            'id': 'en-US-JennyNeural',
            'name': 'Jenny',
            'gender': 'Female',
            'locale': 'en-US'
        },
        {
            'id': 'en-US-AriaNeural',
            'name': 'Aria',
            'gender': 'Female',
            'locale': 'en-US'
        },
        {
            'id': 'en-US-GuyNeural',
            'name': 'Guy',
            'gender': 'Male',
            'locale': 'en-US'
        },
        {
            'id': 'en-US-DavisNeural',
            'name': 'Davis',
            'gender': 'Male',
            'locale': 'en-US'
        },
        {
            'id': 'en-GB-SoniaNeural',
            'name': 'Sonia',
            'gender': 'Female',
            'locale': 'en-GB'
        },
        {
            'id': 'en-GB-RyanNeural',
            'name': 'Ryan',
            'gender': 'Male',
            'locale': 'en-GB'
        }
    ]
