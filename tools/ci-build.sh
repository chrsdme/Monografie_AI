#!/usr/bin/env bash
# Construieste si verifica toate formatele din sursa editoriala unica.
set -euo pipefail
cd "$(dirname "$0")/.."

python -m unittest discover -s tests -p "test_feedback_hook.py"
python -m unittest discover -s tests -p "test_tech_theme.py" -v
python -m unittest discover -s tests -p "test_site_links.py" -v
python -m unittest discover -s tests -p "test_studio.py" -v
python -m unittest discover -s tests -p "test_intent_crossrefs.py" -v
python -m unittest discover -s tests -p "test_release_archive.py" -v
python -m unittest discover -s tests -p "test_archive_pr_guard.py" -v
python -m unittest discover -s examples/agent_studies/tests -v

python tools/build.py --repo . --toc --wiki --pdf

pdf="Monografie_AI_De_la_Chat_la_Sisteme_Agentice.pdf"
published_pdf="wiki/downloads/$pdf"
mkdir -p wiki/downloads
cp "$pdf" "$published_pdf"

python - <<'PY'
from pathlib import Path
from pypdf import PdfReader
source = Path("Monografie_AI_De_la_Chat_la_Sisteme_Agentice.pdf")
target = Path("wiki/downloads/Monografie_AI_De_la_Chat_la_Sisteme_Agentice.pdf")
assert source.is_file() and source.stat().st_size > 50_000, "PDF lipsa sau prea mic"
assert target.read_bytes() == source.read_bytes(), "PDF-ul din wiki difera de cel generat"
reader = PdfReader(str(source))
pages = len(reader.pages)

# Previne pierderea tacuta a anexelor din PDF daca lipseste un rand gol Markdown.
def titles(items):
    for item in items:
        if isinstance(item, list):
            yield from titles(item)
        else:
            yield item.title

pdf_headings = list(titles(reader.outline))
for required in ("Anexa A.", "Anexa B.", "Anexa C.", "Anexa D.", "Anexa E.", "Bibliografie"):
    assert any(t.startswith(required) for t in pdf_headings), (
        f"Lipseste heading-ul PDF: {required}"
    )
print("PASS: anexele A-E si bibliografia sunt prezente in outline-ul PDF")
assert pages >= 20, f"PDF suspect: {pages} pagini"
print(f"PDF verificat: {pages} pagini, {source.stat().st_size} octeti")
PY

mkdocs build --strict

# Validate raw HTML URLs too; MkDocs strict does not rewrite/validate them.
python tools/check_site_links.py --site site

python - <<'PY'
from pathlib import Path
pdf = "Monografie_AI_De_la_Chat_la_Sisteme_Agentice.pdf"
site = Path("site")
assert (site / "index.html").exists(), "Lipseste pagina principala"
home_html = (site / "index.html").read_text(encoding="utf-8")
assert 'tech-hero' in home_html and 'tech-edition' in home_html, "Homepage Tech nu a fost randat"
assert 'stylesheets/tech.css' in home_html, "Stilul Tech nu este incarcat"
assert (site / "stylesheets/tech.css").exists(), "Fisierul CSS Tech lipseste"
print("PASS: homepage Tech, tema si panoul editiei curente")
assert (site / "anexe/sabloane/index.html").exists(), "Lipseste Anexa B"
assert (site / "anexe/evaluare/index.html").exists(), "Lipseste Anexa C"
assert (site / "downloads" / pdf).read_bytes() == Path(pdf).read_bytes(), "PDF-ul publicat difera de sursa"
print("PASS: MkDocs strict, anexe, homepage si PDF descarcabil")
PY

# Test real rendering in both palette modes. Previous text-only checks missed
# a broken Material logo and almost invisible headings in the light palette.
python - <<'PY'
from pathlib import Path
from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    try:
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto((Path("site") / "index.html").resolve().as_uri(), wait_until="domcontentloaded")
        assert page.locator(".md-header__button.md-logo svg").count() == 1, (
            "Logo-ul trebuie sa fie pictograma SVG Material, nu o imagine lipsa"
        )
        assert page.locator(".md-header__button.md-logo img").count() == 0, (
            "Logo-ul nu trebuie incarcat dintr-o cale de imagine inexistenta"
        )
        for scheme, background in (
            ("slate", "rgb(11, 16, 32)"),
            ("default", "rgb(234, 241, 250)"),
        ):
            page.evaluate(
                "(scheme) => document.body.setAttribute('data-md-color-scheme', scheme)",
                scheme,
            )
            actual = page.evaluate("getComputedStyle(document.body).backgroundColor")
            assert actual == background, (
                f"Fundalul MkDocs Tech pentru {scheme}: {actual} != {background}"
            )
            assert page.locator(".md-sidebar--primary").evaluate(
                "(el) => getComputedStyle(el).backgroundImage"
            ) != "none", f"Navigatia laterala nu este stilizata in modul {scheme}"
            expected_nav_title = {
                "slate": "rgb(16, 26, 45)",
                "default": "rgb(227, 237, 248)",
            }[scheme]
            nav_title_bg = page.locator(
                ".md-sidebar--primary .md-nav--primary > .md-nav__title"
            ).evaluate("(el) => getComputedStyle(el).backgroundColor")
            assert nav_title_bg == expected_nav_title, (
                f"Sticky sidebar title must be opaque in {scheme}: {nav_title_bg}"
            )
        page.evaluate(
            "() => document.body.setAttribute('data-md-color-scheme', 'default')"
        )
        heading_color = page.locator(".tech-section-heading h2").first.evaluate(
            "(el) => getComputedStyle(el).color"
        )
        assert heading_color == "rgb(20, 40, 66)", (
            f"Contrast insuficient pentru titlurile Tech in light mode: {heading_color}"
        )

        # Render actual collection pages, not only the homepage. These checks
        # prevent invisible secondary buttons and literal :material-...: labels.
        import re

        def luminance(css_color):
            match = re.search(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", css_color)
            assert match, f"Expected RGB color, got {css_color}"
            channels = [int(match.group(i)) / 255 for i in (1, 2, 3)]
            linear = [x / 12.92 if x <= 0.04045
                      else ((x + 0.055) / 1.055) ** 2.4 for x in channels]
            return sum(weight * value for weight, value in zip(
                (0.2126, 0.7152, 0.0722), linear))

        def contrast(first, second):
            low, high = sorted((luminance(first), luminance(second)))
            return (high + 0.05) / (low + 0.05)

        for relative in (
            "colectii/resurse/index.html",
            "colectii/orchestrare-multi-agent/index.html",
            "colectii/experimente/index.html",
            "colectii/fb-ai-romania/index.html",
        ):
            page.goto((Path("site") / relative).resolve().as_uri(),
                      wait_until="domcontentloaded")
            buttons = page.locator(".md-typeset a.md-button")
            assert buttons.count() >= 1, f"No rendered actions on {relative}"
            assert ":material-" not in page.locator(".md-content").inner_text(), (
                f"Unrendered icon markup on {relative}")
            for scheme in ("slate", "default"):
                page.evaluate(
                    "scheme => document.body.setAttribute('data-md-color-scheme', scheme)",
                    scheme,
                )
                for index in range(buttons.count()):
                    button = buttons.nth(index)
                    label = button.inner_text().strip()
                    assert label and ":material" not in label, (
                        f"Invalid action label: {label!r}")
                    colors = button.evaluate(
                        "el => { const c = getComputedStyle(el); "
                        "return [c.color, c.backgroundColor] }")
                    assert contrast(*colors) >= 4.5, (
                        f"Unreadable button on {relative} / {scheme}: {label!r}, "
                        f"foreground {colors[0]}, background {colors[1]}, "
                        f"contrast {contrast(*colors):.2f}")
                    button.hover()
                    colors = button.evaluate(
                        "el => { const c = getComputedStyle(el); "
                        "return [c.color, c.backgroundColor] }")
                    assert contrast(*colors) >= 4.5, (
                        f"Unreadable hover state on {relative} / {scheme}: {label!r}")
                background = page.evaluate(
                    "getComputedStyle(document.body).backgroundColor")
                text_links = page.locator(
                    ".md-typeset p a:not(.md-button):not(.headerlink)")
                for index in range(text_links.count()):
                    link = text_links.nth(index)
                    foreground = link.evaluate(
                        "el => getComputedStyle(el).color")
                    assert contrast(foreground, background) >= 4.5, (
                        f"Unreadable link on {relative} / {scheme}: "
                        f"{link.inner_text().strip()!r}")
                if relative in (
                    "colectii/resurse/index.html",
                    "colectii/orchestrare-multi-agent/index.html",
                ):
                    out = Path("ui-preview")
                    out.mkdir(exist_ok=True)
                    name = relative.split("/")[1]
                    page.screenshot(
                        path=str(out / f"{name}-{scheme}.png"), full_page=True)
            page.set_viewport_size({"width": 390, "height": 844})
            for index in range(buttons.count()):
                bounds = buttons.nth(index).bounding_box()
                assert bounds and 0 < bounds["width"] <= 390, (
                    f"Mobile button overflow on {relative}: {bounds}")
            page.set_viewport_size({"width": 1440, "height": 900})
        print("PASS: collection links and actions in light/dark, hover and mobile")

        print("PASS: browser render - logo SVG, dark/light shell si contrast")
    finally:
        browser.close()
PY
