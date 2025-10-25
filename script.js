/* NeuraAI_v10k Hyper-Luxe — Frontend JS
   - theme grid (100+), quick dropdown
   - sidebar drawer (slide + fade)
   - sections: chat, education, novels, web, crypto, community, games, settings
   - CoinGecko integration, community feed, mini-games, autosave prefs
*/

const API_BASE = ""; // empty means same origin; backend endpoints: /api/chat, /api/crypto, /feed/*

// ---------- Utilities ----------
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => Array.from(document.querySelectorAll(sel));
function el(tag, cls){const d=document.createElement(tag); if(cls) d.className=cls; return d;}
function savePref(k,v){ if(document.getElementById('autosavePref')?.checked !== false) localStorage.setItem(k, JSON.stringify(v)); }
function loadPref(k,def){ try{ const v=JSON.parse(localStorage.getItem(k)); return v===null?def:v;}catch(e){return def;} }

// ---------- Theme system (100+ swatches) ----------
const THEMES = (() => {
  // build 100+ color variants programmatically
  const base = ["#00e5ff","#ff33cc","#ffd24d","#00ff99","#a070ff","#4dabf7","#ff6b6b","#00c97e","#ff8c42","#9d7cff"];
  const themes = [];
  base.forEach((c, i) => {
    for(let j=0;j<10;j++){
      const id = `th_${i}_${j}`;
      // simple tint/shift by mixing with white or black
      const mix = (j-4.5)/10;
      themes.push({id, name:`Theme ${i+1}-${j+1}`, color: shadeBlend(mix, c)});
    }
  });
  return themes;
})();

// shadeBlend function (small helper) - returns hex
function shadeBlend(p, c0) {
  // p: -1..1, c0 hex
  let r=parseInt(c0.slice(1,3),16), g=parseInt(c0.slice(3,5),16), b=parseInt(c0.slice(5,7),16);
  const blend = v => Math.round(Math.min(255, Math.max(0, v + (255 - v) * Math.max(0,p) + (0 - v) * Math.max(0,-p))));
  return `#${(blend(r).toString(16).padStart(2,'0'))}${(blend(g).toString(16).padStart(2,'0'))}${(blend(b).toString(16).padStart(2,'0'))}`;
}

function buildThemeUI(){
  const quick = $("#quickTheme");
  THEMES.slice(0,20).forEach(t => { const o=document.createElement('option'); o.value=t.id; o.textContent=t.name; quick.appendChild(o); });
  // full grid
  const grid = $("#themeGrid");
  THEMES.forEach(t=>{
    const s = el('div','theme-swatch'); s.style.background = t.color; s.dataset.id=t.id; s.dataset.color=t.color;
    s.title = t.name;
    s.onclick = () => selectTheme(t);
    grid.appendChild(s);
  });
}
function selectTheme(t){
  document.body.classList.remove('neon','violet','crimson','emerald');
  // apply color by CSS var
  document.documentElement.style.setProperty('--accent', t.color);
  savePref('neura_theme_selected', t);
}

// quick dropdown handler
$("#quickTheme").addEventListener('change', (e)=>{
  const id = e.target.value;
  const t = THEMES.find(x=>x.id===id);
  if(t) selectTheme(t);
});

// open full grid
$("#openGrid").onclick = () => { $("#themeModal").classList.remove('hidden'); }
$("#closeThemeGrid").onclick = () => { $("#themeModal").classList.add('hidden'); }
$("#applyTheme").onclick = () => { $("#themeModal").classList.add('hidden'); }

// reapplies saved preferences
function applySavedPrefs(){
  const t = loadPref('neura_theme_selected', null);
  if(t){ document.documentElement.style.setProperty('--accent', t.color); }
  const mode = loadPref('neura_mode','dark');
  if(mode==='light') document.body.classList.add('light');
  const color = loadPref('neura_color',null);
  if(color) document.body.classList.add(color);
}
buildThemeUI();
applySavedPrefs();

// ---------- Drawer & navigation (slide + fade) ----------
$("#openDrawer").onclick = () => { $("#drawer").classList.add('open'); };
$("#closeDrawer").onclick = () => { $("#drawer").classList.remove('open'); };
$$('.nav-item').forEach(btn => {
  btn.onclick = () => {
    const section = btn.dataset.section;
    $("#drawer").classList.remove('open');
    $$('.panel').forEach(p => p.classList.remove('active'));
    $(`#${section}`).classList.add('active');
  };
});

// ---------- Mode toggles ----------
$("#modeToggle").onclick = () => {
  document.body.classList.toggle('light');
  savePref('neura_mode', document.body.classList.contains('light') ? 'light' : 'dark');
};
$("#avatarToggle").onclick = () => {
  document.body.classList.toggle('no-avatar');
  savePref('neura_avatar', document.body.classList.contains('no-avatar') ? false : true);
};

// animation/sound toggles
$("#toggleAnimations")?.addEventListener('change', (e)=> savePref('neura_animations', e.target.checked));
$("#toggleSound")?.addEventListener('change', (e)=> savePref('neura_sound', e.target.checked));
$("#toggleBgAnim")?.addEventListener('change', (e)=> {
  if(e.target.checked) $("#bgLayer").style.opacity = 1; else $("#bgLayer").style.opacity = .3;
  savePref('neura_bg_anim', e.target.checked);
});

// ---------- Chat (connect to /api/chat) ----------
const chatWindow = $("#chatWindow");
function appendChat(role, text){
  const d = el('div','message '+(role==='user'?'user':'ai'));
  if(role==='ai' && !document.body.classList.contains('no-avatar')){
    const avatar = el('span','avatar'); avatar.textContent = '🤖'; d.appendChild(avatar);
  }
  const p = el('div','text'); p.textContent = text; d.appendChild(p);
  chatWindow.appendChild(d);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}
$("#chatForm").onsubmit = async (e) => {
  e.preventDefault();
  const msg = $("#chatInput").value.trim();
  if(!msg) return;
  appendChat('user', msg);
  $("#chatInput").value = '';
  // visual typing
  const typing = el('div','message ai'); typing.textContent = 'NeuraAI is thinking...'; chatWindow.appendChild(typing);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  try {
    const res = await fetch(API_BASE + '/api/chat', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})});
    const j = await res.json();
    typing.remove();
    appendChat('ai', j.reply || j.choices?.[0]?.message?.content || 'Sorry, no reply.');
    if(loadPref('neura_sound', true)) document.getElementById('sndPop').play().catch(()=>{});
  } catch (err) {
    typing.remove();
    appendChat('ai', '⚠️ Connection error.');
  }
};

// auto-summary button (calls /feed/summary)
$("#summaryBtn").onclick = async () => {
  appendChat('ai','Generating summary...');
  try {
    const r = await fetch(API_BASE + '/feed/summary'); const j = await r.json();
    appendChat('ai', j.summary || 'No summary available.');
  } catch(e){ appendChat('ai','⚠️ Summary error.'); }
};

// ---------- Education: subject trainer ----------
$("#startLesson").onclick = async () => {
  const subject = $("#subjectSelect").value;
  $("#lessonArea").textContent = 'Loading lesson...';
  try {
    const r = await fetch(API_BASE + '/api/edu', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({subject})});
    const j = await r.json();
    $("#lessonArea").innerHTML = `<h4>${j.title||'Lesson'}</h4><p>${j.content||'No data'}</p>`;
  } catch(e){ $("#lessonArea").textContent = 'Failed to load lesson.'; }
};

// ---------- Novels list (connects to /api/novels or local book_platform) ----------
async function loadNovels(page=1){
  $("#novelList").textContent = 'Loading...';
  try{
    const res = await fetch(API_BASE + `/api/novels?page=${page}`);
    const j = await res.json();
    if(!j.books) { $("#novelList").textContent = 'No books'; return; }
    $("#novelList").innerHTML = j.books.map(b=>`<div class="book"><strong>${b.title}</strong><div>${b.author}</div><div>${b.description||''}</div><div>Price: ${b.price}</div><button onclick="buyBook('${b.id}')">Open</button></div>`).join('');
  }catch(e){ $("#novelList").textContent = 'Failed to load novels'; }
}
window.buyBook = async (id) => { const r = await fetch(API_BASE + `/books/get/${id}`); const j=await r.json(); alert(JSON.stringify(j)); }

// ---------- Web search (calls backend /api/search) ----------
$("#webSearchBtn").onclick = async () => {
  const q = $("#webQuery").value.trim(); if(!q) return;
  $("#webResults").textContent = 'Searching...';
  try{
    const res = await fetch(API_BASE + '/api/search', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({q})});
    const j = await res.json();
    $("#webResults").innerHTML = (j.results||[]).map(r=>`<article><h4>${r.title}</h4><p>${r.snippet}</p><a href="${r.url}" target="_blank">Open</a></article>`).join('');
  } catch(e){ $("#webResults").textContent = 'Search failed.'; }
};

// ---------- Crypto (CoinGecko) ----------
async function loadCrypto(){
  const el = $("#cryptoFeed"); el.textContent = 'Loading...';
  try{
    const res = await fetch('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,solana,binancecoin,dogecoin,cardano&order=market_cap_desc&per_page=10&page=1');
    const data = await res.json();
    el.innerHTML = data.map(c => `<div class="coin"><strong>${c.name} (${c.symbol.toUpperCase()})</strong> ${formatPrice(c.current_price)} • ${c.price_change_percentage_24h?.toFixed(2)}% • MCap: ${formatPrice(c.market_cap)} <span class="advice">${coinAdvice(c.price_change_percentage_24h)}</span></div>`).join('');
  }catch(e){ el.textContent = 'Failed to load crypto.'; }
}
function formatPrice(n){ return '$' + Number(n).toLocaleString(undefined,{minimumFractionDigits:2,maximumFractionDigits:2}); }
function coinAdvice(change){ if(change>5) return 'Buy 🚀'; if(change<-5) return 'Sell ⚠️'; return 'Hold'; }
$("#refreshCrypto").onclick = loadCrypto;
$("#portfolioBtn").onclick = async () => {
  try{
    const holdings = JSON.parse($("#portfolioInput").value||"{}");
    const res = await fetch(API_BASE + '/api/crypto/portfolio', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({holdings})});
    const j = await res.json();
    alert(JSON.stringify(j));
  }catch(e){ alert('Invalid portfolio JSON'); }
};
loadCrypto();

// ---------- Community feed (interactive) ----------
async function loadPosts(){
  try{
    const res = await fetch(API_BASE + '/feed/posts');
    const j = await res.json();
    $("#feedList").innerHTML = j.map(p => `<div class="post"><strong>${p.user}</strong> <small>${new Date(p.created_at).toLocaleString()}</small><p>${p.content}</p><div>❤️ ${p.likes} <button onclick="like(${p.id})">Like</button></div></div>`).join('');
  }catch(e){ $("#feedList").textContent = 'Failed to load posts'; }
}
async function like(id){ await fetch(API_BASE + `/feed/like/${id}`,{method:'POST'}); loadPosts(); }
$("#postForm").onsubmit = async (e) => {
  e.preventDefault();
  const user = $("#postUser").value || 'Guest';
  const content = $("#postContent").value || '';
  await fetch(API_BASE + '/feed/post',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user,content})});
  $("#postContent").value=''; loadPosts();
};
loadPosts();

// ---------- Mini-games (simple) ----------
document.getElementById('tttNew').onclick = () => { $("#gameArea").innerHTML = '<em>Tic-Tac-Toe coming soon (server-side play available)</em>'; }
document.getElementById('numNew').onclick = () => { $("#gameArea").innerHTML = '<em>Number Guess (client demo) - try 1..100</em>'; }

// ---------- Sound FX (tiny) ----------
try{ if(loadPref('neura_sound',true)) document.getElementById('sndPop').volume = .6; }catch(e){}

// ---------- Init apply saved preferences ----------
(function init(){
  // load theme selection
  const savedTheme = loadPref('neura_theme_selected', null);
  if(savedTheme) document.documentElement.style.setProperty('--accent', savedTheme.color);
  const mode = loadPref('neura_mode','dark');
  if(mode==='light') document.body.classList.add('light');
  if(loadPref('neura_bg_anim', true)) $("#bgLayer").style.opacity = 1; else $("#bgLayer").style.opacity = 0.25;
  // fill languages (example)
  const langs = ['English','Español','Français','Deutsch','Português','中文'];
  const ls = $("#langSelect");
  langs.forEach(l=>{ const o=document.createElement('option'); o.value=l; o.textContent=l; ls.appendChild(o); });
})();

// helpful exposure for console testing
window.NeuraiFrontend = { THEMES, loadCrypto, loadPosts, loadNovels };
async function sendMessage() {
  const input = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");
  const message = input.value.trim();
  if (!message) return;

  chatBox.innerHTML += `<div class="user-msg">🧑‍💻 ${message}</div>`;
  input.value = "";

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt: message, voice: false }),
  });
  const data = await res.json();

  chatBox.innerHTML += `<div class="bot-msg">🤖 ${data.response}</div>`;
  chatBox.scrollTop = chatBox.scrollHeight;
}