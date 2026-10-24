#!/usr/bin/env python3
"""Reject stale and conflicting PDF archive submissions before creating a PR.

Exit codes: 0 = safe to propose, 10 = identical edition already archived,
20 = same edition with different PDF (collision), 21 = superseded release,
23 = competing archive PR already open.
"""
import argparse
import hashlib
import importlib.util
import json
import pathlib
import re
import subprocess
import sys

STEM = "Monografie_AI_De_la_Chat_la_Sisteme_Agentice"


def edition(source):
    match = re.search(r'^edition: "([0-9]+(?:\.[0-9]+){1,2})"\r?$',
                      source, re.MULTILINE)
    if not match:
        raise ValueError("Missing or invalid edition in monograph front matter")
    return match.group(1)


def version_key(version):
    return tuple(int(part) for part in version.split("."))


def _editorial_core(source):
    """Mask only technical YAML release fields; all Markdown stays auditable."""
    match = re.match(r'\A(\ufeff?---\r?\n)(.*?)(\r?\n---(?:\r?\n|\Z))',
                     source, re.DOTALL)
    if not match:
        return source
    fields = re.sub(
        r'(?m)^((?:edition|previous_edition|changelog_anchor|date):\s*)"[^"\r\n]*"(?=\r?$)',
        r'\1"<release-metadata>"', match.group(2))
    return match.group(1) + fields + match.group(3) + source[match.end():]


def _matches_generated_release(repo, before_master, after_master, changed_paths):
    """Prove a manuscript transition by replaying release.py from Git history."""
    if repo is None:
        return False
    root = pathlib.Path(repo)
    master_path = f"{STEM}.md"
    try:
        before = before_master.encode("utf-8")
        after = after_master.encode("utf-8")
        old_edition = edition(before_master)
        new_edition = edition(after_master)
        release_spec = importlib.util.spec_from_file_location(
            "archive_release_for_guard", pathlib.Path(__file__).with_name("release.py"))
        release = importlib.util.module_from_spec(release_spec)
        release_spec.loader.exec_module(release)
        if release.next_patch(old_edition) != new_edition:
            return False
        date = release.field(after_master, "date")
        commits = subprocess.check_output(
            ["git", "log", "--format=%H", "HEAD", "--", master_path],
            cwd=root, text=True).splitlines()
        matches = set()
        for release_commit in commits:
            release_parents = subprocess.check_output(
                ["git", "rev-list", "--parents", "-n", "1", release_commit],
                cwd=root, text=True).split()[1:]
            if git_show(root, release_commit, master_path) != after:
                continue
            source_options = []
            for parent in release_parents:
                if git_show(root, parent, master_path) != before:
                    continue
                parent_line = subprocess.check_output(
                    ["git", "rev-list", "--parents", "-n", "1", parent],
                    cwd=root, text=True).split()
                if len(parent_line) == 3:
                    # GitHub's archive PR commit is a child of the source
                    # merge. The source merge's first parent is the baseline.
                    source_options.append((parent, parent_line[1]))

            # Retain compatibility with merge-shaped release commits.
            if len(release_parents) == 2:
                source_options.append((release_parents[1], None))

            for source_commit, source_parent in source_options:
                if source_parent is None:
                    source_line = subprocess.check_output(
                        ["git", "rev-list", "--parents", "-n", "1", source_commit],
                        cwd=root, text=True).split()
                    if len(source_line) < 3:
                        continue
                    source_parent = source_line[2]
                if git_show(root, source_commit, master_path) != before:
                    continue
                source_paths = subprocess.check_output(
                    ["git", "diff", "--name-only", source_parent, source_commit],
                    cwd=root, text=True).splitlines()
                if not source_paths:
                    continue
                message = subprocess.check_output(
                    ["git", "log", "-1", "--format=%B", source_commit],
                    cwd=root, text=True)
                path_variants = [source_paths]
                if any(path == "content/book" or path.startswith("content/book/")
                       for path in source_paths) and master_path not in source_paths:
                    # Studio release also records the assembled manuscript as an
                    # input when a fragment or manifest triggered the release.
                    path_variants.append(source_paths + [master_path])
                for release_paths in path_variants:
                    expected = release.update_text(
                        before_master, old_edition, new_edition, date, release_paths,
                        message, source_commit)
                    if expected.encode("utf-8") == after:
                        matches.add((source_commit, tuple(release_paths)))
        return len(matches) == 1
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError,
            UnicodeError, AttributeError, TypeError):
        return False


def is_archive_only(changed_paths, before_master, after_master, repo=None):
    """Accept only a release persistence diff whose editorial body is unchanged."""
    allowed_exact = {f"{STEM}.md", "docs/README.md", "docs/.publication.json",
                     "wiki/index.md", f"wiki/downloads/{STEM}.pdf",
                     f"docs/{STEM}.pdf"}
    allowed_prefix = ("content/book/fragments/",)
    for path in changed_paths:
        if path in allowed_exact or path.startswith(allowed_prefix):
            continue
        if path.startswith(("wiki/partea-", "wiki/anexe/")) and path.endswith(".md"):
            continue
        if re.fullmatch(rf"docs/{re.escape(STEM)}_[0-9]+(?:\.[0-9]+){{1,2}}\.pdf", path):
            continue
        if path == "content/book/manifest.json":
            continue
        return False
    if not changed_paths:
        return False
    current_edition = edition(after_master)
    if ("docs/.publication.json" not in changed_paths or
            f"docs/{STEM}_{current_edition}.pdf" not in changed_paths):
        return False
    if repo is not None:
        root = pathlib.Path(repo)
        metadata_path = root / "docs/.publication.json"
        archive_path = root / f"docs/{STEM}_{current_edition}.pdf"
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            archive_bytes = archive_path.read_bytes()
        except (OSError, json.JSONDecodeError):
            return False
        if (not isinstance(metadata, dict) or metadata.get("edition") != current_edition or
                metadata.get("archived_pdf") != archive_path.name or
                metadata.get("pdf_sha256") != hashlib.sha256(archive_bytes).hexdigest()):
            return False
        for copy_path in (root / "docs" / f"{STEM}.pdf",
                          root / "wiki/downloads" / f"{STEM}.pdf"):
            if copy_path.exists() and copy_path.read_bytes() != archive_bytes:
                return False
    if repo is not None:
        book = pathlib.Path(repo) / "content/book"
        manifest_path = book / "manifest.json"
        if not manifest_path.exists():
            if any(path.startswith("content/book/") for path in changed_paths):
                return False
        else:
            spec = importlib.util.spec_from_file_location("archive_studio", pathlib.Path(__file__).with_name("studio.py"))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            try:
                manifest = module.load_manifest(pathlib.Path(repo))
                master_bytes = after_master.encode("utf-8")
                if (module.combine(book, manifest) != master_bytes or
                        manifest.get("last_generated_sha256") != module.sha(master_bytes)):
                    return False
                tracked = subprocess.check_output(
                    ["git", "ls-files", "--", "content/book/fragments"],
                    cwd=pathlib.Path(repo), text=True).splitlines()
                declared = {"content/book/" + item["path"] for item in manifest["fragments"]}
                if set(tracked) != declared:
                    return False
            except (OSError, ValueError, KeyError, TypeError):
                return False
    if _editorial_core(before_master) == _editorial_core(after_master):
        return True
    return _matches_generated_release(repo, before_master, after_master, changed_paths)


def classify(candidate_version, main_version, archived_pdf, candidate_pdf):
    """Return a code; archived_pdf=None means the edition is not on main."""
    if archived_pdf is not None:
        return 10 if archived_pdf == candidate_pdf else 20
    if version_key(main_version) > version_key(candidate_version):
        return 21
    return 0


def open_archive_pr_numbers(prs, candidate_version):
    """Find open archive PRs for exactly this edition (not similar labels)."""
    title = f"Archive edition {candidate_version} PDF and metadata"
    return sorted(
        pr["number"] for pr in prs
        if isinstance(pr, dict)
        and pr.get("title") == title
        and isinstance(pr.get("number"), int)
    )


def check_open_archive_prs(repo, candidate_version):
    """Fail closed when GitHub can't confirm an unclaimed edition."""
    result = subprocess.run(
        ["gh", "pr", "list", "--base", "main", "--state", "open",
         "--limit", "200", "--json", "number,title"],
        cwd=repo, capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "Cannot inspect open archive PRs: " + result.stderr.strip()
        )
    try:
        prs = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError("GitHub returned invalid PR JSON") from exc
    if not isinstance(prs, list):
        raise ValueError("GitHub returned an invalid open-PR list")
    existing = open_archive_pr_numbers(prs, candidate_version)
    if existing:
        labels = ", ".join(f"#{number}" for number in existing)
        print(
            f"::error::Archive edition {candidate_version} already has an OPEN PR "
            f"({labels}). Do not create another. Review/merge the existing PR "
            "or publish new content under a later edition.",
            file=sys.stderr,
        )
        return 23
    print(f"ARCHIVE_GUARD: no competing open PR for edition {candidate_version}")
    return 0


def git_show(repo, ref, path, missing_ok=False):
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"], cwd=repo,
        capture_output=True, check=False,
    )
    if result.returncode != 0:
        if missing_ok and b"exists on disk, but not in" in result.stderr:
            return None
        if missing_ok and b"does not exist in" in result.stderr:
            return None
        if missing_ok and b"exists in working tree, but not in" in result.stderr:
            return None
        raise RuntimeError(
            f"Cannot read {ref}:{path}: {result.stderr.decode(errors='replace').strip()}"
        )
    return result.stdout


def check(repo, main_ref):
    candidate_version = edition((repo / f"{STEM}.md").read_text(encoding="utf-8"))
    path = f"docs/{STEM}_{candidate_version}.pdf"
    pdf = (repo / path).read_bytes()
    if len(pdf) < 50_000:
        raise ValueError("Staged archive PDF missing or unexpectedly small")
    main_version = edition(git_show(repo, main_ref, f"{STEM}.md").decode("utf-8"))
    archived = git_show(repo, main_ref, path, missing_ok=True)
    decision = classify(candidate_version, main_version, archived, pdf)
    if decision == 10:
        print(f"ARCHIVE_GUARD: {candidate_version} already exists on main with identical bytes; no PR needed")
    elif decision == 20:
        print(
            f"::error::Archive edition {candidate_version} already exists on main "
            "with DIFFERENT PDF bytes. This run is stale; do not overwrite immutable history. "
            "Publish the intervening changes as a new edition.",
            file=sys.stderr,
        )
    elif decision == 21:
        print(
            f"::error::Staged edition {candidate_version} is older than main edition "
            f"{main_version}. Refusing a superseded archive PR.",
            file=sys.stderr,
        )
    else:
        print(f"ARCHIVE_GUARD: edition {candidate_version} is not archived on main; PR may be created")
    return decision


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--main-ref", default="refs/remotes/origin/main")
    parser.add_argument("--check-open-prs", action="store_true")
    parser.add_argument("--classify-archive-only", action="store_true")
    args = parser.parse_args()
    try:
        repo = pathlib.Path(args.repo).resolve()
        if args.classify_archive_only:
            changed = subprocess.check_output(
                ["git", "diff", "--name-only", f"{args.main_ref}...HEAD"],
                cwd=repo, text=True).splitlines()
            before = git_show(repo, args.main_ref, f"{STEM}.md").decode("utf-8")
            after = (repo / f"{STEM}.md").read_text(encoding="utf-8")
            result = is_archive_only(changed, before, after, repo=repo)
            print("true" if result else "false")
            return 0
        decision = check(repo, args.main_ref)
        if decision == 0 and args.check_open_prs:
            candidate = edition((repo / f"{STEM}.md").read_text(encoding="utf-8"))
            return check_open_archive_prs(repo, candidate)
        return decision
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"::error::Archive preflight failed: {exc}", file=sys.stderr)
        return 22


if __name__ == "__main__":
    sys.exit(main())
