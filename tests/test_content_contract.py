from html.parser import HTMLParser
from pathlib import Path
import json
import re
import subprocess
import unittest
from urllib.parse import unquote

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
    def test_contact_query_initialization_runtime_contract(self):
        runtime_test = Path(__file__).with_name("contact-query-runtime.mjs")
        result = subprocess.run(
            ["node", str(runtime_test)],
            cwd=PUBLIC.parent,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_public_pages_exist(self):
        for page in ("index.html", "servicios.html", "casos.html", "tecnologias.html", "contacto.html", "privacidad.html"):
            with self.subTest(page=page):
                self.assertTrue((PUBLIC / page).is_file())

    def test_primary_conversion_is_whatsapp(self):
        for page in ("index.html", "servicios.html", "casos.html", "tecnologias.html", "contacto.html"):
            with self.subTest(page=page):
                self.assertIn("https://wa.me/595971141032", html(page))

    def test_requested_camera_lineups_are_used_in_primary_visual_positions(self):
        homepage = parsed_html("index.html")
        hero = next(node for node in homepage.find_all("figure", "hero__media"))
        hero_image = hero.find_all("img")[0]
        self.assertEqual(hero_image.attrs.get("src"), "assets/img/brands/dahua-camera-lineup.webp")
        self.assertEqual((hero_image.attrs.get("width"), hero_image.attrs.get("height")), ("1600", "659"))

        technologies = parsed_html("tecnologias.html")
        hikvision_image = next(
            image for image in technologies.find_all("img")
            if image.attrs.get("src") == "assets/img/brands/hikvision-camera-lineup.webp"
        )
        self.assertEqual((hikvision_image.attrs.get("width"), hikvision_image.attrs.get("height")), ("1000", "347"))

        registry = json.loads((PUBLIC.parent / "docs" / "image-sources.json").read_text(encoding="utf-8"))
        records = {record["local_file"]: record for record in registry["images"]}
        for local_file in (
            "assets/img/brands/dahua-camera-lineup.webp",
            "assets/img/brands/hikvision-camera-lineup.webp",
        ):
            with self.subTest(local_file=local_file):
                self.assertEqual(records[local_file]["source_type"], "user_provided_upload")

        disclaimer = next(node for node in technologies.find_all("p", "asset-disclaimer")).text().lower()
        self.assertIn("aportado por el propietario del sitio", disclaimer)
        self.assertIn("referencias publicadas por fabricantes", disclaimer)
        self.assertNotIn("provienen de páginas oficiales", disclaimer)

    def test_contact_prioritizes_whatsapp_and_has_accessible_errors(self):
        source = html("contacto.html")
        page = parsed_html("contacto.html")
        form = next(node for node in page.find_all("form") if node.attrs.get("id") == "contactForm")

        self.assertIn('class="contact-primary ', source)
        self.assertLess(source.index('class="contact-primary '), source.index('id="contactForm"'))
        self.assertLess(source.index('id="sendWhatsApp"'), source.index('id="sendEmail"'))
        phone_links = [link for link in page.find_all("a", "contact-phone") if link.attrs.get("href") == "tel:+595971141032"]
        self.assertEqual(len(phone_links), 1)
        phone = phone_links[0]
        self.assertEqual(phone.text(), "+595 971 141 032")
        for field in ("name", "city", "service", "message"):
            with self.subTest(field=field):
                control = next(node for node in form.find_all() if node.attrs.get("id") == field)
                label = next(node for node in form.find_all("label") if node.attrs.get("for") == field)
                error = next(node for node in form.find_all() if node.attrs.get("data-error-for") == field)
                self.assertTrue(label.text())
                self.assertEqual(error.attrs.get("id"), f"{field}Error")
                self.assertEqual(control.attrs.get("aria-describedby"), None)
        status = next(node for node in form.find_all() if node.attrs.get("id") == "formStatus")
        self.assertEqual(status.attrs.get("role"), "status")
        self.assertEqual(status.attrs.get("aria-live"), "polite")

    def test_contact_form_uses_a_secure_same_origin_action_and_keeps_a_no_javascript_fallback(self):
        page = parsed_html("contacto.html")
        form = next(node for node in page.find_all("form") if node.attrs.get("id") == "contactForm")
        self.assertEqual(form.attrs.get("action"), "/contacto")
        self.assertEqual(form.attrs.get("method"), "post")
        self.assertEqual(form.attrs.get("enctype"), "text/plain")
        self.assertNotIn("novalidate", form.attrs)
        email_submit = next(node for node in form.find_all("button") if node.attrs.get("id") == "sendEmail")
        self.assertEqual(email_submit.attrs.get("type"), "submit")
        fallback = next(node for node in form.find_all("p", "no-js-fallback"))
        self.assertIn("mailto:alemateo07@gmail.com", [link.attrs.get("href") for link in fallback.find_all("a")])

    def test_email_destination_is_not_exposed_as_visible_page_copy(self):
        for page_name in ("index.html", "servicios.html", "casos.html", "tecnologias.html", "contacto.html", "privacidad.html"):
            with self.subTest(page=page_name):
                page = parsed_html(page_name)
                visible_regions = page.find_all("main") + page.find_all("footer")
                self.assertNotIn("alemateo07@gmail.com", " ".join(region.text() for region in visible_regions))

    def test_footer_is_reduced_to_three_compact_information_groups(self):
        for page_name in ("index.html", "servicios.html", "casos.html", "tecnologias.html", "contacto.html", "privacidad.html"):
            with self.subTest(page=page_name):
                footer = parsed_html(page_name).find_all("footer", "site-footer")[0]
                grid = footer.children("div", "footer-grid")[0]
                groups = [node for node in grid.content if isinstance(node, HtmlNode)]
                self.assertEqual(len(groups), 3)
                self.assertEqual([group.children("h2")[0].text() for group in groups[1:]], ["Explorar", "Contacto"])

    def test_global_whatsapp_calls_to_action_include_a_prefilled_message(self):
        for page_name in ("index.html", "servicios.html", "casos.html", "tecnologias.html", "contacto.html"):
            page = parsed_html(page_name)
            for link in page.find_all("a"):
                href = link.attrs.get("href", "")
                if href.startswith("https://wa.me/595971141032"):
                    with self.subTest(page=page_name, href=href):
                        self.assertIn("?text=", href)

    def test_contact_script_initializes_service_safely_and_links_errors(self):
        script = (PUBLIC / "assets" / "js" / "main.js").read_text(encoding="utf-8")
        initialization = re.search(
            r'const requestedService = new URLSearchParams\(window\.location\.search\)\.get\("servicio"\);\s*'
            r'if \(requestedService && ALLOWED_SERVICES\.has\(requestedService\)\) \{\s*'
            r'serviceSelect\.value = requestedService;\s*\}',
            script,
        )
        self.assertIsNotNone(initialization)
        self.assertNotIn("serviceAliases", script)
        self.assertEqual(script.count("serviceSelect.value ="), 1)

        cleanup = re.search(r"function clearFieldError\(fieldName\) \{(?P<body>.*?)\n  \}\n\n  function values", script, re.S)
        self.assertIsNotNone(cleanup)
        cleanup_body = cleanup.group("body")
        self.assertIn('removeAttribute("aria-invalid")', cleanup_body)
        self.assertIn('removeAttribute("aria-describedby")', cleanup_body)
        self.assertIn('setAttribute("aria-describedby", error.id)', script)

    def test_contact_service_queries_are_limited_to_allowed_select_values(self):
        allowed = {
            "Revisión técnica / diagnóstico",
            "Redes y WiFi",
            "CCTV, alarmas, accesos e incendio",
            "Soporte e infraestructura",
            "Web, monitoreo y automatización",
            "Otro",
        }
        values = []
        for page in PUBLIC.glob("*.html"):
            values.extend(unquote(value) for value in re.findall(r'href="[^"]*\?servicio=([^"&]+)', page.read_text(encoding="utf-8")))

        self.assertTrue(values)
        self.assertTrue(set(values).issubset(allowed), set(values) - allowed)

    def test_contact_phone_has_a_full_touch_target(self):
        styles = STYLES.read_text(encoding="utf-8")
        rule = re.search(r"(?s)\.contact-phone\s*\{(?P<body>[^}]*)\}", styles)
        self.assertIsNotNone(rule)
        self.assertRegex(rule.group("body"), r"display:\s*inline-flex;")
        self.assertRegex(rule.group("body"), r"min-height:\s*3rem;")

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
        self.assertRegex(styles, r"(?s)\.hero__media\s*\{[^}]*aspect-ratio:\s*1600\s*/\s*659;")

    def test_services_follows_customer_decision_contract(self):
        source = html("servicios.html")
        page = parsed_html("servicios.html")
        index = next(nav for nav in page.find_all("nav") if nav.attrs.get("aria-label") == "Rutas de servicio")
        route_links = index.find_all("a", "service-row__item")
        self.assertEqual([link.attrs.get("href") for link in route_links], ["#redes", "#seguridad", "#soporte"])

        details = page.find_all("section", "service-detail")
        self.assertEqual([detail.attrs.get("id") for detail in details], ["redes", "seguridad", "soporte"])
        self.assertLess(source.index('aria-label="Rutas de servicio"'), source.index('id="redes"'))

        contact_services = {
            "redes": "Redes%20y%20WiFi",
            "seguridad": "CCTV%2C%20alarmas%2C%20accesos%20e%20incendio",
            "soporte": "Soporte%20e%20infraestructura",
        }
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
                self.assertEqual(contextual_links[0].attrs.get("href"), f"/contacto?servicio={contact_services[service]}")

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
        self.assertIn("Presentamos estas aplicaciones como escenarios de trabajo, no como proyectos ejecutados.", source)
        self.assertEqual(
            [study.children("div", "case-study__body")[0].children("h2")[0].text() for study in studies],
            [
                "Comercio con puntos ciegos",
                "Vivienda con WiFi inestable",
                "Oficina con accesos y documentación dispersos",
            ],
        )
        for study in studies:
            with self.subTest(case=study.text()):
                self.assertEqual(len(study.children("div", "case-study__media")), 1)
                bodies = study.children("div", "case-study__body")
                self.assertEqual(len(bodies), 1)
                body = bodies[0].text()
                for label in ("Situación", "Criterio", "Intervención"):
                    self.assertIn(label, body)

        main_text = next(node for node in page.find_all("main")).text().lower()
        for invented_proof in ("Resultado:", "%", "cliente:", "caso real"):
            with self.subTest(invented_proof=invented_proof):
                self.assertNotIn(invented_proof.lower(), main_text)

    def test_cases_components_have_focused_styles(self):
        styles = STYLES.read_text(encoding="utf-8")
        for selector in (".case-study", ".case-study__media", ".case-study__body"):
            with self.subTest(selector=selector):
                self.assertRegex(styles, rf"(?m)^{re.escape(selector)}(?:,|\s*\{{)")
        study_rules = re.findall(r"(?ms)^[ \t]*\.case-study\s*\{(?P<body>.*?)^[ \t]*\}", styles)
        self.assertEqual(len(study_rules), 2)
        base = study_rules[0]
        self.assertRegex(base, r"grid-template-columns:\s*minmax\(0,\s*1fr\);")
        self.assertRegex(
            styles,
            r"(?s)@media\s*\(min-width:\s*48rem\).*?\.case-study\s*\{[^}]*grid-template-columns:\s*minmax\(9rem,\s*\.34fr\)\s+minmax\(0,\s*1fr\);",
        )
        case_component_rules = re.findall(r"(?ms)^[ \t]*\.case-study(?:__media|__body)?\s*\{(?P<body>.*?)^[ \t]*\}", styles)
        self.assertNotRegex("".join(case_component_rules), r"(?:min-|max-)?height\s*:|overflow(?:-x)?\s*:")

    def test_cases_metadata_describes_frequent_scenarios(self):
        source = html("casos.html")
        title = "Aplicaciones frecuentes de seguridad, WiFi y soporte | Jesareko"
        description = "Aplicaciones frecuentes de seguridad, WiFi y soporte técnico para comercios, viviendas y oficinas en Encarnación e Itapúa."
        self.assertIn(f"<title>{title}</title>", source)
        self.assertEqual(source.count(f'content="{title}"'), 2)
        self.assertEqual(source.count(f'content="{description}"'), 3)
        self.assertIn(f'"description": "{description}"', source)
        self.assertNotIn("resultados esperables", source.lower())

    def test_technologies_is_an_editorial_application_catalog(self):
        source = html("tecnologias.html")
        page = parsed_html("tecnologias.html")
        products = page.find_all("article", "product-editorial")

        self.assertEqual(len(products), 4)
        self.assertNotIn("product-ref-grid", source)
        self.assertNotIn("tech-grid", source)
        self.assertEqual(
            [product.children("div", "product-editorial__copy")[0].children("h2")[0].text() for product in products],
            [
                "Videovigilancia para cobertura útil.",
                "Alarmas que avisan cuando importa.",
                "Accesos con permisos y trazabilidad.",
                "Video y acceso como un solo sistema.",
            ],
        )
        self.assertEqual(
            [product.children("div", "product-editorial__copy")[0].children("span", "brand-wordmark")[0].text() for product in products],
            ["Hikvision", "Hikvision", "Dahua", "Dahua"],
        )
        for product in products:
            with self.subTest(product=product.text()):
                self.assertTrue({"product-editorial", "editorial-grid"}.issubset(product.attrs.get("class", "").split()))
                self.assertEqual(len(product.children("figure", "product-editorial__media")), 1)
                self.assertEqual(len(product.children("div", "product-editorial__copy")), 1)
                element_children = [child for child in product.content if isinstance(child, HtmlNode)]
                self.assertTrue(element_children[0].has_class("product-editorial__copy"))
                self.assertTrue(element_children[1].has_class("product-editorial__media"))

        for product in products:
            media = product.children("figure", "product-editorial__media")[0]
            self.assertEqual(media.attrs.get("class", "").split(), ["product-editorial__media"])

    def test_technologies_covers_networks_and_support_without_unshown_promises(self):
        source = html("tecnologias.html")
        page = parsed_html("tecnologias.html")
        capabilities = page.find_all("article", "technology-capability")
        self.assertEqual([capability.children("h2")[0].text() for capability in capabilities], ["Redes y WiFi", "Soporte técnico"])
        self.assertIn("cobertura", capabilities[0].text().lower())
        self.assertIn("documentación", capabilities[1].text().lower())
        for promise in ("detección de incendio", "monitoreo"):
            with self.subTest(promise=promise):
                self.assertNotIn(promise, source.lower())

    def test_image_source_registry_blocks_publication_without_redistribution_authorization(self):
        registry = (PUBLIC.parent / "docs" / "image-sources.json").read_text(encoding="utf-8")
        self.assertIn('"status": "blocked"', registry)
        self.assertIn('"redistribution_authorization": "unverified"', registry)

    def test_technologies_components_have_mobile_first_styles(self):
        styles = STYLES.read_text(encoding="utf-8")
        for selector in (
            ".product-editorial",
            ".product-editorial__media",
            ".product-editorial__copy",
            ".brand-wordmark",
        ):
            with self.subTest(selector=selector):
                self.assertRegex(styles, rf"(?m)^{re.escape(selector)}(?:,|\s*\{{)")
        base = re.search(r"(?ms)^\.product-editorial\s*\{(?P<body>.*?)^\}", styles)
        self.assertIsNotNone(base)
        self.assertRegex(base.group("body"), r"grid-template-columns:\s*minmax\(0,\s*1fr\);")
        self.assertRegex(
            styles,
            r"(?s)@media\s*\(min-width:\s*52\.01rem\).*?\.product-editorial\s*\{[^}]*grid-template-columns:\s*repeat\(2,\s*minmax\(0,\s*1fr\)\);",
        )

    def test_technology_media_uses_one_bounded_frame_for_every_aspect_ratio(self):
        styles = STYLES.read_text(encoding="utf-8")
        media = re.search(r"(?ms)^\.product-editorial__media\s*\{(?P<body>.*?)^\}", styles)
        image = re.search(r"(?ms)^\.product-editorial__media img\s*\{(?P<body>.*?)^\}", styles)
        self.assertIsNotNone(media)
        self.assertIsNotNone(image)
        self.assertRegex(media.group("body"), r"display:\s*flex;")
        self.assertRegex(media.group("body"), r"align-items:\s*center;")
        self.assertRegex(media.group("body"), r"justify-content:\s*center;")
        self.assertRegex(media.group("body"), r"height:\s*clamp\(13rem,\s*58vw,\s*20rem\);")
        self.assertRegex(media.group("body"), r"overflow:\s*hidden;")
        self.assertNotRegex(media.group("body"), r"aspect-ratio:")
        self.assertRegex(image.group("body"), r"width:\s*auto;")
        self.assertRegex(image.group("body"), r"max-width:\s*100%;")
        self.assertRegex(image.group("body"), r"height:\s*auto;")
        self.assertRegex(image.group("body"), r"max-height:\s*100%;")
        self.assertRegex(image.group("body"), r"object-fit:\s*contain;")

    def test_mobile_product_copy_precedes_its_matching_media(self):
        styles = STYLES.read_text(encoding="utf-8")
        media = re.search(r"(?ms)^\.product-editorial__media\s*\{(?P<body>.*?)^\}", styles)
        copy = re.search(r"(?ms)^\.product-editorial__copy\s*\{(?P<body>.*?)^\}", styles)
        self.assertRegex(media.group("body"), r"order:\s*2;")
        self.assertRegex(copy.group("body"), r"order:\s*1;")
        self.assertRegex(
            styles,
            r"(?s)@media\s*\(min-width:\s*52\.01rem\).*?\.product-editorial__media\s*\{[^}]*grid-column:\s*1;[^}]*grid-row:\s*1;",
        )
        self.assertRegex(
            styles,
            r"(?s)@media\s*\(min-width:\s*52\.01rem\).*?\.product-editorial__copy\s*\{[^}]*grid-column:\s*2;[^}]*grid-row:\s*1;",
        )
