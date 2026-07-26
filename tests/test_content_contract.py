from pathlib import Path
import re
import unittest

PUBLIC = Path(__file__).resolve().parents[1] / "public"
STYLES = PUBLIC / "assets" / "css" / "styles.css"


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
        hero = source[positions[0]:positions[1]]
        cases = source[positions[4]:positions[5]]
        self.assertEqual(hero.count("<p>"), 1)
        self.assertEqual(hero.count('class="btn btn--primary"'), 1)
        self.assertEqual(cases.count("<article>"), 3)
        self.assertIn('<p class="eyebrow">Encarnación · Itapúa</p>', hero)
        self.assertIn('width="1175" height="448"', hero)
        for forbidden in ("chip-list", "dashboard", "metric-grid", "metric-card", "service-card__icon"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)

    def test_homepage_components_have_focused_styles(self):
        styles = STYLES.read_text(encoding="utf-8")
        selectors = (
            ".hero__copy",
            ".hero__media",
            ".service-row",
            ".service-row__item",
            ".technology-proof",
            ".brand-list",
            ".process-section",
            ".process-list",
            ".case-preview",
            ".case-preview__grid",
            ".diagnostic-cta",
        )
        for selector in selectors:
            with self.subTest(selector=selector):
                self.assertRegex(styles, rf"(?m)^{re.escape(selector)}(?:,|\s*\{{)")
        self.assertRegex(styles, r"(?s)\.hero__media img\s*\{[^}]*height:\s*auto;")
        self.assertRegex(styles, r"(?s)\.hero__media\s*\{[^}]*aspect-ratio:\s*1175\s*/\s*448;")

    def test_services_has_three_decision_paths(self):
        source = html("servicios.html")
        for section in ("redes", "seguridad", "soporte"):
            self.assertIn(f'id="{section}"', source)
        self.assertNotIn("Incluye:</strong>", source)
        self.assertNotIn("Conviene cuando:</strong>", source)
        self.assertNotIn("Resultado:</strong>", source)

    def test_services_components_have_focused_styles(self):
        styles = STYLES.read_text(encoding="utf-8")
        for selector in (
            ".service-detail",
            ".service-detail__intro",
            ".service-detail__scope",
            ".service-detail__note",
        ):
            with self.subTest(selector=selector):
                self.assertRegex(styles, rf"(?m)^{re.escape(selector)}(?:,|\s*\{{)")
