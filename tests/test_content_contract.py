from pathlib import Path
import unittest

PUBLIC = Path(__file__).resolve().parents[1] / "public"


def html(name):
    return (PUBLIC / name).read_text(encoding="utf-8")


class ContentContractTests(unittest.TestCase):
    def test_public_pages_exist(self):
        for page in ("index.html", "servicios.html", "casos.html", "tecnologias.html", "contacto.html", "privacidad.html"):
            with self.subTest(page=page):
                self.assertTrue((PUBLIC / page).is_file())

    def test_primary_conversion_is_whatsapp(self):
        for page in ("index.html", "servicios.html", "casos.html", "tecnologias.html", "contacto.html"):
            with self.subTest(page=page):
                self.assertIn("https://wa.me/595971141032", html(page))

    def test_homepage_follows_approved_narrative(self):
        source = html("index.html")
        positions = [source.index(f'id="{section}"') for section in ("hero", "areas", "evidence", "process", "cases", "diagnostic")]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(source.count('class="service-row__item"'), 3)
        self.assertIn("Infraestructura clara. Sistemas que funcionan.", source)
        self.assertIn("Encarnación", source)
