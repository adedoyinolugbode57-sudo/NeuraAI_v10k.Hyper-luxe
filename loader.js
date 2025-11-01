// Neuraluxe-AI Smooth Page Transition Loader ✨
document.addEventListener("DOMContentLoaded", () => {
  const loader = document.createElement("div");
  loader.id = "loaderOverlay";
  loader.innerHTML = `<div class="loader-spinner"></div>`;
  document.body.appendChild(loader);

  // Show loader on page load
  loader.classList.add("active");
  setTimeout(() => loader.classList.remove("active"), 1000);

  // Add smooth transitions for internal links
  const links = document.querySelectorAll("a[href]");
  links.forEach(link => {
    link.addEventListener("click", e => {
      const href = link.getAttribute("href");
      if (href && !href.startsWith("#") && !href.startsWith("http")) {
        e.preventDefault();
        loader.classList.add("active");
        setTimeout(() => {
          window.location.href = href;
        }, 800);
      }
    });
  });
});