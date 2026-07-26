import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";

const source = readFileSync(new URL("../public/assets/js/main.js", import.meta.url), "utf8");

function initializedService(search, initialValue = "sentinel") {
  const field = () => ({ addEventListener() {} });
  const service = { ...field(), value: initialValue };
  const contactForm = {
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
