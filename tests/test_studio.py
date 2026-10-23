"""Studio bootstrap tests. No network, Github or PDF toolchain required."""
import importlib.util
from pathlib import Path
import json
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("studio_tool", ROOT / "tools/studio.py")
studio = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(studio)
BUILD_SPEC = importlib.util.spec_from_file_location("build_tool", ROOT / "tools/build.py")
build_tool = importlib.util.module_from_spec(BUILD_SPEC)
BUILD_SPEC.loader.exec_module(build_tool)


class StudioTests(unittest.TestCase):
    def repo(self, path, branch="studio-test"):
        root = Path(path)
        subprocess.run(["git", "init", "-b", branch], cwd=root,
                       check=True, capture_output=True)
        return root

    def test_split_preserves_crlf_and_heading_inside_fence(self):
        raw = (b'---\r\nedition: "1.2.4"\r\n---\r\n'
               b'# Monografie\r\n'
               b'## 14. Orchestrare\r\n'
               b'Text\r\n'
               b'~~~markdown\r\n### NOT A REAL HEADING\r\n~~~\r\n'
               b'### 14.12. Test\r\nFinal\r\n')
        entries = studio.split_bytes(raw)
        self.assertEqual(b"".join(chunk[2] for chunk in entries), raw)
        self.assertFalse(any(title.startswith("NOT A REAL") for title, _, _ in entries))

    def test_migrate_assemble_and_conflict_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.repo(tmp)
            raw = b'---\nedition: "1.2.4"\n---\n# Intro\n## 1. One\nbody\n'
            (root / studio.MASTER).write_bytes(raw)
            studio.migrate(root)
            manifest = studio.load_manifest(root)
            self.assertGreaterEqual(len(manifest["fragments"]), 3)
            self.assertEqual(studio.combine(root / studio.BOOK, manifest), raw)
            studio.assemble(root, write=False)
            with self.assertRaisesRegex(ValueError, "exista"):
                studio.migrate(root)
            # Modificarea manuala a MASTER interzice suprascrierea.
            (root / studio.MASTER).write_bytes(b"unknown external edit")
            with self.assertRaisesRegex(ValueError, "extern"):
                studio.assemble(root, write=True)

    def test_fragment_escape_and_duplicate_ids_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "fragments").mkdir()
            (root / "fragments/a.md").write_text("A")
            data = {"fragments": [
                {"id": "BOOK-0001", "path": "fragments/a.md"},
                {"id": "BOOK-0001", "path": "fragments/a.md"},
            ]}
            with self.assertRaisesRegex(ValueError, "duplicata"):
                studio.combine(root, data)
            data["fragments"][1] = {"id": "BOOK-0002", "path": "../../outside.md"}
            with self.assertRaisesRegex(ValueError, "nesigur"):
                studio.combine(root, data)

    def test_creation_uses_detailed_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.repo(tmp)
            (root / "studio/templates").mkdir(parents=True)
            (root / "studio/templates/article.md").write_text(
                '---\nid: "ART-YYYY-NNN"\ntitle: "Template"\n---\n# Draft\n',
                encoding="utf-8")
            studio.new(root, "article", "Un articol nou")
            path = root / "content/articles/un-articol-nou.md"
            self.assertTrue(path.is_file())
            self.assertIn('id: "ART-', path.read_text(encoding="utf-8"))
            with self.assertRaisesRegex(ValueError, "existent"):
                studio.new(root, "article", "Un articol nou")

    def test_batch_preflight_cannot_escape_inbox(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML unavailable in test environment")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "inbox").mkdir()
            (root / "inbox/article.md").write_text("Draft", encoding="utf-8")
            valid = {"schema_version": 1, "batch_id": "b1",
                     "owner_approval": "required",
                     "items": [{"id": "t1", "file": "article.md",
                                "action": "propose_article", "targets": ["wiki"]}]}
            (root / "inbox/zzz.yaml").write_text(yaml.safe_dump(valid), encoding="utf-8")
            studio.plan(root, "inbox/zzz.yaml")
            self.assertTrue((root / ".studio-local/plans/b1.json").is_file())
            valid["items"][0]["file"] = "../secrets.txt"
            (root / "inbox/zzz.yaml").write_text(yaml.safe_dump(valid), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "invalid"):
                studio.plan(root, "inbox/zzz.yaml")

    def test_refuses_modify_main(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.repo(tmp, branch="main")
            with self.assertRaisesRegex(ValueError, "main"):
                studio.migrate(root)

    def test_toc_build_updates_fragment_master_and_wiki_deterministically(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.repo(tmp)
            raw = (b'---\nedition: "1.2.6"\ndate: "23 octombrie 2026"\n'
                   b'title: "Test"\nauthor: "Test"\nlicense: "CC"\nsource: "https://example.test"\n---\n'
                   b'# Test\n\n## Cuprins\n\n<!-- TOC:START -->\nstale\n<!-- TOC:END -->\n\n'
                   b'# Partea I. Start\n\n## 1. Primul capitol\nText editorial actualizat.\n'
                   b'# Anexa A. Glosar\n\n## A.1. Termeni\n\n# Anexa B. Sabloane\n\n'
                   b'# Anexa C. Evaluare\n\n# Anexa D. Metoda\n\n# Anexa E. Istoric\n\n'
                   b'# Bibliografie si resurse de aprofundare\n\n')
            (root / studio.MASTER).write_bytes(raw)
            studio.migrate(root)
            before_ids = [e["id"] for e in studio.load_manifest(root)["fragments"]]
            count = build_tool.update_toc(root / studio.MASTER)
            self.assertGreater(count, 0)
            manifest = studio.load_manifest(root)
            assembled = studio.combine(root / studio.BOOK, manifest)
            self.assertEqual((root / studio.MASTER).read_bytes(), assembled)
            self.assertEqual(manifest["last_generated_sha256"], studio.sha(assembled))
            self.assertIn(b'edition: "1.2.6"', assembled)
            self.assertIn(b"Text editorial actualizat.", assembled)
            self.assertEqual(before_ids, [e["id"] for e in manifest["fragments"]])
            self.assertEqual(build_tool.update_toc(root / studio.MASTER), 0)
            index = root / "wiki/index.md"
            index.parent.mkdir(parents=True, exist_ok=True)
            index.write_bytes(b"# Manual\r\n\r\nText manual\r\n\r\n"
                              b"<!-- MONOGRAFIE:START -->old<!-- MONOGRAFIE:END -->\r\n")
            build_tool.build_wiki(root, root / studio.MASTER, {})
            chapter = root / "wiki/partea-1/01-ce-este-ai.md"
            first_build = {p.relative_to(root): p.read_bytes()
                           for p in (root / "wiki").rglob("*.md")}
            self.assertIn(b"Text editorial actualizat.", chapter.read_bytes())
            for path, content in first_build.items():
                self.assertNotIn(b"\r\n", content, path)
            self.assertEqual(index.read_bytes().count(b"Text manual"), 1)
            self.assertIn(b"Descarca PDF-ul curent", index.read_bytes())
            self.assertNotIn(b"\r\n", index.read_bytes())
            second_build = {p.relative_to(root): p.read_bytes()
                            for p in (root / "wiki").rglob("*.md")}
            self.assertEqual(first_build.keys(), second_build.keys())
            for path in first_build:
                self.assertEqual(first_build[path], second_build[path], path)
            self.assertTrue((root / ".studio-local/wiki_index_block.md").is_file())
            self.assertFalse((root / "wiki_index_block.md").exists())

    def test_wiki_build_creates_missing_wiki_directory_and_homepage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            master = root / "source.md"
            master.write_text(
                '---\ntitle: "Test"\nsource: "https://example.test"\nlicense: "CC"\n---\n'
                '# Test\n\n# Partea I. Start\n\n## 1. Primul capitol\nText.\n'
                '# Anexa A. Glosar\n\n# Anexa B. Sabloane\n\n'
                '# Anexa C. Evaluare\n\n# Anexa D. Metoda\n\n'
                '# Anexa E. Istoric\n\n# Bibliografie si resurse de aprofundare\n',
                encoding="utf-8")
            self.assertFalse((root / "wiki").exists())

            build_tool.build_wiki(root, master, {})

            self.assertTrue((root / "wiki/index.md").is_file())
            self.assertTrue((root / "wiki/partea-1/01-ce-este-ai.md").is_file())

    def test_generated_pdf_download_matches_source_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            generated = root / "Monografie.pdf"
            generated.write_bytes(b"generated pdf bytes" * 10)
            destination = build_tool.publish_download_pdf(root, generated)
            self.assertEqual(destination.read_bytes(), generated.read_bytes())

    def test_toc_validation_failure_leaves_canonical_files_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.repo(tmp)
            raw = b"# Test\n\n## 1. Fara marcaje\nText\n"
            (root / studio.MASTER).write_bytes(raw)
            studio.migrate(root)
            manifest_before = (root / studio.BOOK / "manifest.json").read_bytes()
            with self.assertRaises(SystemExit):
                build_tool.update_toc(root / studio.MASTER)
            self.assertEqual((root / studio.MASTER).read_bytes(), raw)
            self.assertEqual((root / studio.BOOK / "manifest.json").read_bytes(), manifest_before)


if __name__ == "__main__":
    unittest.main()
