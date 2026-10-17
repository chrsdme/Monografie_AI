#!/usr/bin/env python3
"""Actualizeaza editia monografiei la publicarea unei modificari in main.

PR-urile sunt doar validate; aceasta operatie ruleaza numai la publicarea main.
O editie noua explicita (de ex. 1.1 -> 1.2) este respectata. Pentru actualizari
ulterioare cresterea este incrementala: 1.2 -> 1.2.1 -> 1.2.2.
"""
import argparse
import datetime
import pathlib
import re
import subprocess
from zoneinfo import ZoneInfo

MASTER = "Monografie_AI_De_la_Chat_la_Sisteme_Agentice.md"
MONTHS = ("ianuarie", "februarie", "martie", "aprilie", "mai", "iunie",
          "iulie", "august", "septembrie", "octombrie", "noiembrie", "decembrie")


def run_git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def field(text, key):
    match = re.search(r'^' + re.escape(key) + r':\s*"([^"]+)"$', text, re.M)
    if not match:
        raise ValueError("Lipseste campul de editie: " + key)
    return match.group(1)


def swap_one(text, pattern, replacement, name):
    text, count = re.subn(pattern, lambda _: replacement, text, count=1, flags=re.M)
    if count != 1:
        raise ValueError("Actualizare nesigura; marcaj lipsa: " + name)
    return text


def next_patch(version):
    parts = version.split(".")
    if len(parts) not in (2, 3) or any(not p.isdigit() for p in parts):
        raise ValueError("Versiune invalida: " + version)
    if len(parts) == 2:
        return version + ".1"
    return ".".join(parts[:2] + [str(int(parts[2]) + 1)])


def slug(title):
    return re.sub(r"[^a-z0-9 _-]", "", title.lower()).replace(" ", "-")


def changelog_changes(changed, message, sha):
    descriptions = []
    if MASTER in changed:
        descriptions.append("Continutul monografiei: modificari ale sursei Markdown canonice.")
    if any(p.startswith("wiki/") for p in changed):
        descriptions.append("Documentatia web: pagini sau legaturi actualizate.")
    if any(p.startswith("Monografie_AI_figuri/") for p in changed):
        descriptions.append("Ilustratii: modificari ale figurilor.")
    if any(p.startswith("tools/") or p.startswith(".github/workflows/") for p in changed):
        descriptions.append("Publicare si verificari: modificari ale instrumentelor si pipeline-ului.")
    if any(p.startswith("docs/") and not p.endswith(".pdf") for p in changed):
        descriptions.append("Materiale suplimentare: actualizari in directorul docs.")
    if not descriptions:
        descriptions.append("Actualizare a materialelor proiectului.")
    label = next((line.strip() for line in message.splitlines()
                  if line.strip() and not line.startswith("Merge pull request")), "Actualizare editoriala")
    label = re.sub(r"\s+", " ", label).encode("ascii", "ignore").decode("ascii").replace("*", "").strip()[:180]
    return (f"- **Origine:** commitul \`{sha[:12]}\`; mesaj: {label}.\n" +
            "".join(f"- {line}\n" for line in descriptions) +
            "- **Nota:** aceasta lista este generata din fisierele modificate; "
            "detaliile editoriale se verifica in diff-ul commitului indicat.\n")


def update_text(text, previous, edition, date, changed, message, sha):
    changelogs = [int(n) for n in re.findall(r"^## E\.(\d+)\.", text, re.M)]
    n = max(changelogs, default=0) + 1
    heading = f"E.{n}. Modificari de la editia {previous} la {edition}"
    anchor = slug(heading)
    text = swap_one(text, r'^edition: "[^"]+"$', f'edition: "{edition}"', "edition")
    text = swap_one(text, r'^previous_edition: "[^"]+"$', f'previous_edition: "{previous}"', "previous")
    text = swap_one(text, r'^changelog_anchor: "[^"]+"$', f'changelog_anchor: "{anchor}"', "anchor")
    text = swap_one(text, r'^date: "[^"]+"$', f'date: "{date}"', "date")
    text = swap_one(text, r'^\*Editia [^\n]* \| Autor: [^\n]*\*$',
                    f'*Editia {edition} | {date} | Autor: {field(text, "author")} | Licenta: {field(text, "license")}*',
                    "cover")
    text = swap_one(text, r'^\*\*Ce este nou fata de editia [^\n]+\n',
                    f'**Ce este nou fata de editia {previous}.** Modificarile sunt descrise in Anexa E.{n}; '
                    f'vezi istoricul E.{n} pentru provenienta commitului si domeniile afectate.\n',
                    "intro")
    text = swap_one(text, r'^- \*\*Editia curenta:\*\* [^\n]+$',
                    f'- **Editia curenta:** {edition}, {date} (editia precedenta: {previous}).',
                    "annex edition")
    text = swap_one(text, r'^- \*\*Citare recomandata:\*\* [^\n]+$',
                    f'- **Citare recomandata:** {field(text,"author")} ({date.split()[-1]}), '
                    f'*{field(text,"title")}*, editia {edition}, {date}, {field(text,"wiki")}.',
                    "citation")
    text = swap_one(text, r'^\*Sfarsitul editiei [^\n]+$',
                    f'*Sfarsitul editiei {edition}. Acest fisier Markdown este sursa editabila a lucrarii; '
                    'versiunea web si PDF-ul se regenereaza din aceeasi revizie.*',
                    "footer")
    section = "\n## " + heading + "\n\n" + changelog_changes(changed, message, sha) + "\n"
    text = swap_one(text, r'^# Bibliografie si resurse de aprofundare
    return text


def prepare(repo, event):
    if event != "push":
        print(f"RELEASE: {event} - fara incrementare de editie")
        return "unchanged"
    source = repo / MASTER
    current = source.read_text(encoding="utf-8")
    try:
        parent = run_git("rev-parse", "HEAD^")
        previous_text = run_git("show", f"{parent}:{MASTER}")
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("Nu se poate citi versiunea precedenta; refuz incrementarea") from exc
    edition = field(current, "edition")
    preceding = field(previous_text, "edition")
    if edition != preceding:
        print(f"RELEASE: versiune stabilita editorial {preceding} -> {edition}; nu o incrementam din nou")
        return "declared"
    changed = run_git("diff", "--name-only", parent, "HEAD").splitlines()
    changed = [p for p in changed if not (
        p.startswith("docs/") and p.endswith(".pdf"))]
    if not changed:
        print("RELEASE: nu exista fisiere publicabile modificate")
        return "unchanged"
    new_version = next_patch(edition)
    now = datetime.datetime.now(ZoneInfo("Europe/London")).date()
    date = f"{now.day} {MONTHS[now.month - 1]} {now.year}"
    updated = update_text(current, edition, new_version, date, changed,
                          run_git("log", "-1", "--format=%B"), run_git("rev-parse", "HEAD"))
    source.write_text(updated, encoding="utf-8")
    print(f"RELEASE: {edition} -> {new_version}; {date}; changelog si citare actualizate")
    return "incremented"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--event", choices=["push", "workflow_dispatch"], required=True)
    args = ap.parse_args()
    prepare(pathlib.Path(args.repo), args.event)


if __name__ == "__main__":
    main()
,
                    section + "# Bibliografie si resurse de aprofundare", "bibliography boundary")
    return text


def prepare(repo, event):
    if event != "push":
        print(f"RELEASE: {event} - fara incrementare de editie")
        return "unchanged"
    source = repo / MASTER
    current = source.read_text(encoding="utf-8")
    try:
        parent = run_git("rev-parse", "HEAD^")
        previous_text = run_git("show", f"{parent}:{MASTER}")
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("Nu se poate citi versiunea precedenta; refuz incrementarea") from exc
    edition = field(current, "edition")
    preceding = field(previous_text, "edition")
    if edition != preceding:
        print(f"RELEASE: versiune stabilita editorial {preceding} -> {edition}; nu o incrementam din nou")
        return "declared"
    changed = run_git("diff", "--name-only", parent, "HEAD").splitlines()
    changed = [p for p in changed if not (
        p.startswith("docs/") and p.endswith(".pdf"))]
    if not changed:
        print("RELEASE: nu exista fisiere publicabile modificate")
        return "unchanged"
    new_version = next_patch(edition)
    now = datetime.datetime.now(ZoneInfo("Europe/London")).date()
    date = f"{now.day} {MONTHS[now.month - 1]} {now.year}"
    updated = update_text(current, edition, new_version, date, changed,
                          run_git("log", "-1", "--format=%B"), run_git("rev-parse", "HEAD"))
    source.write_text(updated, encoding="utf-8")
    print(f"RELEASE: {edition} -> {new_version}; {date}; changelog si citare actualizate")
    return "incremented"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--event", choices=["push", "workflow_dispatch"], required=True)
    args = ap.parse_args()
    prepare(pathlib.Path(args.repo), args.event)


if __name__ == "__main__":
    main()
