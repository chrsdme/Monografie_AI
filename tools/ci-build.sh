#!/usr/bin/env bash
# Construieste si verifica toate formatele din sursa editoriala unica.
set -euo pipefail
cd "$(dirname "$0")/.."

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
pages = len(PdfReader(str(source)).pages)
assert pages >= 20, f"PDF suspect: {pages} pagini"
print(f"PDF verificat: {pages} pagini, {source.stat().st_size} octeti")
PY

mkdocs build --strict

python - <<'PY'
from pathlib import Path
pdf = "Monografie_AI_De_la_Chat_la_Sisteme_Agentice.pdf"
site = Path("site")
assert (site / "index.html").exists(), "Lipseste pagina principala"
assert (site / "anexe/sabloane/index.html").exists(), "Lipseste Anexa B"
assert (site / "anexe/evaluare/index.html").exists(), "Lipseste Anexa C"
assert (site / "downloads" / pdf).read_bytes() == Path(pdf).read_bytes(), "PDF-ul publicat difera de sursa"
print("PASS: MkDocs strict, anexe, homepage si PDF descarcabil")
PY
