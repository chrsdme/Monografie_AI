# Audit site si monografie - 22 octombrie 2026

## Domeniu si dovezi

Baza: artefactul `github-pages` din rularea [39826920056](https://github.com/chrsdme/Monografie_AI/actions/runs/39826920056), dupa integrarea PR #26. Site-ul publicat este generat la editia 1.2.4; manifestul stabil din `main` ramane la 1.2.3 pana la integrarea PR #27.

Auditul HTML a acoperit 42 de fisiere HTML (41 de pagini cu `index.html`, plus pagina `404.html`) si aproximativ 3.055 de referinte locale din linkuri, imagini, scripturi si stylesheet-uri. A fost comparata si structura celor 22 de capitole, anexele A-E, cele 8 figuri si bibliografia cu 44 de intrari, din Markdown-ul generat pentru editia 1.2.4.

## Probleme confirmate

1. **Link intern defect, homepage:** panoul editiei introduce un URL raw HTML `anexe/metoda-surse.md#...`, neprelucrat de MkDocs. Ruta reala este `anexe/metoda-surse/#...`. Rezultat inainte de fix: 1 referinta locala invalida. Dupa fix, auditul local al artefactului: 0/3.055 invalid.
2. **Changelog Markdown:** `tools/release.py` emitea `\\`...`` cu backtick-uri escapate, afisate drept semne literale, nu cod inline. Corectat la generator si in sursa istoricului.
3. **Publicare intermitenta:** workflow-ul #39825849119, pornit dupa PR #25, a esuat la verificarea contrastului unui link in light mode, fara deploy. Workflow-ul #39826920056, pornit dupa PR #26, a trecut si a publicat interfata corectata. Tranzitia CSS a linkurilor inline a fost dezactivata, pentru a evita stari intermediare cu contrast insuficient.
4. **Separare editie publicata/arhivata:** varianta live 1.2.4 este distincta de versiunea persistata in `main` (1.2.3) pana la integrarea PR #27. Arhiva istorica nu trebuie rescrisa sau dublata.

## Verificari trecute

- MkDocs `--strict` si verificari anterioare de corespondenta intre sursa Markdown, paginile wiki si PDF, conform workflow-ului publicat.
- Niciun marcaj literal `:material-...:` ramas in paginile HTML extrase.
- Imaginile, intrarile din meniu si tintele locale din paginile generate au fost analizate static. Auditul automat nu inlocuieste interactiunea manuala cu toate elementele UI.
- Verificari factuale **selective**, pe surse primare: termene AI Act / AI Omnibus (Comisia Europeana, octombrie 2026), A2A 1.0 (repo oficial A2A), OWASP Agentic Top 10 (OWASP, decembrie 2025), disparitati de tokenizare (Petrov et al., 2023). Nu au rezultat contradictii din aceste verificari.

## Limite si continuare

- Nu a fost efectuata o verificare a disponibilitatii *tuturor* linkurilor externe si nici o validare independenta pentru toate afirmatiile factuale din carte.
- Nu se pretinde certificarea tuturor combinatiilor browser-dispozitiv. Testele Playwright existente valideaza contrastul, butoanele si mobilul pe paginile colectiilor, in ambele scheme.
- Recomandat: integrarea arhivei #27 inaintea PR-ului de remediere, apoi verificare vizuala pe domeniul public (eventual hard refresh daca browserul pastreaza o versiune cache).

## Surse primare pentru verificarile factuale

- [Comisia Europeana - AI Omnibus](https://digital-strategy.ec.europa.eu/en/news/ai-omnibus-enters-force)
- [Comisia Europeana - AI Act enforcement](https://digital-strategy.ec.europa.eu/en/policies/enforcement-ai-act)
- [A2A v1.0, release](https://github.com/a2aproject/A2A/releases/tag/v1.0.0)
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [Petrov et al. (2023), arXiv:2305.15425](https://arxiv.org/abs/2305.15425)
