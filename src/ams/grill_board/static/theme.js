// Grill Board theme: follows the system preference until the owner picks one
// with the toggle; the pick is remembered in this browser only.
(function () {
  var KEY = "grill-board-theme";
  var root = document.documentElement;
  function stored() {
    try { return localStorage.getItem(KEY); } catch (error) { return null; }
  }
  function current() {
    var picked = root.getAttribute("data-theme");
    if (picked) return picked;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
  }
  var saved = stored();
  if (saved === "light" || saved === "dark") root.setAttribute("data-theme", saved);
  function label() {
    var text = document.querySelector("[data-theme-label]");
    if (text) text.textContent = current() === "light" ? "Light" : "Dark";
  }
  document.addEventListener("DOMContentLoaded", function () {
    var button = document.querySelector("[data-theme-toggle]");
    label();
    if (!button) return;
    button.hidden = false;
    button.addEventListener("click", function () {
      var next = current() === "light" ? "dark" : "light";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem(KEY, next); } catch (error) {}
      label();
    });
  });
})();
