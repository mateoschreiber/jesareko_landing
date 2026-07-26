from html.parser import HTMLParser
from pathlib import Path
import json
import unittest

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
        self.class_tokens = set()
        self.dialog_count = 0
        self.selects = []
        self.navs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.class_tokens.update(attrs.get("class", "").split())
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "h1":
            self.h1_count += 1
        if tag == "img":
            self.images.append(attrs)
        if tag == "a":
            self.links.append(attrs)
        if tag == "dialog":
            self.dialog_count += 1
        if tag == "select":
            self.selects.append(attrs)
        if tag == "nav":
            self.navs.append(attrs)


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


if __name__ == "__main__":
    unittest.main()
