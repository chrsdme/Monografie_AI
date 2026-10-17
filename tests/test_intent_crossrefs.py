"""Tests for Intent Engineering wiki/PDF cross-references."""
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build import internalize_wiki_links_for_pdf

BASE = "https://chrsdme.github.io/Monografie_AI/"
LINKS = {
    "67-intent-engineering-de-la-cerere-la-obiectiv-verificabil": "wiki/partea-2/06-prompturi-instructiuni-briefuri.md",
    "217-studiul-de-caz-e-acelasi-retur-prin-trei-arhitecturi": "wiki/partea-5/21-studii-de-caz.md",
    "218-studiul-de-caz-f-cercetare-youtube-si-productie-editoriala-cu-doi-agenti": "wiki/partea-5/21-studii-de-caz.md",
    "b8-specificatie-de-intentie-de-la-obiectiv-la-verificare": "wiki/anexe/sabloane.md",
}

def mk_slug(title):
    return re.sub(r"[^a-z0-9 _-]", "", title.lower()).replace(" ", "-")

class CrossrefTests(unittest.TestCase):
    def test_targets_exist_in_wiki(self):
        for anchor, file in LINKS.items():
            titles = re.findall(r"^#{1,5} (.+)$", (ROOT/file).read_text(encoding="utf-8"), re.M)
            self.assertIn(anchor, {mk_slug(t) for t in titles}, file)

    def test_source_links_match_wiki_routes(self):
        source = (ROOT/"Monografie_AI_De_la_Chat_la_Sisteme_Agentice.md").read_text(encoding="utf-8")
        links = re.findall(r"\]\((https?://[^)]+)\)", source)
        found = set()
        for address in links:
            if not address.startswith(BASE) or "#" not in address:
                continue
            u = urlparse(address)
            if u.fragment not in LINKS:
                continue
            file = LINKS[u.fragment].removeprefix("wiki/").removesuffix(".md")
            self.assertEqual(u.path, "/Monografie_AI/" + file + "/")
            found.add(u.fragment)
        self.assertEqual(found, set(LINKS))

    def test_pdf_internalizes_existing_targets_only(self):
        target = next(iter(LINKS))
        link = BASE+"partea-2/06-prompturi-instructiuni-briefuri/#"+target
        doc = f'<h3 id="{target}">Title</h3><a href="{link}">Link</a>'
        self.assertIn('href="#'+target+'"', internalize_wiki_links_for_pdf(doc, BASE))
        self.assertIn(link, internalize_wiki_links_for_pdf(f'<a href="{link}">Link</a>', BASE))
        other = '<a href="https://example.org/foo">Outside</a>'
        self.assertEqual(other, internalize_wiki_links_for_pdf(other, BASE))

if __name__ == "__main__":
    unittest.main()
