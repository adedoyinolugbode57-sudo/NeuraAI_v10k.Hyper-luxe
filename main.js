/* =========================================
   Neuraluxe-AI Premium - main.js
   Final Neon-Cyber Upgrade ✨
========================================= */

/* ====== Global Variables ====== */
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
const mainContent = document.querySelector('.main-content');
const panels = document.querySelectorAll('.panel');
const themeButtons = document.querySelectorAll('[data-theme]');
const chatWindow = document.getElementById('chatWindow');
const chatForm = document.getElementById('chatForm');
const chatInput = chatForm.querySelector('input[type="text"]');
const chatButton = chatForm.querySelector('button');
const multiTaskPanel = document.querySelector('.multi-task-panel');
const marketplacePanel = document.querySelector('.marketplace-panel');
const tradingPanel = document.querySelector('.trading-panel');
const searchBar = document.getElementById('searchBar');
let currentTheme = 'theme-neon';

/* ====== Utility Functions ====== */
// Smooth scroll chat to bottom
function scrollChatToBottom() {
    chatWindow.scrollTo({ top: chatWindow.scrollHeight, behavior: 'smooth' });
}

// Toggle class helper
function toggleClass(element, className) {
    if (element.classList.contains(className)) {
        element.classList.remove(className);
    } else {
        element.classList.add(className);
    }
}

// Debounce helper
function debounce(func, wait) {
    let timeout;
    return function () {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, arguments), wait);
    };
}

/* ====== Sidebar Toggle ====== */
sidebarToggle.addEventListener('click', () => {
    toggleClass(sidebar, 'active');
    toggleClass(mainContent, 'sidebar-open');
    sidebarToggle.classList.toggle('active');
});

/* ====== Theme Switching ====== */
themeButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const theme = btn.getAttribute('data-theme');
        document.body.classList.remove(currentTheme);
        document.body.classList.add(theme);
        currentTheme = theme;
    });
});

/* ====== Panel Switching ====== */
document.querySelectorAll('#sidebar ul li').forEach(item => {
    item.addEventListener('click', () => {
        const target = item.getAttribute('data-panel');
        panels.forEach(panel => panel.classList.remove('active'));
        const activePanel = document.getElementById(target);
        if (activePanel) activePanel.classList.add('active');
    });
});

/* ====== Chat Functionality ====== */
function addChatMessage(message, sender = 'ai') {
    const div = document.createElement('div');
    div.classList.add('chat-message', sender);
    div.textContent = message;
    chatWindow.appendChild(div);
    scrollChatToBottom();
}

// Mock AI response
function getAIResponse(input) {
    // Simple mock responses
    const responses = [
        "I'm processing that...",
        "Interesting, tell me more.",
        "Neuraluxe-AI thinks that is valid.",
        "Analyzing data streams...",
        "Response generated!"
    ];
    return responses[Math.floor(Math.random() * responses.length)];
}

chatForm.addEventListener('submit', e => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;
    addChatMessage(message, 'user');
    chatInput.value = '';
    setTimeout(() => {
        addChatMessage(getAIResponse(message), 'ai');
    }, 700 + Math.random() * 800);
});

/* ====== Marketplace Filter ====== */
if (searchBar) {
    searchBar.addEventListener('input', debounce(() => {
        const query = searchBar.value.toLowerCase();
        const items = document.querySelectorAll('.market-item');
        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(query) ? 'block' : 'none';
        });
    }, 300));
}

/* ====== Task Card Click ====== */
document.querySelectorAll('.task-card').forEach(card => {
    card.addEventListener('click', () => {
        card.classList.toggle('active-task');
        card.style.transform = card.classList.contains('active-task') ? 'scale(1.08)' : 'scale(1)';
    });
});

/* ====== Trading Panel ====== */
tradingPanel.querySelectorAll('button').forEach(btn => {
    btn.addEventListener('click', () => {
        const resultDiv = document.createElement('div');
        resultDiv.textContent = `Executed trade at ${new Date().toLocaleTimeString()}`;
        tradingPanel.appendChild(resultDiv);
    });
});

/* ====== Multi-task Panel Logic ====== */
multiTaskPanel.querySelectorAll('.task-card').forEach(card => {
    card.addEventListener('click', () => {
        alert(`Launching task: ${card.textContent}`);
    });
});

/* ====== Panel Animation Enhancements ====== */
panels.forEach(panel => {
    panel.addEventListener('animationend', () => {
        if (!panel.classList.contains('active')) panel.style.display = 'none';
        else panel.style.display = 'flex';
    });
});

/* ====== Dynamic Theme Glow ====== */
function animateThemeGlow() {
    const root = document.documentElement;
    let hue = 180;
    setInterval(() => {
        hue = (hue + 1) % 360;
        root.style.setProperty('--neon-hue', hue);
    }, 80);
}
animateThemeGlow();

/* ====== Sidebar Scroll Highlight ====== */
sidebar.addEventListener('scroll', () => {
    const scrollTop = sidebar.scrollTop;
    sidebar.querySelectorAll('li').forEach((li, idx) => {
        li.style.opacity = 1 - Math.min(scrollTop / 300, 0.7);
    });
});

/* ====== Auto-expand Sidebar on Hover ====== */
sidebar.addEventListener('mouseenter', () => {
    sidebar.classList.add('active-hover');
});
sidebar.addEventListener('mouseleave', () => {
    sidebar.classList.remove('active-hover');
});

/* ====== Keyboard Shortcuts ====== */
document.addEventListener('keydown', e => {
    if (e.ctrlKey && e.key === 't') { // Ctrl+T: Toggle sidebar
        sidebarToggle.click();
    }
    if (e.ctrlKey && e.key === 'm') { // Ctrl+M: Open marketplace
        panels.forEach(p => p.classList.remove('active'));
        marketplacePanel.classList.add('active');
    }
    if (e.ctrlKey && e.key === 'c') { // Ctrl+C: Focus chat
        chatInput.focus();
    }
});

/* ====== Dynamic Chat Background Effects ====== */
function chatBackgroundPulse() {
    let alpha = 0.05, increment = 0.01;
    setInterval(() => {
        alpha += increment;
        if (alpha >= 0.25 || alpha <= 0.05) increment *= -1;
        chatWindow.style.background = `rgba(25,25,25,${alpha})`;
    }, 150);
}
chatBackgroundPulse();

/* ====== Tooltip Generator ====== */
function createTooltip(element, text) {
    const tip = document.createElement('span');
    tip.className = 'tooltip';
    tip.textContent = text;
    element.appendChild(tip);
    element.addEventListener('mouseenter', () => tip.classList.add('visible'));
    element.addEventListener('mouseleave', () => tip.classList.remove('visible'));
}
document.querySelectorAll('[data-tooltip]').forEach(el => {
    createTooltip(el, el.getAttribute('data-tooltip'));
});

/* ====== Notification System ====== */
function showNotification(message, type = 'info', duration = 2500) {
    const notif = document.createElement('div');
    notif.className = `neuralux-notif ${type}`;
    notif.textContent = message;
    document.body.appendChild(notif);
    setTimeout(() => notif.classList.add('show'), 50);
    setTimeout(() => notif.classList.remove('show'), duration);
    setTimeout(() => document.body.removeChild(notif), duration + 300);
}

/* ====== Random Neon Animations ====== */
function randomNeonFlicker() {
    const elements = document.querySelectorAll('.task-card, #sidebar h2, .market-item');
    setInterval(() => {
        elements.forEach(el => {
            if (Math.random() < 0.1) {
                el.style.opacity = 0.4 + Math.random() * 0.6;
            } else {
                el.style.opacity = 1;
            }
        });
    }, 200);
}
randomNeonFlicker();

/* ====== Memory Panel Mock ====== */
const memoryPanel = document.getElementById('memory');
if (memoryPanel) {
    for (let i = 0; i < 10; i++) {
        const memDiv = document.createElement('div');
        memDiv.textContent = `Memory Slot ${i + 1}: Ready`;
        memoryPanel.appendChild(memDiv);
    }
}

/* ====== Security Panel Mock ====== */
const securityPanel = document.getElementById('security');
if (securityPanel) {
    ['Firewall', 'Encryption', '2FA'].forEach(sec => {
        const secDiv = document.createElement('div');
        secDiv.textContent = `${sec}: Active`;
        securityPanel.appendChild(secDiv);
    });
}

/* ====== Notifications Panel Mock ====== */
const notificationsPanel = document.getElementById('notifications');
if (notificationsPanel) {
    for (let i = 1; i <= 5; i++) {
        const noteDiv = document.createElement('div');
        noteDiv.textContent = `Notification ${i}: All systems normal.`;
        notificationsPanel.appendChild(noteDiv);
    }
}

/* ====== Languages Panel Mock ====== */
const languagesPanel = document.getElementById('languages');
if (languagesPanel) {
    ['English', 'Spanish', 'French', 'German', 'Mandarin'].forEach(lang => {
        const langDiv = document.createElement('div');
        langDiv.textContent = lang;
        languagesPanel.appendChild(langDiv);
    });
}

/* ====== Analytics Panel Mock ====== */
const analyticsPanel = document.getElementById('analytics');
if (analyticsPanel) {
    for (let i = 1; i <= 6; i++) {
        const statDiv = document.createElement('div');
        statDiv.textContent = `Metric ${i}: ${Math.floor(Math.random() * 1000)}`;
        analyticsPanel.appendChild(statDiv);
    }
}

/* ====== AI Engine Panel Mock ====== */
const aiEnginePanel = document.getElementById('aiEngine');
if (aiEnginePanel) {
    ['Neuralux AI Core v5', 'Inference Engine', 'Memory Module', 'Response Predictor'].forEach(mod => {
        const modDiv = document.createElement('div');
        modDiv.textContent = mod;
        aiEnginePanel.appendChild(modDiv);
    });
}

/* ====== Smooth Theme Transition Loop ====== */
function smoothThemeTransition() {
    const colors = ['#00ffcc', '#00aaff', '#00ffee', '#0099ff', '#00ccaa'];
    let index = 0;
    setInterval(() => {
        document.body.style.setProperty('--dynamic-color', colors[index]);
        index = (index + 1) % colors.length;
    }, 600);
}
smoothThemeTransition();

/* ====== Neon Cursor Effect ====== */
document.body.addEventListener('mousemove', e => {
    let cursor = document.getElementById('neonCursor');
    if (!cursor) {
        cursor = document.createElement('div');
        cursor.id = 'neonCursor';
        cursor.style.position = 'fixed';
        cursor.style.width = '12px';
        cursor.style.height = '12px';
        cursor.style.borderRadius = '50%';
        cursor.style.pointerEvents = 'none';
        cursor.style.zIndex = 9999;
        cursor.style.background = 'var(--dynamic-color, #00ffcc)';
        cursor.style.boxShadow = '0 0 12px var(--dynamic-color, #00ffcc), 0 0 25px var(--dynamic-color, #00ffcc)';
        document.body.appendChild(cursor);
    }
    cursor.style.left = `${e.clientX - 6}px`;
    cursor.style.top = `${e.clientY - 6}px`;
});

/* ====== End of Neuraluxe-AI main.js ====== */