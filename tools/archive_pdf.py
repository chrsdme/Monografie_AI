#!/usr/bin/env python3
"""Arhiveaza editii PDF imuabile in docs/, mentinand PDF-ul curent in Pages."""
import argparse
import hashlib
import json
import pathlib
import re
import shutil

STEM = "Monografie_AI_De_la_Chat_la_Sisteme_Agentice"


def edition_from_master(text):
    match = re.search(r'^edition: "([0-9]+(?:\.[0-9]+){1,2})"$', text, re.M)
    if not match:
        raise ValueError("Versiune lipsa sau invalida in Markdown")
    return match.group(1)


def version_key(path):
    version = path.stem.removeprefix(STEM + "_")
    return tuple(int(v) for v in version.split("."))


def archive(repo, reuse_existing=False):
    docs = repo / "docs"
    docs.mkdir(exist_ok=True)
    version = edition_from_master((repo / (STEM + ".md")).read_text(encoding="utf-8"))
    rendered = repo / (STEM + ".pdf")
    if not rendered.exists() or rendered.stat().st_size < 50_000:
        raise ValueError("PDF generat lipsa sau invalid")
    archived = docs / f"{STEM}_{version}.pdf"
    if archived.exists():
        if archived.read_bytes() != rendered.read_bytes():
            raise ValueError(f"Editia {version} exista deja si difera! Nu suprascriem arhiva.")
        print(f"ARCHIVE: editia {version} exista; fisierul istoric ramane imuabil")
    else:
        shutil.copyfile(rendered, archived)
        print(f"ARCHIVE: editie noua {archived.name}")
    for file in (
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
