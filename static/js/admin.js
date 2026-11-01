(function () {
  "use strict";

  const toggle = document.getElementById("sidebarToggle");
  const sidebar = document.querySelector(".admin-sidebar");
  if (toggle && sidebar) {
    toggle.addEventListener("click", () => sidebar.classList.toggle("open"));
  }

  // Flash dismiss
  document.querySelectorAll(".flash-close").forEach((btn) => {
    btn.addEventListener("click", () => {
      const el = btn.closest(".admin-flash");
      if (el) el.remove();
    });
  });
  document.querySelectorAll(".admin-flash").forEach((el) => {
    setTimeout(() => el.remove(), 6000);
  });
})();
