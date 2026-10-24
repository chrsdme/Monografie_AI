#!/usr/bin/env python3
"""Arhiveaza editii PDF imuabile in docs/, mentinand PDF-ul curent in Pages."""
import argparse
import hashlib
import importlib.util
import json
import pathlib
import re
import shutil
import subprocess

STEM = "Monografie_AI_De_la_Chat_la_Sisteme_Agentice"


def edition_from_master(text):
    match = re.search(r'^edition: "([0-9]+(?:\.[0-9]+){1,2})"$', text, re.M)
    if not match:
        raise ValueError("Versiune lipsa sau invalida in Markdown")
    return match.group(1)


def version_key(path):
    version = path.stem.removeprefix(STEM + "_")
    return tuple(int(v) for v in version.split("."))


def _verify_reuse_provenance(repo, version, archived):
    """Require a committed archive and byte-identical committed book sources."""
    master_path = repo / (STEM + ".md")
    manifest_path = repo / "content/book/manifest.json"
    metadata_path = repo / "docs/.publication.json"
    try:
        master_bytes = master_path.read_bytes()
        manifest_bytes = manifest_path.read_bytes()
        metadata_bytes = metadata_path.read_bytes()
        archive_bytes = archived.read_bytes()
        metadata = json.loads(metadata_bytes.decode("utf-8"))
        manifest = json.loads(manifest_bytes.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("Provenienta arhivei existente nu poate fi verificata") from exc

    expected_name = f"{STEM}_{version}.pdf"
    digest = hashlib.sha256(archive_bytes).hexdigest()
    if (not isinstance(manifest, dict) or not isinstance(metadata, dict) or
            len(archive_bytes) < 50_000 or metadata.get("edition") != version or
            metadata.get("archived_pdf") != expected_name or
            metadata.get("pdf_sha256") != digest):
        raise ValueError("Metadatele sau hash-ul arhivei istorice sunt invalide")

    studio_spec = importlib.util.spec_from_file_location(
        "archive_reuse_studio", pathlib.Path(__file__).with_name("studio.py"))
    studio = importlib.util.module_from_spec(studio_spec)
    studio_spec.loader.exec_module(studio)
    manifest = studio.load_manifest(repo)
    if (manifest.get("source") != STEM + ".md" or
            manifest.get("last_generated_sha256") != hashlib.sha256(master_bytes).hexdigest()):
        raise ValueError("Manifestul nu corespunde manuscrisului curent")
    if studio.combine(repo / "content/book", manifest) != master_bytes:
        raise ValueError("Fragmentele nu corespund manuscrisului curent")

    source_paths = [STEM + ".md", "content/book/manifest.json",
                    "docs/.publication.json", f"docs/{expected_name}"]
    source_paths.extend("content/book/" + item["path"] for item in manifest["fragments"])
    try:
        status = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all", "--",
             STEM + ".md", "content/book", "docs/.publication.json", f"docs/{expected_name}"],
            cwd=repo, text=True, capture_output=True, check=True)
        if status.stdout:
            raise ValueError("Surse editoriale sau provenienta arhivei au modificari neversionate")
        tracked_fragments = subprocess.run(
            ["git", "ls-files", "--", "content/book/fragments"], cwd=repo,
            text=True, capture_output=True, check=True).stdout.splitlines()
        declared_fragments = {"content/book/" + item["path"] for item in manifest["fragments"]}
        if set(tracked_fragments) != declared_fragments:
            raise ValueError("Setul de fragmente versionate difera de manifest")
        for relative in source_paths:
            subprocess.run(["git", "ls-files", "--error-unmatch", "--", relative],
                           cwd=repo, text=True, capture_output=True, check=True)
            committed = subprocess.run(
                ["git", "show", f"HEAD:{relative}"], cwd=repo,
                capture_output=True, check=True).stdout
            if committed != (repo / relative).read_bytes():
                raise ValueError("Sursele versionate difera de fisierele curente")
    except subprocess.CalledProcessError as exc:
        raise ValueError("Arhiva si sursele nu au provenienta Git verificabila") from exc


def archive(repo, reuse_existing=False):
    docs = repo / "docs"
    docs.mkdir(exist_ok=True)
    version = edition_from_master((repo / (STEM + ".md")).read_text(encoding="utf-8"))
    rendered = repo / (STEM + ".pdf")
    if not rendered.exists() or rendered.stat().st_size < 50_000:
        raise ValueError("PDF generat lipsa sau invalid")
    archived = docs / f"{STEM}_{version}.pdf"
    if archived.exists():
        if reuse_existing:
            _verify_reuse_provenance(repo, version, archived)
            print(f"ARCHIVE: reutilizez editia {version} verificata; arhiva ramane imuabila")
        elif archived.read_bytes() != rendered.read_bytes():
            raise ValueError(f"Editia {version} exista deja si difera! Nu suprascriem arhiva.")
        else:
            print(f"ARCHIVE: editia {version} exista; fisierul istoric ramane imuabil")
    else:
        shutil.copyfile(rendered, archived)
        print(f"ARCHIVE: editie noua {archived.name}")
    for file in (
        rendered,
        docs / (STEM + ".pdf"),
        repo / "wiki/downloads" / (STEM + ".pdf"),
        repo / "site/downloads" / (STEM + ".pdf")
    ):
        file.parent.mkdir(parents=True, exist_ok=True)
        if file.resolve() != archived.resolve():
            shutil.copyfile(archived, file)
        if file.read_bytes() != archived.read_bytes():
            raise AssertionError("Copie PDF diferita: " + str(file))
    manifest = {
        "edition": version,
        "pdf_sha256": hashlib.sha256(archived.read_bytes()).hexdigest(),
        "archived_pdf": archived.name,
    }
    (docs / ".publication.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    copies = sorted(docs.glob(STEM + "_*.pdf"), key=version_key, reverse=True)
    lines = [
        "<!-- ARCHIVE:START -->",
        "## Arhiva editiilor PDF",
        "",
        f"[Descarca PDF-ul curent]({STEM}.pdf) (editia {version}).",
        "",
        "Fisierele cu numar de editie sunt arhive stabile: nu sunt suprascrise.",
        "",
    ]
    for file in copies:
        v = file.stem.removeprefix(STEM + "_")
        lines.append(f"- [Editia {v}]({file.name})")
    lines.append("<!-- ARCHIVE:END -->")
    readme = docs / "README.md"
    text = readme.read_text(encoding="utf-8") if readme.exists() else "# Materiale suplimentare\n\n"
    block = "\n".join(lines)
    if "<!-- ARCHIVE:START -->" in text and "<!-- ARCHIVE:END -->" in text:
        text = re.sub(r"<!-- ARCHIVE:START -->.*?<!-- ARCHIVE:END -->",
                      lambda _: block, text, flags=re.S)
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    readme.write_text(text.rstrip() + "\n", encoding="utf-8")
    print(f"ARCHIVE: {len(copies)} editii; PDF curent si site verificate")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--reuse-existing", action="store_true")
    args = ap.parse_args()
    archive(pathlib.Path(args.repo).resolve(), args.reuse_existing)


if __name__ == "__main__":
    main()
