# Anexa D. Metoda de studiu si utilizarea responsabila a surselor

O lucrare educationala despre AI imbatraneste repede daca amesteca principiile generale cu descrierea unor functii comerciale trecatoare. De aceea merita sa pastrezi in Markdown data accesarii, titlul sursei si legatura dintre afirmatie si documentatie. Cand un furnizor isi schimba platforma, actualizezi exemplele, nu rescrii toata arhitectura conceptuala.

Ca sa inveti gradual, poti urma un ciclu repetabil: citesti o definitie, o reformulezi cu cuvintele tale, incerci un exemplu mic, observi un esec, identifici sursa cauzei si notezi ce s-a schimbat. Articolele practice despre baze personale de cunostinte sustin ideea de a pastra surse, versiuni si rezultate reutilizabile [S21](../anexe/bibliografie.md#s21). Ghidul UNESCO pentru AI generativ in educatie si cercetare insista, la randul lui, pe utilizarea responsabila si pe pastrarea controlului uman asupra invatarii [S24](../anexe/bibliografie.md#s24). Nu ai nevoie de o colectie uriasa de documente. O nota bine verificata valoreaza mai mult decat douazeci de linkuri uitate.

O varianta aplicata la securitate porneste de la un buletin oficial, trece printr-o sursa de context si se incheie cu un raport scurt care separa vulnerabilitatea, produsul afectat, verificarea si masura recomandata. Metoda e ilustrata in ghiduri educationale despre studiul CVE-urilor si al advisories [S25](../anexe/bibliografie.md#s25). In aceasta carte devine un exemplu general despre provenienta si verificabilitate, nu un curs separat de securitate cibernetica.

**Ce nu includem ca dovezi.** Nu preluam procente de crestere a productivitatii din brosuri fara sa cunoastem esantionul, contextul si metodologia. Nu transformam etichetele de marketing in taxonomii stiintifice. Nu copiem instructiuni comerciale asociate unui produs doar pentru ca sunt prezentate ca reteta universala. Cand folosim materiale ale furnizorilor, extragem mecanismele generalizabile, le verificam pe cat se poate in alte surse si notam limitele. Comunicatele si paginile de proiect cu cifre le citim cu lista de intrebari din sectiunea 21.6.

**Cum marcam ce stim si ce nu.** In text, o afirmatie legata de o sursa poarta trimiterea [Sxx]. O inferenta a autorului, adica o concluzie care nu apare ca atare in sursa, este formulata cu verbe precum "poate", "de regula" sau "in practica". Informatiile care se schimba repede (versiuni de protocol, termene legale, preturi) poarta data consultarii in bibliografie si trebuie reverificate inainte de folosire.


# Anexa E. Istoricul editiilor si ce s-a schimbat in editia 1.1

## E.1. Informatii despre lucrare

- **Titlu:** De la conversatia cu AI la sisteme agentice verificabile.
- **Autor:** chrsdme.
- **Editia curenta:** 1.1, 15 octombrie 2026 (editia 1.0: 13 octombrie 2026).
- **Licenta:** MIT. Reutilizarea trebuie sa respecte conditiile licentei din depozit.
- **Versiunea web:** https://chrsdme.github.io/Monografie_AI/
- **Sursa editabila:** https://github.com/chrsdme/Monografie_AI
- **Citare recomandata:** chrsdme (2026), *De la conversatia cu AI la sisteme agentice verificabile*, editia 1.1, 15 octombrie 2026, https://chrsdme.github.io/Monografie_AI/.

Fisierul Markdown este sursa unica. Pagina web si PDF-ul se genereaza din aceeasi revizie, ca sa afiseze aceeasi editie si aceeasi data.

## E.2. Changelog 1.0 la 1.1

**Rescriere.** Intregul text a fost rescris pentru un ritm mai natural: fraze si paragrafe de lungimi diferite, explicatii cu analogii si exemple, citate scurte din surse primare. Continutul tehnic s-a pastrat acolo unde era corect.

**Corectat**

- Numerotarea: sectiunile 8.7, 8.8 si 9.7, care lipseau, au fost completate cu continut nou; numerotarea este acum continua in toata lucrarea.
- Greseli de scriere: "Instruciuni" (6.3), "un incantatie" (6.1), `linkuri_surze` (B.3), "ejecutarilor" (glosar).
- Introducerea Partii V descria "doua proiecte"; acum precizeaza ca sunt patru studii simulate si o sectiune cu cazuri publice reale.
- Afirmatia "95% dintre facturile standard", fara sursa, a fost inlocuita cu o formulare fara cifra.
- OWASP: editiile 2025 si 2026 ale listei LLM sunt citate separat (Excessive Agency este LLM06:2025 in prima si LLM03:2026 in a doua).
- Figurile: toate cele opt sunt numerotate (Figura 1 pana la Figura 8) in ordinea aparitiei, cu legenda unica si trimitere in text. Exemplul din Figura 6 a fost aliniat cu textul (3 clase, 7 instante).
- Glosarul: ordine alfabetica reala si termeni noi.
- Bibliografie: linkul MCP (S07) actualizat la pagina de arhitectura; linkul OpenTelemetry (S12) la depozitul oficial de conventii; intrarea S19 desfacuta de linkul secundar; intrarea S22 separata in doua surse; o sursa comerciala necitata in text (S26 in editia 1.0) a fost eliminata, iar numerotarea surselor este acum continua, S01 pana la S40.
- Nota despre "sase PDF-uri furnizate" a fost inlocuita cu o declaratie neutra despre materialele personale nepublicate folosite drept context.

**Adaugat**

- Sectiuni noi: 8.7 (masurarea unui sistem RAG), 8.8 (GraphRAG si limitele RAG simplu), 9.7 (cinci tipare de workflow), 18.7 (cadrul legal european), 20.5 (parghii concrete de cost), 21.6 (cum citim un caz cu cifre: Raleigh si Cordoba), Anexa E.
- Completari punctuale: starea protocolului MCP si donarea lui catre Linux Foundation (7.4), protocolul A2A (14.5), evaluari de capabilitate si de regresie, `pass@k` si `pass^k`, interval Wilson si regula celor trei (cap. 17), computer use (18.3), reluarea nodurilor in LangGraph (19.3), diferente de tokenizare intre limbi (20.1), prompt caching (20.5).
- Front matter cu autor, licenta, adresa web si adresa sursei.
- Cuprins cu trimiteri functionale in PDF si in versiunea web.

**Neinclus intentionat.** Cifre de performanta si afirmatii din auditurile externe pe care nu le-am putut confirma dintr-o sursa primara accesibila au fost lasate deoparte. Cazurile Raleigh si Cordoba apar doar ca exemple de lectura critica, nu ca dovada a eficientei unor solutii.

## E.3. Notita despre editia 1.0

Editia 1.0 (13 octombrie 2026) ramane in istoricul depozitului. Daca ai citat-o, referinta ramane valida; numerotarea sectiunilor din 1.1 este insa diferita acolo unde au fost completate golurile.
