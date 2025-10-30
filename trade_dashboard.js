// trade_dashboard.js

// ====== Dummy Data ======
const tokens = [];
for (let i = 1; i <= 50; i++) {
  tokens.push({
    rank: i,
    name: `Token ${i}`,
    symbol: `T${i}`,
    price: (Math.random() * 200).toFixed(2),
    change: (Math.random() * 20 - 10).toFixed(2),
    marketCap: Math.floor(Math.random() * 1e9)
  });
}

// Portfolio Data
let portfolio = tokens.slice(0, 10).map(t => ({
  symbol: t.symbol,
  amount: +(Math.random() * 10).toFixed(2)
}));

// ====== Populate Portfolio Widgets ======
function updatePortfolioWidgets() {
  document.getElementById("dailyGain").querySelector("span").textContent = `$${(Math.random()*1000).toFixed(2)}`;
  document.getElementById("weeklyGain").querySelector("span").textContent = `$${(Math.random()*5000).toFixed(2)}`;
  document.getElementById("monthlyGain").querySelector("span").textContent = `$${(Math.random()*20000).toFixed(2)}`;
  document.getElementById("totalGain").querySelector("span").textContent = `$${(Math.random()*100000).toFixed(2)}`;
  document.getElementById("portfolioValue").textContent = `Total Portfolio: $${portfolio.reduce((sum, t) => sum + t.amount * tokens.find(x=>x.symbol===t.symbol).price,0).toFixed(2)}`;
  document.getElementById("activeTokens").textContent = `Active Tokens: ${portfolio.length}`;
}

// ====== Populate Top Movers & Losers ======
function updateTopMovers() {
  const sortedByChange = [...tokens].sort((a,b)=>b.change - a.change);
  const topGainers = sortedByChange.slice(0,5);
  const topLosers = sortedByChange.slice(-5).reverse();

  const gainerDiv = document.getElementById("topGainers");
  gainerDiv.innerHTML = topGainers.map(t=>`<div>${t.name} (${t.symbol}): ${t.change}%</div>`).join('');
  const loserDiv = document.getElementById("topLosers");
  loserDiv.innerHTML = topLosers.map(t=>`<div>${t.name} (${t.symbol}): ${t.change}%</div>`).join('');
}

// ====== Token Table ======
function populateTokenTable() {
  const tbody = document.getElementById("tokenTableBody");
  tbody.innerHTML = tokens.map(t=>`
    <tr>
      <td>${t.rank}</td>
      <td>${t.name}</td>
      <td>${t.symbol}</td>
      <td>$${t.price}</td>
      <td>${t.change}%</td>
      <td>$${t.marketCap.toLocaleString()}</td>
    </tr>
  `).join('');
}

// ====== Portfolio Chart ======
function renderPortfolioChart() {
  const ctx = document.getElementById("portfolioChart").getContext("2d");
  const data = {
    labels: portfolio.map(t=>t.symbol),
    datasets: [{
      label: 'Portfolio Allocation',
      data: portfolio.map(t=>t.amount * tokens.find(x=>x.symbol===t.symbol).price),
      backgroundColor: portfolio.map(()=>`hsl(${Math.random()*360}, 70%, 50%)`)
    }]
  };
  new Chart(ctx, { type: 'pie', data });
}

// ====== Trade Execution ======
document.getElementById("tradeCoin").innerHTML = tokens.map(t=>`<option value="${t.symbol}">${t.name} (${t.symbol})</option>`).join('');
document.getElementById("executeTrade").addEventListener("click", () => {
  const symbol = document.getElementById("tradeCoin").value;
  const amount = parseFloat(document.getElementById("tradeAmount").value);
  const type = document.getElementById("tradeType").value;
  const price = parseFloat(document.getElementById("tradePrice").value) || tokens.find(t=>t.symbol===symbol).price;
  if(!amount || amount <=0) return alert("Enter valid amount");

  const logDiv = document.getElementById("tradeLog");
  const entry = document.createElement("div");
  entry.textContent = `[${new Date().toLocaleTimeString()}] ${type.toUpperCase()} ${amount} ${symbol} @ $${price}`;
  logDiv.prepend(entry);

  // Update portfolio
  let pos = portfolio.find(p=>p.symbol===symbol);
  if(!pos) {
    if(type.startsWith("buy")) portfolio.push({symbol, amount});
  } else {
    if(type.startsWith("buy")) pos.amount += amount;
    else if(type.startsWith("sell")) pos.amount -= amount;
  }
  updatePortfolioWidgets();
  renderPortfolioChart();
});

// ====== Recent Trades ======
function populateRecentTrades() {
  const ul = document.getElementById("recentTrades");
  ul.innerHTML = Array.from({length:10}, (_,i)=>`<li>${tokens[i].symbol} traded ${Math.floor(Math.random()*50+1)} units</li>`).join('');
}

// ====== Watchlist & Favorites ======
function populateWatchlistFavorites() {
  const watchlist = document.querySelector("#watchlistWidget ul");
  const favorites = document.querySelector("#favoritesWidget ul");
  watchlist.innerHTML = tokens.slice(0,5).map(t=>`<li>${t.symbol}</li>`).join('');
  favorites.innerHTML = tokens.slice(5,10).map(t=>`<li>${t.symbol}</li>`).join('');
}

// ====== Alerts & Signals ======
function populateAlerts() {
  const alerts = document.getElementById("alertsList");
  alerts.innerHTML = [
    "BTC price > $50k",
    "ETH volume spike detected",
    "SOL bearish trend",
    "New token listing: Token 51"
  ].map(a=>`<li>${a}</li>`).join('');
}

// ====== Extra Panels (dummy) ======
function populateExtraPanels() {
  document.querySelector("#newsPanel").innerHTML += "<p>Latest crypto headlines...</p>";
  document.querySelector("#stakingPanel").innerHTML += "<p>Stake your tokens here...</p>";
  document.querySelector("#lendingPanel").innerHTML += "<p>Lend/Borrow options...</p>";
  document.querySelector("#nftPanel").innerHTML += "<p>NFT Marketplace preview...</p>";
  document.querySelector("#walletsPanel").innerHTML += "<p>Manage multiple wallets...</p>";
  document.querySelector("#performancePanel").innerHTML += "<p>Portfolio performance stats...</p>";
  document.querySelector("#heatmapPanel").innerHTML += "<p>Token heatmap demo...</p>";
}

// ====== Search Token ======
document.getElementById("searchToken").addEventListener("input", (e)=>{
  const val = e.target.value.toLowerCase();
  const tbody = document.getElementById("tokenTableBody");
  tbody.innerHTML = tokens.filter(t=>t.name.toLowerCase().includes(val)||t.symbol.toLowerCase().includes(val))
    .map(t=>`
      <tr>
        <td>${t.rank}</td>
        <td>${t.name}</td>
        <td>${t.symbol}</td>
        <td>$${t.price}</td>
        <td>${t.change}%</td>
        <td>$${t.marketCap.toLocaleString()}</td>
      </tr>
    `).join('');
});

// ====== Init ======
updatePortfolioWidgets();
updateTopMovers();
populateTokenTable();
renderPortfolioChart();
populateRecentTrades();
populateWatchlistFavorites();
populateAlerts();
populateExtraPanels();
// Feedback submission & stats
const fbUsername = document.getElementById("fbUsername");
const fbRating = document.getElementById("fbRating");
const fbCategory = document.getElementById("fbCategory");
const fbMessage = document.getElementById("fbMessage");
const submitBtn = document.getElementById("submitFeedback");

async function updateFeedbackStats() {
  try {
    const res = await fetch("/api/feedback/stats");
    const data = await res.json();
    document.getElementById("totalFeedback").textContent = data.total_feedback;
    document.getElementById("avgRating").textContent = data.average_rating.toFixed(2);
  } catch (err) {
    console.warn("Failed to fetch feedback stats:", err);
  }
}

submitBtn.addEventListener("click", async () => {
  const payload = {
    username: fbUsername.value || "Guest",
    rating: parseInt(fbRating.value),
    category: fbCategory.value || "general",
    message: fbMessage.value
  };
  try {
    const res = await fetch("/api/feedback", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    console.log("Feedback submitted:", data);
    fbMessage.value = "";
    updateFeedbackStats();
  } catch (err) {
    console.error("Error submitting feedback:", err);
  }
});

// Initialize stats
updateFeedbackStats();
setInterval(updateFeedbackStats, 60000);