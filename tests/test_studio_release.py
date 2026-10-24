import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("studio_release", ROOT / "tools/studio_release.py")
sr = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(sr)
studio = sr.studio

def manuscript(edition="1.2.4", date="1 ianuarie 2025"):
    rows = ['---', f'edition: "{edition}"', 'previous_edition: "1.2.3"',
            'changelog_anchor: "old"', f'date: "{date}"', 'author: "Autor"',
            'license: "CC"', 'title: "Titlu"', 'wiki: "https://example.test"', '---',
            '# Cartea', f'*Editia {edition} | {date} | Autor: Autor | Licenta: CC*',
            '**Ce este nou fata de editia 1.2.3.** text',
            f'- **Editia curenta:** {edition}, {date} (editia precedenta: 1.2.3).',
            f'- **Citare recomandata:** Autor (2025), *Titlu*, editia {edition}, {date}, https://example.test.',
            f'*Sfarsitul editiei {edition}.*', '# Bibliografie si resurse de aprofundare', '']
    return '\n'.join(rows).encode()

class StudioReleaseTests(unittest.TestCase):
    def fixture(self, root, raw=None):
        book = root / 'content/book'; fragments = book / 'fragments'; fragments.mkdir(parents=True)
        raw = raw or manuscript()
        (fragments / 'BOOK-0001.md').write_bytes(raw)
        manifest = {'schema_version': 1, 'source': studio.MASTER,
                    'original_sha256': sr.sha(raw), 'last_generated_sha256': sr.sha(raw),
                    'fragments': [{'id': 'BOOK-0001', 'path': 'fragments/BOOK-0001.md'}]}
        (book / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        (root / studio.MASTER).write_bytes(raw)
        return book

    def multi_fragment_fixture(self, root):
        raw = manuscript()
        (root / studio.MASTER).write_bytes(raw)
        cuts = [raw.index(b'- **Editia curenta'), raw.index(b'# Bibliografie')]
        blobs = [raw[:cuts[0]], raw[cuts[0]:cuts[1]], raw[cuts[1]:]]
        book = root / 'content/book'; fragments = book / 'fragments'; fragments.mkdir(parents=True)
        ids = ['BOOK-0004', 'BOOK-0009', 'BOOK-0015']
        entries = []
        for ident, blob in zip(ids, blobs):
            relative = f'fragments/{ident}.md'
            (book / relative).write_bytes(blob)
            entries.append({'id': ident, 'path': relative})
        manifest = {'schema_version': 1, 'source': studio.MASTER,
                    'original_sha256': sr.sha(raw), 'last_generated_sha256': sr.sha(raw),
                    'fragments': entries}
        (book / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        return book, raw, ids

    def call(self, root, **kw):
        args = dict(event='push', date='22 octombrie 2026', changed=['wiki/index.md'],
                    message='Actualizare', sha_value='abcdef0123456789')
        args.update(kw); return sr.dry_run(root, **args)

    def test_increment_and_changelog_match_existing_release_logic(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.fixture(root); r = self.call(root)
            expected = sr.release.update_text(manuscript().decode(), '1.2.4', '1.2.5',
                '22 octombrie 2026', ['wiki/index.md'], 'Actualizare', 'abcdef0123456789').encode()
            self.assertEqual(r['expected'], expected)
            self.assertEqual(b''.join(r['projected']), expected)
            self.assertIn(b'## E.1.', expected)
            self.assertEqual(r['affected_ids'], ['BOOK-0001'])

    def test_increment_projects_updates_to_multiple_fragment_owners(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); book, raw, original_ids = self.multi_fragment_fixture(root)
            r = self.call(root)
            self.assertEqual(r['expected'], sr.release.update_text(
                raw.decode(), '1.2.4', '1.2.5', '22 octombrie 2026',
                ['wiki/index.md'], 'Actualizare', 'abcdef0123456789').encode())
            self.assertEqual(r['affected_ids'], original_ids[:2])
            self.assertEqual(r['new_fragments'], ['BOOK-0016'])
            self.assertEqual([e['id'] for e in r['manifest']['fragments']],
                             ['BOOK-0004', 'BOOK-0009', 'BOOK-0016', 'BOOK-0015'])
            self.assertEqual(b''.join(r['projected']), r['expected'])

    def test_content_book_path_is_described_as_book_content_in_changelog(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.fixture(root)
            r = self.call(root, changed=['content/book/fragments/BOOK-0001.md'])
            changelog = r['expected'].decode().split('## E.1.', 1)[1]
            self.assertIn('Continutul monografiei:', changelog)
            self.assertNotIn('Actualizare a materialelor proiectului.', changelog)

    def test_edited_fragment_can_be_published_from_its_previous_master_baseline(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); book = self.fixture(root)
            original = manuscript()
            (root / studio.MASTER).write_bytes(original)
            fragment = book / 'fragments/BOOK-0001.md'
            fragment.write_bytes(fragment.read_bytes().replace(b'# Cartea', b'# Continut nou'))
            r = self.call(root, changed=['content/book/fragments/BOOK-0001.md'])
            self.assertEqual(r['mode'], 'incremented')
            self.assertIn(b'Continut nou', r['expected'])
            self.assertIn(b'Continutul monografiei:', r['expected'])

    def test_boundary_changelog_gets_stable_new_fragment_id(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); book = root / 'content/book'; fragments = book / 'fragments'; fragments.mkdir(parents=True)
            raw = manuscript(); split = raw.index(b'# Bibliografie')
            first, second = raw[:split], raw[split:]
            (fragments / 'a.md').write_bytes(first); (fragments / 'b.md').write_bytes(second)
            data = {'schema_version': 1, 'source': studio.MASTER, 'original_sha256': sr.sha(raw),
                    'last_generated_sha256': sr.sha(raw), 'fragments': [
                    {'id': 'BOOK-0001', 'path': 'fragments/a.md'},
                    {'id': 'BOOK-0002', 'path': 'fragments/b.md'}]}
            (book / 'manifest.json').write_text(json.dumps(data), encoding='utf-8')
            (root / studio.MASTER).write_bytes(raw)
            r = self.call(root)
            self.assertEqual(r['new_fragments'], ['BOOK-0003'])
            self.assertEqual([x['id'] for x in r['manifest']['fragments']],
                             ['BOOK-0001', 'BOOK-0003', 'BOOK-0002'])
            self.assertEqual(b''.join(r['projected']), r['expected'])

    def test_explicit_edition_refreshes_date_cover_citation(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); original = manuscript('2.0'); self.fixture(root, original)
            r = self.call(root, previous_edition='1.9')
            text = r['expected'].decode()
            self.assertEqual(r['proposed_edition'], '2.0')
            self.assertEqual(r['expected'], sr.release.refresh_current_date(
                original.decode(), '2.0', '22 octombrie 2026').encode())
            self.assertEqual(b''.join(r['projected']), r['expected'])
            self.assertIn('date: "22 octombrie 2026"', text)
            self.assertIn('Editia 2.0 | 22 octombrie 2026', text)
            self.assertIn('**Editia curenta:** 2.0, 22 octombrie 2026', text)
            self.assertIn('editia 2.0, 22 octombrie 2026', text)

    def test_workflow_dispatch_and_archive_do_not_increment(self):
        for event in ('workflow_dispatch', 'release'):
            with self.subTest(event=event), tempfile.TemporaryDirectory() as d:
                root = Path(d); original = manuscript(); self.fixture(root, original)
                r = self.call(root, event=event)
                self.assertEqual(r['expected'], original)
                self.assertEqual(r['proposed_edition'], '1.2.4')

    def test_manifest_hash_duplicate_and_incomplete_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); book = self.fixture(root); p = book / 'manifest.json'
            data = json.loads(p.read_text()); data['fragments'].append(data['fragments'][0]); p.write_text(json.dumps(data))
            with self.assertRaises(ValueError): self.call(root)
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); book = self.fixture(root)
            fragment = book / 'fragments/BOOK-0001.md'
            fragment.write_bytes(fragment.read_bytes().replace(b'# Cartea', b'# Cartea editata'))
            # A real fragment edit is allowed when the manuscript still matches
            # the last generated baseline; the release publishes the new assembly.
            r = self.call(root, changed=['content/book/fragments/BOOK-0001.md'])
            self.assertEqual(r['mode'], 'incremented')
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); book = self.fixture(root); p = book / 'manifest.json'
            data = json.loads(p.read_text()); data.pop('last_generated_sha256'); p.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, 'incomplet'): self.call(root)

    def test_missing_generated_manuscript_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.fixture(root)
            (root / studio.MASTER).unlink()
            with self.assertRaisesRegex(ValueError, 'manuscrisul generat lipseste'):
                self.call(root)

    def test_manifest_and_generated_manuscript_conflict_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.fixture(root)
            (root / studio.MASTER).write_bytes(manuscript().replace(b'# Cartea', b'# Editorial schimbat'))
            with self.assertRaisesRegex(ValueError, 'baseline-ului verificat'):
                self.call(root)

    def test_divergent_manifest_master_and_fragments_are_never_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); book = self.fixture(root)
            original = manuscript()
            fragment = book / 'fragments/BOOK-0001.md'
            fragment.write_bytes(original.replace(b'# Cartea', b'# Fragment independent'))
            master = root / studio.MASTER
            master.write_bytes(original.replace(b'# Cartea', b'# Manuscris independent'))
            before = (fragment.read_bytes(), master.read_bytes(),
                      (book / 'manifest.json').read_bytes())
            with self.assertRaisesRegex(ValueError, 'baseline-ului verificat'):
                self.call(root)
            self.assertEqual((fragment.read_bytes(), master.read_bytes(),
                              (book / 'manifest.json').read_bytes()), before)

    def test_failed_validation_never_changes_sources(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); book = self.fixture(root); p = book / 'fragments/BOOK-0001.md'
            before = p.read_bytes()
            with patch.object(sr, '_project', side_effect=ValueError('injected validation failure')):
                with self.assertRaisesRegex(ValueError, 'injected'):
                    sr.apply(root, event='push', date='22 octombrie 2026', changed=[], message='x', sha_value='abc')
            self.assertEqual(p.read_bytes(), before)

    def test_partial_write_failure_restores_fragments_and_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); book, _, _ = self.multi_fragment_fixture(root)
            paths = [book / item['path'] for item in json.loads(
                (book / 'manifest.json').read_text(encoding='utf-8'))['fragments']]
            paths.append(book / 'manifest.json')
            paths.append(root / studio.MASTER)
            before = {path: path.read_bytes() for path in paths}
            replace = sr.os.replace
            count = 0

            def fail_second_replace(source, target):
                nonlocal count
                count += 1
                if count == 2:
                    raise OSError('injected partial write failure')
                return replace(source, target)

            with patch.object(sr.os, 'replace', side_effect=fail_second_replace):
                with self.assertRaisesRegex(OSError, 'injected partial write failure'):
                    sr.apply(root, event='push', date='22 octombrie 2026',
                             changed=['wiki/index.md'], message='Actualizare',
                             sha_value='abcdef0123456789')
            self.assertEqual({path: path.read_bytes() for path in paths}, before)
            self.assertEqual(list((book / 'fragments').glob('*.release-tmp')), [])
            self.assertEqual(list((book / 'fragments').glob('*.release-rollback')), [])

    def test_apply_stages_and_commits_new_fragment_and_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); book = root / 'content/book'; fragments = book / 'fragments'; fragments.mkdir(parents=True)
            raw = manuscript(); cut = raw.index(b'# Bibliografie')
            (fragments / 'a.md').write_bytes(raw[:cut]); (fragments / 'b.md').write_bytes(raw[cut:])
            data = {'schema_version': 1, 'source': studio.MASTER, 'original_sha256': sr.sha(raw),
                    'last_generated_sha256': sr.sha(raw), 'fragments': [
                    {'id': 'BOOK-0001', 'path': 'fragments/a.md'},
                    {'id': 'BOOK-0002', 'path': 'fragments/b.md'}]}
            (book / 'manifest.json').write_text(json.dumps(data), encoding='utf-8')
            (root / studio.MASTER).write_bytes(raw)
            r = sr.apply(root, event='push', date='22 octombrie 2026', changed=['wiki/index.md'],
                         message='Actualizare', sha_value='abcdef0123456789')
            updated = json.loads((book / 'manifest.json').read_text())
            self.assertEqual(updated['last_generated_sha256'], r['after_sha256'])
            self.assertEqual(studio.combine(book, updated), r['expected'])
            self.assertEqual((root / studio.MASTER).read_bytes(), r['expected'])
            self.assertTrue((book / 'fragments/BOOK-0003-release-changelog.md').is_file())

    def test_authorized_ci_main_apply_in_both_modes_and_local_apply_is_denied(self):
        github = {'GITHUB_ACTIONS': 'true', 'GITHUB_REF': 'refs/heads/main',
                  'GITHUB_WORKFLOW': 'Publish monograph and documentation',
                  'GITHUB_REPOSITORY': 'chrsdme/Monografie_AI', 'GITHUB_RUN_ID': '12345'}
        for operation in (sr.apply, sr.compatibility_apply):
            with self.subTest(operation=operation.__name__), tempfile.TemporaryDirectory() as d:
                root = Path(d); self.fixture(root)
                args = dict(event='push', date='22 octombrie 2026', changed=['wiki/index.md'],
                            message='Actualizare', sha_value='abcdef0123456789')
                with patch.object(studio, 'branch', return_value='main'):
                    with self.assertRaisesRegex(ValueError, 'workflow-ul de publicare autorizat'):
                        operation(root, **args)
                    with patch.dict(os.environ, github, clear=True):
                        result = operation(root, **args, ci_main_release=True)
                self.assertEqual(result['proposed_edition'], '1.2.5')

    def test_interactive_studio_writable_still_rejects_main(self):
        with patch.object(studio, 'branch', return_value='main'):
            with self.assertRaisesRegex(ValueError, 'Nu modifica main cu Studio'):
                studio.writable(Path('.'))

    def test_real_main_merge_release_ticks_once_and_preserves_historic_pdf(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)

            def git(*args):
                return subprocess.run(['git', *args], cwd=root, check=True,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            git('init', '-b', 'main')
            git('config', 'user.email', 'studio@example.invalid')
            git('config', 'user.name', 'Studio Test')
            book = self.fixture(root)
            docs = root / 'docs'; docs.mkdir()
            historic = docs / f'{sr.release.MASTER[:-3]}_1.2.4.pdf'
            historic_bytes = b'original historical PDF bytes'
            historic.write_bytes(historic_bytes)
            git('add', '.')
            git('commit', '-m', 'canonical edition 1.2.4')
            git('switch', '-c', 'editorial-change')
            fragment = book / 'fragments/BOOK-0001.md'
            fragment.write_bytes(fragment.read_bytes().replace(b'# Cartea', b'# Cartea din PR'))
            git('add', 'content/book/fragments/BOOK-0001.md')
            git('commit', '-m', 'editorial change')
            git('switch', 'main')
            git('merge', '--no-ff', 'editorial-change', '-m', 'Merge editorial PR')
            self.assertEqual(git('branch', '--show-current').stdout.decode().strip(), 'main')

            previous = git('show', 'HEAD^:' + studio.MASTER).stdout.decode('utf-8')
            previous_edition = sr.release.field(previous, 'edition')
            changed = git('diff', '--name-only', 'HEAD^', 'HEAD').stdout.decode().splitlines()
            args = dict(event='push', date='22 octombrie 2026', changed=changed,
                        message='Merge editorial PR', sha_value=git('rev-parse', 'HEAD').stdout.decode().strip(),
                        previous_edition=previous_edition)
            github = {'GITHUB_ACTIONS': 'true', 'GITHUB_REF': 'refs/heads/main',
                      'GITHUB_WORKFLOW': 'Publish monograph and documentation',
                      'GITHUB_REPOSITORY': 'chrsdme/Monografie_AI', 'GITHUB_RUN_ID': '12345'}
            with patch.dict(os.environ, github, clear=True), \
                    patch.object(studio, 'branch', return_value='main'):
                released = sr.apply(root, **args, ci_main_release=True)
            self.assertEqual(released['mode'], 'incremented')
            self.assertEqual(released['proposed_edition'], '1.2.5')
            self.assertEqual(sr.release.field((root / studio.MASTER).read_text(), 'edition'), '1.2.5')
            self.assertEqual(historic.read_bytes(), historic_bytes)

            rendered = root / f'{sr.release.MASTER[:-3]}.pdf'
            rendered.write_bytes(b'N' * 50_001)
            archive_spec = importlib.util.spec_from_file_location('archive_pdf', ROOT / 'tools/archive_pdf.py')
            archive_pdf = importlib.util.module_from_spec(archive_spec); archive_spec.loader.exec_module(archive_pdf)
            archive_pdf.archive(root)
            self.assertEqual(historic.read_bytes(), historic_bytes)
            self.assertEqual((docs / f'{sr.release.MASTER[:-3]}_1.2.5.pdf').read_bytes(), rendered.read_bytes())

    def test_git_history_legacy_compatibility_archive_then_studio_release(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            def git(*args):
                return subprocess.run(['git', *args], cwd=root, check=True,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            git('init', '-b', 'studio-test')
            git('config', 'user.email', 'studio@example.invalid')
            git('config', 'user.name', 'Studio Test')
            raw = manuscript()
            self.fixture(root, raw)
            master = root / studio.MASTER
            master.write_bytes(raw)
            git('add', '.')
            git('commit', '-m', 'initial canonical book')

            # Editorial push changes only a fragment. Compatibility must keep
            # release.py's one patch increment and reconcile all three sources.
            fragment = root / 'content/book/fragments/BOOK-0001.md'
            fragment.write_bytes(fragment.read_bytes().replace(b'# Cartea', b'# Cartea editata'))
            git('add', '.')
            git('commit', '-m', 'editorial change')
            args = dict(event='push', date='22 octombrie 2026',
                        changed=['content/book/fragments/BOOK-0001.md'],
                        message='editorial change', sha_value='1234567890123456')
            first = sr.compatibility_apply(root, **args)
            self.assertEqual(first['proposed_edition'], '1.2.5')
            self.assertIn(b'## E.1.', master.read_bytes())
            manifest = studio.load_manifest(root)
            self.assertEqual(studio.combine(root / studio.BOOK, manifest), master.read_bytes())
            self.assertEqual(manifest['last_generated_sha256'], sr.sha(master.read_bytes()))
            git('add', '.')
            git('commit', '-m', 'legacy compatible release')

            # Archive persistence is archive-only and dispatch does not tick.
            archive = root / 'docs' / f'{sr.release.MASTER[:-3]}_1.2.5.pdf'
            archive.parent.mkdir(parents=True, exist_ok=True)
            archive.write_bytes(b'P' * 50_001)
            metadata = root / 'docs/.publication.json'
            metadata.write_text(json.dumps({'edition': '1.2.5',
                'archived_pdf': archive.name,
                'pdf_sha256': sr.sha(archive.read_bytes())}), encoding='utf-8')
            git('add', '.')
            git('commit', '-m', 'archive-only persistence')
            changed = subprocess.run(['git', 'diff', '--name-only', 'HEAD^', 'HEAD'],
                cwd=root, check=True, stdout=subprocess.PIPE, text=True).stdout.splitlines()
            self.assertEqual(changed, ['docs/.publication.json', f'docs/{archive.name}'])
            prior = git('show', f'HEAD^:{studio.MASTER}').stdout.decode('utf-8')
            after = git('show', f'HEAD:{studio.MASTER}').stdout.decode('utf-8')
            self.assertEqual(prior, after)
            guard_spec = __import__('importlib.util').util.spec_from_file_location(
                'archive_guard', ROOT / 'tools/archive_pr_guard.py')
            guard = __import__('importlib.util').util.module_from_spec(guard_spec)
            guard_spec.loader.exec_module(guard)
            self.assertTrue(guard.is_archive_only(changed, prior, after, repo=root))
            unchanged = sr.compatibility_apply(root, event='workflow_dispatch',
                date='22 octombrie 2026', changed=[], message='archive merge',
                sha_value='0' * 40)
            self.assertEqual(unchanged['proposed_edition'], '1.2.5')
            self.assertEqual(master.read_bytes(), first['expected'])

            # A second inactive release and then an activated Studio release
            # each advance exactly once without accumulating divergence.
            fragment.write_bytes(fragment.read_bytes().replace(b'Cartea editata', b'Cartea editata din nou'))
            second = sr.compatibility_apply(root, **{**args, 'sha_value': '2234567890123456'})
            self.assertEqual(second['proposed_edition'], '1.2.6')
            self.assertEqual(studio.combine(root / studio.BOOK,
                             studio.load_manifest(root)), master.read_bytes())
            third = sr.apply(root, **{**args, 'sha_value': '3234567890123456'})
            self.assertEqual(third['proposed_edition'], '1.2.7')
            self.assertEqual(studio.combine(root / studio.BOOK,
                             studio.load_manifest(root)), master.read_bytes())

    def test_archive_pr_accepts_verified_generated_release_and_rejects_e1_edit(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)

            def git(*args):
                return subprocess.run(['git', *args], cwd=root, check=True,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            git('init', '-b', 'studio-test')
            git('config', 'user.email', 'studio@example.invalid')
            git('config', 'user.name', 'Studio Test')
            book = self.fixture(root)
            master = root / studio.MASTER
            wiki = root / 'wiki/index.md'
            wiki.parent.mkdir(parents=True)
            wiki.write_text('Index initial.\n', encoding='utf-8')
            git('add', '.')
            git('commit', '-m', 'initial canonical book')
            base = git('rev-parse', 'HEAD').stdout.decode().strip()

            wiki.write_text('Index actualizat.\n', encoding='utf-8')
            git('add', '.')
            git('commit', '-m', 'wiki content change')
            source_sha = git('rev-parse', 'HEAD').stdout.decode().strip()
            source_paths = subprocess.run(
                ['git', 'diff', '--name-only', 'HEAD^', 'HEAD'], cwd=root,
                check=True, stdout=subprocess.PIPE, text=True).stdout.splitlines()
            sr.compatibility_apply(root, event='push', date='22 octombrie 2026',
                changed=source_paths, message='wiki content change', sha_value=source_sha)
            git('add', '.')
            git('commit', '-m', 'generated release')
            release_expected = master.read_bytes()
            generated_expected = sr.release.update_text(
                git('show', f'{base}:{studio.MASTER}').stdout.decode('utf-8'),
                '1.2.4', '1.2.5', '22 octombrie 2026',
                source_paths, 'wiki content change', source_sha)
            self.assertEqual(release_expected, generated_expected.encode('utf-8'))

            archive = root / 'docs' / f'{sr.release.MASTER[:-3]}_1.2.5.pdf'
            archive.parent.mkdir(parents=True, exist_ok=True)
            archive.write_bytes(b'P' * 50_001)
            metadata = root / 'docs/.publication.json'
            metadata.write_text(json.dumps({'edition': '1.2.5',
                'archived_pdf': archive.name,
                'pdf_sha256': sr.sha(archive.read_bytes())}), encoding='utf-8')
            git('add', '.')
            git('commit', '-m', 'archive generated release')

            def changed_from_base():
                return subprocess.run(['git', 'diff', '--name-only', base, 'HEAD'],
                    cwd=root, check=True, stdout=subprocess.PIPE, text=True).stdout.splitlines()

            guard_spec = __import__('importlib.util').util.spec_from_file_location(
                'archive_guard_generated_release', ROOT / 'tools/archive_pr_guard.py')
            guard = __import__('importlib.util').util.module_from_spec(guard_spec)
            guard_spec.loader.exec_module(guard)
            before = git('show', f'{base}:{studio.MASTER}').stdout.decode('utf-8')
            after = git('show', f'HEAD:{studio.MASTER}').stdout.decode('utf-8')
            self.assertEqual(after.encode('utf-8'), release_expected)
            self.assertTrue(guard.is_archive_only(changed_from_base(), before, after, repo=root))

            edited = after.replace('detaliile editoriale se verifica',
                                   'detalii editoriale noi se verifica')
            self.assertNotEqual(after, edited)
            master.write_text(edited, encoding='utf-8')
            fragment = book / 'fragments/BOOK-0001.md'
            fragment.write_text(edited, encoding='utf-8')
            git('add', '.')
            git('commit', '-m', 'independent E.1 editorial edit')
            edited_after = git('show', f'HEAD:{studio.MASTER}').stdout.decode('utf-8')
            self.assertEqual(studio.combine(book, studio.load_manifest(root)),
                             edited_after.encode('utf-8'))
            self.assertFalse(guard.is_archive_only(
                changed_from_base(), before, edited_after, repo=root))

if __name__ == '__main__': unittest.main()
