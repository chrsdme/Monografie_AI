# Anexa A. Dictionar de termeni: de la vocabularul de baza la arhitecturi agentice

Glosarul este organizat pentru consultare rapida. Termenii sunt grupati in mare parte alfabetic, dar prioritatea este claritatea si legatura cu explicatiile din capitole. Pentru intelegerea treptata, explicatiile complete se gasesc in capitolele anterioare. Definitii de referinta pentru vocabularul general pot fi consultate si in glosarul Stanford HAI [S18]. Cand termenii au sensuri diferite in produse diferite, am ales intelesul operational folosit in aceasta carte.

**Agent AI.** Componenta software care urmareste un obiectiv si poate decide, in limite definite, ce actiune sa execute si cum sa foloseasca rezultatul. Nu orice chatbot este automat un agent.

**API — Application Programming Interface.** Interfata prin care doua programe comunica. De exemplu, o aplicatie solicita unui serviciu meteo temperatura pentru o localitate si primeste date structurate.

**Apel de instrument (tool call).** Cererea structurata prin care modelul solicita o operatie externa. Instrumentul este executat de mediul de lucru, nu de simpla generare a textului.

**Automatizare determinista.** Proces in care pasii si regulile sunt stabilite explicit. Datele identice, in aceleasi conditii, ar trebui sa duca la acelasi rezultat.

**Baseline.** Masurarea situatiei initiale, folosita pentru comparatie dupa o modificare. Poate include timpul, costul, erorile si interventiile umane.

**Benchmark.** Test standardizat pentru compararea unor modele sau sisteme. Un benchmark bun precizeaza setul de sarcini, metoda de evaluare si limitarile.

**Bucla agentica.** Secventa repetata *observa → decide → actioneaza → verifica*. O bucla corecta are conditii de oprire si limita de resurse.

**Checkpoint.** Punct de salvare a starii, din care executia poate fi reluata dupa o intrerupere fara a repeta intregul proces.

**Clasa de agenti.** Categorie logica de responsabilitati, precum Research, Development sau QA. Este un termen de proiectare folosit aici, nu neaparat o clasa in limbajul Python.

**Conector.** Integrare care face un serviciu extern accesibil unei aplicatii. Un conector poate gestiona autentificare, operatii, conversia datelor si erori.

**Context.** Informatiile furnizate modelului intr-o cerere sau sesiune, inclusiv instructiuni, mesaje, documente si rezultate de instrumente.

**Context engineering.** Selectarea, ordonarea si actualizarea informatiei accesibile modelului pentru o anumita sarcina.

**Contract de iesire.** Definirea explicita a rezultatului asteptat: campuri, format, conditii de validare si tratamentul erorilor.

**Embeddings.** Reprezentari numerice ale unui continut, utile pentru cautarea fragmentelor apropiate semantic. Asemanarea numerica nu garanteaza adevarul informatiei.

**Escalare.** Trimiterea unei situatii catre alt agent, un serviciu specializat sau un operator uman, atunci cand lipsesc datele ori sunt depasite limitele autorizate.

**Evaluare (eval).** Procedura prin care comportamentul modelului sau al sistemului este comparat cu criterii stabilite anterior. Poate combina reguli, teste si judecata umana.

**Fallback.** Alternativa controlata folosita atunci cand fluxul principal nu poate continua. De exemplu, o cerere este trimisa unui operator in loc sa fie executata automat.

**Fine-tuning.** Adaptarea unui model prin antrenare suplimentara. Este diferit de adaugarea unui document in context sau intr-o baza RAG.

**Fereastra de context.** Limita de informatii exprimata in tokeni pe care modelul le poate procesa intr-o anumita interactiune. Limita declarata nu garanteaza utilizare corecta a tuturor informatiilor.

**Foundation model.** Model general antrenat pe date ample, utilizabil pentru mai multe sarcini, eventual adaptat ulterior.

**Guardrail.** Control care limiteaza, verifica sau blocheaza comportamentul. Un guardrail poate fi o regula in cod, o permisiune, o validare sau o aprobare umana.

**Harness.** Mediul care conecteaza modelul cu instrumentele, contextul, starea, regulile si bucla de executie. Poate folosi un model local ori un API cloud.

**Harness engineering.** Proiectarea acelui mediu astfel incat executia sa fie clara, repetabila, observabila si controlabila.

**Human-in-the-loop.** Etapa in care o persoana verifica, decide sau aproba anumite actiuni. Nu inseamna ca omul trebuie sa supravegheze fiecare token.

**IDP — Intelligent Document Processing.** Combinatie de extragere, clasificare si verificare a datelor din documente. Poate folosi OCR, reguli, modele de limbaj si operatori umani.

**Idempotenta.** Proprietatea unei operatii prin care repetarea aceleiasi cereri nu produce efecte suplimentare nedorite. Esentiala la plati, comenzi si operatii reluate dupa erori.

**Inferenta.** Utilizarea unui model deja antrenat pentru a genera un raspuns sau o predictie. Nu trebuie confundata cu antrenarea.

**Instanta de agent.** O activare concreta a configuratiei unui agent pentru o sarcina. Mai multe instante pot folosi acelasi model partajat.

**LLM — Large Language Model.** Model de limbaj antrenat la scara mare, capabil sa produca text si, in functie de arhitectura, alte tipuri de iesiri.

**Loop engineering.** Proiectarea buclelor de executie, observatie, evaluare si corectare, cu limite si conditii de oprire.

**Memorie persistenta.** Informatii pastrate intre sesiuni. Ele nu modifica automat parametrii modelului si trebuie gestionate din perspectiva provenientei si actualizarii.

**MCP — Model Context Protocol.** Protocol care standardizeaza integrarea dintre aplicatii AI si surse de date sau instrumente externe.

**Motor de inferenta.** Program care incarca si executa modelul, de exemplu intr-un serviciu local. Un motor de inferenta nu este automat un harness agentic.

**Observabilitate.** Capacitatea de a intelege starea si comportamentul sistemului prin jurnale, metrici si trasee de executie.

**Orchestrator.** Componenta care aloca sarcini, coordoneaza dependente, urmareste stari si decide transferurile intre etapele unui workflow. Poate fi cod cu reguli sau poate folosi si un model AI.

**OCR — Optical Character Recognition.** Transformarea textului aflat intr-o imagine sau scanare in caractere procesabile de calculator.

**Prompt.** Mesaj, instructiune sau colectie de intrari oferite unui model pentru o sarcina. Promptul nu este acelasi lucru cu permisiunea tehnica de a executa actiuni.

**Prompt engineering.** Proiectarea si testarea instructiunilor date modelului, cu scopul de a obtine rezultate cat mai bune pentru o sarcina.

**Provenienta (provenance).** Informatii despre originea unui rezultat: sursa, versiune, data, autor sau mecanism de obtinere. Este diferita de simpla citare a unui link.

**RAG — Retrieval-Augmented Generation.** Metoda prin care informatia este recuperata din surse externe si furnizata modelului in momentul generarii. Nu este sinonim cu memoria si nu garanteaza exactitatea.

**Rata de succes.** Proportia ejecutarilor care indeplinesc criteriile stabilite. Fara distributia cazurilor si gravitatea erorilor, poate fi inselatoare.

**RPA — Robotic Process Automation.** Automatizare care reproduce sau orchestreaza operatii repetitive din interfete si aplicatii. Poate functiona si fara un LLM.

**Run.** O executie delimitata a unei sarcini, identificata printr-un cod si descrisa prin intrari, actiuni si rezultate.

**Sandbox.** Mediu izolat sau restrictionat pentru executie. Restrictiile reale depind de sistemul de operare, containere, retea, permisiuni si configuratie.

**Scor de incredere (Trust Score).** Indicator propus pentru evaluarea unui agent intr-un domeniu concret. Nu este o proprietate universala a modelului si nu trebuie sa inlocuiasca analiza riscului.

**Sesiune.** Istoric si stare legate de una sau mai multe interactiuni. Poate traversa mai multe apeluri de model, dar nu inseamna neaparat memorie permanenta.

**Token.** Unitate in care modelul proceseaza textul, adesea un cuvant scurt, parte de cuvant sau simbol. Nu coincide obligatoriu cu un cuvant intreg.

**Trace.** Reconstructie a traseului unei executii prin evenimente corelate: cerere, apeluri de instrument, raspunsuri, erori si rezultate.

**Workflow.** Succesiune de etape si decizii care transforma intrari in rezultate. Poate contine reguli fixe, oameni, modele si agenti.
