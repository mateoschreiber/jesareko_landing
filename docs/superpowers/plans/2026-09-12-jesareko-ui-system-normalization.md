# Jesareko UI System Normalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Normalize the static site's visual system so every public route uses the same responsive layout, header contract, typography, controls, and accessibility behavior.

**Architecture:** Keep the existing HTML, routes, SEO, contact integration, and single CSS entry point. Establish semantic CSS tokens and shared primitives in `styles.css`, then simplify the existing page blocks to consume them; JavaScript remains behavioral only and must not be used for layout.

**Tech Stack:** Static HTML, CSS custom properties, vanilla JavaScript, Python `unittest`, Node runtime tests, Playwright CLI for local visual QA.

## Global Constraints

- Preserve Jesareko's existing green, Inter/Merriweather pairing, copy, routes, SEO metadata, contact flow, WhatsApp links, and source registry controls.
- Do not add a framework, UI library, build system, deployment, commit, or push.
- Keep a single global stylesheet and use CSS Grid/Flex for layout.
- Validate all six public routes at 360x800, 390x844, 430x932, 768x1024, 1024x768, 1280x800, 1366x768, 1440x900, 1920x1080, and 2560x1440.

---

### Task 1: Lock the shared layout contract

**Files:**
- Modify: `tests/test_site_contract.py`
- Modify: `public/assets/css/styles.css`

**Interfaces:**
- Consumes: `.container`, `.site-header`, `.site-nav`, and `.service-detail`.
- Produces: `--header-height`, `--container-max`, `--page-gutter`, and global anchor/focus clearance.

- [ ] **Step 1: Write the failing test**

```python
def test_shared_layout_contract_exposes_header_and_container_tokens(self):
    css = (PUBLIC / "assets" / "css" / "styles.css").read_text(encoding="utf-8")
    for token in ("--header-height", "--container-max", "--page-gutter"):
        self.assertIn(token, css)
    self.assertIn("scroll-padding-top: var(--header-height)", css)
    self.assertNotIn("scroll-margin-top: 6rem", css)
```

- [ ] **Step 2: Run the focused test and verify it fails**

Run: `python -m unittest tests.test_site_contract.SiteContractTests.test_shared_layout_contract_exposes_header_and_container_tokens -v`

Expected: fail because the header and container tokens are not yet defined.

- [ ] **Step 3: Implement the shared CSS contract**

Define header height, responsive gutters, container width, and layer tokens in `:root`; apply them to `.container`, `.site-header`, `html`, anchors, and skip-link focus behavior. Remove `6rem` anchor compensation from page-specific rules.

- [ ] **Step 4: Run the focused test and verify it passes**

Run: `python -m unittest tests.test_site_contract.SiteContractTests.test_shared_layout_contract_exposes_header_and_container_tokens -v`

Expected: pass.

### Task 2: Normalize visual primitives and controls

**Files:**
- Modify: `tests/test_site_contract.py`
- Modify: `public/assets/css/styles.css`

**Interfaces:**
- Consumes: tokens from Task 1.
- Produces: semantic typography, section, button, surface, form-control, transition, and focus primitives used by all pages.

- [ ] **Step 1: Write the failing test**

```python
def test_visual_system_has_semantic_control_tokens(self):
    css = (PUBLIC / "assets" / "css" / "styles.css").read_text(encoding="utf-8")
    for token in ("--color-focus", "--color-error", "--control-height", "--transition-fast"):
        self.assertIn(token, css)
    self.assertNotIn("border-color: #aa342d !important", css)
```

- [ ] **Step 2: Run the focused test and verify it fails**

Run: `python -m unittest tests.test_site_contract.SiteContractTests.test_visual_system_has_semantic_control_tokens -v`

Expected: fail because semantic control tokens and the non-`!important` error style are absent.

- [ ] **Step 3: Implement the primitives**

Expand the token scale and make `.btn`, `.contact-form`, `.contact-points`, `.technology-capability`, form fields, focus rings, and error states consume it. Preserve class names and contact behavior.

- [ ] **Step 4: Run the focused test and verify it passes**

Run: `python -m unittest tests.test_site_contract.SiteContractTests.test_visual_system_has_semantic_control_tokens -v`

Expected: pass.

### Task 3: Remove layout-dependent content hiding

**Files:**
- Modify: `tests/test_site_contract.py`
- Modify: `public/assets/css/styles.css`

**Interfaces:**
- Consumes: `.reveal-item` classes added by `main.js`.
- Produces: non-essential motion that cannot hide content when JavaScript, intersection timing, or snapshots behave differently.

- [ ] **Step 1: Write the failing test**

```python
def test_reveal_animation_never_hides_content_before_intersection(self):
    css = (PUBLIC / "assets" / "css" / "styles.css").read_text(encoding="utf-8")
    reveal = re.search(r"(?ms)^\.js \.reveal-item\s*\{(?P<body>.*?)^\}", css)
    self.assertIsNotNone(reveal)
    self.assertNotRegex(reveal.group("body"), r"opacity:\s*0")
```

- [ ] **Step 2: Run the focused test and verify it fails**

Run: `python -m unittest tests.test_site_contract.SiteContractTests.test_reveal_animation_never_hides_content_before_intersection -v`

Expected: fail because the initial animation sets `opacity: 0`.

- [ ] **Step 3: Implement non-blocking motion**

Limit reveal styling to a small transform/transition when allowed, leaving content fully rendered before and after intersection. Retain the reduced-motion override.

- [ ] **Step 4: Run the focused test and verify it passes**

Run: `python -m unittest tests.test_site_contract.SiteContractTests.test_reveal_animation_never_hides_content_before_intersection -v`

Expected: pass.

### Task 4: Validate the site as one system

**Files:**
- Modify: `public/assets/css/styles.css`
- Test: `tests/test_site_contract.py`, `tests/test_content_contract.py`, `tests/nav-menu-runtime.mjs`, `tests/contact-query-runtime.mjs`

**Interfaces:**
- Consumes: Tasks 1-3.
- Produces: a visually consistent, responsive static site without layout-obscured focus or hidden critical content.

- [ ] **Step 1: Run automated contracts**

Run: `python -m unittest discover -s tests`, `node tests/nav-menu-runtime.mjs`, `node tests/contact-query-runtime.mjs`, `node --check public/assets/js/main.js`, and `git diff --check`.

Expected: all pass without output errors.

- [ ] **Step 2: Perform browser QA**

Capture each public route at the ten required viewport dimensions using the existing local server and Playwright CLI. Inspect each viewport for overlap, horizontal overflow, broken navigation, malformed controls, and visible focus.

- [ ] **Step 3: Review the final diff**

Confirm the stylesheet contains no page-specific header offsets, negative-margin hacks, `overflow-x: hidden`, redundant breakpoint copies, or unrelated functional changes.
