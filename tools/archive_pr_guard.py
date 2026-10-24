#!/usr/bin/env python3
"""Reject stale and conflicting PDF archive submissions before creating a PR.

Exit codes: 0 = safe to propose, 10 = identical edition already archived,
20 = same edition with different PDF (collision), 21 = superseded release,
23 = competing archive PR already open.
"""
import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

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


def _matches_generated_release(repo, before_master, after_master, changed_paths,
                               source_ref=None, explain=None):
    """Replay release.py from the exact main commit that triggered publication."""
    if repo is None:
        return False
    root = pathlib.Path(repo)
    master_path = f"{STEM}.md"
    details = explain if explain is not None else {}
    details.setdefault("release_reconstruction", {})
    report = details["release_reconstruction"]
    try:
        old_edition = edition(before_master)
        new_edition = edition(after_master)
        release_spec = importlib.util.spec_from_file_location(
            "archive_release_for_guard", pathlib.Path(__file__).with_name("release.py"))
        release = importlib.util.module_from_spec(release_spec)
        release_spec.loader.exec_module(release)
        report.update({"previous_edition": old_edition, "current_edition": new_edition,
                       "expected_patch_edition": release.next_patch(old_edition),
                       "source_ref": source_ref, "candidates": [], "validated_candidates": 0})
        if release.next_patch(old_edition) != new_edition:
            report["result"] = "edition is not the next patch version"
            return False
        resolved_source = None
        if source_ref is not None:
            resolved_source = subprocess.check_output(
                ["git", "rev-parse", source_ref], cwd=root, text=True).strip()
            report["resolved_source_ref"] = resolved_source
        date = release.field(after_master, "date")
        # --full-history prevents path simplification at merge commits from
        # hiding the staged release commit on the archive PR's second parent.
        commits = subprocess.check_output(
            ["git", "log", "--full-history", "--format=%H", "HEAD", "--", master_path],
            cwd=root, text=True).splitlines()
        report["git_log_candidates"] = commits
        matches = 0
        for release_commit in commits:
            item = {"commit": release_commit}
            report["candidates"].append(item)
            parents = subprocess.check_output(
                ["git", "rev-list", "--parents", "-n", "1", release_commit],
                cwd=root, text=True).split()
            item["parents"] = parents[1:]
            if len(parents) != 2:
                item["result"] = "merge/root commit is not a staged release commit"
                continue
            source_commit = parents[1]
            item["source_commit"] = source_commit
            if git_show(root, release_commit, master_path) != after_master.encode("utf-8"):
                item["result"] = "candidate manuscript does not equal archive manuscript"
                continue
            if git_show(root, source_commit, master_path) != before_master.encode("utf-8"):
                item["result"] = "source commit manuscript does not equal main baseline"
                continue
            if resolved_source is not None and source_commit != resolved_source:
                item["result"] = "release parent is not the supplied main ref"
                continue

            # The source commit may itself be a PR merge. Use its first parent
            # as the source diff, matching the publication workflow's HEAD^.
            source_parents = subprocess.check_output(
                ["git", "rev-list", "--parents", "-n", "1", source_commit],
                cwd=root, text=True).split()
            if len(source_parents) < 2:
                item["result"] = "source history is incomplete"
                continue
            source_parent = source_parents[1]
            item["source_parent"] = source_parent
            source_paths = subprocess.check_output(
                ["git", "diff", "--name-only", source_parent, source_commit],
                cwd=root, text=True).splitlines()
            item["source_paths"] = source_paths
            if not source_paths:
                item["result"] = "source commit has no changed paths"
                continue
            message = subprocess.check_output(
                ["git", "log", "-1", "--format=%B", source_commit],
                cwd=root, text=True)
            path_variants = [source_paths]
            if any(path == "content/book" or path.startswith("content/book/")
                   for path in source_paths) and master_path not in source_paths:
                path_variants.append(source_paths + [master_path])
            for release_paths in path_variants:
                item["reconstructed_paths"] = release_paths
                expected = release.update_text(
                    before_master, old_edition, new_edition, date, release_paths,
                    message, source_commit)
                item["reconstruction_matches"] = (
                    expected.encode("utf-8") == after_master.encode("utf-8"))
                if item["reconstruction_matches"]:
                    matches += 1
                    item["result"] = "validated"
                    break
            if item.get("result") != "validated":
                item["result"] = "release.update_text reconstruction differs"
        report["validated_candidates"] = matches
        report["result"] = "exactly one candidate validated" if matches == 1 else (
            f"expected one validated candidate, found {matches}")
        return matches == 1
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError,
            UnicodeError, AttributeError, TypeError) as exc:
        report["error"] = str(exc)
        report.setdefault("validated_candidates", 0)
        return False


def _wiki_changes_match_generated(repo, after_master, changed_paths, explain,
                                  source_ref=None):
    """Rebuild changed wiki pages in a temporary tree and compare exact bytes."""
    wiki_paths = [path for path in changed_paths
                  if path.startswith("wiki/") and path.endswith(".md")]
    if not wiki_paths:
        explain["checks"]["wiki_rendering"] = {"passed": True, "checked": []}
        return True
    root = pathlib.Path(repo)
    try:
        with tempfile.TemporaryDirectory(prefix="archive-wiki-check-") as temp:
            expected_root = pathlib.Path(temp)
            master_path = expected_root / f"{STEM}.md"
            master_path.write_bytes(after_master.encode("utf-8"))
            index = root / "wiki/index.md"
            if source_ref is not None:
                baseline_index = git_show(root, source_ref, "wiki/index.md", missing_ok=True)
            else:
                baseline_index = index.read_bytes() if index.exists() else None
            if baseline_index is not None:
                (expected_root / "wiki").mkdir(parents=True, exist_ok=True)
                (expected_root / "wiki/index.md").write_bytes(baseline_index)
            source_figures = root / "Monografie_AI_figuri"
            if source_figures.exists():
                shutil.copytree(source_figures, expected_root / "Monografie_AI_figuri")
            spec = importlib.util.spec_from_file_location(
                "archive_build_for_guard", pathlib.Path(__file__).with_name("build.py"))
            build = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(build)
            _, front_matter, _ = build.read_master(master_path)
            with contextlib.redirect_stdout(io.StringIO()):
                build.build_wiki(expected_root, master_path, front_matter)
            results = {}
            for relative in wiki_paths:
                actual = root / relative
                expected = expected_root / relative
                same = expected.is_file() and actual.is_file() and expected.read_bytes() == actual.read_bytes()
                results[relative] = {"matches_generated_bytes": same,
                                     "generated": expected.is_file(),
                                     "present": actual.is_file()}
            passed = all(item["matches_generated_bytes"] for item in results.values())
            explain["checks"]["wiki_rendering"] = {"passed": passed, "files": results}
            return passed
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError,
            UnicodeError, AttributeError, TypeError) as exc:
        explain["checks"]["wiki_rendering"] = {"passed": False, "error": str(exc)}
        return False


def _archive_only_report(changed_paths, before_master, after_master, repo=None,
                         source_ref=None):
    """Accept only a release persistence diff whose editorial body is unchanged."""
    allowed_exact = {f"{STEM}.md", "docs/README.md", "docs/.publication.json",
                     "wiki/index.md", f"wiki/downloads/{STEM}.pdf",
                     "wiki/introducere.md", f"docs/{STEM}.pdf"}
    allowed_prefix = ("content/book/fragments/",)
    exact = sorted(allowed_exact | {"content/book/manifest.json"})
    prefixes = list(allowed_prefix) + ["wiki/partea-", "wiki/anexe/"]
    report = {"archive_only": False, "changed_paths": list(changed_paths),
              "allowed_paths": {"exact": exact, "prefixes": prefixes},
              "checks": {}, "rejection_reasons": []}
    disallowed = []
    for path in changed_paths:
        allowed = (path in allowed_exact or path == "content/book/manifest.json" or
                   path.startswith(allowed_prefix) or
                   (path.startswith(("wiki/partea-", "wiki/anexe/")) and path.endswith(".md")) or
                   re.fullmatch(rf"docs/{re.escape(STEM)}_[0-9]+(?:\.[0-9]+){{1,2}}\.pdf", path))
        if not allowed:
            disallowed.append(path)
    report["checks"]["allowed_paths"] = {"passed": not disallowed,
                                               "disallowed": disallowed}
    if disallowed:
        report["rejection_reasons"].append(
            "changed path is not on the archive allowlist: " + ", ".join(disallowed))
    if not changed_paths:
        report["rejection_reasons"].append("no changed paths")
    try:
        old_edition = edition(before_master)
        current_edition = edition(after_master)
        report["editions"] = {"previous": old_edition, "current": current_edition}
    except ValueError as exc:
        report["rejection_reasons"].append(str(exc))
        current_edition = None
    if current_edition is not None:
        required_paths = ["docs/.publication.json", f"docs/{STEM}_{current_edition}.pdf"]
        missing = [path for path in required_paths if path not in changed_paths]
        report["checks"]["required_archive_paths"] = {"passed": not missing,
                                                            "missing": missing}
        if missing:
            report["rejection_reasons"].append(
                "required archive paths are absent: " + ", ".join(missing))
    if repo is not None:
        root = pathlib.Path(repo)
        metadata_path = root / "docs/.publication.json"
        archive_path = root / f"docs/{STEM}_{current_edition}.pdf" if current_edition else None
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            archive_bytes = archive_path.read_bytes() if archive_path else b""
            archive_hash = hashlib.sha256(archive_bytes).hexdigest()
            metadata_ok = (archive_path is not None and isinstance(metadata, dict) and
                           metadata.get("edition") == current_edition and
                           metadata.get("archived_pdf") == archive_path.name and
                           metadata.get("pdf_sha256") == archive_hash and len(archive_bytes) >= 50_000)
            report["pdf"] = {"path": archive_path.relative_to(root).as_posix() if archive_path else None,
                             "sha256": archive_hash, "bytes": len(archive_bytes)}
            report["metadata"] = metadata
            report["checks"]["metadata_and_pdf_hash"] = {"passed": metadata_ok}
            if not metadata_ok:
                report["rejection_reasons"].append(
                    "publication metadata does not verify the current archived PDF")
        except (OSError, json.JSONDecodeError) as exc:
            report["checks"]["metadata_and_pdf_hash"] = {"passed": False, "error": str(exc)}
            report["rejection_reasons"].append("publication metadata or archived PDF is missing/invalid")

        # The two published current-PDF mirrors must retain the exact archived bytes.
        mirrors = [f"docs/{STEM}.pdf", f"wiki/downloads/{STEM}.pdf"]
        mirror_results = {}
        for relative in mirrors:
            try:
                mirror_bytes = (root / relative).read_bytes()
                mirror_results[relative] = {
                    "exists": True, "sha256": hashlib.sha256(mirror_bytes).hexdigest(),
                    "matches_archive": bool(archive_path and mirror_bytes == archive_bytes)}
            except OSError:
                mirror_results[relative] = {"exists": False, "matches_archive": False}
        report["pdf_copies"] = mirror_results
        # A checkout used for the early classification step may not contain
        # ignored/generated mirrors yet. Existing mirrors must match; archive_pdf
        # verifies and materializes them after this classification.
        checked_copies = [path for path, value in mirror_results.items() if value["exists"]]
        absent_copies = [path for path, value in mirror_results.items() if not value["exists"]]
        copies_ok = all(mirror_results[path]["matches_archive"] for path in checked_copies)
        report["checks"]["pdf_copies"] = {
            "passed": copies_ok, "verified": checked_copies, "not_materialized": absent_copies}
        if not copies_ok:
            report["rejection_reasons"].append("one or more current PDF copies differ from the archive")

        book = pathlib.Path(repo) / "content/book"
        manifest_path = book / "manifest.json"
        if not manifest_path.exists():
            consistent = not any(path.startswith("content/book/") for path in changed_paths)
            report["checks"]["manifest_fragments_manuscript"] = {
                "passed": consistent, "present": False}
        else:
            spec = importlib.util.spec_from_file_location("archive_studio", pathlib.Path(__file__).with_name("studio.py"))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            try:
                manifest = module.load_manifest(pathlib.Path(repo))
                master_bytes = after_master.encode("utf-8")
                round_trip = module.combine(book, manifest) == master_bytes
                digest_matches = (manifest.get("last_generated_sha256") ==
                                  hashlib.sha256(master_bytes).hexdigest())
                tracked = subprocess.check_output(
                    ["git", "ls-files", "--", "content/book/fragments"],
                    cwd=root, text=True).splitlines()
                declared = {"content/book/" + item["path"] for item in manifest["fragments"]}
                fragments_match = set(tracked) == declared
                consistent = round_trip and digest_matches and fragments_match
                report["checks"]["manifest_fragments_manuscript"] = {
                    "passed": consistent, "source": manifest.get("source"),
                    "fragment_count": len(manifest.get("fragments", [])),
                    "round_trip_matches": round_trip,
                    "manifest_hash_matches": digest_matches,
                    "tracked_fragments_match_manifest": fragments_match,
                    "last_generated_sha256": manifest.get("last_generated_sha256"),
                    "manuscript_sha256": hashlib.sha256(master_bytes).hexdigest()}
            except (OSError, ValueError, KeyError, TypeError) as exc:
                consistent = False
                report["checks"]["manifest_fragments_manuscript"] = {
                    "passed": False, "error": str(exc)}
            if not consistent:
                report["rejection_reasons"].append("manifest/fragments do not reproduce the manuscript")

        if source_ref is None:
            wiki_ok = True
            report["checks"]["wiki_rendering"] = {
                "passed": True, "skipped": "no source ref supplied"}
        else:
            wiki_ok = _wiki_changes_match_generated(
                root, after_master, changed_paths, report, source_ref=source_ref)
        if not wiki_ok:
            report["rejection_reasons"].append("changed wiki Markdown does not match generated manuscript output")
    else:
        report["checks"]["wiki_rendering"] = {"passed": not any(
            path.startswith("wiki/") and path.endswith(".md") for path in changed_paths),
            "reason": "repository unavailable for generated page verification"}
        if not report["checks"]["wiki_rendering"]["passed"]:
            report["rejection_reasons"].append("cannot verify changed wiki pages without repository history")

    core_same = _editorial_core(before_master) == _editorial_core(after_master)
    report["checks"]["editorial_core_unchanged"] = {"passed": core_same}
    provenance = core_same
    if not core_same:
        provenance = _matches_generated_release(
            repo, before_master, after_master, changed_paths,
            source_ref=source_ref, explain=report)
        if not provenance:
            report["rejection_reasons"].append(
                "editorial core changed and release.update_text provenance did not validate")
    report["checks"]["release_provenance"] = {"passed": provenance}
    gates_ok = all(check.get("passed", False) for name, check in report["checks"].items()
                   if name not in {"editorial_core_unchanged", "release_provenance"})
    report["archive_only"] = bool(gates_ok and provenance and not report["rejection_reasons"])
    return report


def is_archive_only(changed_paths, before_master, after_master, repo=None, source_ref=None):
    """Accept only a verified release persistence diff with no independent edits."""
    return _archive_only_report(changed_paths, before_master, after_master,
                                repo=repo, source_ref=source_ref)["archive_only"]


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
    parser.add_argument("--explain", action="store_true",
                        help="print structured diagnostics for archive-only classification")
    args = parser.parse_args()
    try:
        repo = pathlib.Path(args.repo).resolve()
        if args.classify_archive_only or args.explain:
            changed = subprocess.check_output(
                ["git", "diff", "--name-only", args.main_ref, "HEAD"],
                cwd=repo, text=True).splitlines()
            before = git_show(repo, args.main_ref, f"{STEM}.md").decode("utf-8")
            after = (repo / f"{STEM}.md").read_text(encoding="utf-8")
            if args.explain:
                report = _archive_only_report(
                    changed, before, after, repo=repo, source_ref=args.main_ref)
                topology = {}
                for label, ref in (("head", "HEAD"), ("main_ref", args.main_ref)):
                    try:
                        row = subprocess.check_output(
                            ["git", "rev-list", "--parents", "-n", "1", ref],
                            cwd=repo, text=True).strip().split()
                        topology[label] = {"commit": row[0], "parents": row[1:]}
                    except (OSError, subprocess.CalledProcessError) as exc:
                        topology[label] = {"error": str(exc)}
                report["topology"] = topology
                report["main_ref"] = args.main_ref
                print(json.dumps(report, indent=2, sort_keys=True))
                return 0
            result = is_archive_only(changed, before, after, repo=repo,
                                     source_ref=args.main_ref)
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
