# voice_handler.py
from murf import Murf
import requests
import re
from api_key import API_KEY

class VoiceHandler:
    def __init__(self, voice_id="en-US-miles", mood="Conversational"):
        self.client = Murf(api_key=API_KEY)
        self.voice_id = voice_id
        self.mood = mood

    def remove_emojis(self, text):
        """Remove emojis from text for TTS."""
        emoji_pattern = re.compile("[" 
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)

    def speak(self, text, pitch=0):
        """Generate and return Murf audio URL for HTML autoplay."""
        if not text.strip():
            print("❌ Empty text for TTS")
            return None

        clean_text = self.remove_emojis(text).strip()
        if not clean_text:
            print("❌ No text left after emoji removal")
            return None

        try:
            response = self.client.text_to_speech.generate(
                format="MP3",
                sample_rate=24000.0,   # ✅ Lowered for speed
                channel_type="MONO",   # ✅ MONO is faster than stereo
                text=clean_text,
                voice_id=self.voice_id,
                style=self.mood,
                pitch=pitch
            )

            if not hasattr(response, "audio_file"):
                print("❌ No audio file returned")
                return None

            return response.audio_file

        except Exception as e:
            print(f"❌ TTS Error: {e}")
            return None
