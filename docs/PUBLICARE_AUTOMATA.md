# Publicarea automata a monografiei

## Sursa canonica si previzualizarea

Sursa editoriala este `Monografie_AI_De_la_Chat_la_Sisteme_Agentice.md`. PR-urile sunt validate doar cu drepturi de citire: `bash tools/ci-build.sh` produce Markdown, wiki, PDF si un artefact `monografie-preview` in GitHub Actions.

Doar proprietarul face merge in `main`. Niciun PR nu poate publica automat PDF-ul final.

## Publicarea dupa merge in main

La fiecare modificare care declanseaza workflow-ul de publicare:

1. `tools/release.py` verifica editia din sursa in raport cu primul parinte Git al merge-ului. Daca PR-ul a stabilit deja explicit o editie noua (de exemplu 1.1 -> 1.2), o respecta. Altfel, creste incremental: **1.2 -> 1.2.1 -> 1.2.2**.
2. Se actualizeaza data in fusul Europe/London, coperta, citarea, Anexa E si sumarul editiei. Se adauga o sectiune E.n pentru modificarile publicate, derivata transparent din commitul integrat. Rezumatul generat identifica tipurile de fisiere schimbate si provenienta, nu inventeaza modificari de continut.
3. `tools/build.py --toc --wiki --pdf` reconstruieste cuprinsul, paginile wiki si PDF-ul. Lint, teste, MkDocs strict si verificarea PDF-ului trebuie sa treaca.
4. `tools/archive_pdf.py` creeaza in `docs/` o copie cu numarul exact al editiei, actualizeaza si PDF-ul cu nume stabil si reconstruieste lista istorica din `docs/README.md`.
5. Workflow-ul face un singur commit tehnic al versiunii si al arhivei catre `main`, numai dupa validare, apoi publica site-ul prin GitHub Pages.

Commitul automat este facut cu tokenul standard GitHub Actions si `[skip ci]`. Nu provoaca o noua rulare `push`, deci nu genereaza o editie noua in bucla. Daca regulile de protectie ale ramurii interzic commitul botului, jobul **esueaza explicit**, iar arhivarea nu este declarata completa.

O noua editie este atasata **fiecarui merge relevant in main**, nu fiecarui commit intermediar dintr-un PR. Un `workflow_dispatch` manual regenereaza aceeasi editie fara incrementare; daca exista deja o arhiva, se reutilizeaza fisierul istoric imuabil.

## URL-uri

- Wiki: https://chrsdme.github.io/Monografie_AI/
- PDF curent (link stabil): https://chrsdme.github.io/Monografie_AI/downloads/Monografie_AI_De_la_Chat_la_Sisteme_Agentice.pdf
- Arhiva pe GitHub: https://github.com/chrsdme/Monografie_AI/tree/main/docs
- Lista versiunilor: https://github.com/chrsdme/Monografie_AI/blob/main/docs/README.md

## Controlul editiei si istoriei

- `tools/lint.py` impune coerenta dintre front matter, coperta, citare, Anexa E, notele finale si changelog.
- Fisierele PDF numerotate nu sunt suprascrise. Incercarea de a republica alte octeti sub acelasi numar de editie la un eveniment `push` produce eroare.
- Changelogurile vechi sunt pastrate; cele noi sunt adaugate incremental.
- Mesajele de commit pot fi insuficient de detaliate. Pentru o versiune majora, descrierea istoricului trebuie revizuita editorial in PR inainte de merge.
- PDF-ul din radacina repo ramane snapshot istoric; `docs/` este arhiva oficiala.
- GitHub Pages si `docs/` folosesc aceeasi copie verificata a PDF-ului.

## Publicare locala (optionala)

```bash
python -m pip install -r requirements.txt -r tools/requirements.txt
python -m playwright install --with-deps chromium
bash tools/ci-build.sh
```

Pentru editare obisnuita sunt suficiente PR-ul si verificarea artefactului PDF din Actions.

## Plan editorial separat

Migrarea optionala la surse modulare `content/` si `book.yml` ramane o lucrare diferita. Feedbackul cititorilor este deja disponibil prin formularul Tally integrat in wiki.
