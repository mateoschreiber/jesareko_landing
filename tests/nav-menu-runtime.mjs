import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";

const source = readFileSync(new URL("../public/assets/js/main.js", import.meta.url), "utf8");
const listeners = new Map();

function classList() {
  const tokens = new Set();
  return {
    contains(token) { return tokens.has(token); },
    toggle(token, force) {
      if (force === undefined ? !tokens.has(token) : force) tokens.add(token);
      else tokens.delete(token);
    }
  };
}

const attributes = new Map([["aria-expanded", "false"]]);
let focusCount = 0;
const navToggle = {
  classList: classList(),
  addEventListener(type, listener) { listeners.set(`toggle:${type}`, listener); },
  contains() { return false; },
  focus() { focusCount += 1; },
  getAttribute(name) { return attributes.get(name) ?? null; },
  setAttribute(name, value) { attributes.set(name, value); }
};
const primaryMenu = {
  classList: classList(),
  contains() { return false; }
};
const document = {
  addEventListener(type, listener) { listeners.set(`document:${type}`, listener); },
  querySelectorAll() { return []; },
  getElementById(id) {
    if (id === "navToggle") return navToggle;
    if (id === "primaryMenu") return primaryMenu;
    return null;
  }
};
const window = {
  addEventListener() {},
  location: { pathname: "/", search: "" },
  scrollY: 0,
  scrollTo() {}
};

vm.runInNewContext(source, {
  document,
  window,
  URLSearchParams,
  requestAnimationFrame(callback) { callback(); }
});

listeners.get("toggle:click")();
assert.equal(attributes.get("aria-expanded"), "true", "the toggle must open the mobile menu");

listeners.get("document:keydown")({ key: "Escape" });
assert.equal(attributes.get("aria-expanded"), "false", "Escape must close the mobile menu");
assert.equal(focusCount, 1, "Escape must return focus to the menu toggle");

console.log("nav menu runtime: 3/3 OK");
