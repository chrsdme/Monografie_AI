#!/usr/bin/env python3
"""Verificari automate pentru sursa Markdown a monografiei.

Utilizare: python tools/lint.py [fisier.md] [--json iesire.json] [--figuri director]
Iese cu cod 1 daca exista erori (avertismentele nu opresc build-ul).
"""
import json
import pathlib
import re
import statistics
import sys

DEFAULT_MD = "Monografie_AI_De_la_Chat_la_Sisteme_Agentice.md"
ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5}


def main(argv):
    md_path = pathlib.Path(DEFAULT_MD)
    json_out = None
    figdir = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--json":
            json_out = argv[i + 1]
            i += 1
        elif a == "--figuri":
            figdir = pathlib.Path(argv[i + 1])
            i += 1
        else:
            md_path = pathlib.Path(a)
        i += 1
    text = md_path.read_text(encoding="utf-8")
    lines = text.split("\n")
    errors, warnings, info = [], [], {}

    def err(msg):
        errors.append(msg)

    def warn(msg):
        warnings.append(msg)

    # ---- front matter
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm = {}
    if not m:
        err("lipseste front matter")
    else:
        for ln in m.group(1).split("\n"):
            k, _, v = ln.partition(":")
            fm[k.strip()] = v.strip().strip('"')
        for k in ("title", "author", "edition", "date", "license", "wiki", "source"):
            if k not in fm:
                err(f"front matter: lipseste '{k}'")
    info["front_matter"] = fm

    # Controlul editiei curente este separat de istoricul editiilor vechi.
    for key in ("previous_edition", "changelog_anchor"):
        if not fm.get(key):
            err(f"front matter: lipseste '{key}'")
    needed = ("edition", "date", "author", "previous_edition", "changelog_anchor")
    if all(fm.get(k) for k in needed):
        edition, date, author = fm["edition"], fm["date"], fm["author"]
        checks = (
            ("coperta", f"*Editia {edition} | {date} | Autor: {author} |"),
            ("anexa E.1", f"**Editia curenta:** {edition}, {date}"),
            ("citare", f"editia {edition}, {date}, {fm.get('wiki', '')}"),
            ("final", f"*Sfarsitul editiei {edition}."),
            ("introducere", f"**Ce este nou fata de editia {fm['previous_edition']}.**"),
        )
        for area, expected in checks:
            if expected not in text:
                err(f"metadata editie neactualizata in {area}: {expected!r}")
        changelogs = re.findall(r"^## (E\.\d+\. Modificari de la editia .+)$", text, re.M)
        expected_name = f"Modificari de la editia {fm['previous_edition']} la {edition}"
        found = [t for t in changelogs if expected_name in t]
        if len(found) != 1:
            err(f"lipseste istoricul editiei {edition}: {expected_name}")
        else:
            slug = re.sub(r"[^a-z0-9 _-]", "", found[0].lower()).replace(" ", "-")
            if fm["changelog_anchor"] != slug:
                err(f"changelog_anchor gresit: {fm['changelog_anchor']!r} != {slug!r}")


    # ---- caractere
    nonascii = {}
    for n, ln in enumerate(lines, 1):
        for ch in ln:
            if ord(ch) > 127:
                nonascii.setdefault(ch, []).append(n)
    for ch, ls in nonascii.items():
        err(f"caracter non-ASCII {ch!r} (U+{ord(ch):04X}) la liniile {ls[:5]}")
    info["non_ascii_chars"] = len(nonascii)
    dashes = [n for n, ln in enumerate(lines, 1) if "—" in ln or "–" in ln or " -- " in ln]
    if dashes:
        err(f"linii cu em/en-dash: {dashes[:10]}")
    info["em_dashes"] = len(dashes)

    # ---- fence-uri cod
    fences = [n for n, ln in enumerate(lines, 1) if ln.strip().startswith("```")]
    if len(fences) % 2:
        err("fence-uri de cod dezechilibrate")
    info["code_fences"] = len(fences) // 2

    # ---- structura (ignora liniile din blocuri de cod)
    in_code = False
    headings = []  # (nivel, text, linie)
    body_lines = []
    for n, ln in enumerate(lines, 1):
        if ln.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        body_lines.append((n, ln))
        hm = re.match(r"^(#{1,4}) (.+)$", ln)
        if hm:
            headings.append((len(hm.group(1)), hm.group(2).strip(), n))
    info["headings"] = len(headings)

    # parti
    parts = [h for h in headings if h[0] == 1 and h[1].startswith("Partea ")]
    expected_roman = list(ROMAN)
    got = []
    for _, t, ln in parts:
        mm = re.match(r"Partea ([IVX]+)\.", t)
        got.append(mm.group(1) if mm else "?")
    if got != expected_roman:
        err(f"Partile: asteptat {expected_roman}, gasit {got}")

    # capitole: H2 'N. Titlu'
    chap = [(t, ln) for lv, t, ln in headings if lv == 2 and re.match(r"^\d+\. ", t)]
    nums = [int(re.match(r"^(\d+)\.", t).group(1)) for t, _ in chap]
    if nums != list(range(1, len(nums) + 1)):
        err(f"Capitole necontinue: {nums}")
    info["capitole"] = len(nums)

    # subsectiuni H3 'N.M.'
    cur = None
    last = {}
    for lv, t, ln in headings:
        if lv == 2:
            mm = re.match(r"^(\d+)\. ", t)
            cur = int(mm.group(1)) if mm else None
            if cur is not None:
                last[cur] = 0
        elif lv == 3 and cur is not None:
            mm = re.match(r"^(\d+)\.(\d+)\. ", t)
            if not mm:
                if not re.match(r"^(\d+)\.", t):
                    continue
            else:
                c, s = int(mm.group(1)), int(mm.group(2))
                if c != cur:
                    err(f"sectiunea {c}.{s} (linia {ln}) apare in capitolul {cur}")
                if s != last[cur] + 1:
                    err(f"numerotare sarita la {c}.{s} (linia {ln}), asteptat {c}.{last[cur] + 1}")
                last[cur] = s

    # anexe
    annex = [t for lv, t, ln in headings if lv == 1 and t.startswith("Anexa ")]
    letters = [re.match(r"Anexa ([A-Z])\.", t).group(1) for t in annex]
    if letters != sorted(letters) or letters != [chr(65 + i) for i in range(len(letters))]:
        err(f"Anexe necontinue: {letters}")
    cur = None
    last = {}
    for lv, t, ln in headings:
        if lv == 1:
            mm = re.match(r"Anexa ([A-Z])\.", t)
            cur = mm.group(1) if mm else None
            if cur:
                last[cur] = 0
        elif lv == 2 and cur:
            mm = re.match(r"^([A-Z])\.(\d+)\. ", t)
            if mm:
                if mm.group(1) != cur:
                    err(f"sectiunea {t[:6]} in anexa {cur}")
                s = int(mm.group(2))
                if s != last[cur] + 1:
                    err(f"numerotare anexa sarita la {mm.group(1)}.{s}")
                last[cur] = s

    # trimiteri "sectiunea X.Y"
    heads_set = set()
    for lv, t, ln in headings:
        mm = re.match(r"^((?:\d+|[A-Z])\.\d+)\. ", t)
        if mm:
            heads_set.add(mm.group(1))
    for n, ln in body_lines:
        for mm in re.finditer(r"sectiuni(?:le|i)? (\d+\.\d+)", ln):
            if mm.group(1) not in heads_set:
                err(f"trimitere la sectiune inexistenta {mm.group(1)} (linia {n})")

    # ---- figuri
    figs = []
    for n, ln in body_lines:
        mm = re.match(r"^!\[(.*?)\]\((.*?)\)\s*$", ln)
        if mm:
            figs.append((n, mm.group(1), mm.group(2)))
    info["figuri"] = len(figs)
    for idx, (n, alt, path) in enumerate(figs, 1):
        if not alt.startswith(f"Figura {idx}."):
            err(f"figura #{idx} (linia {n}): alt text trebuie sa inceapa cu 'Figura {idx}.'")
        cap = lines[n + 1] if n + 1 < len(lines) else ""
        if not cap.startswith(f"*Figura {idx}."):
            err(f"figura {idx} (linia {n}): lipseste legenda italica '*Figura {idx}. ...*'")
        # trimitere in text inainte de figura
        before = "\n".join(l for k, l in body_lines if k < n and not l.startswith("!["))
        if not re.search(rf"Figura {idx}\b", before):
            err(f"figura {idx}: nu este mentionata in text inainte de aparitie")
        if figdir is not None:
            if not (figdir / pathlib.Path(path).name).exists():
                err(f"figura {idx}: fisier lipsa {path}")
    if len(figs) != 8:
        warn(f"numar de figuri: {len(figs)} (asteptat 8)")

    # ---- citari
    bib_ids = re.findall(r"^\*\*\[(S\d\d)\]", text, re.M)
    expected = [f"S{i:02d}" for i in range(1, len(bib_ids) + 1)]
    if bib_ids != expected:
        err(f"Bibliografia nu este continua: {bib_ids}")
    bib_start = next((n for lv, t, n in headings if lv == 1 and t.startswith("Bibliografie")), len(lines))
    cited = set()
    for n, ln in body_lines:
        if n >= bib_start:
            continue
        for grp in re.findall(r"\[(S\d\d(?:, S\d\d)*)\]", ln):
            for sid in re.findall(r"S\d\d", grp):
                cited.add(sid)
                if sid not in bib_ids:
                    err(f"citare {sid} fara intrare in bibliografie (linia {n})")
    uncited = [s for s in bib_ids if s not in cited]
    if uncited:
        err(f"surse din bibliografie necitate in text: {uncited}")
    info["surse"] = len(bib_ids)
    info["surse_citate"] = len(cited)

    # ---- resturi si tipare suspecte
    patterns = {
        "text de mentinut": r"\\bTODO\\b|\\bFIXME\\b|\\b[Ll]orem ipsum",
        "nota arhiva veche": r"sase PDF|arhiva furnizata",
        "typo cunoscut": r"Instruciuni|linkuri_surze|ejecutarilor|un incantatie|Esti un expert contabil\.\"",
        "mentiune Raleigh nelegata de comunicat": r"^$",
    }
    annexE = next((n for lv, t, n in headings if lv == 1 and t.startswith("Anexa E")), len(lines) + 1)
    for name, pat in patterns.items():
        if name.startswith("mentiune"):
            continue
        for n, ln in body_lines:
            if n >= annexE:
                continue
            if re.search(pat, ln):
                err(f"{name}: linia {n}: {ln[:80]}")
    for n, ln in body_lines:
        if re.search(r"  +\S", ln) and not ln.startswith(("|", "    ", "- ", "  ")):
            pass

    # ---- ritm text (informativ)
    prose = []
    in_code = False
    for ln in lines:
        if ln.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or ln.startswith(("#", "|", "-", "!", "*Figura", ">", "---", "    ")) or not ln.strip():
            continue
        prose.append(ln)
    sents = []
    for p in prose:
        for s in re.split(r"(?<=[.!?])\s+", p):
            w = len(s.split())
            if w:
                sents.append(w)
    if sents:
        info["propozitii"] = len(sents)
        info["lungime_medie_propozitie"] = round(statistics.mean(sents), 1)
        info["abatere_standard_lungime"] = round(statistics.pstdev(sents), 1)
        info["propozitii_scurte_(<=8 cuvinte)"] = sum(1 for w in sents if w <= 8)
        info["propozitii_lungi_(>=30 cuvinte)"] = sum(1 for w in sents if w >= 30)
    info["cuvinte"] = sum(len(p.split()) for p in prose)

    # ---- rezultat
    res = {"fisier": str(md_path), "erori": errors, "avertismente": warnings, "info": info}
    if json_out:
        pathlib.Path(json_out).write_text(json.dumps(res, ensure_ascii=True, indent=2), encoding="utf-8")
    print(f"Fisier: {md_path}")
    for k, v in info.items():
        if k != "front_matter":
            print(f"  {k}: {v}")
    for w in warnings:
        print("AVERTISMENT:", w)
    for e in errors:
        print("EROARE:", e)
    print("REZULTAT:", "OK" if not errors else f"{len(errors)} erori")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
