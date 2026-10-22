"""Regression checks for published HTML links that bypass Markdown processing."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("linkaudit", ROOT / "tools/check_site_links.py")
linkaudit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(linkaudit)


class SiteLinkTests(unittest.TestCase):
    def test_raw_html_md_href_fails_and_pretty_route_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            site = Path(temp)
            (site / "index.html").write_text(
                '<a href="anexe/metoda-surse.md#history">History</a>', encoding="utf-8"
            )
            annex = site / "anexe/metoda-surse"
            annex.mkdir(parents=True)
            (annex / "index.html").write_text(
                '<h2 id="history">History</h2>', encoding="utf-8"
            )
            _, _, broken = linkaudit.audit(site)
            self.assertEqual(len(broken), 1)
            self.assertEqual(broken[0][2], "missing target")
            (site / "index.html").write_text(
                '<a href="anexe/metoda-surse/#history">History</a>', encoding="utf-8"
            )
            self.assertEqual(linkaudit.audit(site)[2], [])

    def test_missing_fragment_and_missing_image_are_reported(self):
        with tempfile.TemporaryDirectory() as temp:
            site = Path(temp)
            (site / "index.html").write_text(
                '<a href="#missing">missing</a><img src="missing.svg">'
                '<a href="https://example.org/ok">external</a>', encoding="utf-8"
            )
            problems = linkaudit.audit(site)[2]
            self.assertEqual({item[2] for item in problems}, {
                "missing fragment", "missing target"
            })

    def test_site_root_escape_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            site = Path(temp)
            (site / "index.html").write_text(
                '<a href="../../outside.html">escape</a>', encoding="utf-8"
            )
            self.assertEqual(linkaudit.audit(site)[2][0][2], "outside site root")


if __name__ == "__main__":
    unittest.main()
