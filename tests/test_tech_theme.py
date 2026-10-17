"""Regression checks for the Tech MkDocs homepage.
No editorial Markdown, chapter content or PDF generator is changed by this theme.
"""
from html.parser import HTMLParser
from pathlib import Path
import importlib.util
import re
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "wiki/index.md"
CSS = ROOT / "wiki/stylesheets/tech.css"
SITE = "https://chrsdme.github.io/Monografie_AI/"


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.classes = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            self.hrefs.append(attrs["href"])
        if "class" in attrs:
            self.classes.extend(attrs["class"].split())


class TechThemeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home = HOME.read_text(encoding="utf-8")
        cls.css = CSS.read_text(encoding="utf-8")
        cls.parser = PageLinks()
        cls.parser.feed(cls.home)

    def test_all_local_cards_have_targets(self):
        for href in self.parser.hrefs:
            if href.startswith(("https://", "http://", "mailto:", "#")):
                continue
            self.assertNotIn("..", href, "Home links must not escape docs root")
            dest, _, fragment = href.partition("#")
            if dest.startswith("downloads/"):
                self.assertEqual(dest, "downloads/Monografie_AI_De_la_Chat_la_Sisteme_Agentice.pdf")
                continue
            if dest.endswith("/"):
                target = ROOT / "wiki" / dest / "index.md"
                if not target.is_file():
                    target = ROOT / "wiki" / (dest.rstrip("/") + ".md")
            else:
                target = ROOT / "wiki" / dest
            self.assertTrue(target.is_file(), "Broken homepage link: " + href)
            if fragment:
                text = target.read_text(encoding="utf-8")
                import sys
                sys.path.insert(0, str(ROOT / "tools"))
                from build import gh_anchor
                headings = re.findall(r"^#{1,6}\s+(.+)$", text, re.M)
                self.assertIn(fragment, [gh_anchor(h) for h in headings], href)

    def test_home_uses_all_major_sections(self):
        classes = set(self.parser.classes)
        for name in ("tech-hero", "tech-system", "tech-metrics", "tech-feature-grid",
                     "tech-path", "tech-practice-grid", "tech-community"):
            self.assertIn(name, classes)
        self.assertEqual(self.home.count("<!-- MONOGRAFIE:START -->"), 1)
        self.assertEqual(self.home.count("<!-- MONOGRAFIE:END -->"), 1)
        self.assertEqual(self.home.count('class="tech-feature"'), 3)
        self.assertEqual(self.home.count('class="tech-practice"'), 3)

    def test_live_edition_block_stays_dynamic(self):
        spec = importlib.util.spec_from_file_location("book_builder", ROOT / "tools/build.py")
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        sample = {"edition": "9.5.1", "date": "1 decembrie 2030",
                  "author": "Autor Test", "license": "MIT",
                  "previous_edition": "9.5", "changelog_anchor": "test-editie",
                  "source": "https://github.com/example/test"}
        block = builder.index_block(sample)
        for text in ("Editia 9.5.1", "1 decembrie 2030", "fata de editia 9.5",
                     "anexe/metoda-surse.md#test-editie", "Descarca PDF-ul curent",
                     "Arhiva editiilor PDF"):
            self.assertIn(text, block)
        self.assertIn("\n<section", block)
        self.assertIn("</section>\n<!-- MONOGRAFIE:END -->", block)

    def test_mkdocs_uses_native_search_and_stylesheet(self):
        conf = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        self.assertEqual(conf["theme"]["name"], "material")
        self.assertEqual(conf["theme"]["palette"][0]["scheme"], "slate")
        self.assertIn("stylesheets/tech.css", conf["extra_css"])
        self.assertTrue(any("search" in p for p in conf["plugins"]))
        self.assertIn("tools/feedback_hook.py", conf["hooks"])

    def test_mobile_and_motion_accessibility(self):
        self.assertIn("@media (max-width: 760px)", self.css)
        self.assertIn("@media (max-width: 430px)", self.css)
        self.assertIn("prefers-reduced-motion: reduce", self.css)
        self.assertIn(":focus-visible", self.css)
        self.assertIn('role="img"', self.home)
        self.assertIn("aria-label=", self.home)


if __name__ == "__main__":
    unittest.main()
