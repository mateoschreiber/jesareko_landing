const WHATSAPP_NUMBER = "595971141032";
const EMAIL_TO = "alemateo07@gmail.com";
const FIELD_LIMITS = { name: 80, company: 100, city: 80, message: 1000 };
const ALLOWED_SERVICES = new Set([
  "Revisión técnica / diagnóstico",
  "Redes y WiFi",
  "CCTV, alarmas, accesos e incendio",
  "Soporte e infraestructura",
  "Web, monitoreo y automatización",
  "Otro"
]);

const header = document.getElementById("siteHeader");
const navToggle = document.getElementById("navToggle");
const primaryMenu = document.getElementById("primaryMenu");
const backToTop = document.getElementById("backToTop");
const contactForm = document.getElementById("contactForm");

function updateScrollState() {
  const isScrolled = window.scrollY > 12;
  header?.classList.toggle("is-scrolled", isScrolled);
  backToTop?.classList.toggle("is-visible", window.scrollY > 520);
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

backToTop?.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));

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
  const serviceSelect = contactForm.elements.service;
  const normalize = (value, limit, multiline = false) => String(value || "")
    .normalize("NFC")
    .replace(multiline ? /[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g : /[\u0000-\u001F\u007F]/g, "")
    .replace(multiline ? /\r\n?/g : /\s+/g, multiline ? "\n" : " ")
    .split("\n").map((line) => line.replace(/[ \t]+/g, " ").trim()).join("\n").trim().slice(0, limit);

  function clearFieldError(fieldName) {
    const control = contactForm.elements[fieldName];
    control?.classList.remove("is-invalid");
    control?.removeAttribute("aria-invalid");
    control?.removeAttribute("aria-describedby");
    contactForm.querySelector(`[data-error-for="${fieldName}"]`)?.replaceChildren();
  }

  function values() {
    const data = new FormData(contactForm);
    return {
      name: normalize(data.get("name"), FIELD_LIMITS.name),
      company: normalize(data.get("company"), FIELD_LIMITS.company),
      city: normalize(data.get("city"), FIELD_LIMITS.city),
      service: normalize(data.get("service"), 60),
      message: normalize(data.get("message"), FIELD_LIMITS.message, true)
    };
  }

  function validate() {
    const data = values();
    const errors = getErrors(data);
    for (const [fieldName, message] of Object.entries(errors)) {
      const control = contactForm.elements[fieldName];
      const error = contactForm.querySelector(`[data-error-for="${fieldName}"]`);
      control.classList.toggle("is-invalid", Boolean(message));
      if (message && error) {
        control.setAttribute("aria-invalid", "true");
        control.setAttribute("aria-describedby", error.id);
      } else {
        control.removeAttribute("aria-invalid");
        control.removeAttribute("aria-describedby");
      }
      if (error) error.textContent = message;
    }
    const invalid = Object.keys(errors).find((fieldName) => errors[fieldName]);
    if (invalid) {
      contactForm.elements[invalid].focus();
      formStatus.textContent = "Revise los campos marcados antes de enviar.";
      return null;
    }
    formStatus.textContent = "";
    return data;
  }

  function getErrors(data) {
    return {
      name: data.name ? "" : "Indique su nombre para poder responder.",
      city: data.city ? "" : "Indique la ciudad donde está la infraestructura.",
      service: ALLOWED_SERVICES.has(data.service) ? "" : "Seleccione el servicio de interés.",
      message: data.message ? "" : "Cuente brevemente qué necesita mejorar."
    };
  }

  function message(data) {
    return ["Hola Jesareko, quiero consultar por una revisión técnica.", "", `Nombre: ${data.name}`, `Empresa u organización: ${data.company || "No indicada"}`, `Ciudad: ${data.city}`, `Servicio de interés: ${data.service}`, "", "Mensaje:", data.message].join("\n");
  }

  document.getElementById("sendWhatsApp")?.addEventListener("click", () => {
    const data = validate();
    if (!data) return;
    formStatus.textContent = "Abriendo WhatsApp con el mensaje preparado.";
    window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message(data))}`, "_blank", "noopener,noreferrer");
  });

  document.getElementById("sendEmail")?.addEventListener("click", () => {
    const data = validate();
    if (!data) return;
    formStatus.textContent = "Abriendo el cliente de correo con el mensaje preparado.";
    window.location.href = `mailto:${EMAIL_TO}?subject=${encodeURIComponent(`Consulta técnica - ${data.service}`)}&body=${encodeURIComponent(message(data))}`;
  });

  ["name", "company", "city", "service", "message"].forEach((fieldName) => {
    contactForm.elements[fieldName].addEventListener("input", () => {
      const error = fieldName === "company" ? "" : getErrors(values())[fieldName];
      if (!error) clearFieldError(fieldName);
      if (![...contactForm.querySelectorAll('[aria-invalid="true"]')].length) formStatus.textContent = "";
    });
  });

  const requestedService = new URLSearchParams(window.location.search).get("servicio");
  if (requestedService && ALLOWED_SERVICES.has(requestedService)) {
    serviceSelect.value = requestedService;
  }
}
