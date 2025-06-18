from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

class ChildFriendlyChatbot:
    def __init__(self):
        self.model = OllamaLLM(
            model="llama3.2",
            temperature=0.1,
            stop=["Child:", "Assistant:"]
        )
        self.context = []

        self.template = """
You are a friendly assistant talking to a child. Be kind, encouraging, and use simple words.
Use emojis and make it fun and short!

Conversation so far:
{history}

Child says: {question}

Assistant replies:
"""
        self.prompt = ChatPromptTemplate.from_template(self.template)

    def set_context(self, context_list):
        """Convert list of dicts into formatted string"""
        history_str = ""
        for entry in context_list:
            role = "Child" if entry["role"] == "user" else "Assistant"
            history_str += f"{role}: {entry['message']}\n"
        self.history_string = history_str.strip()

    def get_response(self, user_input):
        chain = self.prompt | self.model
        return chain.invoke({
            "history": self.history_string,
            "question": user_input
        })
