const WHATSAPP_NUMBER = "595971141032";
const EMAIL_TO = "alemateo07@gmail.com";

const FIELD_LIMITS = {
  name: 80,
  company: 100,
  city: 80,
  message: 1000
};

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
const navLinks = Array.from(document.querySelectorAll(".nav-links a"));
const contactForm = document.getElementById("contactForm");
const sendWhatsApp = document.getElementById("sendWhatsApp");
const sendEmail = document.getElementById("sendEmail");
const formStatus = document.getElementById("formStatus");
const accordionButtons = Array.from(document.querySelectorAll(".accordion__trigger"));

function setHeaderState() {
  const isScrolled = window.scrollY > 12;
  header.classList.toggle("is-scrolled", isScrolled);
  backToTop.classList.toggle("is-visible", window.scrollY > 520);
}

let scrollUpdatePending = false;

function scheduleHeaderStateUpdate() {
  if (scrollUpdatePending) return;

  scrollUpdatePending = true;
  requestAnimationFrame(() => {
    setHeaderState();
    scrollUpdatePending = false;
  });
}

function closeMobileMenu() {
  navToggle.classList.remove("is-open");
  primaryMenu.classList.remove("is-open");
  navToggle.setAttribute("aria-expanded", "false");
  navToggle.setAttribute("aria-label", "Abrir menú");
}

navToggle.addEventListener("click", () => {
  const isOpen = primaryMenu.classList.toggle("is-open");
  navToggle.classList.toggle("is-open", isOpen);
  navToggle.setAttribute("aria-expanded", String(isOpen));
  navToggle.setAttribute("aria-label", isOpen ? "Cerrar menú" : "Abrir menú");
});

document.addEventListener("click", (event) => {
  const clickedInsideMenu = primaryMenu.contains(event.target);
  const clickedToggle = navToggle.contains(event.target);

  if (!clickedInsideMenu && !clickedToggle) {
    closeMobileMenu();
  }
});

navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    closeMobileMenu();
  });
});

backToTop.addEventListener("click", () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});

window.addEventListener("scroll", scheduleHeaderStateUpdate, { passive: true });
setHeaderState();

const observedSections = navLinks
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);

if ("IntersectionObserver" in window) {
  const sectionObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;

        navLinks.forEach((link) => {
          link.classList.toggle("is-active", link.getAttribute("href") === `#${entry.target.id}`);
        });
      });
    },
    {
      rootMargin: "-35% 0px -55% 0px",
      threshold: 0
    }
  );

  observedSections.forEach((section) => sectionObserver.observe(section));
}

function setAccordionState(button, shouldOpen) {
  const panelId = button.getAttribute("aria-controls");
  const panel = panelId ? document.getElementById(panelId) : null;

  if (!panel) return;

  button.setAttribute("aria-expanded", String(shouldOpen));
  button.classList.toggle("is-open", shouldOpen);
  panel.classList.toggle("is-open", shouldOpen);
  panel.hidden = !shouldOpen;
}

function moveAccordionFocus(targetIndex) {
  const total = accordionButtons.length;
  if (!total) return;

  const normalizedIndex = (targetIndex + total) % total;
  accordionButtons[normalizedIndex].focus();
}

accordionButtons.forEach((button, index) => {
  if (button.dataset.accordionBound === "true") return;
  button.dataset.accordionBound = "true";

  const isExpanded = button.getAttribute("aria-expanded") === "true";
  const panelId = button.getAttribute("aria-controls");
  const panel = panelId ? document.getElementById(panelId) : null;

  button.classList.toggle("is-open", isExpanded);

  if (panel) {
    panel.hidden = !isExpanded;
    panel.classList.toggle("is-open", isExpanded);
  }

  button.addEventListener("click", () => {
    const shouldOpen = button.getAttribute("aria-expanded") !== "true";
    setAccordionState(button, shouldOpen);
  });

  button.addEventListener("keydown", (event) => {
    if (event.key === "ArrowDown") {
      event.preventDefault();
      moveAccordionFocus(index + 1);
    }

    if (event.key === "ArrowUp") {
      event.preventDefault();
      moveAccordionFocus(index - 1);
    }

    if (event.key === "Home") {
      event.preventDefault();
      moveAccordionFocus(0);
    }

    if (event.key === "End") {
      event.preventDefault();
      moveAccordionFocus(accordionButtons.length - 1);
    }
  });
});

function removeControlCharacters(value, allowLineBreaks = false) {
  const controlPattern = allowLineBreaks ? /[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g : /[\u0000-\u001F\u007F]/g;
  return value.replace(controlPattern, "");
}

function normalizeSpaces(value, allowLineBreaks = false) {
  if (allowLineBreaks) {
    return value
      .replace(/\r\n?/g, "\n")
      .split("\n")
      .map((line) => line.replace(/[ \t]+/g, " ").trim())
      .join("\n")
      .replace(/\n{3,}/g, "\n\n")
      .trim();
  }

  return value.replace(/\s+/g, " ").trim();
}

function normalizeField(value, maxLength, allowLineBreaks = false) {
  const normalized = String(value || "").normalize("NFC");
  const withoutControls = removeControlCharacters(normalized, allowLineBreaks);
  return normalizeSpaces(withoutControls, allowLineBreaks).slice(0, maxLength);
}

function normalizeContactValue(value, pattern) {
  const normalized = String(value || "").trim();
  return pattern.test(normalized) ? normalized : "";
}

function getFormValues() {
  const formData = new FormData(contactForm);

  return {
    name: normalizeField(formData.get("name"), FIELD_LIMITS.name),
    company: normalizeField(formData.get("company"), FIELD_LIMITS.company),
    city: normalizeField(formData.get("city"), FIELD_LIMITS.city),
    service: normalizeField(formData.get("service"), 60),
    message: normalizeField(formData.get("message"), FIELD_LIMITS.message, true)
  };
}

function syncSanitizedValues(values) {
  contactForm.elements.name.value = values.name;
  contactForm.elements.company.value = values.company;
  contactForm.elements.city.value = values.city;
  contactForm.elements.message.value = values.message;
}

function setFieldError(fieldName, message) {
  const field = contactForm.elements[fieldName];
  const error = contactForm.querySelector(`[data-error-for="${fieldName}"]`);

  if (!field || !error) return;

  field.classList.toggle("is-invalid", Boolean(message));
  field.setAttribute("aria-invalid", message ? "true" : "false");
  error.textContent = message;
}

function validateForm() {
  const values = getFormValues();
  syncSanitizedValues(values);

  const errors = {
    name: values.name ? "" : "Indique su nombre para poder responder.",
    company: "",
    city: values.city ? "" : "Indique la ciudad donde está la infraestructura.",
    service: ALLOWED_SERVICES.has(values.service) ? "" : "Seleccione el servicio de interés.",
    message: values.message ? "" : "Cuente brevemente qué necesita mejorar."
  };

  Object.entries(errors).forEach(([field, message]) => setFieldError(field, message));

  const firstInvalidField = Object.keys(errors).find((field) => errors[field]);
  if (firstInvalidField) {
    contactForm.elements[firstInvalidField].focus();
    formStatus.textContent = "Revise los campos marcados antes de enviar.";
    return null;
  }

  formStatus.textContent = "";
  return values;
}

function buildMessage(values) {
  const companyLine = values.company ? `Empresa u organización: ${values.company}` : "Empresa u organización: No indicada";

  return [
    "Hola Jesareko, quiero consultar por una revisión técnica.",
    "",
    `Nombre: ${values.name}`,
    companyLine,
    `Ciudad: ${values.city}`,
    `Servicio de interés: ${values.service}`,
    "",
    "Mensaje:",
    values.message
  ].join("\n");
}

function openWhatsApp() {
  const values = validateForm();
  if (!values) return;

  const whatsappNumber = normalizeContactValue(WHATSAPP_NUMBER, /^[0-9]+$/);
  if (!whatsappNumber) {
    formStatus.textContent = "El enlace de WhatsApp no está configurado correctamente.";
    return;
  }

  const text = encodeURIComponent(buildMessage(values));
  const url = `https://wa.me/${whatsappNumber}?text=${text}`;
  formStatus.textContent = "Abriendo WhatsApp con el mensaje preparado.";
  window.open(url, "_blank", "noopener,noreferrer");
}

function openEmail() {
  const values = validateForm();
  if (!values) return;

  const emailAddress = normalizeContactValue(EMAIL_TO, /^[^\s@]+@[^\s@]+\.[^\s@]+$/);
  if (!emailAddress) {
    formStatus.textContent = "El correo de contacto no está configurado correctamente.";
    return;
  }

  const subject = encodeURIComponent(`Consulta técnica - ${values.service}`);
  const body = encodeURIComponent(buildMessage(values));
  const url = `mailto:${emailAddress}?subject=${subject}&body=${body}`;
  formStatus.textContent = "Abriendo el cliente de correo con el mensaje preparado.";
  window.location.href = url;
}

sendWhatsApp.addEventListener("click", openWhatsApp);
sendEmail.addEventListener("click", openEmail);

["name", "company", "city", "service", "message"].forEach((fieldName) => {
  const field = contactForm.elements[fieldName];
  field.addEventListener("input", () => setFieldError(fieldName, ""));
});

const canUseLiquidPointer = !window.matchMedia("(pointer: coarse)").matches && !window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (canUseLiquidPointer) {
  const rootElement = document.documentElement;
  const liquidTargets = ".site-header, .nav-menu, .nav-links a, .btn, .dashboard, .metric-card, .service-card, .case-card, .benefit-card, .tech-group, .security-solution-card, .security-usecase-card, .product-ref-card, .accordion-item, .contact-form, .final-cta__inner, .back-to-top";
  let frame = 0;
  let lastEvent = null;
  let activeTargets = new Set();

  function setLocalLight(target, event) {
    const rect = target.getBoundingClientRect();
    if (!rect.width || !rect.height) return;

    const x = Math.max(0, Math.min(100, ((event.clientX - rect.left) / rect.width) * 100));
    const y = Math.max(0, Math.min(100, ((event.clientY - rect.top) / rect.height) * 100));

    target.style.setProperty("--mx", `${x.toFixed(2)}%`);
    target.style.setProperty("--my", `${y.toFixed(2)}%`);
  }

  function updateLiquidPointer() {
    frame = 0;
    if (!lastEvent) return;

    const xPercent = (lastEvent.clientX / window.innerWidth) * 100;
    const yPercent = (lastEvent.clientY / window.innerHeight) * 100;

    document.body.classList.add("has-pointer-glow");
    rootElement.style.setProperty("--page-mx-px", `${lastEvent.clientX}px`);
    rootElement.style.setProperty("--page-my-px", `${lastEvent.clientY}px`);
    rootElement.style.setProperty("--page-mx", `${xPercent.toFixed(2)}%`);
    rootElement.style.setProperty("--page-my", `${yPercent.toFixed(2)}%`);

    const target = lastEvent.target.closest(liquidTargets);
    const nextTargets = new Set();

    if (target) {
      nextTargets.add(target);
      [".dashboard", ".accordion-item", ".contact-form", ".final-cta__inner"].forEach((selector) => {
        const parent = target.closest(selector);
        if (parent) nextTargets.add(parent);
      });
    }

    activeTargets.forEach((activeTarget) => {
      if (!nextTargets.has(activeTarget)) {
        activeTarget.style.removeProperty("--mx");
        activeTarget.style.removeProperty("--my");
      }
    });

    nextTargets.forEach((activeTarget) => setLocalLight(activeTarget, lastEvent));
    activeTargets = nextTargets;
  }

  document.addEventListener("pointermove", (event) => {
    lastEvent = event;
    if (!frame) frame = window.requestAnimationFrame(updateLiquidPointer);
  }, { passive: true });

  document.addEventListener("pointerleave", () => {
    document.body.classList.remove("has-pointer-glow");
    activeTargets.forEach((activeTarget) => {
      activeTarget.style.removeProperty("--mx");
      activeTarget.style.removeProperty("--my");
    });
    activeTargets = new Set();
    lastEvent = null;
  });
}

