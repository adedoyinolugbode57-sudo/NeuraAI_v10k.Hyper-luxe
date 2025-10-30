import React, { useState, useEffect } from "react";

export default function Marketplace() {
  const [items, setItems] = useState([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("all");
  const [sort, setSort] = useState("price-asc");

  useEffect(() => {
    const generatedItems = [];
    const categories = ["AI Tools", "Automation", "Freelancer Kits", "Trading Bots", "Premium Plugins", "Education Packs"];

    for (let i = 1; i <= 200; i++) {
      const price = (Math.random() * 999970 + 29.99).toFixed(2);
      const cat = categories[Math.floor(Math.random() * categories.length)];
      generatedItems.push({
        id: i,
        name: `${cat} #${i}`,
        category: cat,
        price: price,
        image: `https://source.unsplash.com/300x200/?technology,ai,${i}`,
      });
    }
    setItems(generatedItems);
  }, []);

  const filteredItems = items
    .filter((item) =>
      item.name.toLowerCase().includes(search.toLowerCase())
    )
    .filter((item) =>
      category === "all" ? true : item.category === category
    )
    .sort((a, b) => {
      if (sort === "price-asc") return a.price - b.price;
      if (sort === "price-desc") return b.price - a.price;
      return 0;
    });

  return (
    <div className="p-6 space-y-4">
      <h2 className="text-3xl font-bold text-center text-purple-600">🛍️ Neuraluxe-AI Marketplace</h2>

      {/* Search and Filters */}
      <div className="flex flex-wrap items-center justify-center gap-4 mb-6">
        <input
          type="text"
          placeholder="🔍 Search products..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="p-2 rounded-lg border border-gray-300 w-60 focus:outline-none focus:ring-2 focus:ring-purple-400"
        />
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="p-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-400"
        >
          <option value="all">All Categories</option>
          <option value="AI Tools">AI Tools</option>
          <option value="Automation">Automation</option>
          <option value="Freelancer Kits">Freelancer Kits</option>
          <option value="Trading Bots">Trading Bots</option>
          <option value="Premium Plugins">Premium Plugins</option>
          <option value="Education Packs">Education Packs</option>
        </select>
        <select
          value={sort}
          onChange={(e) => setSort(e.target.value)}
          className="p-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-400"
        >
          <option value="price-asc">Sort by Price: Low → High</option>
          <option value="price-desc">Sort by Price: High → Low</option>
        </select>
      </div>

      {/* Product Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {filteredItems.map((item) => (
          <div
            key={item.id}
            className="bg-white rounded-2xl shadow-md hover:shadow-xl transition-transform transform hover:-translate-y-1 cursor-pointer"
          >
            <img
              src={item.image}
              alt={item.name}
              className="rounded-t-2xl w-full h-40 object-cover"
            />
            <div className="p-4">
              <h3 className="font-semibold text-lg text-gray-700">{item.name}</h3>
              <p className="text-sm text-gray-500">{item.category}</p>
              <p className="mt-2 text-purple-600 font-bold">${item.price}</p>
              <button className="mt-3 bg-purple-600 text-white px-3 py-1 rounded-lg hover:bg-purple-700 transition">
                Buy Now
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}