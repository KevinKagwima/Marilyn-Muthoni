(function () {
  "use strict";

  const nav = document.getElementById("siteNav");
  if (nav) {
    const onScroll = () => {
      if (window.scrollY > 40) nav.classList.add("scrolled");
      else nav.classList.remove("scrolled");
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  const toggle = document.getElementById("navToggle");
  const menu = document.getElementById("navMenu");
  if (toggle && menu) {
    const setMenuIcon = (open) => {
      toggle.innerHTML = open
        ? '<i class="bi bi-x-lg"></i>'
        : '<i class="bi bi-list"></i>';
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    };

    toggle.addEventListener("click", () => {
      const open = menu.classList.toggle("open");
      setMenuIcon(open);
    });

    menu.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        menu.classList.remove("open");
        setMenuIcon(false);
      });
    });
  }

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -60px 0px" },
    );
    document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
  } else {
    document
      .querySelectorAll(".reveal")
      .forEach((el) => el.classList.add("in-view"));
  }

  document.querySelectorAll(".flash-close").forEach((btn) => {
    btn.addEventListener("click", () => {
      const msg = btn.closest(".flash-msg");
      if (msg) msg.remove();
    });
  });
  document.querySelectorAll(".flash-msg").forEach((msg) => {
    setTimeout(() => msg.remove(), 6000);
  });
})();
