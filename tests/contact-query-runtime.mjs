import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";

const source = readFileSync(new URL("../public/assets/js/main.js", import.meta.url), "utf8");

function contactChannelResults() {
  let whatsAppHandler;
  let emailHandler;
  let openedUrl = "";
  const contactPanel = {};
  const formStatus = { textContent: "" };
  const sendWhatsApp = {
    addEventListener(type, handler) {
      if (type === "click") whatsAppHandler = handler;
    }
  };
  const sendEmail = {
    addEventListener(type, handler) {
      if (type === "click") emailHandler = handler;
    }
  };
  const document = {
    addEventListener() {},
    documentElement: { classList: { add() {} } },
    querySelectorAll() { return []; },
    getElementById(id) {
      if (id === "contactForm") return contactPanel;
      if (id === "formStatus") return formStatus;
      if (id === "sendWhatsApp") return sendWhatsApp;
      if (id === "sendEmail") return sendEmail;
      return null;
    }
  };
  const location = { pathname: "/contacto", search: "", href: "" };
  const window = {
    addEventListener() {},
    location,
    scrollY: 0,
    scrollTo() {},
    open(url) { openedUrl = url; }
  };

  vm.runInNewContext(source, {
    document,
    window,
    requestAnimationFrame() {}
  });

  whatsAppHandler();
  emailHandler();
  return { openedUrl, mailtoUrl: location.href, formStatus: formStatus.textContent };
}

const { openedUrl, mailtoUrl, formStatus } = contactChannelResults();
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
    assert.equal(decoded.includes(sensitiveValue), false, `contact URL must not contain ${sensitiveValue}`);
  }
}
assert.match(openedUrl, /^https:\/\/wa\.me\/595971141032\?text=/);
assert.match(mailtoUrl, /^mailto:alemateo07@gmail\.com\?subject=Consulta%20t%C3%A9cnica&body=/);
assert.match(formStatus, /mensaje general/);

console.log("contact channel runtime: 3/3 OK");
