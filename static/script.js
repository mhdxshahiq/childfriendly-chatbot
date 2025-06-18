async function sendMessage() {
  const input = document.getElementById("userInput");
  const msg = input.value.trim();
  if (!msg) return;

  addMessage(msg, "user");
  input.value = "";

  const response = await fetch("/chat", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: msg })
  });

  const data = await response.json();
  addMessage(data.reply, "bot");

  if (data.audio_url) {
    const audio = new Audio(data.audio_url);
    audio.play();
  }

  const chatbox = document.getElementById("chatbox");
  chatbox.scrollTop = chatbox.scrollHeight;
}

function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);
  msg.innerText = (sender === "user" ? "🧒 " : "🤖 ") + text;
  document.getElementById("chatbox").appendChild(msg);
}
