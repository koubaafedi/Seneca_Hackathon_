import os
import time
import uuid
import pygame
from mutagen.mp3 import MP3
from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY, VOICE_ID

# --- Audio Generation and Playback (ElevenLabs) ---
# Initialize the ElevenLabs client if API keys are available.
if ELEVENLABS_API_KEY and VOICE_ID:
    elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
else:
    elevenlabs_client = None
    print("Warning: ElevenLabs API key or voice ID not found. Audio generation will be skipped.")

def get_audio_from_elevenlabs(text_to_speak):
    """
    Generates audio from text, saves it as an MP3, plays it, and cleans up the file.
    """
    if not elevenlabs_client:
        return

    try:
        # Generate audio from the provided text.
        audio = elevenlabs_client.text_to_speech.convert(
            text=text_to_speak,
            voice_id=VOICE_ID,
            model_id="eleven_flash_v2",
            output_format="mp3_44100_128",
        )
        
        # Save the audio stream to a temporary file.
        filename = str(uuid.uuid4())
        save_file_path = f"{filename}.mp3"

        with open(save_file_path, "wb") as f:
            for chunk in audio:
                if chunk:
                    f.write(chunk)
        
        # Get the audio duration to know how long to sleep.
        audio_file = MP3(save_file_path)
        audio_duration = audio_file.info.length

        # Initialize the pygame mixer for playback.
        pygame.mixer.init()
        pygame.mixer.music.load(save_file_path)
        pygame.mixer.music.play()

        # Wait for the audio to finish playing.
        if audio_duration > 0:
            time.sleep(audio_duration)

        # Stop the mixer and delete the temporary file.
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        os.remove(save_file_path)
        
    except Exception as e:
        print(f"Error during audio generation or playback: {e}")