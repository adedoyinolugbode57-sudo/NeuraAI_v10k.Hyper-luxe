// ============================================
// loader.js - Neuraluxe-AI Premium Loader Module
// Fully independent, animated neon/futuristic spinner
// ============================================

export default class Loader {
    constructor(containerId = "loader-container") {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            this.container = document.createElement("div");
            this.container.id = containerId;
            this.container.style.position = "fixed";
            this.container.style.top = "50%";
            this.container.style.left = "50%";
            this.container.style.transform = "translate(-50%, -50%)";
            this.container.style.zIndex = "9998";
            this.container.style.display = "none";
            document.body.appendChild(this.container);
        }
    }

    show() {
        this.container.innerHTML = `
            <div class="neon-loader" style="
                border: 6px solid rgba(255,255,255,0.1);
                border-top: 6px solid #00fff0;
                border-radius: 50%;
                width: 60px;
                height: 60px;
                animation: spin 1s linear infinite;
                box-shadow: 0 0 20px #00fff0, 0 0 40px #00fff0, 0 0 60px #00fff0;
            "></div>
            <style>
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        `;
        this.container.style.display = "block";
    }

    hide() {
        this.container.style.display = "none";
    }
}