# Jesareko Home Mobile-First Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Convert only the Home into a mobile-first technical infrastructure landing page with coherent local imagery and measured browser performance.

**Architecture:** Retain static HTML, CSS and JavaScript. Add a home-page root to the Home and scope every new selector below it with home-* classes. Use CSS for all visual states and only use the existing IntersectionObserver mechanism to trigger optional, finite motion.

**Tech Stack:** Static HTML, CSS custom properties, vanilla JavaScript, generated local raster images, Python unittest, Node checks, browser DevTools/Lighthouse.

## Global Constraints

- Change visual content only in public/index.html; new styles are exclusively .home-page .home-*.
- Preserve URLs, IDs, semantic headings, CTA/WhatsApp links, global visual identity and all other page output.
- Generate four local assets with one documentary-commercial photographic direction; no text, logos, brands, people as subject, cyberpunk or generic stock style.
- Hero photo has meaningful alt text, fetchpriority=high and no lazy loading. Redundant service photos use alt="", declared dimensions and lazy loading.
- Controls are at least 48 × 48 CSS px; WCAG 2.2 AA is the compliance floor.
- Fast interactions run 160–220 ms. Ambient topology motion runs once and retains a static final state; all non-essential motion is removed under reduced motion.
- Test named widths, adjacent intermediate widths, and a 25 px continuous sweep. Measure actual DevTools/Lighthouse LCP and CLS before reporting performance.
- Do not add dependencies, remote production assets, CSS overflow masking, invented claims, or visual changes outside /.

---

### Task 1: Lock Home-only markup and asset contracts

**Files:**
- Modify: public/index.html:118-133
- Modify: tests/test_content_contract.py
- Modify: tests/test_site_contract.py

**Interfaces:**
- Consumes: existing hero, service-row, technology-proof and service anchor destinations.
- Produces: .home-page, .home-hero, .home-services, .home-service-card, .home-technology and four local image references.

- [ ] **Step 1: Add failing Home contract tests**

~~~python
def test_home_visual_components_are_scoped_and_use_local_assets(self):
    source = html("index.html")
    self.assertIn('<main id="mainContent" class="home-page">', source)
    for token in ("home-hero", "home-services", "home-service-card", "home-technology"):
        self.assertIn(token, source)
    for asset in ("home-hero-infrastructure", "home-service-networks", "home-service-security", "home-service-support"):
        self.assertIn(f"assets/img/{asset}", source)
    self.assertIn('fetchpriority="high"', source)
    self.assertIn('loading="lazy"', source)
    self.assertIn('alt=""', source)
~~~

- [ ] **Step 2: Run the focused test and verify failure**

Run: python -m unittest tests.test_content_contract.ContentContractTests.test_home_visual_components_are_scoped_and_use_local_assets -v

Expected: FAIL because the Home-only root, classes and four images are absent.

- [ ] **Step 3: Update the semantic Home only**

~~~html
<main id="mainContent" class="home-page">
  <section class="hero editorial-grid home-hero" id="hero">…</section>
  <section class="service-row home-services" id="areas">
    <a class="service-row__item home-service-card" href="/servicios#redes">…</a>
  </section>
  <section class="technology-proof home-technology" id="evidence">…</section>
</main>
~~~

Keep every current ID, H1/H2/H3 order, link URL and existing global class. Add a decorative topology wrapper with aria-hidden=true to home-technology; retain text equivalents of all capabilities.

- [ ] **Step 4: Generate and record the series**

Use built-in image generation for four separate images sharing: photorealistic documentary commercial photography, orderly professional business infrastructure, natural softened daylight, low-saturation green and neutral gray, moderate depth of field, no readable text, no logos, no brands, no people as subject, no cyberpunk or futuristic data center. Subjects: wide rack with subtle CCTV for hero; structured cabling/switch/AP for networks; commercial entrance with dome camera for security; rack, documentation and tools without people for support.

Save selected local outputs as public/assets/img/home-hero-infrastructure.*, home-service-networks.*, home-service-security.*, and home-service-support.*. Add exact filename, dimensions, byte size, prompt, creation date and owned/generated basis in docs/image-sources.json under an owned_generated_images array.

- [ ] **Step 5: Insert intentional image semantics**

~~~html
<img src="assets/img/home-hero-infrastructure.webp"
  alt="Gabinete de red ordenado con patch panels, switches y una cámara de seguridad"
  width="1600" height="1000" fetchpriority="high" decoding="async">
<img src="assets/img/home-service-networks.webp"
  alt="" width="1600" height="1000" loading="lazy" decoding="async">
~~~

Use dimensions matching the generated files exactly. Give all three service photos alt="" because adjacent title and copy already supply their meaning.

- [ ] **Step 6: Verify Home and asset contracts**

Run: python -m unittest tests.test_content_contract.ContentContractTests.test_home_visual_components_are_scoped_and_use_local_assets tests.test_site_contract.SiteContractTests.test_images_have_alt_and_dimensions tests.test_site_contract.SiteContractTests.test_local_asset_references_exist -v

Expected: PASS.

- [ ] **Step 7: Commit markup and assets**

Run: git add public/index.html public/assets/img docs/image-sources.json tests && git commit -m "feat: add scoped home imagery"

### Task 2: Build mobile-first visual hierarchy and identity block

**Files:**
- Modify: public/assets/css/styles.css
- Modify: tests/test_site_contract.py

**Interfaces:**
- Consumes: Home-only markup and image classes from Task 1.
- Produces: no-leak Home surface styles, responsive service cards and a dark technology identity composition.

- [ ] **Step 1: Add failing CSS scope test**

~~~python
def test_home_visual_rules_are_root_scoped_and_mobile_first(self):
    css = (PUBLIC / "assets" / "css" / "styles.css").read_text(encoding="utf-8")
    for selector in (".home-page .home-hero", ".home-page .home-service-card", ".home-page .home-technology"):
        self.assertIn(selector, css)
    self.assertNotIn("\n.home-service-card {", css)
    self.assertIn("@media (min-width: 48rem)", css)
~~~

- [ ] **Step 2: Run focused test and confirm failure**

Run: python -m unittest tests.test_site_contract.SiteContractTests.test_home_visual_rules_are_root_scoped_and_mobile_first -v

Expected: FAIL before Home-only visual rules exist.

- [ ] **Step 3: Add scoped mobile baseline then additive grids**

~~~css
.home-page .home-services { display: grid; gap: var(--space-2); }
.home-page .home-service-card { min-width: 0; min-height: 48px; }
.home-page .home-technology { background: var(--color-brand-dark); color: var(--color-paper); }
@media (min-width: 48rem) {
  .home-page .home-services { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}
~~~

Mobile shows hero copy, CTA and full-width media in that order; all cards remain full-width with visible photo and directional affordance; technology content stays linear. At content-safe widths, make hero and technology two-column compositions and services three equivalent editorials. Use minmax(0, …), declared aspect ratios and object-fit: cover; never hide horizontal overflow.

Use home-technology as a composed dark signature: high-contrast heading, three textual capabilities, descriptive static state labels and decorative topology. Scope heading/color overrides under .home-page.

- [ ] **Step 4: Verify CSS contracts**

Run: python -m unittest tests.test_site_contract.SiteContractTests.test_home_visual_rules_are_root_scoped_and_mobile_first tests.test_site_contract.SiteContractTests.test_css_does_not_mask_layout_failures tests.test_site_contract.SiteContractTests.test_responsive_queries_are_consolidated -v

Expected: PASS.

- [ ] **Step 5: Commit surfaces**

Run: git add public/assets/css/styles.css tests/test_site_contract.py && git commit -m "feat: add mobile-first home hierarchy"

### Task 3: Separate fast feedback from finite ambient movement

**Files:**
- Modify: public/assets/css/styles.css
- Modify: public/assets/js/main.js
- Modify: tests/test_site_contract.py

**Interfaces:**
- Consumes: .home-service-card, .home-technology and existing reducedMotion.
- Produces: hover/focus response and one-time ambient topology state without hiding content.

- [ ] **Step 1: Add failing movement contract**

~~~python
def test_home_motion_is_scoped_finite_and_reduced_motion_safe(self):
    css = (PUBLIC / "assets" / "css" / "styles.css").read_text(encoding="utf-8")
    self.assertIn(".home-page .home-service-card:hover", css)
    self.assertIn("animation-iteration-count: 1", css)
    self.assertIn("@media (prefers-reduced-motion: reduce)", css)
    self.assertNotIn("animation: home-network-pulse 2s infinite", css)
~~~

- [ ] **Step 2: Run test and verify failure**

Run: python -m unittest tests.test_site_contract.SiteContractTests.test_home_motion_is_scoped_finite_and_reduced_motion_safe -v

Expected: FAIL because no scoped Home feedback or finite ambient animation exists.

- [ ] **Step 3: Implement the two motion classes**

~~~css
@media (hover: hover) and (prefers-reduced-motion: no-preference) {
  .home-page .home-service-card:hover { transform: translateY(-3px); }
  .home-page .home-service-card:hover .home-service-card__media img { transform: scale(1.04); }
}
.home-page .home-technology.is-ambient-ready .home-topology__node--active {
  animation: home-network-pulse 2.4s ease-out 1 both;
  animation-iteration-count: 1;
}
~~~

Use the existing IntersectionObserver pattern to add is-ambient-ready once to the technology block only when motion is allowed. The final keyframe is the static visual state; no infinite loop. Keep all reveal targets visibly rendered before JavaScript runs.

- [ ] **Step 4: Verify behavior contracts**

Run: python -m unittest tests.test_site_contract.SiteContractTests.test_home_motion_is_scoped_finite_and_reduced_motion_safe tests.test_site_contract.SiteContractTests.test_reveal_animation_does_not_hide_content_before_intersection -v; node tests/nav-menu-runtime.mjs; node tests/contact-query-runtime.mjs; node --check public/assets/js/main.js

Expected: all commands return zero.

- [ ] **Step 5: Commit interactions**

Run: git add public/assets/css/styles.css public/assets/js/main.js tests/test_site_contract.py && git commit -m "feat: add restrained home motion"

### Task 4: Browser, responsive and performance evidence

**Files:**
- Create: docs/verification/2026-09-13-home-before-*.png
- Create: docs/verification/2026-09-13-home-after-*.png
- Modify only the scoped Home files when a browser finding identifies a defect.

**Interfaces:**
- Consumes: completed HTML, CSS, JS and local image assets.
- Produces: screenshots and real browser validation evidence.

- [ ] **Step 1: Capture visual evidence with a local static server**

Run: python scripts/serve-static.py --port 4173

Use a dedicated local browser tab/profile. Capture full-page before/after images at the named mobile, tablet and desktop widths.

- [ ] **Step 2: Check named and intermediate widths**

At 320, 360, 375, 390, 414, 430, 600, 767, 768, 820, 1023, 1024, 1100, 1280, 1366, 1440, 1920 and 2560 CSS px, confirm document.documentElement.scrollWidth <= window.innerWidth, intact headings, visible images/cards/CTA and no compression. Sweep each 25 px from 320 through 1440 and fix the responsible scoped CSS rule for every observed overflow or abrupt transition.

- [ ] **Step 3: Validate behavior and accessibility in DevTools**

Inspect DOM and accessibility tree for one H1, ordered headings, hero alt, three empty service alts, named links, 48 px card target, focus order, keyboard navigation, Escape menu behavior and reduced motion. Test service/CTA links, hover/focus state, console and network; resolve every new error, warning or failed asset.

- [ ] **Step 4: Measure actual Core Web Vitals**

With cache disabled, run a Performance trace or Lighthouse on fresh local mobile and desktop loads. Record actual LCP element/timing and CLS. Confirm hero is intended LCP and that responsive image loading causes no observable layout shift. If the trace finds a Home regression, reduce asset cost or correct reservation/loading, then rerun the trace; do not infer success only from HTML attributes.

- [ ] **Step 5: Run full suite and review diff**

Run: python -m unittest discover -s tests -v; node tests/nav-menu-runtime.mjs; node tests/contact-query-runtime.mjs; node --check public/assets/js/main.js; git diff --check

Expected: all commands exit zero.

- [ ] **Step 6: Commit verified output**

Run: git add public/index.html public/assets/css/styles.css public/assets/js/main.js public/assets/img docs/image-sources.json docs/verification tests && git commit -m "test: verify mobile-first home"

## Plan Self-Review

| Requirement | Task |
| --- | --- |
| Home root and isolated CSS | 1–2 |
| Four aligned generated photographs and alt policy | 1 |
| Mobile-first hero, services and dark identity | 2 |
| Fast vs finite ambient motion | 3 |
| Intermediate and continuous responsive validation | 4 |
| Real DevTools/Lighthouse LCP and CLS | 4 |
| Existing test and route regression validation | 1–4 |
