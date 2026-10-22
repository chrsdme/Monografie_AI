"""Regression tests for stale/duplicate publication PR protection."""
import importlib.util
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("archive_pr_guard", ROOT / "tools" / "archive_pr_guard.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class ArchiveGuardTests(unittest.TestCase):
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
            (root / f"{guard.STEM}.md").write_text('edition: "1.2.1"\n', encoding="utf-8")
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


if __name__ == "__main__":
    unittest.main()
