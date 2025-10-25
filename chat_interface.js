const chatContainer = document.getElementById("chatContainer");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const voiceToggle = document.getElementById("voiceToggle");
const themeToggle = document.getElementById("themeToggle");

let darkMode = false;

// Append message
function addMessage(text, sender = "bot") {
  const div = document.createElement("div");
  div.classList.add("message", sender);
  div.textContent = text;
  chatContainer.appendChild(div);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Send to backend
async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  addMessage(text, "user");
  userInput.value = "";

  addMessage("NeuraAI is thinking...", "bot");

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });

    const data = await response.json();
    const botReply = data.reply || "Hmm, I couldn’t generate a response.";

    // Replace placeholder
    chatContainer.lastChild.textContent = botReply;

    // Optional voice response
    if (voiceToggle.checked) {
      const utter = new SpeechSynthesisUtterance(botReply);
      utter.lang = "en-US";
      utter.rate = 1;
      speechSynthesis.speak(utter);
    }

  } catch (err) {
    chatContainer.lastChild.textContent = "⚠️ Error connecting to AI engine.";
  }
}

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

themeToggle.addEventListener("change", () => {
  darkMode = !darkMode;
  document.body.style.background = darkMode
    ? "linear-gradient(135deg, #0b0f19, #1a0033)"
    : "linear-gradient(135deg, #00b4ff, #c600ff)";
});