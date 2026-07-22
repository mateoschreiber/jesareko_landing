const WHATSAPP_NUMBER = "595971141032";
const EMAIL_TO = "alemateo07@gmail.com";
document.documentElement.classList.add("has-js");
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

function closeMobileMenu() {
  navToggle?.classList.remove("is-open");
  primaryMenu?.classList.remove("is-open");
  navToggle?.setAttribute("aria-expanded", "false");
  navToggle?.setAttribute("aria-label", "Abrir menú");
}

navToggle?.addEventListener("click", () => {
  const isOpen = primaryMenu?.classList.toggle("is-open");
  navToggle.classList.toggle("is-open", Boolean(isOpen));
  navToggle.setAttribute("aria-expanded", String(isOpen));
  navToggle.setAttribute("aria-label", isOpen ? "Cerrar menú" : "Abrir menú");
});

document.addEventListener("click", (event) => {
  if (primaryMenu && navToggle && !primaryMenu.contains(event.target) && !navToggle.contains(event.target)) closeMobileMenu();
});

document.querySelectorAll(".nav-links a").forEach((link) => {
  link.addEventListener("click", closeMobileMenu);
  const currentPath = window.location.pathname.split("/").pop() || "index.html";
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
  const servicePicker = contactForm.querySelector("[data-service-picker]");
  const serviceTrigger = servicePicker?.querySelector("[data-service-trigger]");
  const serviceLabel = servicePicker?.querySelector("[data-service-label]");
  const serviceOptions = servicePicker?.querySelector("[data-service-options]");
  const serviceOptionButtons = [...(servicePicker?.querySelectorAll("[data-service-option]") || [])];
  const servicePickerEnabled = Boolean(servicePicker && serviceSelect && serviceTrigger && serviceOptions && typeof serviceOptions.showModal === "function");
  const serviceControl = servicePickerEnabled ? serviceTrigger : serviceSelect;
  const normalize = (value, limit, multiline = false) => String(value || "")
    .normalize("NFC")
    .replace(multiline ? /[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g : /[\u0000-\u001F\u007F]/g, "")
    .replace(multiline ? /\r\n?/g : /\s+/g, multiline ? "\n" : " ")
    .split("\n").map((line) => line.replace(/[ \t]+/g, " ").trim()).join("\n").trim().slice(0, limit);

  function closeServicePicker(returnFocus = false) {
    if (!servicePickerEnabled) return;
    servicePicker.classList.remove("is-open");
    serviceTrigger.setAttribute("aria-expanded", "false");
    if (serviceOptions.open) serviceOptions.close();
    if (returnFocus) serviceTrigger.focus();
  }

  function updateServicePicker(value) {
    if (!servicePicker || !serviceTrigger || !serviceLabel) return;
    const selected = serviceOptionButtons.find((option) => option.dataset.value === value) || serviceOptionButtons[0];
    serviceLabel.textContent = selected?.textContent || "Seleccione un servicio";
    serviceTrigger.classList.toggle("is-placeholder", !value);
    serviceOptionButtons.forEach((option) => option.classList.toggle("is-selected", option === selected));
  }

  function openServicePicker(focusOption = false) {
    if (!servicePickerEnabled) return;
    servicePicker.classList.add("is-open");
    serviceTrigger.setAttribute("aria-expanded", "true");
    if (!serviceOptions.open) serviceOptions.showModal();
    if (focusOption) (serviceOptionButtons.find((option) => option.dataset.value === serviceSelect.value) || serviceOptionButtons[0])?.focus();
  }

  function clearFieldError(fieldName) {
    const field = contactForm.elements[fieldName];
    const control = fieldName === "service" ? serviceControl : field;
    field?.classList.remove("is-invalid");
    field?.setAttribute("aria-invalid", "false");
    control?.classList.remove("is-invalid");
    control?.setAttribute("aria-invalid", "false");
    contactForm.querySelector(`[data-error-for="${fieldName}"]`)?.replaceChildren();
  }

  if (servicePickerEnabled) {
    serviceSelect.setAttribute("tabindex", "-1");
    serviceSelect.setAttribute("aria-hidden", "true");
    updateServicePicker(serviceSelect.value);

    serviceTrigger.addEventListener("click", () => {
      if (servicePicker.classList.contains("is-open")) closeServicePicker();
      else openServicePicker();
    });

    serviceTrigger.addEventListener("keydown", (event) => {
      if (!['ArrowDown', 'ArrowUp'].includes(event.key)) return;
      event.preventDefault();
      openServicePicker(true);
    });

    serviceOptionButtons.forEach((option, index) => {
      option.addEventListener("click", () => {
        serviceSelect.value = option.dataset.value || "";
        updateServicePicker(serviceSelect.value);
        serviceSelect.dispatchEvent(new Event("input", { bubbles: true }));
        closeServicePicker(true);
      });
      option.addEventListener("keydown", (event) => {
        const offset = { ArrowDown: 1, ArrowUp: -1, Home: -index, End: serviceOptionButtons.length - 1 - index }[event.key];
        if (event.key === "Escape") {
          event.preventDefault();
          closeServicePicker(true);
        } else if (offset !== undefined) {
          event.preventDefault();
          serviceOptionButtons[(index + offset + serviceOptionButtons.length) % serviceOptionButtons.length].focus();
        } else if (event.key === "Tab") {
          closeServicePicker();
        }
      });
    });

    serviceSelect.addEventListener("change", () => updateServicePicker(serviceSelect.value));
    serviceOptions.addEventListener("cancel", (event) => {
      event.preventDefault();
      closeServicePicker(true);
    });
    serviceOptions.addEventListener("click", (event) => {
      if (event.target === serviceOptions) closeServicePicker(true);
    });
    servicePicker.querySelector("[data-service-close]")?.addEventListener("click", () => {
      closeServicePicker(true);
    });
  } else {
    document.documentElement.classList.remove("has-js");
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
    const errors = {
      name: data.name ? "" : "Indique su nombre para poder responder.",
      city: data.city ? "" : "Indique la ciudad donde está la infraestructura.",
      service: ALLOWED_SERVICES.has(data.service) ? "" : "Seleccione el servicio de interés.",
      message: data.message ? "" : "Cuente brevemente qué necesita mejorar."
    };
    for (const [fieldName, message] of Object.entries(errors)) {
      const field = contactForm.elements[fieldName];
      const control = fieldName === "service" ? serviceControl : field;
      const error = contactForm.querySelector(`[data-error-for="${fieldName}"]`);
      field.classList.toggle("is-invalid", Boolean(message));
      field.setAttribute("aria-invalid", String(Boolean(message)));
      control?.classList.toggle("is-invalid", Boolean(message));
      control?.setAttribute("aria-invalid", String(Boolean(message)));
      if (error) error.textContent = message;
    }
    const invalid = Object.keys(errors).find((fieldName) => errors[fieldName]);
    if (invalid) {
      (invalid === "service" ? serviceControl : contactForm.elements[invalid]).focus();
      formStatus.textContent = "Revise los campos marcados antes de enviar.";
      return null;
    }
    formStatus.textContent = "";
    return data;
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
      clearFieldError(fieldName);
    });
  });
}
