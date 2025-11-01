// marketplace.js - Neuraluxe-AI Premium Visual Marketplace

document.addEventListener("DOMContentLoaded", () => {
    const marketplacePanel = document.getElementById("marketplace");
    if (!marketplacePanel) return;

    // --- Create Search and Filter Bar ---
    const controlBar = document.createElement("div");
    controlBar.classList.add("market-controls");
    controlBar.innerHTML = `
        <input type="text" id="marketSearch" placeholder="🔍 Search items...">
        <select id="marketFilter">
            <option value="all">All</option>
            <option value="software">Software</option>
            <option value="ai-tools">AI Tools</option>
            <option value="education">Education</option>
            <option value="healthcare">Healthcare</option>
            <option value="premium">Premium</option>
        </select>
    `;
    marketplacePanel.appendChild(controlBar);

    // --- Marketplace Grid ---
    const grid = document.createElement("div");
    grid.classList.add("market-grid");
    marketplacePanel.appendChild(grid);

    // --- Generate Large Range of Items ---
    const categories = ["software", "ai-tools", "education", "healthcare", "premium"];
    const items = [];

    const generateItem = (i) => {
        const price = (Math.random() * 970 + 29.99).toFixed(2);
        const category = categories[Math.floor(Math.random() * categories.length)];
        const rating = (Math.random() * 2 + 3).toFixed(1);
        const item = {
            id: i,
            name: `Neuraluxe Item #${i}`,
            category,
            price,
            rating,
            description: `A cutting-edge ${category} solution powered by Neuraluxe-AI for productivity and creativity.`,
            image: `https://picsum.photos/seed/neuraluxe${i}/200/200`
        };
        items.push(item);
    };

    // Create ~10,000 visible and lazy-load more
    for (let i = 1; i <= 10000; i++) generateItem(i);

    // --- Render Items ---
    const renderItems = (list) => {
        grid.innerHTML = "";
        list.slice(0, 500).forEach(item => {
            const card = document.createElement("div");
            card.classList.add("market-item-card");
            card.innerHTML = `
                <img src="${item.image}" alt="${item.name}">
                <h3>${item.name}</h3>
                <p>${item.description}</p>
                <div class="market-meta">
                    <span class="price">$${item.price}</span>
                    <span class="rating">⭐ ${item.rating}</span>
                </div>
                <button class="buy-btn">Buy Now</button>
            `;
            grid.appendChild(card);
        });
    };

    renderItems(items);

    // --- Search and Filter Logic ---
    const searchInput = document.getElementById("marketSearch");
    const filterSelect = document.getElementById("marketFilter");

    const applyFilters = () => {
        const query = searchInput.value.toLowerCase();
        const filter = filterSelect.value;
        const filtered = items.filter(item =>
            (filter === "all" || item.category === filter) &&
            item.name.toLowerCase().includes(query)
        );
        renderItems(filtered);
    };

    searchInput.addEventListener("input", applyFilters);
    filterSelect.addEventListener("change", applyFilters);

    // --- Infinite Scroll Simulation (optional) ---
    window.addEventListener("scroll", () => {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
            const moreItems = [];
            const start = items.length + 1;
            for (let i = start; i < start + 5000; i++) generateItem(i);
            renderItems(items);
        }
    });
});