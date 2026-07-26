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
