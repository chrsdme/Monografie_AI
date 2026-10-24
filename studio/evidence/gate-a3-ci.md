# Gate A3.1 - Tranzitie sigura legacy-to-Studio

Data: 2026-10-23
Branch: `studio-test`
Stare: cod si teste pregatite; executia Python locala este `NOT_VERIFIED`.

## Rutare release si coerenta canonica

- Cu manifest prezent, workflow-ul foloseste `studio_release.py`. Cand `STUDIO_RELEASE_ENABLED` este exact `true`, ruleaza release Studio; in rest ruleaza `--legacy-compatible`, care pastreaza politica existenta din `release.py` si reconciliaza fragmentele.
- Fara manifest, workflow-ul continua sa ruleze `release.py`. Variabila nu este schimbata. Release-ul Studio activ nu ruleaza operatiile legacy in paralel.
- Baseline-ul manifestului este verificat inainte de proiectie. Manuscrisul trebuie sa corespunda hashului generat anterior; schimbari independente ale manuscrisului/fragmentelor, hashuri stale, ID-uri duplicate, locuri ambigue sau diferente in afara campurilor release cunoscute opresc pasul inainte de build/arhivare/upload/deploy.
- Numai campurile canonice produse de `release.py` si changelogul sau sunt proiectate. Fragmentele existente isi pastreaza ID-urile si ordinea; changelogul de la granita bibliografiei primeste urmatorul ID stabil.
- Manuscrisul, fragmentele si manifestul sunt scrise din staging temporar dupa reasamblare byte-cu-byte. Esecul de inlocuire restaureaza fisierele deja inlocuite. Sincronizarea TOC cere de asemenea paritate cu baseline-ul verificat.

## Arhivare si clasificare

- Persistenta arhivei fara manuscris este acceptata cand commitul Git modifica exact metadata publicatiei si PDF-ul editiei, metadata corespunde editiei curente si SHA256-ul PDF-ului, iar manuscrisul din `HEAD^` si `HEAD` este identic.
- Pentru un manuscris care difera editorial de baseline, clasificatorul cauta in istoricul Git commitul de release si commitul editorial parinte, apoi reexecuta `release.update_text` cu caile, mesajul si SHA-ul reale din commit. Tranzitia trebuie sa corespunda byte-cu-byte, versiunea trebuie sa fie urmatorul patch, iar verificarea trebuie sa aiba o singura potrivire.
- Niciun changelog nu este eliminat din comparatie. Orice editare independenta, inclusiv in sectiuni E.x, ramane detectabila si produce NON-ARCHIVE. Fara istoric Git reproductibil, validare PDF/metadata sau paritate manifest-fragmente-manuscris, clasificatorul refuza cazul.
- PDF-urile istorice raman imuabile; un PDF local cu bytes diferiti este refuzat fara suprascriere.
- Lista de staging initiala ramane de 260 fisiere. Modificarile A3.1 ating numai fisiere deja incluse in acea lista: workflow, raport, teste si unelte Studio/archive guard. PDF-ul local, `wiki/downloads/`, `inbox/`, drafturi si `.studio-local/` sunt excluse.

## Teste si verificari

- Testul de integrare nou simuleaza intr-un repository Git temporar commitul initial, push editorial, reconcilierea legacy, arhivarea archive-only fara incrementare, al doilea release legacy si release Studio ulterior cu o singura incrementare per push.
- Testele acopera esec de validare si rollback partial existent, hash/manuscris/fragmente divergente, PDF istoric cu bytes diferiti si modificare editoriala combinata cu metadata de arhiva.
- Verificare Windows pe checkout-ul `studio-test`: `test_archive_pr_guard.py` 13/13 PASS; `test_studio_release.py` 16/16 PASS; suita completa `unittest discover -s tests -v` 64/64 PASS.
- Fixture-urile Git verifica distinct commitul archive-only cu exact doua cai si manuscris identic, apoi un release automat reprodus din commiturile sursa reale. O editare independenta in E.1, cu manifestul si fragmentele in continuare consistente, este respinsa.
- MkDocs strict, build PDF complet si published-link checker nu au fost rulate in aceasta verificare concentrata pe clasificator.
- Risc GitHub Actions: testul end-to-end nu a rulat aici. Primul push cu manifest si Studio inactiv va valida calea noua in runner. Orice conflict de baseline opreste jobul inainte de build si publicare.

Nu s-au facut commit, push, merge, deploy, activare sau release.

## Bloc PowerShell unic pentru verificarea Windows

Ruleaza din radacina repository-ului dupa checkout complet, pe `studio-test`, cu Python functional:

```powershell
$ErrorActionPreference = 'Stop'
$python = '.\.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) { throw "Python lipsa: $python" }
$branch = (& git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $branch -ne 'studio-test') { throw "Branch asteptat studio-test; gasit: $branch" }
if (-not (Test-Path -LiteralPath 'content/book/manifest.json')) { throw 'Manifest lipsa din checkout.' }

& $python -m unittest discover -s tests -p 'test_studio_release.py' -v
if ($LASTEXITCODE -ne 0) { throw 'Testele studio_release au esuat.' }
& $python -m unittest discover -s tests -p 'test_archive_pr_guard.py' -v
if ($LASTEXITCODE -ne 0) { throw 'Testele archive_pr_guard au esuat.' }
& $python -m unittest discover -s tests -p 'test_release_archive.py' -v
if ($LASTEXITCODE -ne 0) { throw 'Testele release/archive au esuat.' }
& $python -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw 'Suites existente au esuat.' }
& $python -m py_compile tools/studio.py tools/studio_release.py tools/release.py tools/archive_pdf.py tools/archive_pr_guard.py
if ($LASTEXITCODE -ne 0) { throw 'Compilarea Python a esuat.' }
git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw 'git diff --cached --check a esuat.' }
git diff --check
if ($LASTEXITCODE -ne 0) { throw 'git diff --check a esuat.' }
Write-Host 'A3.1 verificat: teste, compilare si ambele diff-check-uri.'
```
