#!/usr/bin/env python3
"""Regenereaza pagina web (wiki), cuprinsul si PDF-ul din sursa Markdown unica.

Utilizare (din radacina depozitului):
    python tools/build.py --repo . --toc --wiki --pdf

Optiuni:
    --repo DIR     radacina depozitului (implicit directorul curent)
    --md FIS       fisierul sursa (implicit Monografie_AI_De_la_Chat_la_Sisteme_Agentice.md)
    --toc          actualizeaza cuprinsul din sursa (intre <!-- TOC:START --> si <!-- TOC:END -->)
    --wiki         genereaza paginile din wiki/ (continutul navigatiei din mkdocs.yml)
    --pdf          genereaza PDF-ul cu cuprins linkat si numere de pagina
    --no-lint      nu rula verificarile inainte

Cerinte: python 3.10+, pandoc, playwright + chromium (pentru PDF), pypdf (pentru numerele de pagina).
"""
import argparse
import html
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

DEFAULT_MD = "Monografie_AI_De_la_Chat_la_Sisteme_Agentice.md"
FIG_SRC_DIR = "Monografie_AI_figuri"
WIKI_FIG_DIR = "figuri"

# Numele fisierelor din nav-ul mkdocs.yml al depozitului public (15.10.2026)
PART_DIRS = {1: "partea-1", 2: "partea-2", 3: "partea-3", 4: "partea-4", 5: "partea-5"}
CHAP_FILES = {
    1: "partea-1/01-ce-este-ai.md",
    2: "partea-1/02-cum-functioneaza-llm.md",
    3: "partea-1/03-browser-cli-api-local.md",
    4: "partea-1/04-context.md",
    5: "partea-1/05-ce-putem-face-cu-ai.md",
    6: "partea-2/06-prompturi-instructiuni-briefuri.md",
    7: "partea-2/07-instrumente-api-conectori-mcp.md",
    8: "partea-2/08-rag-memorie-cunostinte.md",
    9: "partea-2/09-automatizare-workflow-agent.md",
    10: "partea-3/10-harness.md",
    11: "partea-3/11-arhitectura-workflow-ai.md",
    12: "partea-3/12-anatomia-agentului.md",
    13: "partea-3/13-specializare-clase-instante.md",
    14: "partea-3/14-orchestrare.md",
    15: "partea-3/15-ai-engineering.md",
    16: "partea-4/16-observabilitate.md",
    17: "partea-4/17-evaluare-trust-score.md",
    18: "partea-4/18-securitate-guardrails.md",
    19: "partea-4/19-fiabilitate-recuperare.md",
    20: "partea-4/20-cost-viteza-calitate.md",
    21: "partea-5/21-studii-de-caz.md",
    22: "partea-5/22-cum-incepi.md",
}
ANNEX_FILES = {
    "A": "anexe/glosar.md",
    "B": "anexe/sabloane.md",
    "C": "anexe/evaluare.md",
    "D": "anexe/metoda-surse.md",  # contine si Anexa E
    "E": "anexe/metoda-surse.md",
}
BIB_FILE = "anexe/bibliografie.md"


# ----------------------------------------------------------------- utilitare
def read_master(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm = {}
    body = text
    if m:
        for ln in m.group(1).split("\n"):
            k, _, v = ln.partition(":")
            fm[k.strip()] = v.strip().strip('"')
        body = text[m.end():]
    return text, fm, body


def gh_anchor(title):
    t = title.strip().lower()
    t = re.sub(r"[^a-z0-9 _-]", "", t)
    return t.replace(" ", "-")


def split_blocks(body):
    """Imparte corpul in blocuri dupa antetele H1/H2, ignorand blocurile de cod."""
    blocks = []  # dict(level, title, lines)
    cur = {"level": 0, "title": "", "lines": []}
    in_code = False
    for ln in body.split("\n"):
        if ln.strip().startswith("```"):
            in_code = not in_code
        m = re.match(r"^(#{1,2}) (.+)$", ln) if not in_code else None
        if m:
            blocks.append(cur)
            cur = {"level": len(m.group(1)), "title": m.group(2).strip(), "lines": [ln]}
        else:
            cur["lines"].append(ln)
    blocks.append(cur)
    return blocks


def strip_trailing(lines):
    out = list(lines)
    while out and not out[-1].strip():
        out.pop()
    while out and out[-1].strip() == "---":
        out.pop()
        while out and not out[-1].strip():
            out.pop()
    return out


def demote_headings(lines, delta):
    out = []
    in_code = False
    for ln in lines:
        if ln.strip().startswith("```"):
            in_code = not in_code
        if not in_code:
            m = re.match(r"^(#{1,6}) (.*)$", ln)
            if m:
                n = max(1, len(m.group(1)) + delta)
                ln = "#" * n + " " + m.group(2)
        out.append(ln)
    return out


def link_citations(text, prefix):
    """[S10] si [S17, S19] devin trimiteri la bibliografie."""
    def one(sid):
        return f"[{sid}]({prefix}#{sid.lower()})"

    def rep(m):
        ids = re.findall(r"S\d\d", m.group(1))
        return "[" + ", ".join(f"[{i}]({prefix}#{i.lower()})" for i in ids) + "]"

    out = []
    for ln in text.split("\n"):
        if ln.startswith("**[S"):
            out.append(ln)
            continue
        ln = re.sub(r"\[(S\d\d(?:, S\d\d)*)\](?!\()", lambda m: _cite(m, prefix), ln)
        out.append(ln)
    return "\n".join(out)


def _cite(m, prefix):
    ids = re.findall(r"S\d\d", m.group(1))
    return ", ".join(f"[{i}]({prefix}#{i.lower()})" for i in ids) if len(ids) > 1 else f"[{ids[0]}]({prefix}#{ids[0].lower()})"


def add_bib_anchors(text):
    out = []
    for ln in text.split("\n"):
        m = re.match(r"^\*\*\[(S\d\d)\]", ln)
        if m:
            out.append(f'<a id="{m.group(1).lower()}"></a>')
            out.append("")
            ln = re.sub(r"(?<![<(])(https?://[^\s<>)]+[^\s<>).,;])", r"<\1>", ln)
        out.append(ln)
    return "\n".join(out)


def fix_images(text, new_prefix):
    return text.replace(FIG_SRC_DIR + "/", new_prefix)


# ---------------------------------------------------------------- cuprins MD
def build_toc_md(body):
    blocks = split_blocks(body)
    lines = []
    for b in blocks:
        if b["level"] == 2 and b["title"] in ("Nota editoriala", "Cum se citeste aceasta carte"):
            lines.append(f"- [{b['title']}](#{gh_anchor(b['title'])})")
    for b in blocks:
        if b["level"] == 1 and (b["title"].startswith("Partea ") or b["title"].startswith("Anexa ") or b["title"].startswith("Bibliografie")):
            lines.append(f"- [{b['title']}](#{gh_anchor(b['title'])})")
            if b["title"].startswith("Partea "):
                pass
        elif b["level"] == 2 and re.match(r"^\d+\. ", b["title"]):
            lines.append(f"  - [{b['title']}](#{gh_anchor(b['title'])})")
    return "\n".join(lines)


def update_toc(path):
    text = path.read_text(encoding="utf-8")
    toc = build_toc_md(text)
    new, n = re.subn(r"<!-- TOC:START -->.*?<!-- TOC:END -->", lambda m: "<!-- TOC:START -->\n" + toc + "\n<!-- TOC:END -->", text, flags=re.S)
    if n != 1:
        sys.exit("Nu gasesc marcajele TOC:START / TOC:END (exact o pereche).")
    if new != text:
        path.write_text(new, encoding="utf-8")
    return len(toc.split("\n"))


# ---------------------------------------------------------------------- wiki
def build_wiki(repo, md_path, fm):
    text, fm, body = read_master(md_path)
    body = re.sub(r"<!-- TOC:START -->.*?<!-- TOC:END -->\n?", "", body, flags=re.S)
    blocks = split_blocks(body)
    wiki = repo / "wiki"
    (wiki / WIKI_FIG_DIR).mkdir(parents=True, exist_ok=True)
    src_figs = repo / FIG_SRC_DIR
    for f in sorted(src_figs.glob("*.svg")):
        shutil.copy2(f, wiki / WIKI_FIG_DIR / f.name)

    written = []

    def write(rel, content):
        p = wiki / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        depth = rel.count("/")
        up = "../" * depth
        content = link_citations(content, up + "anexe/bibliografie.md")
        content = fix_images(content, up + WIKI_FIG_DIR + "/")
        p.write_text(content.rstrip("\n") + "\n", encoding="utf-8")
        written.append(rel)

    # --- pagina principala si introducere
    front = []
    intro = []
    mode = "front"
    cur_title = None
    part_blocks = []
    for b in blocks:
        if b["level"] == 1 and b["title"].startswith("Partea "):
            mode = "parts"
        if mode == "front":
            if b["level"] == 2 and b["title"] in ("Nota editoriala", "Cum se citeste aceasta carte"):
                intro.append(b)
            elif b["level"] == 2 and b["title"] == "Cuprins":
                continue
            else:
                front.append(b)
        else:
            part_blocks.append(b)

    front_lines = []
    for b in front:
        front_lines.extend(b["lines"])
    front_txt = "\n".join(strip_trailing(front_lines))
    nav_links = (
        "\n\n## Cum navighezi\n\n"
        "- [Introducere](introducere.md)\n"
        "- Partea I: [De unde pornim](partea-1/index.md)\n"
        "- Partea II: [De la o intrebare la o actiune](partea-2/index.md)\n"
        "- Partea III: [Din componente separate construim un sistem](partea-3/index.md)\n"
        "- Partea IV: [Cum construim incredere](partea-4/index.md)\n"
        "- Partea V: [Doua proiecte si cazuri reale](partea-5/index.md)\n"
        "- Anexe: [Dictionar](anexe/glosar.md), [Sabloane](anexe/sabloane.md), [Protocol de evaluare](anexe/evaluare.md), "
        "[Metoda, surse si istoricul editiilor](anexe/metoda-surse.md), [Bibliografie](anexe/bibliografie.md)\n"
        f"\n*Sursa: [{fm.get('source', '')}]({fm.get('source', '')}). Licenta: {fm.get('license', '')}.*"
    )
    merge_index(wiki, fm)

    intro_lines = ["# Introducere", ""]
    for b in intro:
        intro_lines.extend(strip_trailing(b["lines"]))
        intro_lines.append("")
    write("introducere.md", "\n".join(intro_lines))

    # --- parti si capitole
    part_no = 0
    chap_in_part = {}
    cur_part = None
    part_intro = {}
    for b in part_blocks:
        t = b["title"]
        if b["level"] == 1 and t.startswith("Partea "):
            part_no = ["I", "II", "III", "IV", "V"].index(re.match(r"Partea ([IVX]+)\.", t).group(1)) + 1
            cur_part = part_no
            part_intro[part_no] = {"title": t, "lines": strip_trailing(b["lines"]), "chapters": []}
        elif b["level"] == 2 and re.match(r"^\d+\. ", t):
            n = int(re.match(r"^(\d+)\.", t).group(1))
            part_intro[cur_part]["chapters"].append((n, t))
            lines = demote_headings(strip_trailing(b["lines"]), -1)
            write(CHAP_FILES[n], "\n".join(lines))
        elif b["level"] == 1 and (t.startswith("Anexa ") or t.startswith("Bibliografie")):
            cur_part = None
            break
    for k, v in part_intro.items():
        lines = list(v["lines"])
        lines.append("")
        lines.append("## Capitolele acestei parti")
        lines.append("")
        for n, t in v["chapters"]:
            fname = CHAP_FILES[n].split("/", 1)[1]
            lines.append(f"- [{t}]({fname})")
        write(f"{PART_DIRS[k]}/index.md", "\n".join(lines))

    # --- anexe
    ann = {}
    key = None
    for b in blocks:
        if b["level"] == 1:
            if b["title"].startswith("Anexa "):
                key = re.match(r"Anexa ([A-Z])\.", b["title"]).group(1)
            elif b["title"].startswith("Bibliografie"):
                key = "BIB"
            else:
                key = None
            if key:
                ann[key] = []
        if key:
            ann[key].extend(b["lines"])  # include si blocurile H2 (B.1, C.1, E.1 ...)
    for k in ann:
        ann[k] = strip_trailing(ann[k])
    write(ANNEX_FILES["A"], "\n".join(ann["A"]))
    write(ANNEX_FILES["B"], "\n".join(ann["B"]))
    write(ANNEX_FILES["C"], "\n".join(ann["C"]))
    write(ANNEX_FILES["D"], "\n".join(ann["D"] + ["", ""] + ann["E"]))
    bib_txt = add_bib_anchors("\n".join(ann["BIB"]))
    write(BIB_FILE, bib_txt)
    check_wiki(wiki, written, body)
    return written


IDX_START, IDX_END = "<!-- MONOGRAFIE:START -->", "<!-- MONOGRAFIE:END -->"


def index_block(fm):
    return (f"{IDX_START}\n## Editia curenta\n\n"
            f"Editia {fm.get('edition', '')}, {fm.get('date', '')}. Autor: {fm.get('author', '')}. Licenta: {fm.get('license', '')}. "
            f"[Ce s-a schimbat fata de editia 1.0](anexe/metoda-surse.md#e2-changelog-10-la-11). "
            f"[Sursa pe GitHub]({fm.get('source', '')}).\n{IDX_END}")


def merge_index(wiki, fm):
    """Pagina principala contine continut comunitar: nu o suprascriem. Actualizam doar blocul marcat."""
    p = wiki / "index.md"
    block = index_block(fm)
    (wiki.parent / "wiki_index_block.md").write_text(block + "\n", encoding="utf-8")
    if not p.exists():
        p.write_text("# " + fm.get("title", "") + "\n\n" + block + "\n", encoding="utf-8")
        print("index.md nu exista: am creat o pagina minima.")
        return
    t = p.read_text(encoding="utf-8")
    if IDX_START in t and IDX_END in t:
        t = re.sub(re.escape(IDX_START) + ".*?" + re.escape(IDX_END), lambda m: block, t, flags=re.S)
        p.write_text(t, encoding="utf-8")
        print("index.md: blocul 'Editia curenta' actualizat; restul paginii a ramas neatins.")
    else:
        print("ATENTIE: index.md nu are marcajele MONOGRAFIE. Nu l-am modificat. "
              "Lipeste manual continutul din wiki_index_block.md unde vrei sa apara.")


def _norm_section(t):
    t = re.sub(r"\[(S\d\d)\]\([^)]*\)", r"[\1]", t)
    t = re.sub(r"!\[([^\]]*)\]\([^)]*/([^/)]+)\)", r"![\1](\2)", t)
    for _ in range(5):
        t = re.sub(r"\], \[(S\d\d)\]", r", \1]", t)
    t = re.sub(r'<a id="s\d\d"></a>', "", t)
    t = re.sub(r"<(https?://[^>]+)>", r"\1", t)
    return re.sub(r"\s+", " ", t).strip()


def _sections(text):
    """Lista de (titlu, corp normalizat) pentru fiecare antet H1-H4, in afara blocurilor de cod."""
    out, in_code, cur = [], False, None
    for ln in text.split("\n"):
        if ln.strip().startswith("```"):
            in_code = not in_code
        m = None if in_code else re.match(r"^#{1,4} (.+)$", ln)
        if m:
            if cur:
                out.append((cur[0], _norm_section("\n".join(cur[1]))))
            cur = (re.sub(r"\s+", " ", m.group(1).strip()), [])
        elif cur is not None:
            cur[1].append(ln)
    if cur:
        out.append((cur[0], _norm_section("\n".join(cur[1]))))
    return out


def _headings(text):
    out, in_code = [], False
    for ln in text.split("\n"):
        if ln.strip().startswith("```"):
            in_code = not in_code
        m = None if in_code else re.match(r"^#{1,4} (.+)$", ln)
        if m:
            out.append(re.sub(r"\s+", " ", m.group(1).strip()))
    return out


def check_wiki(wiki, written, body):
    """Esueaza daca wiki-ul nu reproduce integral sursa (antete si volum de text)."""
    mb0 = re.search(r"^# (.+)$", body, re.M)
    master_h = [h for h in _headings(body) if h not in ("Cuprins", mb0.group(1).strip() if mb0 else "")]
    wiki_text = "\n".join((wiki / w).read_text(encoding="utf-8") for w in written)
    wiki_h = set(_headings(wiki_text))
    missing = [h for h in master_h if h not in wiki_h]
    def words(t):
        t = re.sub(r"\(\.\./[^)]*\)|\([^)]*\.md[^)]*\)", "", t)
        return len(re.findall(r"[A-Za-z0-9]+", t))
    wm, ww = words(body), words(wiki_text)
    problems = []
    if missing:
        problems.append(f"antete lipsa din wiki ({len(missing)}): {missing[:8]}")
    if ww < 0.97 * wm:
        problems.append(f"volum wiki {ww} cuvinte fata de {wm} in sursa")
    from collections import Counter
    mb = re.search(r"^# (.+)$", body, re.M)
    book = mb.group(1).strip() if mb else ""
    ms = Counter((t, b) for t, b in _sections(body) if t not in ("Cuprins", book))
    ws = Counter(_sections(wiki_text))
    diff = [t for (t, b), c in ms.items() if ws[(t, b)] < c]
    if diff:
        problems.append(f"sectiuni diferite sau lipsa in wiki ({len(diff)}): {diff[:6]}")
    print(f"Verificare pe sectiuni: {sum(ms.values())} sectiuni comparate, {len(diff)} diferite")
    print(f"Verificare wiki: {len(master_h)} antete in sursa, {len(missing)} lipsa; cuvinte sursa {wm}, wiki {ww}")
    if problems:
        sys.exit("WIKI INCOMPLET: " + "; ".join(problems))


def internalize_wiki_links_for_pdf(html_text, site_url):
    """Resolve MkDocs heading anchors to Pandoc heading IDs inside the PDF HTML."""
    prefix = site_url.rstrip("/") + "/"
    existing = set(re.findall(r'\bid="([^"]+)"', html_text))
    aliases = {}

    # Pandoc strips leading numerals when assigning identifiers; MkDocs keeps
    # them (for example "21.7." -> "217-..."). Match by visible heading text.
    for match in re.finditer(
        r'<h[1-6]\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</h[1-6]>',
        html_text, flags=re.S
    ):
        pandoc_id = match.group(1)
        heading_title = html.unescape(re.sub(r"<[^>]+>", "", match.group(2)))
        aliases[gh_anchor(heading_title)] = pandoc_id

    def rep(match):
        link = html.unescape(match.group(1))
        if link.startswith(prefix) and "#" in link:
            fragment = link.split("#", 1)[1]
            target = fragment if fragment in existing else aliases.get(fragment)
            if target:
                return f'href="#{target}"'
        return match.group(0)

    return re.sub(r'href="(https?://[^"]+)"', rep, html_text)


# ----------------------------------------------------------------------- PDF
PDF_CSS = """
@page { size: A4; margin: 22mm 18mm 22mm 18mm; }
html { font-size: 10.5pt; }
body { font-family: 'Bitstream Charter', 'Charter', 'DejaVu Serif', serif; line-height: 1.5; color: #1b1f27; margin: 0; hyphens: auto; }
h1, h2, h3, h4 { font-family: 'Inter', 'DejaVu Sans', sans-serif; color: #15253e; line-height: 1.25; }
h1 { font-size: 21pt; margin: 0 0 14pt 0; padding-bottom: 6pt; border-bottom: 2pt solid #15253e; break-before: page; break-after: avoid; }
h2 { font-size: 15pt; margin: 22pt 0 8pt 0; break-after: avoid; }
h3 { font-size: 12pt; margin: 16pt 0 6pt 0; break-after: avoid; }
h4 { font-size: 10.5pt; margin: 12pt 0 4pt 0; break-after: avoid; }
p { margin: 0 0 7pt 0; orphans: 3; widows: 3; text-align: left; }
a { color: #1d4f91; text-decoration: none; }
blockquote { margin: 10pt 0; padding: 4pt 12pt; border-left: 3pt solid #6f96cd; background: #f2f5f9; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.8pt; background: #eef1f5; padding: 0 2pt; border-radius: 2pt; }
pre { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.2pt; background: #f2f5f9; border: 0.6pt solid #cfd8e3; border-radius: 3pt; padding: 7pt 9pt; white-space: pre-wrap; break-inside: avoid; }
pre code { background: none; padding: 0; font-size: inherit; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0 12pt 0; font-size: 9.2pt; break-inside: avoid; }
th, td { border: 0.6pt solid #b7c6d8; padding: 3pt 6pt; vertical-align: top; text-align: left; }
th { background: #e6f0ff; font-family: 'Inter', sans-serif; }
img { display: block; width: 100%; max-width: 100%; margin: 8pt auto 2pt auto; break-inside: avoid; }
p > img + em, p:has(img) + p em { font-size: 9pt; color: #42536d; }
ul, ol { margin: 0 0 8pt 0; padding-left: 18pt; }
li { margin-bottom: 2pt; }
hr { border: 0; border-top: 0.6pt solid #cfd8e3; margin: 14pt 0; }
.cover { height: 235mm; display: flex; flex-direction: column; justify-content: center; break-after: page; }
.cover .band { height: 6pt; background: #15253e; margin-bottom: 28pt; }
.cover h1 { border: 0; break-before: avoid; font-size: 30pt; margin: 0 0 12pt 0; padding: 0; }
.cover .sub { font-family: 'Inter', sans-serif; font-size: 13pt; color: #42536d; margin-bottom: 36pt; }
.cover .meta { font-family: 'Inter', sans-serif; font-size: 10.5pt; line-height: 1.7; color: #1b1f27; }
.cover .meta b { color: #15253e; }
nav#TOC { break-after: page; }
nav#TOC::before { content: 'Cuprins'; display: block; font-family: 'Inter', sans-serif; font-size: 21pt; font-weight: 700; color: #15253e; border-bottom: 2pt solid #15253e; padding-bottom: 6pt; margin-bottom: 12pt; }
nav#TOC ul { list-style: none; padding-left: 0; margin: 0; }
nav#TOC ul ul { padding-left: 14pt; }
nav#TOC li { margin: 0; font-size: 9.8pt; line-height: 1.55; }
nav#TOC > ul > li { margin-top: 5pt; font-weight: 700; font-family: 'Inter', sans-serif; font-size: 10pt; }
nav#TOC > ul > li > ul > li { font-weight: 400; font-family: 'Bitstream Charter', serif; }
nav#TOC a { display: flex; gap: 5pt; color: #1b1f27; }
nav#TOC a .t { flex: 0 1 auto; }
nav#TOC a .lead { flex: 1 1 auto; border-bottom: 0.7pt dotted #8a97a8; margin-bottom: 4pt; min-width: 12pt; }
nav#TOC a .pg { flex: none; font-variant-numeric: tabular-nums; }
"""


def build_pdf(repo, md_path, out_pdf):
    from playwright.sync_api import sync_playwright

    text, fm, body = read_master(md_path)
    body = re.sub(r"## Cuprins\n+<!-- TOC:START -->.*?<!-- TOC:END -->\n?", "", body, flags=re.S)
    # scoate blocul de coperta (titlul, subtitlul si liniile italice de editie)
    lines = body.split("\n")
    out = []
    skipped_h1 = False
    for ln in lines:
        if not skipped_h1 and ln.startswith("# ") and not ln.startswith("# Partea"):
            skipped_h1 = True
            continue
        if ln.startswith("**O introducere graduala") or ln.startswith("*Editia ") or ln.startswith("*Versiunea web:"):
            continue
        out.append(ln)
    body = "\n".join(out)
    body = link_citations(body, "")
    body = add_bib_anchors(body)

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="monografie_pdf_"))
    md_tmp = tmp / "corp.md"
    md_tmp.write_text(body, encoding="utf-8")
    (tmp / "print.css").write_text(PDF_CSS, encoding="utf-8")
    cover = f"""<div class="cover"><div class="band"></div>
<h1 class="cover-title" style="break-before:avoid">{html.escape(fm.get('title', ''))}</h1>
<div class="sub">{html.escape(fm.get('subtitle', ''))}</div>
<div class="meta"><b>Autor:</b> {html.escape(fm.get('author', ''))}<br>
<b>Editia:</b> {html.escape(fm.get('edition', ''))}, {html.escape(fm.get('date', ''))}<br>
<b>Licenta:</b> {html.escape(fm.get('license', ''))}<br>
<b>Versiunea web:</b> {html.escape(fm.get('wiki', ''))}<br>
<b>Sursa:</b> {html.escape(fm.get('source', ''))}</div></div>"""
    (tmp / "cover.html").write_text(cover, encoding="utf-8")
    html_out = tmp / "carte.html"
    cmd = [
        "pandoc", str(md_tmp), "-f", "markdown-implicit_figures-smart+pipe_tables+raw_html+fenced_code_blocks",
        "-t", "html5", "-s", "--toc", "--toc-depth=2", "--embed-resources",
        f"--resource-path={repo}", "--css", str(tmp / "print.css"), "-B", str(tmp / "cover.html"),
        "--metadata", f"pagetitle={fm.get('title', '')}", "--metadata", "lang=ro",
        "--metadata", f"author-meta={fm.get('author', '')}", "-o", str(html_out),
    ]
    subprocess.run(cmd, check=True)
    page = html_out.read_text(encoding="utf-8")
    wiki_prefix = fm.get("wiki", "").rstrip("/") + "/"
    # Toate trimiterile Markdown catre capitolele acestei carti trebuie sa
    # ajunga in PDF la ancore interne, nu sa forteze iesirea spre browser.
    source_refs = re.findall(r"\]\((https?://[^)]+)\)", body)
    internal_refs = [u for u in source_refs if u.startswith(wiki_prefix) and "#" in u]
    page = internalize_wiki_links_for_pdf(page, fm.get("wiki", ""))
    unresolved = [u for u in internal_refs if 'href="' + u + '"' in page]
    if unresolved:
        raise RuntimeError(f"Linkuri PDF interne nerezolvate: {unresolved}")
    print(f"PDF: {len(internal_refs)} trimiteri interne catre subcapitole verificate")

    # structura TOC: <a href="#id" id="toc-id">Titlu</a>; adauga spatiu pentru numere de pagina
    entries = re.findall(r'<a href="#([^"]+)" id="toc-[^"]+"[^>]*>(.*?)</a>', page, flags=re.S)

    def decorate(pages):
        def rep(m):
            hid, label = m.group(1), m.group(3)
            n = pages.get(hid, "000")
            return f'<a href="#{hid}"{m.group(2)}><span class="t">{label}</span><span class="lead"></span><span class="pg">{n}</span></a>'
        return re.sub(r'<a href="#([^"]+)"( id="toc-[^"]+"[^>]*)>(.*?)</a>', rep, page, flags=re.S)

    def render(doc_html, target):
        h = tmp / "render.html"
        h.write_text(doc_html, encoding="utf-8")
        with sync_playwright() as p:
            b = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
            pg = b.new_page()
            pg.goto(h.as_uri())
            pg.wait_for_timeout(500)
            footer = ('<div style="font-size:8pt;width:100%;text-align:center;color:#42536d;font-family:Inter,sans-serif">'
                      '<span class="pageNumber"></span> / <span class="totalPages"></span></div>')
            header = ('<div style="font-size:7.5pt;width:100%;padding:0 18mm;color:#8a97a8;font-family:Inter,sans-serif">'
                      f'{html.escape(fm.get("title", ""))} | editia {html.escape(fm.get("edition", ""))}</div>')
            kw = dict(path=str(target), format="A4", print_background=True, display_header_footer=True,
                      header_template=header, footer_template=footer, prefer_css_page_size=True,
                      margin={"top": "22mm", "bottom": "22mm", "left": "18mm", "right": "18mm"})
            try:
                pg.pdf(outline=True, tagged=True, **kw)
            except TypeError:
                pg.pdf(**kw)
            b.close()

    def norm(s):
        s = re.sub(r"<[^>]+>", "", s)
        s = html.unescape(s)
        return re.sub(r"\s+", " ", s).strip().lower()

    first = tmp / "pass1.pdf"
    render(decorate({}), first)
    from pypdf import PdfReader

    def find_pages(pdf_path):
        """Citeste paginile din destinatiile bookmark-urilor PDF.

        Textul extras din PDF poate avea randuri frante si antete repetitive.
        Chromium plaseaza bookmark-uri direct la antetele HTML; destinatiile lor
        reprezinta pozitiile reale ale titlurilor din cuprins.
        """
        reader = PdfReader(str(pdf_path))
        outlines = {}

        def key_for(s):
            return re.sub(r"\s+", "", norm(s))

        def walk(items):
            for item in items:
                if isinstance(item, list):
                    walk(item)
                    continue
                page_idx = reader.get_destination_page_number(item)
                if page_idx is not None and page_idx >= 0:
                    outlines.setdefault(key_for(item.title), []).append(page_idx + 1)

        walk(reader.outline)
        used = {}
        pages = {}
        for hid, label in entries:
            key = key_for(label)
            idx = used.get(key, 0)
            candidates = outlines.get(key, [])
            if idx < len(candidates):
                pages[hid] = str(candidates[idx])
                used[key] = idx + 1
        return pages, len(reader.pages)

    pages, total = find_pages(first)
    missing = [l for h, l in entries if h not in pages]
    render(decorate(pages), out_pdf)
    fix_outline(out_pdf, page)
    # verificare: aceleasi pagini dupa a doua trecere
    pages2, total2 = find_pages(out_pdf)
    stable = pages2 == pages
    return {"pagini": total2, "intrari_cuprins": len(entries), "fara_pagina": missing, "numere_stabile": stable}


def fix_outline(pdf_path, page_html):
    """Chromium pierde spatiile la randurile frante in marcaje; refacem titlurile din HTML."""
    from pypdf import PdfReader, PdfWriter
    heads = re.findall(r"<h[1-3][^>]*>(.*?)</h[1-3]>", page_html, flags=re.S)
    table = {}
    for h in heads:
        t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h))).strip()
        table[re.sub(r"\s+", "", t)] = t
    r = PdfReader(str(pdf_path))
    w = PdfWriter(clone_from=r)

    def walk(items, parent):
        last = None
        for it in items:
            if isinstance(it, list):
                walk(it, last)
            else:
                key = re.sub(r"\s+", "", it.title)
                title = table.get(key, it.title)
                if key not in table:
                    for k, v in table.items():
                        if k.startswith(key):
                            title = v
                            break
                last = w.add_outline_item(title, r.get_destination_page_number(it), parent=parent)

    w._root_object.pop("/Outlines", None)
    walk(r.outline, None)
    w.add_metadata({"/Title": "De la conversatia cu AI la sisteme agentice verificabile", "/Author": "chrsdme"})
    with open(pdf_path, "wb") as f:
        w.write(f)


# ---------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--md", default=DEFAULT_MD)
    ap.add_argument("--toc", action="store_true")
    ap.add_argument("--wiki", action="store_true")
    ap.add_argument("--pdf", action="store_true")
    ap.add_argument("--no-lint", action="store_true")
    a = ap.parse_args(argv)
    repo = pathlib.Path(a.repo).resolve()
    md = repo / a.md
    if not md.exists():
        sys.exit(f"Nu gasesc {md}")
    if not a.no_lint:
        lint = pathlib.Path(__file__).with_name("lint.py")
        r = subprocess.run([sys.executable, str(lint), str(md), "--figuri", str(repo / FIG_SRC_DIR)])
        if r.returncode:
            sys.exit("Verificarile au esuat. Corecteaza erorile si reia.")
    if a.toc:
        n = update_toc(md)
        print(f"Cuprins actualizat ({n} intrari).")
    if a.wiki:
        files = build_wiki(repo, md, {})
        print(f"Wiki: {len(files)} pagini scrise in {repo / 'wiki'}")
    if a.pdf:
        res = build_pdf(repo, md, md.with_suffix(".pdf"))
        print("PDF:", json.dumps(res, ensure_ascii=True))
        if res["fara_pagina"] or not res["numere_stabile"]:
            sys.exit("PDF generat, dar numerele din cuprins nu sunt complete sau stabile.")


if __name__ == "__main__":
    main()
