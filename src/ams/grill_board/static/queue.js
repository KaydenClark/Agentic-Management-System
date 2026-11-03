// Read the current queue automatically; never replace an owner's unsaved words.
(function () {
  var revision = document.body.dataset.boardRevision;
  var notice = document.querySelector("[data-queue-update]");
  var pending = false;
  var changed = false;

  function editing() {
    return Array.from(document.querySelectorAll("textarea, input:not([type=hidden])"))
      .some(function (field) { return field.value.trim() !== ""; });
  }

  async function refresh() {
    if (pending || document.visibilityState === "hidden") return;
    pending = true;
    try {
      var response = await fetch("/api/revision", { cache: "no-store" });
      if (!response.ok) throw new Error("unavailable");
      var value = await response.json();
      if (typeof value.revision !== "string") throw new Error("unavailable");
      changed = value.revision !== revision;
      if (changed && !editing()) {
        location.reload();
      } else {
        notice.hidden = !changed;
        notice.textContent = changed
          ? "The queue changed. Your unsaved words are kept; finish or clear them before it refreshes."
          : "";
      }
    } catch (error) {
      notice.hidden = false;
      notice.textContent = "The current queue is unavailable. Showing the last loaded questions; saved answers are preserved.";
    } finally {
      pending = false;
    }
  }

  setInterval(refresh, 5000);
  document.addEventListener("visibilitychange", refresh);
  document.addEventListener("input", function () {
    if (changed && !editing()) refresh();
  });
})();
