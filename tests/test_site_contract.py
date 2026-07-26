from html.parser import HTMLParser
from pathlib import Path
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

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "h1":
            self.h1_count += 1
        if tag == "img":
            self.images.append(attrs)
        if tag == "a":
            self.links.append(attrs)


def parse_page(name):
    parser = PageParser()
    parser.feed((PUBLIC / name).read_text(encoding="utf-8"))
    return parser


class SiteContractTests(unittest.TestCase):
    def test_every_page_uses_new_shared_shell(self):
        for page in PAGES:
            source = (PUBLIC / page).read_text(encoding="utf-8")
            with self.subTest(page=page):
                self.assertIn('class="site-nav"', source)
                self.assertIn('class="brand-lockup"', source)
                self.assertIn('class="site-footer"', source)
                self.assertIn('aria-controls="primaryMenu"', source)

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
