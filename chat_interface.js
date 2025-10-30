const chatContainer = document.getElementById("chatContainer");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const voiceToggle = document.getElementById("voiceToggle");
const themeToggle = document.getElementById("themeToggle");

let darkMode = false;

// In-memory chat logs (will mirror chat_logs.json)
let chatLogs = {
  version: "1.0",
  generated_at: new Date().toISOString(),
  logs: []
};

// Load previous logs from backend
async function loadLogs() {
  try {
    const response = await fetch("/chat_logs.json");
    const data = await response.json();
    if (data.logs) {
      chatLogs = data;
      data.logs.forEach(log => {
        addMessage(log.message, log.sender, false);
      });
    }
  } catch (err) {
    console.warn("Could not load previous logs:", err);
  }
}

// Append message to chat and log
function addMessage(text, sender = "bot", logIt = true) {
  const div = document.createElement("div");
  div.classList.add("message", sender, "new");
  div.textContent = text;
  chatContainer.appendChild(div);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  if (logIt) {
    // Add to chatLogs
    chatLogs.logs.push({
      timestamp: new Date().toISOString(),
      sender: sender,
      message: text
    });

    // Persist logs
    persistLogs();
  }
}

// Persist updated logs to backend
async function persistLogs() {
  try {
    await fetch("/update_logs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(chatLogs)
    });
  } catch (err) {
    console.warn("Failed to persist chat logs:", err);
  }
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
      body: JSON.stringify({ message: text })
    });

    const data = await response.json();
    const botReply = data.reply || "Hmm, I couldn’t generate a response.";

    // Replace placeholder
    chatContainer.lastChild.textContent = botReply;

    // Update last log entry for bot
    chatLogs.logs[chatLogs.logs.length - 1].message = botReply;
    persistLogs();

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

// Event listeners
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

// Load previous logs on page load
window.addEventListener("load", loadLogs);