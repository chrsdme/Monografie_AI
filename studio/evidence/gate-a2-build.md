# Gate A2 - Build si TOC

Data: 2026-10-23
Branch: `studio-test`

## Scop si implementare

`tools/studio.py build` reasambleaza manuscrisul din fragmente, apoi ruleaza generatorul cu `--toc --wiki`. Cand exista manifest canonic, `tools/build.py --toc` trimite schimbarea TOC prin `studio.sync_toc`: verifica paritatea initiala, confirma ca regiunea TOC apartine unui singur fragment, reasambleaza in memorie si compara byte-cu-byte rezultatul asteptat. Abia apoi pregateste temporar fragmentul, manifestul si manuscrisul si le inlocuieste cu rollback la esec de scriere.

Hashul `last_generated_sha256` este actualizat impreuna cu sursele. Alte campuri din manifest sunt pastrate. Astfel editia, data si changelogul aplicate de A1 raman in continutul fragmentelor si in manuscrisul produs. Modificarile editoriale din fragmente sunt reasamblate inainte de generarea wiki; ID-urile si ordinea manifestului nu sunt schimbate.

## Teste de regresie

Adaugate in `tests/test_studio.py`:

- TOC devine identic intre fragment si manuscris, hashul manifestului corespunde, iar ID-urile fragmentelor si metadatele de editie/data se pastreaza.
- Repetarea `--toc` fara diferente este determinista (returneaza zero modificari).
- Continutul editorial din fragment se regaseste in manuscris si in pagina wiki a capitolului.
- Lipsa marcajelor TOC opreste transformarea fara sa schimbe manuscrisul sau manifestul.

Testele folosesc repository-uri Git temporare si nu ating manuscrisul, fragmentele sau paginile wiki reale.

## A2.1 - remedieri Windows si build

- `archive_pr_guard.edition()` accepta acum terminatorul CRLF, pastrand aceeasi validare a formatului editiei. Testele acopera LF, CRLF si snapshot-uri Git temporare pentru ambele terminatoare; logica de coliziune si codurile de refuz nu au fost schimbate.
- Toate paginile Markdown generate si blocul de editie din homepage sunt scrise cu LF explicit. Continutul homepage-ului din afara markerelor este pastrat. `wiki_index_block.md` este tratat ca artefact local in `.studio-local/`, director ignorat deja de Git.
- `build.py --pdf` copiaza PDF-ul tocmai generat in `wiki/downloads/` si verifica egalitatea byte-cu-byte inainte ca `studio build --pdf` sa ruleze MkDocs strict si checkerul de linkuri.
- In modul HTML-only, Studio ruleaza MkDocs strict. Daca PDF-ul curent nu este verificat ca produs in build-ul prezent, raporteaza ca PDF-ul este indisponibil/nevalidat si omite checkerul linkurilor descarcabile. Nu declara toate linkurile verificate.
- Mesajul TOC foloseste „0 modificari” cand TOC-ul existent este deja sincronizat; nu inseamna cuprins gol. Testul verifica faptul ca intrarile se genereaza si raman in sursa/manifest.
- Testele adaugate acopera output LF, doua build-uri identice cu homepage manual, linkurile homepage, PDF identic la descarcare, paritatea sursa-manifest si conservarea fragmentelor la esecul validarii.
- `git diff --check`: PASS dupa conversia paginilor wiki deja modificate la LF.
- Testele Python nu au putut fi rulate in mediul agentului: comanda `python` lipseste, iar executabilul `.venv` se leaga la `C:\Users\Cristian\AppData\Local\Programs\Python\Python314\python.exe`, inaccesibil aici. Build-ul PDF, MkDocs si link checkerul nu au fost rulate in acest mediu.
- Nu au fost modificate manuscrisul, fragmentele canonice, arhive PDF istorice sau GitHub Actions. Nu au fost facute push, merge sau deploy.

## Bloc PowerShell pentru validarea finala A2

## Rezultat validare Windows A2.1

Validarea Windows raportata de proprietar a executat 54 de teste: 53 au trecut, iar `test_toc_build_updates_fragment_master_and_wiki_deterministically` a esuat la pregatirea fixture-ului, deoarece `wiki/` nu exista cand testul scria `wiki/index.md`. Testul creeaza acum explicit `index.parent` inainte de scriere. Verificarile existente pentru CRLF -> LF, continutul manual al homepage-ului, determinismul TOC si sincronizarea fragmentelor au fost pastrate.

A fost adaugat separat `test_wiki_build_creates_missing_wiki_directory_and_homepage`, care apeleaza direct generatorul cu directorul `wiki/` absent. Implementarea `build_wiki` creeaza `wiki/` prin `mkdir(parents=True, exist_ok=True)` inainte de `merge_index`, iar `merge_index` creeaza homepage-ul minim cand acesta lipseste.

Dupa modificare, testele nu au putut fi rerulate in mediul agentului: `.venv\\Scripts\\python.exe` depinde de Python 3.14 din profilul local Windows, iar executabilul respectiv este inaccesibil. `git diff --check` a trecut. Testul Windows raportat initial nu mai este considerat validare dupa corectie; gate-ul ramane `NOT_VERIFIED` pana la rerularea testului afectat si a suitei pe Windows.

Modificari pentru remedierea A2.1: doar `tests/test_studio.py` si aceasta evidenta. Nu s-au schimbat manuscrisul, fragmentele canonice, GitHub Actions sau PDF-urile istorice. Nu s-au facut push, merge ori deploy si nu a fost inceput A3.

## Comanda rerulare dupa corectie

```powershell
$ErrorActionPreference = 'Stop'
$python = '.\\.venv\\Scripts\\python.exe'
& $python -m unittest tests.test_studio.StudioTests.test_toc_build_updates_fragment_master_and_wiki_deterministically -v
if ($LASTEXITCODE -ne 0) { throw 'Testul TOC afectat a esuat.' }
& $python -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw 'Suita de teste a esuat.' }
git diff --check
if ($LASTEXITCODE -ne 0) { throw 'git diff --check a esuat.' }
```

## Bloc PowerShell pentru validarea finala A2

Rulati din radacina repository-ului intr-o sesiune PowerShell. Blocul opreste executia la prima eroare, verifica ramura, ruleaza suita de teste, build-ul cu PDF, MkDocs strict si checkerul de linkuri, apoi confirma paritatea si determinismul TOC. Build-ul poate actualiza TOC-ul canonic daca este necesar; toate celelalte transformari canonice sunt validate inaintea scrierii.

```powershell
$ErrorActionPreference = 'Stop'
$python = '.\.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) { throw "Python lipsa: $python" }
$branch = (& git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $branch -ne 'studio-test') { throw "Branch asteptat studio-test; gasit: $branch" }

& $python -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw 'Suita de teste a esuat.' }

function Get-WikiMarkdownHashes {
    $result = @{}
    Get-ChildItem -LiteralPath wiki -Recurse -File -Filter '*.md' | ForEach-Object {
        $relative = [IO.Path]::GetRelativePath((Get-Location).Path, $_.FullName)
        $result[$relative] = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash
    }
    return ,$result
}

& $python tools/studio.py --repo . build --pdf
if ($LASTEXITCODE -ne 0) { throw 'Build PDF, MkDocs strict sau verificarea linkurilor a esuat.' }
$pdf = 'Monografie_AI_De_la_Chat_la_Sisteme_Agentice.pdf'
$download = Join-Path 'wiki/downloads' $pdf
if (-not (Test-Path -LiteralPath $download)) { throw 'Lipseste PDF-ul descarcabil.' }
if ((Get-FileHash $pdf -Algorithm SHA256).Hash -ne (Get-FileHash $download -Algorithm SHA256).Hash) { throw 'PDF-ul descarcabil difera de cel generat.' }
$wikiFirst = Get-WikiMarkdownHashes

& $python tools/studio.py --repo . build --pdf
if ($LASTEXITCODE -ne 0) { throw 'Al doilea build PDF a esuat.' }
$wikiSecond = Get-WikiMarkdownHashes
if ($wikiFirst.Count -ne $wikiSecond.Count) { throw 'Numarul paginilor wiki s-a schimbat la rebuild.' }
foreach ($path in $wikiFirst.Keys) {
    if ($wikiFirst[$path] -ne $wikiSecond[$path]) { throw "Output wiki nedeterminist: $path" }
}

& $python tools/studio.py --repo . assemble
if ($LASTEXITCODE -ne 0) { throw 'Round-trip-ul fragmente -> manuscris a esuat.' }
git diff --check
if ($LASTEXITCODE -ne 0) { throw 'git diff --check a esuat.' }
Write-Host 'PASS A2: teste, PDF descarcabil identic, build-uri deterministe, round-trip si diff-check.'
```

## Stare

Remedierile A2.1 sunt implementate, dar gate-ul ramane `NOT_VERIFIED` pana la rularea blocului de mai sus pe Windows si confirmarea rezultatelor. Rezultatele anterioare A1/A2 raportate de proprietar raman distincte de aceasta validare. PDF-ul real nu a fost generat de agent.
