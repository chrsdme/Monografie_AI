#!/usr/bin/env python3
"""Local-only Monografie Studio bootstrap: no network, push, merge or deploy."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
MASTER = "Monografie_AI_De_la_Chat_la_Sisteme_Agentice.md"
BOOK = Path("content/book")
KINDS = {"article": ("ART", "articles"), "resource": ("RES", "resources"),
         "correction": ("FIX", "corrections"), "idea": ("IDEA", "ideas")}
TARGETS = {"wiki", "book", "resource"}
ACTIONS = {"propose_article", "propose_resource", "propose_integration",
           "research_only", "correction", "defer"}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stop(message: str):
    raise ValueError(message)


def branch(root: Path) -> str:
    p = subprocess.run(["git", "branch", "--show-current"], cwd=root,
                       text=True, capture_output=True, check=False)
    return p.stdout.strip() if p.returncode == 0 else "unknown"


def writable(root: Path):
    if branch(root) == "main":
        stop("Nu modifica main cu Studio. Foloseste ramura studio-test.")


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9_-]+", "-", text.lower()).strip("-")[:40] or "intro"


def split_bytes(raw: bytes) -> list[tuple[str, int, bytes]]:
    """Lossless UTF-8 heading split, ignoring Markdown fenced code."""
    lines = raw.decode("utf-8").splitlines(keepends=True)
    if not lines:
        stop("Manuscris gol")
    markers = [(0, "prolog", 0)]
    fence = None
    for index, line in enumerate(lines):
        f = re.match(r"^\s{0,3}(\x60{3,}|~{3,})", line)
        if f:
            marker = f.group(1)
            if fence is None:
                fence = marker[0], len(marker)
            elif marker[0] == fence[0] and len(marker) >= fence[1]:
                fence = None
            continue
        header = re.match(r"^(#{1,4})[ \t]+(.+?)\s*(?:\r?\n)?$", line)
        if fence is None and header and index:
            markers.append((index, header.group(2).strip(), len(header.group(1))))
    chunks = []
    for n, (start, title, level) in enumerate(markers):
        end = markers[n + 1][0] if n + 1 < len(markers) else len(lines)
        blob = "".join(lines[start:end]).encode("utf-8")
        if blob:
            chunks.append((title, level, blob))
    if b"".join(chunk[2] for chunk in chunks) != raw:
        stop("Migrarea nu este byte-identica")
    return chunks


def load_manifest(root: Path) -> dict:
    p = root / BOOK / "manifest.json"
    if not p.exists():
        stop("Nu exista manifest. Foloseste migrate.")
    data = json.loads(p.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("fragments"), list):
        stop("Schema manifestului nu este acceptata")
    return data


def combine(folder: Path, manifest: dict) -> bytes:
    output = bytearray()
    ids, paths = set(), set()
    allowed = (folder / "fragments").resolve()
    if not manifest["fragments"]:
        stop("Manifest fara fragmente")
    for item in manifest["fragments"]:
        ident, relative = item.get("id"), item.get("path")
        if not isinstance(ident, str) or not re.fullmatch(r"BOOK-\d{4,}", ident):
            stop("ID invalid")
        if not isinstance(relative, str):
            stop("Cale invalida")
        path = (folder / relative).resolve()
        if ident in ids or path in paths:
            stop("Identitate duplicata")
        if not path.is_relative_to(allowed) or not path.is_file() or path.suffix != ".md":
            stop("Fragment lipsa sau nesigur: " + relative)
        ids.add(ident)
        paths.add(path)
        blob = path.read_bytes()
        blob.decode("utf-8")
        output.extend(blob)
    return bytes(output)


def migrate(root: Path):
    writable(root)
    target = root / BOOK
    if target.exists():
        stop("content/book exista deja, migrarea nu suprascrie fisierele.")
    original = (root / MASTER).read_bytes()
    chunks = split_bytes(original)
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=target.parent, prefix=".book-migrate-") as temporary:
        folder = Path(temporary)
        (folder / "fragments").mkdir()
        entries = []
        for n, (title, level, blob) in enumerate(chunks, 1):
            ident = f"BOOK-{n:04d}"
            relative = f"fragments/{ident}-{slug(title)}.md"
            (folder / relative).write_bytes(blob)
            entries.append({"id": ident, "path": relative, "heading_level": level,
                            "title_at_migration": title, "baseline_sha256": sha(blob)})
        manifest = {"schema_version": 1, "source": MASTER,
                    "original_sha256": sha(original), "last_generated_sha256": sha(original),
                    "fragments": entries}
        (folder / "manifest.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if combine(folder, manifest) != original:
            stop("Round-trip invalid, manuscrisul ramane neatins.")
        folder.rename(target)
    print(f"PASS MIGRATION: {len(entries)} fragmente; SHA256={sha(original)}")


def assemble(root: Path, write: bool):
    manifest = load_manifest(root)
    body = combine(root / BOOK, manifest)
    master = root / MASTER
    existing = master.read_bytes()
    if not write:
        if body != existing:
            stop(f"DIFF: fragmente={sha(body)}, master={sha(existing)}")
        print(f"PASS ROUND-TRIP: {sha(body)}")
        return
    writable(root)
    if sha(existing) != manifest.get("last_generated_sha256"):
        stop("Master modificat extern: nu suprascriem fara reconciliere.")
    if body != existing:
        handle, filename = tempfile.mkstemp(dir=root, prefix=".studio-master-")
        try:
            with os.fdopen(handle, "wb") as out:
                out.write(body)
            os.replace(filename, master)
        finally:
            if os.path.exists(filename):
                os.unlink(filename)
    manifest["last_generated_sha256"] = sha(body)
    (root / BOOK / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"PASS ASSEMBLY: {sha(body)}")


def new(root: Path, kind: str, title: str):
    writable(root)
    prefix, directory = KINDS[kind]
    destination = root / "content" / directory / (slug(title) + ".md")
    if destination.exists():
        stop("Fisier existent: " + str(destination))
    template = (root / "studio/templates" / f"{kind}.md").read_text(encoding="utf-8")
    year = datetime.now().year
    numbers = []
    if destination.parent.is_dir():
        for path in destination.parent.glob("*.md"):
            match = re.search(rf'^id:\s*["\x27]?{prefix}-{year}-(\d+)',
                              path.read_text(encoding="utf-8"), re.M)
            if match:
                numbers.append(int(match.group(1)))
    ident = f"{prefix}-{year}-{max(numbers, default=0) + 1:03d}"
    template = re.sub(r'^id:.*$', f'id: "{ident}"', template, count=1, flags=re.M)
    template = re.sub(r'^title:.*$', "title: " + json.dumps(title, ensure_ascii=False),
                      template, count=1, flags=re.M)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(template, encoding="utf-8")
    print(f"CREATED {destination.relative_to(root)} [{ident}] status=draft")


def plan(root: Path, name: str):
    try:
        import yaml
    except ImportError as e:
        raise RuntimeError("Instaleaza PyYAML din tools/requirements.txt") from e
    inbox = (root / "inbox").resolve()
    batch = (root / name).resolve()
    if not batch.is_relative_to(inbox):
        stop("Manifestul trebuie sa fie in inbox/")
    data = yaml.safe_load(batch.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1 or data.get("owner_approval") != "required":
        stop("Schema sau aprobare invalida")
    if not isinstance(data.get("items"), list) or not data["items"]:
        stop("Batch gol")
    seen = set()
    rows = []
    for item in data["items"]:
        ident = item.get("id")
        file = (inbox / str(item.get("file", ""))).resolve()
        targets = item.get("targets", [])
        if not isinstance(ident, str) or ident in seen or not file.is_relative_to(inbox) or not file.is_file():
            stop(f"Material invalid: {ident}")
        if item.get("action") not in ACTIONS or not isinstance(targets, list) or any(t not in TARGETS for t in targets):
            stop(f"Actiune/targets invalide: {ident}")
        if "book" in targets and not item.get("book_section_id"):
            stop(f"Fara book_section_id: {ident}")
        seen.add(ident)
        rows.append({"id": ident, "file": str(file.relative_to(inbox)), "sha256": sha(file.read_bytes()),
                     "action": item["action"], "targets": targets, "status": "PENDING"})
    dest = root / ".studio-local/plans" / (slug(str(data.get("batch_id", "batch"))) + ".json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        stop("Planul exista deja, refuz suprascriere")
    dest.write_text(json.dumps({"batch_id": data.get("batch_id"), "approved": False,
                                "items": rows}, indent=2) + "\n", encoding="utf-8")
    print(f"PASS PLAN ONLY: {len(rows)} materiale, {dest.relative_to(root)}")


def run(root: Path, command: list[str]):
    print("RUN:", " ".join(command), flush=True)
    subprocess.run(command, cwd=root, check=True)


def build(root: Path, pdf: bool):
    assemble(root, write=True)
    command = [sys.executable, "tools/build.py", "--repo", ".", "--toc", "--wiki"]
    if pdf:
        command.append("--pdf")
    run(root, command)
    run(root, [sys.executable, "-m", "mkdocs", "build", "--strict"])
    run(root, [sys.executable, "tools/check_site_links.py", "--site", "site"])
    print("PASS local build, fara publicare")


def main() -> int:
    p = argparse.ArgumentParser(description="Monografie Studio offline bootstrap")
    p.add_argument("--repo", default=str(ROOT))
    subs = p.add_subparsers(dest="command", required=True)
    subs.add_parser("migrate")
    subs.add_parser("status")
    a = subs.add_parser("assemble")
    a.add_argument("--write", action="store_true")
    a = subs.add_parser("new")
    a.add_argument("kind", choices=sorted(KINDS))
    a.add_argument("title")
    a = subs.add_parser("plan")
    a.add_argument("--batch", default="inbox/zzz.yaml")
    a = subs.add_parser("build")
    a.add_argument("--pdf", action="store_true")
    subs.add_parser("preview")
    subs.add_parser("check")
    args = p.parse_args()
    root = Path(args.repo).resolve()
    try:
        if not (root / MASTER).is_file():
            stop("Lipseste manuscrisul canonic")
        if args.command == "migrate":
            migrate(root)
        elif args.command == "assemble":
            assemble(root, write=args.write)
        elif args.command == "new":
            new(root, args.kind, args.title)
        elif args.command == "plan":
            plan(root, args.batch)
        elif args.command == "status":
            print("Branch:", branch(root))
            print("Migrated:", (root / BOOK / "manifest.json").exists())
            print("Master SHA256:", sha((root / MASTER).read_bytes()))
        elif args.command in ("build", "preview", "check"):
            build(root, pdf=args.command == "check" or getattr(args, "pdf", False))
            if args.command == "preview":
                run(root, [sys.executable, "-m", "mkdocs", "serve",
                           "--dev-addr", "127.0.0.1:8000"])
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError, UnicodeDecodeError) as err:
        print(f"STUDIO ERROR: {err}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
