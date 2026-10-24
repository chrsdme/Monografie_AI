#!/usr/bin/env python3
"""Dry-run release planning for canonical Studio book fragments."""
from __future__ import annotations

import argparse
import difflib
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import os
import tempfile

HERE = Path(__file__).resolve().parent
_studio_spec = importlib.util.spec_from_file_location("studio_tool", HERE / "studio.py")
studio = importlib.util.module_from_spec(_studio_spec)
_studio_spec.loader.exec_module(studio)
_release_spec = importlib.util.spec_from_file_location("release_tool", HERE / "release.py")
release = importlib.util.module_from_spec(_release_spec)
_release_spec.loader.exec_module(release)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _edition(text: str) -> str:
    return release.field(text, "edition")


def _new_changelog_id(entries: list[dict]) -> str:
    numbers = [int(m.group(1)) for e in entries
               if (m := re.fullmatch(r"BOOK-(\d+)", str(e.get("id", ""))))]
    return f"BOOK-{max(numbers, default=0) + 1:04d}"


_RELEASE_FIELDS = (
    ("edition", r'^edition: "[^"]+"\r?$'),
    ("previous_edition", r'^previous_edition: "[^"]+"\r?$'),
    ("changelog_anchor", r'^changelog_anchor: "[^"]+"\r?$'),
    ("date", r'^date: "[^"]+"\r?$'),
    ("cover", r'^\*Editia [^\n]* \| Autor: [^\n]*\*$'),
    ("intro", r'^\*\*Ce este nou fata de editia [^\n]+\n'),
    ("annex edition", r'^- \*\*Editia curenta:\*\* [^\n]+$'),
    ("citation", r'^- \*\*Citare recomandata:\*\* [^\n]+$'),
    ("footer", r'^\*Sfarsitul editiei [^\n]+$'),
)
_BIBLIOGRAPHY = "# Bibliografie si resurse de aprofundare"


def _conflict(operation: str, kind: str, pattern: str, matches: list[tuple[int, int, str]],
              entries: list[dict], reason: str) -> ValueError:
    details = []
    for start, end, ident in matches:
        details.append(f"{ident}[{start}:{end}]")
    return ValueError(
        f"Conflict: release operation={operation!r}, type={kind!r}, "
        f"pattern={pattern!r}, fragments={details or 'none'}; {reason}")


def _project(folder: Path, manifest: dict, expected: bytes, *, update_fields: bool = True,
             changelog: bool = False):
    """Project known release.py editorial markers onto their owning fragments."""
    entries = manifest["fragments"]
    old_blobs = [(folder / item["path"]).read_bytes() for item in entries]
    try:
        fragment_texts = [blob.decode("utf-8") for blob in old_blobs]
        expected_text = expected.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Manuscrisul release nu este UTF-8") from exc

    result_texts = list(fragment_texts)
    affected: set[int] = set()
    field_edits: dict[int, list[tuple[int, int, str]]] = {}
    for label, pattern in _RELEASE_FIELDS if update_fields else ():
        original_matches = [(n, m) for n, text in enumerate(fragment_texts)
                            for m in re.finditer(pattern, text, re.M)]
        new_matches = list(re.finditer(pattern, expected_text, re.M))
        match_info = [(m.start(), m.end(), entries[n]["id"]) for n, m in original_matches]
        if len(original_matches) != 1 or len(new_matches) != 1:
            raise _conflict(label, "anchored replacement", pattern, match_info, entries,
                            f"expected one original owner and one release target; found "
                            f"{len(original_matches)} and {len(new_matches)}")
        n, old_match = original_matches[0]
        replacement = new_matches[0].group(0)
        if old_match.group(0) == replacement:
            continue
        field_edits.setdefault(n, []).append((old_match.start(), old_match.end(), replacement))
        affected.add(n)
    for n, edits in field_edits.items():
        text = result_texts[n]
        for start, end, replacement in sorted(edits, reverse=True):
            text = text[:start] + replacement + text[end:]
        result_texts[n] = text

    projected = [text.encode("utf-8") for text in result_texts]
    base = b"".join(projected)
    if not changelog:
        if base != expected:
            at = next((i for i, (x, y) in enumerate(zip(base, expected)) if x != y), min(len(base), len(expected)))
            raise _conflict("round-trip", "unexpected release change", "anchored release fields",
                            [(at, at + 1, entries[0]["id"])], entries,
                            f"projected bytes differ at offset {at}; lengths {len(base)} and {len(expected)}")
        manifest["fragments"] = entries
        return projected, [entries[n]["id"] for n in sorted(affected)], []

    try:
        base_text = base.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Manuscrisul proiectat nu este UTF-8") from exc
    bib_pattern = r"(?m)^" + re.escape(_BIBLIOGRAPHY) + r"\r?$"
    bib_base = re.search(bib_pattern, base_text)
    bib_expected = re.search(bib_pattern, expected_text)
    bib_locations = [(m.start(), m.end(), entries[n]["id"])
                     for n, text in enumerate(result_texts)
                     for m in re.finditer(bib_pattern, text)]
    if not bib_base or not bib_expected:
        raise _conflict("insert changelog", "anchored insertion", _BIBLIOGRAPHY, bib_locations, entries,
                        "bibliography anchor is missing")
    if (base_text[:bib_base.start()] != expected_text[:bib_expected.start()][:len(base_text[:bib_base.start()])] or
            base_text[bib_base.start():] != expected_text[bib_expected.start():]):
        raise _conflict("insert changelog", "anchored insertion", _BIBLIOGRAPHY, bib_locations, entries,
                        "release text differs outside the bibliography insertion point")
    insertion_text = expected_text[len(base_text[:bib_base.start()]):bib_expected.start()]
    if not re.search(r"(?m)^## E\.\d+\.", insertion_text):
        raise _conflict("insert changelog", "anchored insertion", _BIBLIOGRAPHY, bib_locations, entries,
                        "new changelog section was not found before bibliography")

    # Locate the bibliography owner using the post-field, pre-changelog fragment lengths.
    offset = 0
    owner = None
    owner_local = None
    for n, text in enumerate(result_texts):
        end = offset + len(text)
        if offset <= bib_base.start() < end:
            owner, owner_local = n, bib_base.start() - offset
            break
        offset = end
    if owner is None:
        raise _conflict("insert changelog", "anchored insertion", _BIBLIOGRAPHY, [], entries,
                        f"bibliography offset {bib_base.start()} has no fragment owner")

    final_entries = list(entries)
    new_ids = []
    if owner_local == 0:
        ident = _new_changelog_id(entries)
        if any(item.get("id") == ident for item in entries):
            raise _conflict("insert changelog", "new fragment identity", ident, [], entries,
                            "stable next ID is already in use")
        new_entry = {"id": ident, "path": f"fragments/{ident}-release-changelog.md",
                     "heading_level": 2, "title_at_migration": "Release changelog"}
        if (folder / new_entry["path"]).exists():
            raise _conflict("insert changelog", "new fragment path", new_entry["path"], [], entries,
                            "stable path already exists outside the manifest")
        final_entries.insert(owner, new_entry)
        projected.insert(owner, insertion_text.encode("utf-8"))
        new_ids.append(ident)
    else:
        text = result_texts[owner]
        result_texts[owner] = text[:owner_local] + insertion_text + text[owner_local:]
        projected[owner] = result_texts[owner].encode("utf-8")
        affected.add(owner)

    joined = b"".join(projected)
    if joined != expected:
        at = next((i for i, (x, y) in enumerate(zip(joined, expected)) if x != y), min(len(joined), len(expected)))
        involved = [(at, at + 1, entries[min(owner, len(entries) - 1)]["id"])]
        raise _conflict("round-trip", "byte mismatch", "release transformation", involved, entries,
                        f"projected bytes differ at offset {at}; lengths {len(joined)} and {len(expected)}")
    manifest["fragments"] = final_entries
    return projected, [entries[n]["id"] for n in sorted(affected)], new_ids


def _validate_staged_projection(manifest: dict, projected: list[bytes], expected: bytes) -> None:
    """Reassemble a temporary fragment copy and require exact release.py parity."""
    with tempfile.TemporaryDirectory(prefix=".studio-release-check-") as tmp:
        staged_book = Path(tmp) / "content" / "book"
        for entry, blob in zip(manifest["fragments"], projected):
            target = staged_book / entry["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(blob)
        assembled = studio.combine(staged_book, manifest)
    if assembled != expected:
        at = next((i for i, (x, y) in enumerate(zip(assembled, expected)) if x != y),
                  min(len(assembled), len(expected)))
        offset = 0
        involved = []
        for entry, blob in zip(manifest["fragments"], projected):
            end = offset + len(blob)
            if offset <= at <= end:
                involved.append(f"{entry['id']}[{offset}:{end}]")
            offset = end
        raise ValueError(
            f"Conflict: release operation='temporary round-trip', type='byte mismatch', "
            f"interval=[{at}:{at + 1}], fragments={involved or 'none'}; "
            f"assembled length={len(assembled)}, expected length={len(expected)}")


def plan(root: Path, *, event: str, date: str, changed: list[str], message: str,
         sha_value: str, previous_text: str | None = None,
         previous_edition: str | None = None) -> dict:
    manifest = studio.load_manifest(root)
    book = root / studio.BOOK
    assembled = studio.combine(book, manifest)
    master_path = root / studio.MASTER
    if len(manifest["fragments"]) != len({x.get("id") for x in manifest["fragments"]}):
        raise ValueError("ID-uri duplicate in manifest")
    if (manifest.get("source") != studio.MASTER or not manifest.get("original_sha256") or
            not manifest.get("last_generated_sha256")):
        raise ValueError("Manifest incomplet: lipsesc source sau hashurile obligatorii")
    baseline_hash = manifest["last_generated_sha256"]
    if not master_path.is_file():
        raise ValueError("Conflict: manuscrisul generat lipseste; reconcilierea este refuzata")
    master_bytes = master_path.read_bytes()
    if sha(master_bytes) != baseline_hash:
        raise ValueError(
            "Conflict: manuscrisul nu mai corespunde baseline-ului verificat "
            "din manifest; reconcilierea este refuzata")
    if master_bytes != assembled and sha(assembled) == baseline_hash:
        raise ValueError(
            "Conflict: fragmentele difera de baseline-ul verificat; "
            "reconcilierea este refuzata")
    current = assembled.decode("utf-8")
    initial = _edition(current)
    release_changed = list(changed)
    if any(path == "content/book" or path.startswith("content/book/") for path in release_changed):
        if studio.MASTER not in release_changed:
            release_changed.append(studio.MASTER)
    if event != "push":
        expected = assembled
        proposed = initial
        mode = "unchanged"
    else:
        preceding = (previous_edition if previous_edition is not None else
                     _edition(previous_text) if previous_text is not None else initial)
        if initial != preceding:
            proposed = initial
            transformed = release.refresh_current_date(current, proposed, date)
            mode = "declared"
        else:
            proposed = release.next_patch(initial)
            transformed = release.update_text(current, initial, proposed, date, release_changed, message, sha_value)
            mode = "incremented"
        expected = transformed.encode("utf-8")
    projected, affected, added = _project(
        book, manifest, expected, update_fields=mode != "unchanged",
        changelog=mode == "incremented")
    _validate_staged_projection(manifest, projected, expected)
    return {"mode": mode, "initial_edition": initial, "proposed_edition": proposed,
            "affected_ids": affected, "new_fragments": added, "before_sha256": sha(assembled),
            "after_sha256": sha(expected), "expected": expected, "projected": projected,
            "manifest": manifest, "original": assembled}


def dry_run(root: Path, **kwargs) -> dict:
    result = plan(root, **kwargs)
    before = result["original"].decode("utf-8")
    after = result["expected"].decode("utf-8")
    result["diff"] = "".join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                                   fromfile="canonical", tofile="release"))
    return result


def apply(root: Path, *, ci_main_release: bool = False, **kwargs) -> dict:
    """Validate in a sibling staging directory, then replace files with rollback."""
    result = plan(root, **kwargs)
    book = root / studio.BOOK
    with tempfile.TemporaryDirectory(dir=book.parent, prefix=".release-stage-") as tmp:
        stage = Path(tmp)
        entries = result["manifest"]["fragments"]
        for entry, blob in zip(entries, result["projected"]):
            target = stage / "content" / "book" / entry["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(blob)
        staged_manifest = dict(result["manifest"])
        staged_manifest["last_generated_sha256"] = result["after_sha256"]
        staged_book = stage / "content" / "book"
        (staged_book / "manifest.json").write_text(json.dumps(staged_manifest, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
        staged = studio.load_manifest(stage)
        if studio.combine(staged_book, staged) != result["expected"]:
            raise ValueError("Validarea staging-ului a esuat; sursa canonica nu a fost schimbata")
        _authorize_apply_target(root, ci_main_release)
        files = [(book / e["path"], (staged_book / e["path"]).read_bytes()) for e in entries]
        manifest_path = book / "manifest.json"
        files.append((manifest_path, (staged_book / "manifest.json").read_bytes()))
        master = root / studio.MASTER
        files.append((master, result["expected"]))
        backups = [(path, path.read_bytes() if path.exists() else None) for path, _ in files]
        written = []
        try:
            for path, blob in files:
                temp = path.with_name(path.name + ".release-tmp")
                try:
                    temp.write_bytes(blob)
                    os.replace(temp, path)
                except Exception:
                    temp.unlink(missing_ok=True)
                    raise
                written.append(path)
        except Exception:
            for path, old in reversed(backups):
                if path in written:
                    if old is None:
                        path.unlink(missing_ok=True)
                    else:
                        temp = path.with_name(path.name + ".release-rollback")
                        temp.write_bytes(old)
                        os.replace(temp, path)
            raise
    return result


def _authorize_apply_target(root: Path, ci_main_release: bool) -> None:
    """Keep main read-only except for this repository's publication workflow."""
    if studio.branch(root) != "main":
        studio.writable(root)
        return
    authorized = studio.authorized_ci_main(root, ci_main_release)
    if not authorized:
        raise ValueError("Release pe main permis doar in workflow-ul de publicare autorizat")


def compatibility_apply(root: Path, *, ci_main_release: bool = False, **kwargs) -> dict:
    """Legacy release policy with verified projection into an existing Studio book."""
    # plan() delegates edition/date/changelog policy to release.py. This adapter
    # only reconciles its known output against the manifest baseline.
    return apply(root, ci_main_release=ci_main_release, **kwargs)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--event", choices=("push", "workflow_dispatch", "release"), required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--changed", action="append", default=[])
    ap.add_argument("--message", default="Actualizare editoriala")
    ap.add_argument("--sha", default="0" * 40)
    ap.add_argument("--previous-edition", help="Editia dinaintea commitului publicat")
    ap.add_argument("--apply", action="store_true", help="Aplica atomic fragmente, manifest si manuscris")
    ap.add_argument("--ci-main-release", action="store_true",
                    help="Autorizeaza apply pe main doar in workflow-ul GitHub de publicare")
    ap.add_argument("--legacy-compatible", action="store_true",
                    help="Pastreaza politica release.py si reconciliaza manifestul existent")
    a = ap.parse_args(argv)
    try:
        operation = (compatibility_apply if a.legacy_compatible else apply) if a.apply else dry_run
        kwargs = dict(event=a.event, date=a.date, changed=a.changed,
                      message=a.message, sha_value=a.sha, previous_edition=a.previous_edition)
        if a.apply:
            kwargs["ci_main_release"] = a.ci_main_release
        r = operation(Path(a.repo), **kwargs)
        print(json.dumps({k: v for k, v in r.items() if k not in ("expected", "projected", "manifest", "original")},
                         ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, UnicodeDecodeError) as exc:
        print(json.dumps({"conflicts": [str(exc)]}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
