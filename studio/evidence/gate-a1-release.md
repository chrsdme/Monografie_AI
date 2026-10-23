# Gate A1 - Release Adapter

Data: 2026-10-23
Branch: `studio-test`

## Stare

**A1 validat local de proprietar.** Testele tintite, dry-run-ul real si reasamblarea ulterioara au trecut conform rezultatelor furnizate de proprietar. Acestea sunt dovezi separate de verificarile executate de agent.

## Dovezi executate de proprietar

Conform `studio/evidence/gate-a-verification.md` si informatiilor furnizate de proprietar:

- Manifestul contine 242 de fragmente in ordinea explicita `BOOK-0001`–`BOOK-0242`.
- `original_sha256` si `last_generated_sha256` sunt `1e12008817bd34dcf161b4aa4f59cae94689fba04dd68c632ba2b5ae253b70ed`.
- `tools/studio.py assemble` a reasamblat manuscrisul byte-identic cu acelasi SHA256.
- Proprietarul a verificat fragmentele in PowerShell; nu s-a repetat migrarea.

Proprietarul a furnizat ulterior dovezi directe pentru A1: 10/10 teste `test_studio_release.py` PASS pe Windows; dry-run real PASS cu exit code 0 pentru tranzitia 1.2.5 -> 1.2.6; fragmente afectate `BOOK-0001`, `BOOK-0002`, `BOOK-0004`, `BOOK-0232`, `BOOK-0242`; fragment nou propus `BOOK-0243`; reasamblare PASS cu SHA256 `1e12008817bd34dcf161b4aa4f59cae94689fba04dd68c632ba2b5ae253b70ed`; manuscrisul original nemodificat. Aceste rezultate sunt raportate de proprietar, nu executate de agent.

## A1.1 - Cauza si corectie

- Cauza identificata in `_project`: un `SequenceMatcher` rula pe manuscrisul concatenat pentru toate modificarile, dupa extragerea optionala a changelog-ului. Un edit care atingea o limita de fragment putea avea mai multi candidati si era respins cu `Conflict: schimbarea traverseaza fragmente sau nu are proprietar unic`.
- Adaptorul proiecteaza acum separat marcajele editoriale folosite de `release.py`: editie, editie precedenta, ancora changelog, data, coperta, introducere, editia curenta din anexa, citare si footer. Fiecare marcaj trebuie sa aiba un singur fragment proprietar.
- Sectiunea noua se extrage prin ancora bibliografiei. Se insereaza in fragmentul care detine acea pozitie; daca bibliografia incepe un fragment, se creeaza un fragment changelog cu ID-ul liber urmator, fara renumerotarea celor existente.
- Proiectia se reasambleaza si se compara byte-cu-byte cu iesirea calculata de `release.py`. Conflictele raporteaza operatia, tipul, intervalul si ID-urile fragmentelor implicate fara sa afiseze continutul manuscrisului.
- Pentru cai `content/book/`, adaptorul furnizeaza catre `release.py` categoria existenta pentru continutul monografiei, evitand descrierea generica.
- La esec dupa o scriere, rollback-ul restaureaza fisierele deja inlocuite; fisierul temporar al inlocuirii esuate este curatat.

## Inspectie si teste locale

- Adaptorul implementeaza push cu incrementare patch sau editie declarata, `workflow_dispatch`/`release` fara incrementare si proiectarea changelog-ului in fragmente. Testele fixture din `tests/test_studio_release.py` contin cazuri pentru incrementare si changelog, editie declarata, `workflow_dispatch`, arhiva, hash/manifest, staging reusit si esec de validare inainte de scriere.
- Testul numit `test_failed_validation_never_changes_sources` acopera separat oprirea inainte de scriere.
- Au fost adaugate fixture-uri pentru schimbari in fragmente diferite cu ID-uri pastrate, changelog la granita bibliografiei, clasificarea `content/book/` si rollback dupa primul `os.replace`.
- Initial, Python nu a putut porni in mediul agentului. In aceasta sesiune Python a devenit disponibil: cele 10 teste `test_studio_release.py` au trecut ca parte a suitei complete. Aceasta executie este distincta de rularea Windows raportata de proprietar.

## Scenarii A1 si rezultate

| Scenariu | Dovada disponibila | Stare |
|---|---|---|
| Incrementare patch, campuri si changelog | Dry-run real 1.2.5 -> 1.2.6; fragmente si fragment nou raportate mai sus | PASS - proprietar |
| Editie declarata si actualizare data | Test fixture `test_explicit_edition_refreshes_date_cover_citation` | PASS - agent si proprietar |
| `workflow_dispatch` fara incrementare si `release` archive-only | Test fixture `test_workflow_dispatch_and_archive_do_not_increment` | PASS - agent si proprietar |
| Rollback dupa scriere partiala | Test fixture `test_partial_write_failure_restores_fragments_and_manifest` | PASS - agent si proprietar |
| Asamblare reala | SHA256 `1e12008817bd34dcf161b4aa4f59cae94689fba04dd68c632ba2b5ae253b70ed`; manuscrisul original nemodificat | PASS - proprietar |

## Limite si pasul necesar

- S-au modificat adaptorul, testele si acest raport. Nu s-au modificat manuscrisul, fragmentele reale, `release.py`, `build.py`, workflow-urile sau PDF-urile istorice.
- Nu s-a rulat `apply()`, build, generare PDF, push, merge sau deploy.
- Agentul nu a rulat `apply()` pe sursele reale, build, PDF, push, merge sau deploy. A1 este validat local de proprietar; testele fixture au rulat separat in mediul agentului.

## Comenzi PowerShell pentru proprietar

Din radacina repository-ului, folositi un Python accesibil si nu rulati `apply()`:

```powershell
$python = '.\.venv\Scripts\python.exe'
& $python -m unittest discover -s tests -p test_studio_release.py -v
& $python tools/studio_release.py --repo . --event push --date "23 octombrie 2026" --previous-edition 1.2.4 --changed content/book/manifest.json --message "A1.1 release adapter verification" --sha abcdef0123456789
& $python tools/studio_release.py --repo . --event push --date "23 octombrie 2026" --previous-edition 1.1 --changed wiki/index.md --message "A1.1 declared edition verification" --sha abcdef0123456789
& $python tools/studio_release.py --repo . --event workflow_dispatch --date "23 octombrie 2026"
& $python tools/studio_release.py --repo . --event release --date "23 octombrie 2026"
Get-FileHash -Algorithm SHA256 -LiteralPath 'Monografie_AI_De_la_Chat_la_Sisteme_Agentice.md'
```

Confirmati pentru fiecare dry-run JSON cu exit code 0, iar pentru primul caz comparati SHA256-ul `after_sha256` cu rezultatul reasamblat temporar. Scenariile si testul rollback raman `NOT_VERIFIED` pana la acele rezultate.

Comenzile de mai sus sunt pastrate ca jurnal istoric; rezultatele proprietarului consemnate aici au validat A1.
