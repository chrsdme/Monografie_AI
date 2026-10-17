"""Regresii ale schemei automate de editii si arhiva PDF."""
import importlib.util
import pathlib
import re
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

def module(file, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

release = module("release.py", "release_module")
archiver = module("archive_pdf.py", "archive_module")
builder = module("build.py", "build_module")


class ReleaseTests(unittest.TestCase):
    def test_patch_sequence(self):
        self.assertEqual(release.next_patch("1.2"), "1.2.1")
        self.assertEqual(release.next_patch("1.2.1"), "1.2.2")
        with self.assertRaises(ValueError):
            release.next_patch("1.2.rc1")

    def test_updates_all_editorial_locations_and_preserves_history(self):
        raw = (ROOT / archiver.STEM).with_suffix(".md").read_text(encoding="utf-8")
        old = release.field(raw, "edition")
        version = release.next_patch(old)
        previous_headings = re.findall(r"^## E\.\d+\..+$", raw, re.M)
        section_number = max((int(n) for n in re.findall(r"^## E\.(\d+)\.", raw, re.M)), default=0) + 1
        heading = f"## E.{section_number}. Modificari de la editia {old} la {version}"
        output = release.update_text(
            raw, old, version, "18 octombrie 2026",
            [archiver.STEM + ".md", "wiki/despre.md"], "Explica actualizari", "abc123456789")
        self.assertIn('edition: "' + version + '"', output)
        self.assertIn(heading, output)
        self.assertIn("**Editia curenta:** " + version, output)
        self.assertIn("Sfarsitul editiei " + version, output)
        self.assertIn("## E.2. Changelog 1.0 la 1.1", output)
        for old_heading in previous_headings:
            self.assertIn(old_heading, output)
        self.assertEqual(output.count(heading), 1)

    def test_homepage_block_follows_current_edition(self):
        raw = (ROOT / archiver.STEM).with_suffix(".md").read_text(encoding="utf-8")
        fm = {key: release.field(raw, key) for key in
              ("edition", "date", "author", "previous_edition",
               "changelog_anchor", "license", "source")}
        block = builder.index_block(fm)
        self.assertIn("Editia " + fm["edition"] + ", " + fm["date"], block)
        self.assertIn("fata de editia " + fm["previous_edition"], block)
        self.assertIn("#" + fm["changelog_anchor"], block)
        self.assertIn("Descarca PDF-ul curent", block)
        self.assertIn("Arhiva editiilor PDF", block)
        self.assertNotIn("#e2-changelog-10-la-11", block)
        with tempfile.TemporaryDirectory() as tmp:
            repo = pathlib.Path(tmp)
            wiki = repo / "wiki"
            wiki.mkdir()
            index = wiki / "index.md"
            index.write_text("# Acasa\n\n<!-- MONOGRAFIE:START -->\nVechi\n"
                             "<!-- MONOGRAFIE:END -->\n", encoding="utf-8")
            builder.merge_index(wiki, fm)
            self.assertIn(block, index.read_text(encoding="utf-8"))

    def test_explicit_edition_gets_actual_publication_date(self):
        raw = (ROOT / archiver.STEM).with_suffix(".md").read_text(encoding="utf-8")
        edition = release.field(raw, "edition")
        updated = release.refresh_current_date(raw, edition, "18 octombrie 2026")
        self.assertIn('date: "18 octombrie 2026"', updated)
        self.assertIn("**Editia curenta:** " + edition + ", 18 octombrie 2026", updated)
        self.assertIn("editia " + edition + ", 18 octombrie 2026,", updated)
        self.assertIn("*Editia " + edition + " | 18 octombrie 2026 |", updated)
        self.assertIn("## E.2. Changelog 1.0 la 1.1", updated)

    def test_archive_idempotence_and_immutability(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = pathlib.Path(tmp)
            (repo / (archiver.STEM + ".md")).write_text('edition: "1.2"\n', encoding="utf-8")
            pdf = repo / (archiver.STEM + ".pdf")
            pdf.write_bytes(b"a" * 52000)
            archiver.archive(repo)
            archived = repo / "docs" / (archiver.STEM + "_1.2.pdf")
            self.assertTrue(archived.exists())
            self.assertIn("Editia 1.2", (repo / "docs/README.md").read_text())
            self.assertEqual(__import__("json").loads((repo / "docs/.publication.json").read_text())["edition"], "1.2")
            archiver.archive(repo)
            pdf.write_bytes(b"b" * 52000)
            with self.assertRaises(ValueError):
                archiver.archive(repo)
            archiver.archive(repo, reuse_existing=True)
            self.assertEqual(pdf.read_bytes(), b"b" * 52000)
            self.assertEqual((repo / "site/downloads" / (archiver.STEM + ".pdf")).read_bytes(),
                             b"a" * 52000)

if __name__ == "__main__":
    unittest.main()
