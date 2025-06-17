# --- Imports ---
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from murf import Murf
import re
import requests
import io
import pygame
import re
from api_key import API_KEY

# --- Chatbot Config ---
template = """
You are a friendly assistant talking to a child. Be kind, encouraging, and use simple words. 
Keep your answers short and fun. Use emojis to make it colorful and exciting!

Here is the conversation history:
{context}

Question: {question}

Answer:
"""
model = OllamaLLM(model="llama3.2")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# --- Voice Config ---
client = Murf(api_key=API_KEY)
DEFAULT_VOICE_ID = "en-US-miles"
DEFAULT_MOOD = "Conversational"

# Initialize pygame mixer for audio playback
pygame.mixer.init()

def remove_emojis(text):
    """Remove emojis from text for TTS."""
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def text_to_voice(text, pitch=0):
    """Generate and play audio instantly using Murf TTS."""
    if not text.strip():
        print("❌ Empty text for TTS")
        return

    # Remove emojis for TTS but keep original text for display
    clean_text = remove_emojis(text).strip()
    if not clean_text:
        print("❌ No text left after emoji removal")
        return

    try:
        response = client.text_to_speech.generate(
            format="MP3",
            sample_rate=48000.0,
            channel_type="STEREO",
            text=clean_text,  # Use clean text without emojis
            voice_id=DEFAULT_VOICE_ID,
            style=DEFAULT_MOOD,
            pitch=pitch
        )

        if not hasattr(response, "audio_file"):
            print("❌ No audio file returned")
            return

        audio_url = response.audio_file
        r = requests.get(audio_url)
        if r.status_code == 200:
            # Play audio directly from memory
            audio_data = io.BytesIO(r.content)
            pygame.mixer.music.load(audio_data)
            pygame.mixer.music.play()
            
            # Wait for audio to finish
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
                
            print("")
        else:
            print("❌ Audio download failed")

    except Exception as e:
        print(f"❌ TTS Error: {e}")


# --- Chatbot Conversation ---
def chatbot_convo():
    context = ""
    print("Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        # Invoke LLM
        response = chain.invoke({
            "context": context,
            "question": user_input
        })

        bot_reply = response
        print(f"Bot: {bot_reply}")

        # Update context
        context += f"You: {user_input}\nBot: {bot_reply}\n"

        # Call TTS
        text_to_voice(bot_reply)

# --- Run ---
if __name__ == "__main__":
    chatbot_convo()