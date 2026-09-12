import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";

const source = readFileSync(new URL("../public/assets/js/main.js", import.meta.url), "utf8");

function initializedService(search, initialValue = "sentinel") {
  const field = () => ({ addEventListener() {} });
  const service = { ...field(), value: initialValue };
  const contactForm = {
    addEventListener() {},
    elements: {
      name: field(),
      company: field(),
      city: field(),
      service,
      message: field()
    },
    querySelector() { return null; },
    querySelectorAll() { return []; }
  };
  const formStatus = { textContent: "" };
  const document = {
    addEventListener() {},
    querySelectorAll() { return []; },
    getElementById(id) {
      if (id === "contactForm") return contactForm;
      if (id === "formStatus") return formStatus;
      return null;
    }
  };
  const window = {
    addEventListener() {},
    location: { pathname: "/contacto", search },
    scrollY: 0,
    scrollTo() {}
  };

  vm.runInNewContext(source, {
    document,
    window,
    URLSearchParams,
    requestAnimationFrame() {}
  });
  return service.value;
}

assert.equal(
  initializedService("?servicio=Valor%20desconocido"),
  "sentinel",
  "an unknown service must preserve the current select value"
);
assert.equal(
  initializedService("?servicio=Redes%20y%20WiFi"),
  "Redes y WiFi",
  "an exact allowed service must initialize the select"
);

console.log("contact query runtime: 2/2 OK");

function contactChannelResults() {
  const fields = {};
  const field = (value = "") => ({
    value,
    classList: { remove() {}, toggle() {} },
    addEventListener() {},
    setAttribute() {},
    removeAttribute() {},
    focus() {}
  });
  for (const [name, value] of Object.entries({
    name: "Ana Seguridad",
    company: "Planta Norte",
    city: "Encarnación",
    service: "CCTV, alarmas, accesos e incendio",
    message: "La cámara del acceso principal falla de noche y la red interna está expuesta."
  })) {
    fields[name] = field(value);
  }

  let clickHandler;
  let submitHandler;
  let openedUrl = "";
  const sendWhatsApp = {
    addEventListener(type, handler) {
      if (type === "click") clickHandler = handler;
    }
  };
  const contactForm = {
    noValidate: false,
    addEventListener(type, handler) {
      if (type === "submit") submitHandler = handler;
    },
    elements: fields,
    querySelector(selector) {
      if (selector.startsWith("[data-error-for=")) {
        return { id: "error", textContent: "", replaceChildren() {} };
      }
      return null;
    },
    querySelectorAll() { return []; }
  };
  const formStatus = { textContent: "" };
  const document = {
    addEventListener() {},
    querySelectorAll() { return []; },
    getElementById(id) {
      if (id === "contactForm") return contactForm;
      if (id === "formStatus") return formStatus;
      if (id === "sendWhatsApp") return sendWhatsApp;
      return null;
    }
  };
  const location = { pathname: "/contacto", search: "", href: "" };
  const window = {
    addEventListener() {},
    location,
    scrollY: 0,
    scrollTo() {},
    open(url) {
      openedUrl = url;
    }
  };

  class FormDataStub {
    get(name) {
      return fields[name]?.value || "";
    }
  }

  vm.runInNewContext(source, {
    document,
    window,
    URLSearchParams,
    FormData: FormDataStub,
    requestAnimationFrame() {}
  });

  clickHandler();
  submitHandler({ preventDefault() {} });
  return { openedUrl, mailtoUrl: location.href };
}

const { openedUrl, mailtoUrl } = contactChannelResults();
for (const url of [openedUrl, mailtoUrl]) {
  const decoded = decodeURIComponent(url);
  for (const sensitiveValue of [
    "Ana Seguridad",
    "Planta Norte",
    "Encarnación",
    "CCTV, alarmas, accesos e incendio",
    "acceso principal",
    "red interna"
  ]) {
    assert.equal(
      decoded.includes(sensitiveValue),
      false,
      `prefilled contact URL must not contain ${sensitiveValue}`
    );
  }
}
assert.match(openedUrl, /^https:\/\/wa\.me\/595971141032\?text=/);
assert.match(mailtoUrl, /^mailto:alemateo07@gmail\.com\?subject=Consulta%20t%C3%A9cnica&body=/);

console.log("contact channel runtime: 2/2 OK");
