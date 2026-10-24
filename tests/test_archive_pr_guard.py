"""Regression tests for stale/duplicate publication PR protection."""
import importlib.util
import hashlib
import json
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("archive_pr_guard", ROOT / "tools" / "archive_pr_guard.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class ArchiveGuardTests(unittest.TestCase):
    def test_edition_accepts_lf_and_crlf_front_matter(self):
        for ending in ("\n", "\r\n"):
            with self.subTest(ending=repr(ending)):
                self.assertEqual(guard.edition(
                    f'---{ending}edition: "1.2.1"{ending}title: Test{ending}---{ending}'
                ), "1.2.1")

    def test_identical_archive_does_not_open_another_pr(self):
        self.assertEqual(guard.classify("1.2.1", "1.2.1", b"pdf", b"pdf"), 10)

    def test_same_edition_different_bytes_is_an_error(self):
        self.assertEqual(guard.classify("1.2.1", "1.2.1", b"first", b"second"), 20)
        self.assertEqual(guard.classify("1.2.1", "1.2.2", b"first", b"second"), 20)

    def test_superseded_archive_is_an_error(self):
        self.assertEqual(guard.classify("1.2.1", "1.2.2", None, b"pdf"), 21)

    def test_new_unarchived_edition_can_proceed(self):
        self.assertEqual(guard.classify("1.2.3", "1.2.2", None, b"pdf"), 0)
        self.assertEqual(guard.classify("1.2.2", "1.2.2", None, b"pdf"), 0)

    def test_archive_only_requires_release_only_body_and_paths(self):
        base = ('---\nedition: "1.2.3"\ndate: "1 ianuarie 2025"\n---\n'
                '# Cartea\n\nText editorial.\n')
        released = ('---\nedition: "1.2.4"\ndate: "22 octombrie 2026"\n---\n'
                    '# Cartea\n\nText editorial.\n')
        allowed = [f"{guard.STEM}.md", "docs/.publication.json",
                   f"docs/{guard.STEM}_1.2.4.pdf", "content/book/manifest.json",
                   "content/book/fragments/BOOK-0001.md"]
        self.assertTrue(guard.is_archive_only(allowed, base, released))
        editorial = released.replace("Text editorial.", "Text editorial nou.")
        self.assertFalse(guard.is_archive_only(allowed + ["wiki/colectii/new.md"], base, editorial))
        self.assertFalse(guard.is_archive_only(allowed, base, editorial))
        self.assertFalse(guard.is_archive_only(["docs/.publication.json"], base, base))
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp); docs = root / "docs"; docs.mkdir()
            pdf = b"verified archive bytes"
            (docs / f"{guard.STEM}_1.2.4.pdf").write_bytes(pdf)
            (docs / ".publication.json").write_text(json.dumps({
                "edition": "1.2.4", "archived_pdf": f"{guard.STEM}_1.2.4.pdf",
                "pdf_sha256": hashlib.sha256(pdf).hexdigest()}), encoding="utf-8")
            legacy_allowed = [f"{guard.STEM}.md", "docs/.publication.json",
                              f"docs/{guard.STEM}_1.2.4.pdf"]
            self.assertTrue(guard.is_archive_only(legacy_allowed, base, released, repo=root))
            (docs / ".publication.json").write_text("{}", encoding="utf-8")
            self.assertFalse(guard.is_archive_only(legacy_allowed, base, released, repo=root))

    def test_archive_only_preserves_changelog_and_editorial_changes(self):
        before = ('---\nedition: "1.2.3"\n---\n# Cartea\nText editorial.\n'
                  '# Bibliografie si resurse de aprofundare\n')
        generated = ('## E.1. Modificari de la editia 1.2.3 la 1.2.4\n\n'
                     '- **Origine:** commitul `123456789abc`; mesaj: actualizare.\n'
                     '- Continutul monografiei: modificari ale sursei Markdown canonice.\n'
                     '- **Nota:** aceasta lista este generata din fisierele modificate;\n'
                     'detaliile editoriale se verifica in diff-ul commitului indicat.\n\n')
        valid = before.replace('edition: "1.2.3"', 'edition: "1.2.4"').replace(
            '# Bibliografie si resurse de aprofundare', generated +
            '# Bibliografie si resurse de aprofundare')
        # Adding a release changelog is a content change, even when its shape
        # matches release.py output. Archive-only commits preserve it as-is.
        self.assertNotEqual(guard._editorial_core(before), guard._editorial_core(valid))
        edited = valid.replace('actualizare.', 'actualizare si continut editorial nou.')
        self.assertNotEqual(guard._editorial_core(before), guard._editorial_core(edited))
        handwritten = valid.replace(generated, generated.replace(
            '- **Origine:**', '- **Origine editoriala:**'))
        self.assertNotEqual(guard._editorial_core(before), guard._editorial_core(handwritten))

        # A legitimate archive commit preserves the already generated
        # changelog while changing only publication metadata.
        archived = valid.replace('edition: "1.2.4"', 'edition: "1.2.5"')
        self.assertEqual(guard._editorial_core(valid), guard._editorial_core(archived))
        archive_paths = [f"{guard.STEM}.md", "docs/.publication.json",
                         f"docs/{guard.STEM}_1.2.5.pdf"]
        self.assertTrue(guard.is_archive_only(archive_paths, valid, archived))
        edited_archive = archived.replace('actualizare.', 'actualizare si text nou.')
        self.assertFalse(guard.is_archive_only(archive_paths, valid, edited_archive))
        handwritten_archive = archived.replace(
            'Origine:', 'Origine editoriala:')
        self.assertFalse(guard.is_archive_only(
            archive_paths, valid, handwritten_archive))

    def test_archive_only_removes_only_release_shaped_changelog(self):
        before = ('---\nedition: "1.2.3"\ndate: "1 ianuarie 2025"\n---\n'
                  '# Cartea\nText editorial.\n# Bibliografie si resurse de aprofundare\n')
        release_changelog = ('## E.1. Modificari de la editia 1.2.3 la 1.2.4\n\n'
                             '- **Origine:** commitul `123456789abc`; mesaj: actualizare.\n'
                             '- Continutul monografiei: modificari ale sursei Markdown canonice.\n'
                             '- **Nota:** aceasta lista este generata din fisierele modificate;\n'
                             'detaliile editoriale se verifica in diff-ul commitului indicat.\n\n')
        after = before.replace('edition: "1.2.3"', 'edition: "1.2.4"').replace(
            'date: "1 ianuarie 2025"', 'date: "22 octombrie 2026"').replace(
            '# Bibliografie si resurse de aprofundare',
            release_changelog + '# Bibliografie si resurse de aprofundare')
        paths = [f"{guard.STEM}.md", "docs/.publication.json",
                 f"docs/{guard.STEM}_1.2.4.pdf"]
        self.assertEqual(guard._editorial_core(before),
                         guard._editorial_core(before.replace(
                             'edition: "1.2.3"', 'edition: "1.2.4"').replace(
                             'date: "1 ianuarie 2025"', 'date: "22 octombrie 2026"')))
        self.assertNotEqual(guard._editorial_core(before),
                            guard._editorial_core(after))
        self.assertFalse(guard.is_archive_only(paths, before, after))

    def test_open_pr_lookup_matches_exact_edition(self):
        rows = [
            {"number": 23, "title": "Archive edition 1.2.3 PDF and metadata"},
            {"number": 24, "title": "Archive edition 1.2.3 PDF and metadata"},
            {"number": 28, "title": "Archive edition 1.2.30 PDF and metadata"},
            {"number": 29, "title": "Unrelated workflow"},
        ]
        self.assertEqual(guard.open_archive_pr_numbers(rows, "1.2.3"), [23, 24])
        self.assertEqual(guard.open_archive_pr_numbers(rows, "1.2.4"), [])

    def test_open_pr_preflight_blocks_second_same_version(self):
        from unittest.mock import patch
        import subprocess
        import json
        fake = subprocess.CompletedProcess(
            args=["gh", "pr", "list"], returncode=0,
            stdout=json.dumps([
                {"number": 24, "title": "Archive edition 1.2.3 PDF and metadata"}
            ]), stderr=""
        )
        with patch.object(guard.subprocess, "run", return_value=fake) as run:
            self.assertEqual(guard.check_open_archive_prs(ROOT, "1.2.3"), 23)
            self.assertEqual(guard.check_open_archive_prs(ROOT, "1.2.4"), 0)
            self.assertEqual(run.call_args.args[0][:4],
                             ["gh", "pr", "list", "--base"])

    def test_open_pr_preflight_fails_closed_on_api_error(self):
        import subprocess
        from unittest.mock import patch
        failed = subprocess.CompletedProcess(
            args=["gh", "pr", "list"], returncode=1,
            stdout="", stderr="API error"
        )
        with patch.object(guard.subprocess, "run", return_value=failed):
            with self.assertRaisesRegex(RuntimeError, "API error"):
                guard.check_open_archive_prs(ROOT, "1.2.3")

    def test_real_git_snapshot_checks_archived_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            def git(*args):
                return subprocess.run(["git", *args], cwd=root, check=True,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            git("init")
            git("config", "user.email", "archive-test@example.invalid")
            git("config", "user.name", "Archive Test")
            (root / f"{guard.STEM}.md").write_bytes(
                f'---\r\nedition: "1.2.1"\r\n---\r\n'.encode("utf-8"))
            docs = root / "docs"
            docs.mkdir()
            archive = docs / f"{guard.STEM}_1.2.1.pdf"
            archive.write_bytes(b"A" * 52_000)
            git("add", ".")
            git("commit", "-m", "initial archive")
            self.assertEqual(guard.check(root, "HEAD"), 10)
            archive.write_bytes(b"B" * 52_000)
            self.assertEqual(guard.check(root, "HEAD"), 20)
            archive.unlink()
            (root / f"{guard.STEM}.md").write_text('edition: "1.2.2"\n', encoding="utf-8")
            newer = docs / f"{guard.STEM}_1.2.2.pdf"
            newer.write_bytes(b"C" * 52_000)
            self.assertEqual(guard.check(root, "HEAD"), 0)

    def test_real_git_snapshot_with_lf_front_matter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            def git(*args):
                return subprocess.run(["git", *args], cwd=root, check=True,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            git("init")
            git("config", "user.email", "archive-test@example.invalid")
            git("config", "user.name", "Archive Test")
            (root / f"{guard.STEM}.md").write_bytes(
                b'---\nedition: "1.2.1"\n---\n')
            docs = root / "docs"
            docs.mkdir()
            (docs / f"{guard.STEM}_1.2.1.pdf").write_bytes(b"A" * 52_000)
            git("add", ".")
            git("commit", "-m", "initial archive")
            self.assertEqual(guard.check(root, "HEAD"), 10)


if __name__ == "__main__":
    unittest.main()
