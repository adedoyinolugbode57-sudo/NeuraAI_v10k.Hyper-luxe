// Marketplace.jsx — Neuraluxe-AI Hyper Marketplace (Final Integration)
// Place in: frontend/src/components/Marketplace.jsx

import React, { useEffect, useState, useRef } from "react";

/**
 * Behavior summary:
 * - Tries to fetch pages from /api/market/items?page=..&page_size=..
 * - If the backend is absent or fails, generates simulated items client-side (fast deterministic generator).
 * - Renders thumbnails, description, rating, price (>=29.99).
 * - Infinite scroll loads next pages lazily.
 * - "Buy" opens checkout_url returned by backend purchase endpoint OR shows a mock modal.
 *
 * Usage:
 * <Marketplace />
 */

const DEFAULT_PAGE_SIZE = 24;
const MIN_PRICE = 29.99;
const MAX_PRICE = 999999.0;
const TOTAL_SIMULATED = 1000000; // 1M simulated cap

// Helper: deterministic client-side generator for item index -> item
function genItem(idx) {
  const categories = [
    "AI Tools",
    "Automation Bots",
    "Trading Scripts",
    "Freelancer Tools",
    "Design Studio",
    "Crypto Assets",
    "Voice & Language",
    "Education Packs",
    "Developer Plugins",
    "Global Add-Ons",
  ];
  const rnd = (seed) => {
    // simple deterministic pseudo-random (mulberry32)
    let t = seed + 0x6D2B79F5;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };

  const r = rnd(idx);
  const category = categories[idx % categories.length];
  const baseName = {
    "AI Tools": "Neuraluxe AI Tool",
    "Automation Bots": "AutoFlow Bot",
    "Trading Scripts": "Neuraluxe Trader",
    "Freelancer Tools": "Freelance Boost Kit",
    "Design Studio": "Studio Pack",
    "Crypto Assets": "Crypto Signal Module",
    "Voice & Language": "Voice Pack",
    "Education Packs": "Learning Module",
    "Developer Plugins": "Dev Plugin",
    "Global Add-Ons": "Legacy Add-On",
  }[category] || "Neuraluxe Asset";

  // price scaled but always >= MIN_PRICE
  const price = +(MIN_PRICE + ((idx % 1000) * ((MAX_PRICE - MIN_PRICE) / 1000)) + (r * 49.99)).toFixed(2);

  return {
    id: `nli-${String(idx).padStart(7, "0")}`,
    name: `${baseName} #${idx}`,
    category,
    price,
    currency: "USD",
    rating: (3 + (r * 2)).toFixed(1),
    description: `A premium ${category.toLowerCase()} powered by Neuraluxe-AI for increased productivity and creativity.`,
    image: `https://picsum.photos/seed/neuraluxe${idx}/400/300`,
    rarity: ["Common","Rare","Ultra","Limited"][Math.floor(r * 4)]
  };
}

export default function Marketplace() {
  const [items, setItems] = useState([]); // loaded items
  const [page, setPage] = useState(1);
  const [pageSize] = useState(DEFAULT_PAGE_SIZE);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("all");
  const [sort, setSort] = useState("recommended");
  const [minPrice, setMinPrice] = useState(MIN_PRICE);
  const [maxPrice, setMaxPrice] = useState(9999);
  const [useBackend, setUseBackend] = useState(true);
  const containerRef = useRef(null);

  // On mount: attempt a small fetch to detect backend availability
  useEffect(() => {
    let cancelled = false;
    async function detect() {
      try {
        const res = await fetch(`/api/market/items?page=1&page_size=1`);
        if (!cancelled) {
          if (!res.ok) throw new Error("no backend");
          const j = await res.json();
          setUseBackend(true);
        }
      } catch (e) {
        setUseBackend(false);
      }
    }
    detect();
    return () => (cancelled = true);
  }, []);

  // Load a page (backend or local generator)
  const loadPage = async (p = 1) => {
    if (loading) return;
    setLoading(true);
    try {
      if (useBackend) {
        const params = new URLSearchParams({
          page: p,
          page_size: pageSize,
          q: query || "",
          category: category === "all" ? "" : category,
          min_price: String(minPrice),
          max_price: String(maxPrice || MAX_PRICE)
        });
        const res = await fetch(`/api/market/items?${params.toString()}`);
        if (res.ok) {
          const data = await res.json();
          const newItems = (data.items || []).map(normalizeItem);
          setItems(prev => [...prev, ...newItems]);
          setHasMore((data.items || []).length >= pageSize);
          setPage(p + 1);
        } else {
          // fallback
          generateLocalPage(p);
        }
      } else {
        generateLocalPage(p);
      }
    } catch (e) {
      console.warn("loadPage error:", e);
      generateLocalPage(p);
    } finally {
      setLoading(false);
    }
  };

  // Normalize backend item into local shape (safe)
  const normalizeItem = it => ({
    id: it.id || it.item_id || it.index || `nli-0000000`,
    name: it.name || it.title || "Neuraluxe Item",
    category: it.category || "AI Tools",
    price: parseFloat(it.price || it.amount || MIN_PRICE),
    currency: it.currency || "USD",
    rating: it.rating || (3 + Math.random() * 2).toFixed(1),
    description: it.description || "",
    image: it.image || `https://picsum.photos/seed/${encodeURIComponent(it.id || it.name)}/400/300`,
    rarity: it.rarity || "Common"
  });

  // Local deterministic generation fills a page using the generator
  const generateLocalPage = (p) => {
    const start = (p - 1) * pageSize + 1;
    const list = [];
    for (let i = start; i < start + pageSize && i <= TOTAL_SIMULATED; i++) {
      const it = genItem(i);
      // apply local filters (search + category + price)
      if (category !== "all" && it.category.toLowerCase() !== category.toLowerCase()) continue;
      if (it.price < minPrice || (maxPrice && it.price > maxPrice)) continue;
      if (query && !(`${it.name} ${it.description} ${it.category}`).toLowerCase().includes(query.toLowerCase())) continue;
      list.push(it);
    }
    setItems(prev => [...prev, ...list.map(normalizeItem)]);
    setHasMore(list.length >= pageSize);
    setPage(p + 1);
  };

  // initial load
  useEffect(() => {
    setItems([]);
    setPage(1);
    setHasMore(true);
    loadPage(1);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [useBackend]);

  // Apply filters/search - reset and load new
  const applyFilter = () => {
    setItems([]);
    setPage(1);
    setHasMore(true);
    // try backend search; if backend unavailable fallback automatically in loadPage
    loadPage(1);
  };

  // Infinite scroll handler
  useEffect(() => {
    const onScroll = () => {
      if (!hasMore || loading) return;
      const c = containerRef.current || document.documentElement;
      const threshold = 400;
      const bottomReached = (window.innerHeight + window.scrollY) >= (document.body.offsetHeight - threshold);
      if (bottomReached) loadPage(page);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
    // eslint-disable-next-line
  }, [page, loading, hasMore, useBackend]);

  // Purchase flow
  const buyItem = async (item) => {
    try {
      // developer bypass or mock quick purchase
      const userEmail = window.__NEURA_USER_EMAIL || ""; // optional global var if your app sets it
      if (userEmail && userEmail.toLowerCase() === "adedoyinolugbode57@gmail.com") {
        alert("Developer bypass: purchase completed for free ✅");
        return;
      }

      // Call backend purchase if available
      if (useBackend) {
        const res = await fetch(`/api/market/purchase`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_email: userEmail || "guest@example.com", item_id: item.id, quantity: 1 })
        });
        const j = await res.json();
        if (j.checkout_url) {
          window.open(j.checkout_url, "_blank");
        } else if (j.status === "success") {
          alert("Purchase successful! ✅");
        } else {
          alert(j.message || "Proceed to checkout.");
        }
      } else {
        // Mock checkout
        alert(`Simulated checkout started for ${item.name} — $${item.price}`);
      }
    } catch (e) {
      console.warn("buyItem error", e);
      alert("Unable to start purchase. Try again later.");
    }
  };

  // small UI helpers
  const categories = ["all","AI Tools","Automation Bots","Trading Scripts","Freelancer Tools","Design Studio","Crypto Assets","Voice & Language","Education Packs","Developer Plugins","Global Add-Ons"];

  return (
    <div className="marketplace-panel panel active" style={{padding:20}} ref={containerRef}>
      <h2 style={{marginBottom:12}}>🛒 Neuraluxe-AI Marketplace</h2>

      <div style={{display:"flex",gap:10,flexWrap:"wrap",marginBottom:14,alignItems:"center"}}>
        <input
          className="search"
          placeholder="Search items, categories, descriptions..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter") applyFilter(); }}
          style={{flex:1,minWidth:220}}
        />

        <select value={category} onChange={(e)=>{ setCategory(e.target.value); }} style={{padding:10,borderRadius:8}}>
          {categories.map(c => <option key={c} value={c}>{c}</option>)}
        </select>

        <select value={sort} onChange={(e)=> setSort(e.target.value)} style={{padding:10,borderRadius:8}}>
          <option value="recommended">Recommended</option>
          <option value="price-asc">Price: Low → High</option>
          <option value="price-desc">Price: High → Low</option>
          <option value="rating">Rating</option>
        </select>

        <button className="btn" onClick={applyFilter} style={{marginLeft:"auto"}}>Apply</button>
      </div>

      <div className="market-grid" style={{marginTop:8}}>
        {items.length === 0 && !loading && (
          <div style={{padding:20}}>No items yet. Try different filters.</div>
        )}

        {items
          .slice()
          .sort((a,b) => {
            if (sort === "price-asc") return a.price - b.price;
            if (sort === "price-desc") return b.price - a.price;
            if (sort === "rating") return parseFloat(b.rating) - parseFloat(a.rating);
            return 0;
          })
          .map((it) => (
          <div key={it.id} className="card" style={{display:"flex",flexDirection:"column"}}>
            <img src={it.image} alt={it.name} style={{width:"100%",height:140,objectFit:"cover",borderRadius:8,marginBottom:8}} />
            <h4 style={{marginBottom:6}}>{it.name}</h4>
            <p className="small" style={{marginBottom:8}}>{it.description}</p>
            <div style={{display:"flex",justifyContent:"space-between",alignItems:"center"}}>
              <div>
                <div className="price">${Number(it.price).toFixed(2)}</div>
                <div className="small">⭐ {it.rating} • {it.rarity}</div>
              </div>
              <div style={{display:"flex",flexDirection:"column",gap:8}}>
                <button className="btn" onClick={()=>buyItem(it)} style={{minWidth:110}}>Buy</button>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div style={{marginTop:18,display:"flex",justifyContent:"center",gap:10}}>
        {loading ? <div className="small">Loading...</div> : hasMore ? <button className="btn" onClick={()=>loadPage(page)}>Load more</button> : <div className="small">No more items</div>}
      </div>

      <div style={{marginTop:16,color:"var(--muted)"}} className="small">
        Showing {items.length} items • Simulated range up to {TOTAL_SIMULATED.toLocaleString()}
      </div>
    </div>
  );
}