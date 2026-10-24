# Monografie Studio (dezvoltare izolata pe \`studio-test\`)

Un editor offline fara CMS, baza de date sau interfata personalizata: fisiere Markdown independente, un manifest de ordine, un CLI Python, MkDocs pentru preview si PR-uri GitHub pentru publicare.

## Stare

Acest director este **bootstrap-ul de dezvoltare**. Nu reprezinta o migrare finalizata si nu trebuie integrat in main pana cand toate criteriile sunt confirmate in CI.

## Surse canonice

- \`content/book/fragments/\`: sectiunile cartii, cu ID-uri stabile in \`content/book/manifest.json\`, dupa migrare.
- \`content/articles/\`: articole independente pentru wiki.
- \`content/resources/\`: resurse documentate si catalogate pe wiki.
- \`inbox/\`: materialele locale brute (Git-ignored), cu \`zzz.yaml\`.
- \`Monografie_AI_De_la_Chat_la_Sisteme_Agentice.md\`: sursa actuala pe main; va deveni un artefact derivat doar dupa testul de conversie si adaptarea release-ului.

## Contract de destinatii

- \`wiki\`: articol vizibil pe site, nu modifica manuscrisul.
- \`book\`: intra in monografie si in capitolul sau de pe wiki; aceasta e singura destinatie care modifica textul cartii.
- \`resource\`: intrare in catalogul de resurse si articol sau pagina pe wiki.
- \`[book, resource]\`: aceeasi sursa apare in carte, wiki si catalog. Nu duplica textul manual.

## Trei moduri de lucru

1. Manual: editezi fisierul Markdown canonic, reconstruiesti si deschizi preview local.
2. Asistat Codex: creezi \`inbox/zzz.yaml\`, Codex propune incadrarea si patch-uri; omul aproba fiecare integrare, nu fiecare comanda.
3. Automatizat: doar materiale aprobate, valida schema, construieste, testeaza si pregateste PR; merge-ul ramane manual.

## Workflow pentru Codex

Citeste \`AGENTS.md\` si \`studio/IMPLEMENTATION.md\`. Implementarea are etape de acceptare separate; nu declara \`DONE\` dupa simple modificari de fisiere. Testeaza intai un round-trip byte-identic al manuscrisului, apoi activeaza generarea din fragmente. Nu importa materialele private fara consimtamantul proprietarului.

## Comenzi planificate

\`python tools/studio.py migrate\`, \`assemble --check\`, \`assemble --write\`, \`build\`, \`preview\`, \`check\`, \`status\`, \`new\`, \`batch plan\`, \`batch apply\`, \`pr\`.

Documentatia detaliata si criteriile sunt in \`studio/IMPLEMENTATION.md\`. Nu considera o comanda functionala pana cand testele sale nu au trecut.
