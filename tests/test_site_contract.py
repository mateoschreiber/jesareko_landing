from html.parser import HTMLParser
from pathlib import Path
import json
import re
import subprocess
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from threading import Thread
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
PAGES = ["index.html", "servicios.html", "casos.html", "tecnologias.html", "contacto.html", "privacidad.html"]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.h1_count = 0
        self.images = []
        self.links = []
        self.article_links = []
        self.class_tokens = set()
        self.dialog_count = 0
        self.selects = []
        self.navs = []
        self.product_editorial_images = []
        self._article_depth = 0
        self._product_editorial_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "article":
            self._article_depth += 1
        if tag == "article" and "product-editorial" in attrs.get("class", "").split():
            self._product_editorial_depth += 1
        self.class_tokens.update(attrs.get("class", "").split())
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "h1":
            self.h1_count += 1
        if tag == "img":
            self.images.append(attrs)
            if self._product_editorial_depth:
                self.product_editorial_images.append(attrs)
        if tag == "a":
            self.links.append(attrs)
            if self._article_depth:
                self.article_links.append(attrs)
        if tag == "dialog":
            self.dialog_count += 1
        if tag == "select":
            self.selects.append(attrs)
        if tag == "nav":
            self.navs.append(attrs)

    def handle_endtag(self, tag):
        if tag == "article" and self._product_editorial_depth:
            self._product_editorial_depth -= 1
        if tag == "article" and self._article_depth:
            self._article_depth -= 1


def parse_page(name):
    parser = PageParser()
    parser.feed((PUBLIC / name).read_text(encoding="utf-8"))
    return parser


class SiteContractTests(unittest.TestCase):
    def test_every_brand_image_has_a_source_record(self):
        registry = json.loads((ROOT / "docs" / "image-sources.json").read_text(encoding="utf-8"))
        registered = {item["local_file"] for item in registry["images"]}
        used = set()
        for page in PAGES:
            for image in parse_page(page).images:
                src = image.get("src", "")
                if "assets/img/brands/" in src:
                    used.add(src)
        self.assertTrue(used.issubset(registered))

    def test_every_technology_catalog_asset_is_used_in_an_editorial_product(self):
        registry = json.loads((ROOT / "docs" / "image-sources.json").read_text(encoding="utf-8"))
        catalog_assets = {
            item["local_file"]
            for item in registry["images"]
            if item["usage_context"] == "technologies_catalog"
        }
        editorial_assets = {
            image["src"]
            for image in parse_page("tecnologias.html").product_editorial_images
            if "assets/img/brands/" in image.get("src", "")
        }

        self.assertEqual(catalog_assets, editorial_assets)

    def test_every_page_uses_new_shared_shell(self):
        for page in PAGES:
            with self.subTest(page=page):
                parsed = parse_page(page)
                self.assertIn("site-nav", parsed.class_tokens)
                self.assertIn("brand-lockup", parsed.class_tokens)
                self.assertIn("site-footer", parsed.class_tokens)
                primary_nav = next(nav for nav in parsed.navs if nav.get("aria-label") == "Navegación principal")
                self.assertTrue({"site-nav", "container"}.issubset(primary_nav.get("class", "").split()))
                source = (PUBLIC / page).read_text(encoding="utf-8")
                self.assertIn('aria-controls="primaryMenu"', source)

    def test_required_service_field_uses_native_select_without_overlay(self):
        parsed = parse_page("contacto.html")
        service_selects = [select for select in parsed.selects if select.get("name") == "service"]

        self.assertEqual(parsed.dialog_count, 0)
        self.assertFalse(any(token.startswith("service-picker") for token in parsed.class_tokens))
        self.assertEqual(len(service_selects), 1)
        self.assertNotEqual(service_selects[0].get("aria-hidden"), "true")
        self.assertNotEqual(service_selects[0].get("tabindex"), "-1")

    def test_whatsapp_uses_symbol_not_emoji(self):
        for page in PAGES:
            source = (PUBLIC / page).read_text(encoding="utf-8")
            with self.subTest(page=page):
                self.assertNotIn("📱", source)
                self.assertNotIn("☎", source)
                if "wa.me/" in source:
                    self.assertIn('href="#icon-whatsapp"', source)

    def test_every_page_has_one_h1_and_unique_ids(self):
        for page in PAGES:
            with self.subTest(page=page):
                parsed = parse_page(page)
                self.assertEqual(parsed.h1_count, 1)
                self.assertEqual(len(parsed.ids), len(set(parsed.ids)))

    def test_images_have_alt_and_dimensions(self):
        for page in PAGES:
            for image in parse_page(page).images:
                with self.subTest(page=page, src=image.get("src")):
                    self.assertIn("alt", image)
                    self.assertIn("width", image)
                    self.assertIn("height", image)

    def test_blank_targets_are_safe(self):
        for page in PAGES:
            for link in parse_page(page).links:
                if link.get("target") == "_blank":
                    rel = set(link.get("rel", "").split())
                    self.assertTrue({"noopener", "noreferrer"}.issubset(rel))

    def test_privacy_contact_links_have_local_touch_targets(self):
        privacy_links = [
            link
            for link in parse_page("privacidad.html").article_links
            if link.get("href", "").startswith(("/contacto", "https://wa.me/"))
        ]
        self.assertEqual(len(privacy_links), 2)
        for link in privacy_links:
            with self.subTest(href=link["href"]):
                self.assertIn("privacy-contact-link", link.get("class", "").split())

        css = (PUBLIC / "assets" / "css" / "styles.css").read_text(encoding="utf-8")
        rule = re.search(r"(?ms)^\.privacy-contact-link\s*\{(?P<body>.*?)^\}", css)
        self.assertIsNotNone(rule)
        body = rule.group("body")
        self.assertRegex(body, r"display:\s*inline-flex;")
        self.assertRegex(body, r"min-height:\s*48px;")
        self.assertRegex(body, r"min-width:\s*48px;")
        self.assertRegex(body, r"max-width:\s*100%;")
        self.assertRegex(body, r"overflow-wrap:\s*anywhere;")

        global_link_rule = re.search(r"(?ms)^a\s*\{(?P<body>.*?)^\}", css)
        self.assertIsNotNone(global_link_rule)
        self.assertNotRegex(global_link_rule.group("body"), r"(?:display|min-(?:height|width))\s*:")

    def test_css_does_not_mask_layout_failures(self):
        css = (PUBLIC / "assets" / "css" / "styles.css").read_text(encoding="utf-8")
        self.assertNotIn("overflow-x: hidden", css)
        self.assertNotIn("margin-left: -", css)
        self.assertIn("@media (prefers-reduced-motion: reduce)", css)
        for token in ("--radius-sm: 10px", "--radius-md: 14px", "--radius-lg: 20px"):
            self.assertIn(token, css)

    def test_responsive_queries_are_consolidated(self):
        css = (PUBLIC / "assets" / "css" / "styles.css").read_text(encoding="utf-8")
        self.assertEqual(css.count("@media (max-width: 52rem)"), 1)

    def test_button_has_one_canonical_definition(self):
        css = (PUBLIC / "assets" / "css" / "styles.css").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"(?m)^\.btn\s*\{", css)), 1)

    def test_mobile_menu_escape_restores_focus(self):
        runtime_test = Path(__file__).with_name("nav-menu-runtime.mjs")
        result = subprocess.run(
            ["node", str(runtime_test)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_mobile_navigation_has_a_no_javascript_fallback(self):
        css = (PUBLIC / "assets" / "css" / "styles.css").read_text(encoding="utf-8")
        mobile = re.search(r"(?s)@media \(max-width: 52rem\) \{(?P<body>.*?)\n\}", css)
        self.assertIsNotNone(mobile)
        body = mobile.group("body")
        self.assertNotRegex(body, r"(?s)^\s*\.nav-menu\s*\{[^}]*display:\s*none;")
        self.assertRegex(body, r"(?s)\.js\s+\.nav-menu\s*\{[^}]*display:\s*none;")
        self.assertRegex(body, r"(?s)\.js\s+\.nav-menu\.is-open\s*\{[^}]*display:\s*flex;")
        self.assertRegex(body, r"(?s)\.js\s+\.nav-toggle\s*\{[^}]*display:\s*flex;")

    def test_focus_and_hidden_back_to_top_are_accessible(self):
        css = (PUBLIC / "assets" / "css" / "styles.css").read_text(encoding="utf-8")
        script = (PUBLIC / "assets" / "js" / "main.js").read_text(encoding="utf-8")
        root = re.search(r"(?s):root\s*\{(?P<body>.*?)\}", css)
        focus = re.search(r"(?s):focus-visible\s*\{(?P<body>.*?)\}", css)
        self.assertIsNotNone(root)
        self.assertIsNotNone(focus)
        colors = dict(re.findall(r"(--color-[\w-]+):\s*(#[0-9a-fA-F]{6})", root.group("body")))
        ring_tokens = re.findall(r"var\((--color-[\w-]+)\)|(#[0-9a-fA-F]{6})", focus.group("body"))
        ring_colors = [colors[token] if token else literal for token, literal in ring_tokens]

        def luminance(hex_color):
            channels = [int(hex_color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
            linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
            return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

        def contrast(first, second):
            high, low = sorted((luminance(first), luminance(second)), reverse=True)
            return (high + 0.05) / (low + 0.05)

        self.assertGreaterEqual(len(set(ring_colors)), 2)
        for background in ("--color-paper", "--color-ink", "--color-brand"):
            with self.subTest(background=background):
                self.assertGreaterEqual(max(contrast(ring, colors[background]) for ring in ring_colors), 3)
        self.assertRegex(css, r"(?s)\.back-to-top\s*\{[^}]*visibility:\s*hidden;")
        self.assertRegex(css, r"(?s)\.back-to-top\.is-visible\s*\{[^}]*visibility:\s*visible;")
        self.assertIn('backToTop?.toggleAttribute("aria-hidden", window.scrollY <= 520);', script)
        self.assertIn('tabIndex = isVisible ? 0 : -1;', script)
        self.assertIn('behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth"', script)

    def test_clean_route_server_resolves_public_pages(self):
        server_path = ROOT / "scripts" / "serve-static.py"
        spec = spec_from_file_location("serve_static", server_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        server = module.make_server(PUBLIC, "127.0.0.1", 0)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            for route in ("/", "/servicios", "/casos", "/tecnologias", "/contacto", "/privacidad"):
                with self.subTest(route=route), urlopen(f"http://127.0.0.1:{server.server_port}{route}") as response:
                    self.assertEqual(response.status, 200)
                    self.assertIn(b"<!DOCTYPE html>", response.read(100))
        finally:
            server.shutdown()
            thread.join()
            server.server_close()

    def test_local_asset_references_exist(self):
        for page in PAGES:
            for image in parse_page(page).images:
                src = image.get("src", "")
                if src and not src.startswith(("http://", "https://", "data:")):
                    self.assertTrue((PUBLIC / src).is_file(), f"{page}: missing {src}")


if __name__ == "__main__":
    unittest.main()
