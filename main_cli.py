# main_cli.py (Original CLI version - kept for reference)
from chatbot import ChildFriendlyChatbot
from voice_handler import VoiceHandler

def main():
    """Main application loop for CLI version."""
    print("🎈 Welcome to the Child-Friendly Voice Chatbot! 🎈")
    print("Type 'exit' to end the conversation.")
    print("Type 'reset' to start a new conversation.")
    print("-" * 50)
    
    # Initialize components
    chatbot = ChildFriendlyChatbot()
    voice = VoiceHandler()
    
    while True:
        user_input = input("\n👶 You: ")
        
        if user_input.lower() == 'exit':
            print("👋 Goodbye! Have a great day!")
            break
        
        if user_input.lower() == 'reset':
            chatbot.reset_context()
            print("🔄 Conversation reset!")
            continue
        
        # Get bot response
        bot_reply = chatbot.get_response(user_input)
        print(f"🤖 Bot: {bot_reply}")
        
        # Speak the response
        voice.speak(bot_reply)

if __name__ == "__main__":
    main()