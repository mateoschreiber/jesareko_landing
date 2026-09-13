const WHATSAPP_NUMBER = "595971141032";
const EMAIL_TO = "alemateo07@gmail.com";
const CONTACT_PROMPT = "Hola Jesareko, quisiera solicitar información técnica.";

const header = document.getElementById("siteHeader");
const navToggle = document.getElementById("navToggle");
const primaryMenu = document.getElementById("primaryMenu");
const backToTop = document.getElementById("backToTop");
const contactForm = document.getElementById("contactForm");
document.documentElement?.classList.add("js");

const reducedMotion = typeof window.matchMedia === "function" && window.matchMedia("(prefers-reduced-motion: reduce)");
if (!reducedMotion?.matches && "IntersectionObserver" in window) {
  const revealTargets = document.querySelectorAll([
    ".service-row__item",
    ".technology-proof",
    ".process-section",
    ".case-preview",
    ".service-detail",
    ".case-study",
    ".product-editorial",
    ".technology-capability",
    ".diagnostic-cta",
    ".contact-grid",
    ".privacy-card"
  ].join(","));
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-revealed");
      observer.unobserve(entry.target);
    });
  }, { threshold: .12, rootMargin: "0px 0px -4%" });

  revealTargets.forEach((target) => {
    target.classList.add("reveal-item");
    revealObserver.observe(target);
  });

  const homeTechnology = document.querySelector(".home-page .home-technology");
  if (homeTechnology) {
    const ambientObserver = new IntersectionObserver((entries) => {
      if (!entries.some((entry) => entry.isIntersecting)) return;
      homeTechnology.classList.add("is-ambient-ready");
      ambientObserver.unobserve(homeTechnology);
    }, { threshold: .35 });
    ambientObserver.observe(homeTechnology);
  }
}

function updateScrollState() {
  const isScrolled = window.scrollY > 12;
  const isVisible = window.scrollY > 520;
  header?.classList.toggle("is-scrolled", isScrolled);
  backToTop?.classList.toggle("is-visible", isVisible);
  backToTop?.toggleAttribute("aria-hidden", window.scrollY <= 520);
  if (backToTop) backToTop.tabIndex = isVisible ? 0 : -1;
}

let scrollPending = false;
window.addEventListener("scroll", () => {
  if (scrollPending) return;
  scrollPending = true;
  requestAnimationFrame(() => {
    updateScrollState();
    scrollPending = false;
  });
}, { passive: true });
updateScrollState();

function setMenuOpen(open) {
  navToggle?.classList.toggle("is-open", open);
  primaryMenu?.classList.toggle("is-open", open);
  navToggle?.setAttribute("aria-expanded", String(open));
  navToggle?.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
}

navToggle?.addEventListener("click", () => {
  setMenuOpen(navToggle.getAttribute("aria-expanded") !== "true");
});

document.addEventListener("click", (event) => {
  if (primaryMenu && navToggle && !primaryMenu.contains(event.target) && !navToggle.contains(event.target)) setMenuOpen(false);
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && navToggle?.getAttribute("aria-expanded") === "true") {
    setMenuOpen(false);
    navToggle.focus();
  }
});

document.querySelectorAll(".nav-menu > a:not(.btn)").forEach((link) => {
  link.addEventListener("click", () => setMenuOpen(false));
  const currentPath = window.location.pathname.replace(/\.html$/, "").replace(/\/$/, "") || "/";
  link.classList.toggle("is-active", link.getAttribute("href") === currentPath);
});

backToTop?.addEventListener("click", () => window.scrollTo({ top: 0, behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" }));

const accordionButtons = [...document.querySelectorAll(".accordion__trigger")];
function setAccordionState(button, isOpen) {
  const panel = document.getElementById(button.getAttribute("aria-controls"));
  if (!panel) return;
  button.setAttribute("aria-expanded", String(isOpen));
  button.classList.toggle("is-open", isOpen);
  panel.classList.toggle("is-open", isOpen);
  panel.hidden = !isOpen;
}

accordionButtons.forEach((button, index) => {
  const panel = document.getElementById(button.getAttribute("aria-controls"));
  if (!panel) return;
  setAccordionState(button, button.getAttribute("aria-expanded") === "true");
  button.addEventListener("click", () => {
    if (!window.matchMedia("(min-width: 1024px)").matches) setAccordionState(button, button.getAttribute("aria-expanded") !== "true");
  });
  button.addEventListener("keydown", (event) => {
    const keys = { ArrowDown: 1, ArrowUp: -1, Home: -index, End: accordionButtons.length - 1 - index };
    if (!(event.key in keys)) return;
    event.preventDefault();
    accordionButtons[(index + keys[event.key] + accordionButtons.length) % accordionButtons.length].focus();
  });
});

if (contactForm) {
  const formStatus = document.getElementById("formStatus");

  document.getElementById("sendWhatsApp")?.addEventListener("click", () => {
    formStatus.textContent = "Abriendo WhatsApp con un saludo general.";
    window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(CONTACT_PROMPT)}`, "_blank", "noopener,noreferrer");
  });

  document.getElementById("sendEmail")?.addEventListener("click", () => {
    formStatus.textContent = "Abriendo el cliente de correo con un mensaje general.";
    window.location.href = `mailto:${EMAIL_TO}?subject=${encodeURIComponent("Consulta técnica")}&body=${encodeURIComponent(CONTACT_PROMPT)}`;
  });
}
