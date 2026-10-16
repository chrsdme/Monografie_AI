# Publicare automata a monografiei

## Obiectiv

Sursa editoriala curenta este `Monografie_AI_De_la_Chat_la_Sisteme_Agentice.md`. Workflow-urile GitHub Actions regenereaza paginile wiki si un PDF nou din acest fisier, fara sa creeze commit-uri automate pe `main`.

Acest document se refera la **PR 1**, inainte de modularizarea capitolelor. Paginile comunitatii sunt pastrate de generator si in configuratia MkDocs.

## Pentru o corectie sau completare

1. Creeaza un branch pornind din `main`.
2. Modifica fisierul `Monografie_AI_De_la_Chat_la_Sisteme_Agentice.md`. Nu edita separat paginile generate din `wiki/partea-*/` sau anexele generate.
3. Pentru schimbari ale structurii actuale (capitol/parte noua), generatorul necesita inca modificarea maparii din `tools/build.py` si navigatiei din `mkdocs.yml`. Aceasta limitare va fi eliminata in PR 2.
4. Deschide un Pull Request. Workflow-ul de validare executa lint, construieste wiki si PDF, verifica paginile si ruleaza `mkdocs build --strict`.
5. Descarca din Actions artefactul `monografie-preview` pentru verificarea PDF si a site-ului. Nu se publica un PR in GitHub Pages.
6. Dupa review, face merge proprietarul. Workflow-ul de deploy regenereaza din `main` si publica site-ul cu PDF-ul.

## URL-uri stabile

- Documentatie: https://chrsdme.github.io/Monografie_AI/
- PDF publicat: https://chrsdme.github.io/Monografie_AI/downloads/Monografie_AI_De_la_Chat_la_Sisteme_Agentice.pdf

Fisierul PDF aflat la radacina repository-ului ramane un snapshot istoric. PDF-ul din Pages este regenerat la fiecare deploy care atinge fisierele urmarite.

## Comenzi locale (optionale)

Necesita Python 3.12, Pandoc, Playwright cu Chromium si pypdf / MkDocs:

```bash
python -m pip install -r requirements.txt -r tools/requirements.txt
python -m playwright install --with-deps chromium
bash tools/ci-build.sh
```

GitHub Actions instaleaza singur dependintele. Pentru o editare obisnuita nu este nevoie sa rulezi generatorul pe calculator.

## Restrictii si verificari

- Workflow-urile nu trimit credentiale de scriere catre codul venit prin PR; au doar `contents: read` la validare.
- Merge-ul si publicarea pe `main` necesita in continuare decizia proprietarului.
- Scriptul publica PDF-ul doar daca verificarea internala a cuprinsului este stabila si site-ul trece `mkdocs build --strict`.
- Dependintele de pe runner pot produce diferente de font sau paginare; verifica vizual previzualizarea PDF cand introduci modificari ample.
- Nu sunt create automat GitHub Releases si nici commit-uri cu PDF la radacina. Arhivarea editiilor oficiale prin Releases necesita un pas ulterior, separat de publicarea zilnica.
- Modificari doar in fisiere neincluse in filtrele de eveniment nu declanseaza automat publicarea; exista si `workflow_dispatch` pentru rulare manuala.
- Nu activa AI Scan sau alte servicii platite pentru acest workflow.

## Etapele urmatoare, separate

**PR 2 - Sursa modulara.** Migrare fara pierderi la `content/...` si un manifest `book.yml` pentru ordinea partilor, capitolelor si anexelor. Generatorul uneste sursele in Markdown integral si pastreaza URL-urile wiki existente. Verificam comparatia continutului si o editie PDF inainte de merge.

**PR 3 - Feedback Tally.** Un formular Tally public, fara cont GitHub pentru cititori. Linkurile contextuale din capitole vor transmite URL-ul paginii prin `?page=...` catre un camp ascuns Tally. Sugestiile raman private pana la triere si nu creeaza automat PR-uri. URL-ul real al formularului si campurile de confidentialitate sunt necesare inainte de activare.
