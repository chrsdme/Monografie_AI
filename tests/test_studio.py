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


if __name__ == "__main__":
    unittest.main()
