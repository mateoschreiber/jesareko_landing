from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

PUBLIC = Path(__file__).resolve().parents[1] / "public"
STYLES = PUBLIC / "assets" / "css" / "styles.css"


def html(name):
    return (PUBLIC / name).read_text(encoding="utf-8")


class HtmlNode:
    def __init__(self, tag, attrs=None, parent=None):
        self.tag = tag
        self.attrs = dict(attrs or ())
        self.parent = parent
        self.content = []

    def has_class(self, name):
        return name in self.attrs.get("class", "").split()

    def children(self, tag=None, class_name=None):
        return [
            child for child in self.content
            if isinstance(child, HtmlNode)
            and (tag is None or child.tag == tag)
            and (class_name is None or child.has_class(class_name))
        ]

    def find_all(self, tag=None, class_name=None):
        matches = []
        for child in self.content:
            if not isinstance(child, HtmlNode):
                continue
            if (tag is None or child.tag == tag) and (class_name is None or child.has_class(class_name)):
                matches.append(child)
            matches.extend(child.find_all(tag, class_name))
        return matches

    def text(self):
        value = "".join(part.text() if isinstance(part, HtmlNode) else part for part in self.content)
        return " ".join(value.split())

    def ancestor(self, tag=None, class_name=None):
        node = self.parent
        while node:
            if (tag is None or node.tag == tag) and (class_name is None or node.has_class(class_name)):
                return node
            node = node.parent
        return None


class TreeParser(HTMLParser):
    VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self):
        super().__init__()
        self.root = HtmlNode("document")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = HtmlNode(tag, attrs, self.stack[-1])
        self.stack[-1].content.append(node)
        if tag not in self.VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].content.append(HtmlNode(tag, attrs, self.stack[-1]))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].content.append(data)


def parsed_html(name):
    parser = TreeParser()
    parser.feed(html(name))
    return parser.root


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

    def test_services_follows_customer_decision_contract(self):
        source = html("servicios.html")
        page = parsed_html("servicios.html")
        index = next(nav for nav in page.find_all("nav") if nav.attrs.get("aria-label") == "Rutas de servicio")
        route_links = index.find_all("a", "service-row__item")
        self.assertEqual([link.attrs.get("href") for link in route_links], ["#redes", "#seguridad", "#soporte"])

        details = page.find_all("section", "service-detail")
        self.assertEqual([detail.attrs.get("id") for detail in details], ["redes", "seguridad", "soporte"])
        self.assertLess(source.index('aria-label="Rutas de servicio"'), source.index('id="redes"'))

        for detail in details:
            service = detail.attrs["id"]
            with self.subTest(service=service):
                self.assertTrue({"service-detail", "editorial-grid"}.issubset(detail.attrs.get("class", "").split()))
                intros = detail.children("div", "service-detail__intro")
                scopes = detail.children("div", "service-detail__scope")
                self.assertEqual(len(intros), 1)
                self.assertEqual(len(scopes), 1)

                intro = intros[0]
                self.assertEqual(len(intro.children("span", "section-index")), 1)
                self.assertEqual(len(intro.children("h2")), 1)
                summaries = intro.children("p")
                self.assertEqual(len(summaries), 1)
                self.assertIn(len(re.findall(r"\b\w+\b", summaries[0].text())), range(20, 36))

                scope = scopes[0]
                self.assertEqual(len(scope.children("h3")), 1)
                lists = scope.children("ul")
                self.assertEqual(len(lists), 1)
                self.assertEqual(len(lists[0].children("li")), 4)
                notes = scope.children("p", "service-detail__note")
                self.assertTrue(any(note.text().lower().startswith("criterio t") for note in notes))
                contextual_links = [link for link in scope.children("a") if link.text() == "Consultar este servicio"]
                self.assertEqual(len(contextual_links), 1)
                self.assertEqual(contextual_links[0].attrs.get("href"), f"/contacto?servicio={service}")

        secondary_notes = page.find_all("p", "service-detail__note--secondary")
        self.assertEqual(len(secondary_notes), 1)
        secondary = secondary_notes[0]
        self.assertEqual(secondary.ancestor("section", "service-detail").attrs.get("id"), "soporte")
        self.assertIn("web", secondary.text().lower())
        self.assertIn("automatiz", secondary.text().lower())
        main = next(node for node in page.find_all("main") if node.attrs.get("id") == "inicio")
        remaining_main_text = main.text().lower().replace(secondary.text().lower(), "")
        self.assertNotRegex(remaining_main_text, r"\bweb\b|automatiz")

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

    def test_services_route_index_uses_single_container_contract(self):
        page = parsed_html("servicios.html")
        index = next(nav for nav in page.find_all("nav") if nav.attrs.get("aria-label") == "Rutas de servicio")
        self.assertIsNone(index.ancestor(class_name="container"))

    def test_cases_are_honestly_labeled(self):
        source = html("casos.html")
        page = parsed_html("casos.html")
        studies = page.find_all("article", "case-study")

        self.assertIn("Aplicaciones frecuentes", source)
        self.assertEqual(len(studies), 3)
        self.assertIn("escenarios de trabajo", source.lower())
        for study in studies:
            with self.subTest(case=study.text()):
                self.assertEqual(len(study.children("div", "case-study__media")), 1)
                bodies = study.children("div", "case-study__body")
                self.assertEqual(len(bodies), 1)
                body = bodies[0].text()
                for label in ("Situación", "Criterio", "Intervención"):
                    self.assertIn(label, body)

        for invented_proof in ("Resultado:", "%", "cliente:", "caso real"):
            with self.subTest(invented_proof=invented_proof):
                self.assertNotIn(invented_proof.lower(), source.lower())

    def test_cases_components_have_focused_styles(self):
        styles = STYLES.read_text(encoding="utf-8")
        for selector in (".case-study", ".case-study__media", ".case-study__body"):
            with self.subTest(selector=selector):
                self.assertRegex(styles, rf"(?m)^{re.escape(selector)}(?:,|\s*\{{)")
