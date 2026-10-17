#!/usr/bin/env bash
# Construieste si verifica toate formatele din sursa editoriala unica.
set -euo pipefail
cd "$(dirname "$0")/.."

python -m unittest discover -s tests -p "test_feedback_hook.py"
python -m unittest discover -s tests -p "test_tech_theme.py" -v
python -m unittest discover -s tests -p "test_intent_crossrefs.py" -v
python -m unittest discover -s tests -p "test_release_archive.py" -v
python -m unittest discover -s examples/agent_studies/tests -v

python tools/build.py --repo . --toc --wiki --pdf

pdf="Monografie_AI_De_la_Chat_la_Sisteme_Agentice.pdf"
published_pdf="wiki/downloads/$pdf"
mkdir -p wiki/downloads
cp "$pdf" "$published_pdf"

python - <<'PY'
from pathlib import Path
from pypdf import PdfReader
source = Path("Monografie_AI_De_la_Chat_la_Sisteme_Agentice.pdf")
target = Path("wiki/downloads/Monografie_AI_De_la_Chat_la_Sisteme_Agentice.pdf")
assert source.is_file() and source.stat().st_size > 50_000, "PDF lipsa sau prea mic"
assert target.read_bytes() == source.read_bytes(), "PDF-ul din wiki difera de cel generat"
reader = PdfReader(str(source))
pages = len(reader.pages)

# Previne pierderea tacuta a anexelor din PDF daca lipseste un rand gol Markdown.
def titles(items):
    for item in items:
        if isinstance(item, list):
            yield from titles(item)
        else:
            yield item.title

pdf_headings = list(titles(reader.outline))
for required in ("Anexa A.", "Anexa B.", "Anexa C.", "Anexa D.", "Anexa E.", "Bibliografie"):
    assert any(t.startswith(required) for t in pdf_headings), (
        f"Lipseste heading-ul PDF: {required}"
    )
print("PASS: anexele A-E si bibliografia sunt prezente in outline-ul PDF")
assert pages >= 20, f"PDF suspect: {pages} pagini"
print(f"PDF verificat: {pages} pagini, {source.stat().st_size} octeti")
PY

mkdocs build --strict

python - <<'PY'
from pathlib import Path
pdf = "Monografie_AI_De_la_Chat_la_Sisteme_Agentice.pdf"
site = Path("site")
assert (site / "index.html").exists(), "Lipseste pagina principala"
home_html = (site / "index.html").read_text(encoding="utf-8")
assert 'tech-hero' in home_html and 'tech-edition' in home_html, "Homepage Tech nu a fost randat"
assert 'stylesheets/tech.css' in home_html, "Stilul Tech nu este incarcat"
assert (site / "stylesheets/tech.css").exists(), "Fisierul CSS Tech lipseste"
print("PASS: homepage Tech, tema si panoul editiei curente")
assert (site / "anexe/sabloane/index.html").exists(), "Lipseste Anexa B"
assert (site / "anexe/evaluare/index.html").exists(), "Lipseste Anexa C"
assert (site / "downloads" / pdf).read_bytes() == Path(pdf).read_bytes(), "PDF-ul publicat difera de sursa"
print("PASS: MkDocs strict, anexe, homepage si PDF descarcabil")
PY
