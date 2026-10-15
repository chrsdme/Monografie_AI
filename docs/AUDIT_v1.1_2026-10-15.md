# Audit editorial si tehnic pentru editia 1.1

Data: 15 octombrie 2026

## Scop

Auditul a pornit de la editia 1.0 si de la rapoarte independente generate de mai multi agenti AI. Propunerile lor nu au fost preluate automat. Fiecare constatare relevanta a fost confruntata cu textul sursa, iar afirmatiile tehnice importante au fost reverificate in surse primare sau documentatie oficiala atunci cand a fost posibil.

## Verdict

Editia 1.0 avea o fundatie conceptuala solida si nu necesita rescriere. Au fost identificate erori editoriale certe, cateva formulari prea largi si mai multe locuri unde explicatia putea deveni mai precisa.

## Corectii editoriale aplicate

- `un incantatie` -> `o incantatie`;
- `Instruciuni` -> `Instructiuni`;
- `O embedding` -> `Un embedding`;
- `linkuri_surze` -> `linkuri_surse`;
- `fara sa sari` -> `fara sa sarim`;
- repararea numerotarii din capitolul 8: 8.9/8.10 -> 8.7/8.8;
- repararea numerotarii din capitolul 9: 9.8/9.9/9.10 -> 9.7/9.8/9.9;
- corectarea descrierii Partii V: exista doua studii principale si doua exemple complementare;
- reformularea promisiunii despre glosar: termenii sunt organizati pentru consultare rapida, nu perfect alfabetic;
- eliminarea referintelor catre figuri care nu sunt inca urmarite in repository, pentru a nu publica linkuri rupte in sursa Markdown.

## Corectii si nuantari tehnice

### Modele de limbaj

Explicatia despre predictia urmatorului token a fost restransa la modelele autoregresive folosite frecvent pentru generare. Nu toate modelele de limbaj au acelasi obiectiv de antrenare.

### Rationament

Formularea a fost schimbata din „modelele executa rationament” intr-o descriere operationala: pot produce comportamente care seamana cu rationamentul si pot rezolva probleme complexe, dar un traseu convingator nu reprezinta automat verificare externa.

### Git si izolarea muncii

Ramurile Git organizeaza versiuni ale modificarilor, dar nu reprezinta singure spatii de lucru independente. Pentru executii simultane sunt mai potrivite clone sau Git worktrees separate. Nici acestea nu reprezinta automat o bariera de securitate.

### Idempotenta

Un identificator unic nu este suficient daca este regenerat la fiecare retry. Aceeasi cheie trebuie reutilizata pentru aceeasi operatie, iar serviciul care produce efectul trebuie sa aplice deduplicarea.

### QA si acces read-only

„Read-only” este raportat la implementarea evaluata. QA poate crea teste si artefacte intr-un workspace separat, fara drept de modificare asupra productiei.

### Statistica evaluarilor

Un esantion mai mare poate reduce incertitudinea statistica in conditii adecvate, dar nu garanteaza varietate sau reprezentativitate. Acestea se masoara separat.

## Imbunatatiri de continut adaugate in 1.1

### Iesiri structurate

A fost adaugata distinctia dintre validarea formei si validarea continutului. Un JSON valid poate contine in continuare date false sau actiuni neautorizate.

### Competenta versus autoritate

Competenta demonstrata prin teste si autoritatea acordata de organizatie sunt tratate separat. Performanta buna poate declansa reevaluarea mandatului, nu extinderea automata a permisiunilor.

### Evaluarea RAG

Retrieval-ul si generarea sunt evaluate separat. Sunt introduse concepte RAGAS precum Context Precision, Context Recall, Response Relevancy si Faithfulness.

### Erori corelate intre agenti

A fost adaugata distinctia dintre consens si independenta dovezilor: zece agenti care folosesc aceeasi sursa gresita nu reprezinta zece confirmari independente.

### Prompt injection directa si indirecta

Capitolul de securitate distinge acum cererea malitioasa introdusa direct de utilizator de instructiunile injectate prin documente, pagini web sau rezultate ale instrumentelor.

## Bibliografie

Au fost revizuite intrarile OWASP, OpenTelemetry si Kuse:

- OWASP este legat explicit de editia 2025 pentru Prompt Injection si Excessive Agency;
- OpenTelemetry indica faptul ca atributele GenAI au fost mutate catre conventiile dedicate;
- articolul Kuse este datat 29 decembrie 2025, nu 2026;
- introducerea bibliografiei nu mai afirma ca toate sursele sunt necomerciale; sursele furnizorilor sunt tratate ca exemple si documentatie, nu ca dovezi universale de performanta.

## Propuneri ale agentilor pe care NU le-am preluat ca atare

### „Spatiile din tabelele Markdown sunt obligatorii”

Nu. Spatiile imbunatatesc lizibilitatea sursei, dar tabelele existente sunt valide pentru renderer-ul folosit. Nu am tratat aceasta observatie drept defect functional.

### „Context Precision inseamna ca informatia utila trebuie sa fie la inceputul contextului”

Aceasta descriere este inexacta pentru RAGAS. Context Precision masoara in esenta daca fragmentele relevante sunt clasate inaintea celor irelevante in contextul recuperat.

### „GraphRAG rezolva RAG-ul clasic”

Formulare prea larga. GraphRAG este o abordare utila mai ales pentru intrebari globale si sensemaking asupra colectiilor mari, dar nu este un inlocuitor universal pentru retrieval-ul clasic sau hibrid.

### „A2A garanteaza ca agentii nu isi trimit prompturi sau istoric”

Prea absolut. A2A standardizeaza interoperabilitatea agent-agent, nu garanteaza singur ce date interne sunt sau nu sunt transmise. Acest lucru depinde de implementare si politica de securitate.

### „Reflexion inseamna ca agentul isi rescrie automat regulile permanente”

Prea puternic. Reflexion descrie folosirea feedback-ului verbal si a memoriei episodice pentru imbunatatirea comportamentului; transformarea automata a fiecarei concluzii intr-o regula permanenta ar necesita controale suplimentare.

### „Swarm/multi-agent este directia naturala pentru orice sistem”

Nu. Principiul monografiei ramane acelasi: folosim cea mai simpla arhitectura care rezolva demonstrabil problema. Multi-agent este justificat numai cand separarea responsabilitatilor, permisiunilor sau fluxurilor aduce un beneficiu masurabil.

## Elemente ramase deschise

### Figurile editiei PDF

Pachetul sursa original contine patru SVG-uri folosite in PDF, dar Markdown-ul 1.0 facea referire la opt nume de fisiere. Pana cand toate figurile sunt restaurate si versionate explicit in repository, editia 1.1 Markdown evita legaturile catre fisiere inexistente.

### PDF 1.1

PDF-ul public existent ramane snapshot-ul editiei 1.0 pana la regenerarea lui din sursa 1.1. Regenerarea trebuie facuta dupa acceptarea acestei revizii si dupa decizia privind figurile.

## Concluzie

Editia 1.1 este o revizie de corectitudine si precizie, nu o schimbare de directie. Structura pedagogica de baza ramane: model -> context -> instrumente -> RAG/memorie -> workflow/agent -> harness -> orchestrare -> observabilitate -> evaluare -> securitate -> operare.
