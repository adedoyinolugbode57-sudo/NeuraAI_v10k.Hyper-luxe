import Popup from './popup.js';
import Loader from './loader.js';

const UIManager = {
    popup: new Popup(),
    loader: new Loader(),

    async showLoaderFor(promise, successMsg="Done!", errorMsg="Error occurred!") {
        this.loader.show();
        try {
            const result = await promise;
            this.popup.show(successMsg, "success", 3500);
            return result;
        } catch(e) {
            this.popup.show(errorMsg, "error", 4000);
            throw e;
        } finally {
            this.loader.hide();
        }
    }
};

// -----------------------------
// Auto-bind Neuraluxe endpoints
// -----------------------------

// AI requests
window.askAI = async (prompt) => UIManager.showLoaderFor(
    fetch("/api/ai/full", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({prompt})
    }).then(r => r.json()),
    "AI Response Ready!", "AI Error!"
);

// Trading bots
window.runBots = async (userId) => UIManager.showLoaderFor(
    fetch(`/api/bots/run_all/${userId}`).then(r => r.json()),
    "Trading Bots Completed!", "Bot Error!"
);

// Mini-games
window.playGame = async (gameId) => UIManager.showLoaderFor(
    fetch(`/api/game/${gameId}`).then(r => r.json()),
    `Game ${gameId} Completed!`, "Game Error!"
);

// Dummy endpoints
window.callDummy = async (endpointId) => UIManager.showLoaderFor(
    fetch(`/api/dummy/${endpointId}`).then(r => r.json()),
    `Dummy ${endpointId} Completed!`, "Dummy Error!"
);

export default UIManager;