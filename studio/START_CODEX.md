# Handover catre Codex, pe Windows

**Branch obligatoriu:** studio-test.
**Locatie:** D:\monografie\Monografie_AI.
**Interzis:** push pe main, merge, deploy, overwrite de arhiva PDF, publicare automata, commit de inbox.

## Prompt de pornire

> Citeste in intregime AGENTS.md, studio/IMPLEMENTATION.md si studio/README.md. Verifica in mod read-only starea actuala a branch-ului studio-test, generatorul tools/build.py, tools/release.py, .github/workflows/docs.yml, tools/archive_pdf.py, archive_pr_guard.py, testele si fisierele canonice.
>
> Avem deja bootstrap-ul tools/studio.py cu comenzi migrate, assemble, status, new, plan, build, preview, check, precum si template-uri detaliate. Acestea sunt un inceput, nu o implementare completa. Evalueaza-le critic, corecteaza defectele si completeaza Gate A-D din studio/IMPLEMENTATION.md; nu reimplementa totul doar pentru ca poti.
>
> PRIORITATE 1: ruleaza mai intai testele studio si migrarea round-trip a monografiei. Verifica SHA256 sursa, fragmente, asamblare si continutul anexelor, figurilor, bibliografiei, codurilor si ancorelor. Nu activa sursa fragmentata pana cand round-trip este byte-identic si generatorul existent poate produce aceleasi outputuri relevante. Nu schimba in prima etapa textul, ordinea sau stilul monografiei.
>
> PRIORITATE 2: modifica release.py si build workflow astfel incat sursa canonica sa fie fragmentele, iar edition, date, changelog si arhivarea PDF sa ramana coerente. Nicio schimbare wiki-only sau resource-only nu trebuie sa injecteze text editorial in carte. Preserva protectiile pentru editie duplicata/PR concurent. Regenereaza indexul cu ID-uri stabile; sursele si glosarul folosesc legaturi explicite, fara schimbari tacite de ancore.
>
> PRIORITATE 3: implementeaza targeturile wiki/book/resource si toate combinatiile semnificative, inclusiv book+resource. Testeaza ca wiki-only si resource-only nu schimba corpul cartii. Automatizeaza indexurile si navigatia, fara sa duplice textul sursa.
>
> PRIORITATE 4: implementeaza flow-ul Codex batch cu zzz.yaml, plan cu dovezi si diff, owner approve separat de verifier, apply atomic cu hashuri verificate, preview vizual MkDocs (light/dark) si pr pregatit dupa validare. Nu este permis niciun PR/merge/push fara autorizare explicita a proprietarului.
>
> Foloseste doar comenzile realmente disponibile in mediul Windows; daca este nevoie de dependente, explica instalarea si fa-o numai cu permisiunea din context. Pastreaza o lista de findings si rezultate de teste in studio/evidence/. Pentru orice blocaj returneaza partial precis, nu inventa PASS. Opreste-te dupa Gate A daca descoperi incompatibilitati majore sau nevoia de decizii editoriale.
>
> Livreaza: comenzi reale de utilizare, structura finala, diff, fixture-uri pentru cele patru destinatii, teste unittest/MkDocs/PDF, raport asupra migrarii (hashuri) si demonstratia preview. Nu face PR decat dupa confirmarea proprietarului.

## Primii pasi

1. \`git branch --show-current\` trebuie sa fie \`studio-test\`.
2. \`python tools/studio.py status\`.
3. \`python -m unittest discover -s tests -p "test_studio.py" -v\`.
4. \`python tools/studio.py migrate\`.
5. \`python tools/studio.py assemble\` (round-trip).
6. Compara \`git diff -- Monografie_AI_De_la_Chat_la_Sisteme_Agentice.md\`: trebuie sa fie gol dupa migrare.
7. Nu rula \`studio build\` pana cand \`release.py\` si logica generarii nu sunt adaptate si validate pentru sursa fragmentata.
