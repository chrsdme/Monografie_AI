"""Teste simple pentru hook-ul de feedback Tally."""
import unittest
from urllib.parse import parse_qs, urlparse

from tools.feedback_hook import FORM_URL, feedback_url, on_page_markdown


class _File:
    def __init__(self, src_uri):
        self.src_uri = src_uri


class _Page:
    def __init__(self, src_uri, url):
        self.file = _File(src_uri)
        self.url = url


class FeedbackTests(unittest.TestCase):
    def setUp(self):
        self.cfg = {"site_url": "https://chrsdme.github.io/Monografie_AI/"}

    def test_url_encodes_original_page(self):
        original = "https://chrsdme.github.io/Monografie_AI/partea-2/08-rag-memorie-cunostinte/"
        target = feedback_url(original)
        self.assertTrue(target.startswith(FORM_URL + "?"))
        self.assertEqual(parse_qs(urlparse(target).query)["page"], [original])

    def test_append_to_chapter(self):
        p = _Page("partea-2/08-rag-memorie-cunostinte.md", "partea-2/08-rag-memorie-cunostinte/")
        result = on_page_markdown("# Textul capitolului\n", p, self.cfg, None)
        self.assertIn("# Textul capitolului", result)
        self.assertIn("tally.so/r/rDyV1M?page=", result)
        self.assertIn("Monografie_AI%2Fpartea-2%2F08-rag", result)
        self.assertIn('rel="noopener noreferrer"', result)

    def test_homepage_context(self):
        p = _Page("index.md", "")
        result = on_page_markdown("# Acasa", p, self.cfg, None)
        self.assertIn("page=https%3A%2F%2Fchrsdme.github.io%2FMonografie_AI%2F", result)

    def test_contribute_has_no_duplicate_footer(self):
        p = _Page("contribuie.md", "contribuie/")
        self.assertEqual(on_page_markdown("# Contribuie", p, self.cfg, None), "# Contribuie")

    def test_site_url_required(self):
        with self.assertRaises(ValueError):
            on_page_markdown("Continut", _Page("x.md", "x/"), {"site_url": ""}, None)


if __name__ == "__main__":
    unittest.main()
