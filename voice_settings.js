const testBtn = document.getElementById("test-voice");
const saveBtn = document.getElementById("save-settings");

testBtn.addEventListener("click", () => {
  const voiceData = getSettings();
  const utterance = new SpeechSynthesisUtterance(
    `Hi! This is your ${voiceData.tone} ${voiceData.gender} voice in ${voiceData.language}.`
  );
  utterance.rate = voiceData.rate / 170;
  utterance.volume = voiceData.volume;
  speechSynthesis.speak(utterance);
});

saveBtn.addEventListener("click", () => {
  const settings = getSettings();
  localStorage.setItem("neura_voice_settings", JSON.stringify(settings));
  alert("✅ Settings saved successfully!");
});

function getSettings() {
  return {
    gender: document.getElementById("voice-gender").value,
    tone: document.getElementById("voice-tone").value,
    language: document.getElementById("voice-language").value,
    rate: document.getElementById("voice-rate").value,
    volume: document.getElementById("voice-volume").value,
  };
}