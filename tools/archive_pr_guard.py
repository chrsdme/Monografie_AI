#!/usr/bin/env python3
"""Reject stale and conflicting PDF archive submissions before creating a PR.

Exit codes: 0 = safe to propose, 10 = identical edition already archived,
20 = same edition with different PDF (collision), 21 = superseded release,
23 = competing archive PR already open.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

STEM = "Monografie_AI_De_la_Chat_la_Sisteme_Agentice"


def edition(source):
    match = re.search(r'^edition: "([0-9]+(?:\.[0-9]+){1,2})"$',
                      source, re.MULTILINE)
    if not match:
        raise ValueError("Missing or invalid edition in monograph front matter")
    return match.group(1)


def version_key(version):
    return tuple(int(part) for part in version.split("."))


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
    args = parser.parse_args()
    try:
        repo = pathlib.Path(args.repo).resolve()
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
