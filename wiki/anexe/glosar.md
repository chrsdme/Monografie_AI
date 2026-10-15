# Anexa A. Dictionar de termeni: de la vocabularul de baza la arhitecturi agentice

Glosarul este in ordine alfabetica, nu in ordinea aparitiei. Explicatiile complete se gasesc in capitolele corespunzatoare. Definitii generale pot fi consultate si in glosarul Stanford HAI [S18](../anexe/bibliografie.md#s18). Cand un termen are sensuri diferite in produse diferite, am ales intelesul operational folosit in aceasta carte.

**A2A (Agent2Agent).** Protocol deschis pentru comunicarea dintre agenti de la furnizori diferiti, dezvoltat initial de Google si gazduit acum de Linux Foundation.

**Agent AI.** Componenta software care urmareste un obiectiv si poate decide, in limite definite, ce actiune sa execute si cum sa foloseasca rezultatul. Nu orice chatbot este automat un agent.

**Apel de unealta (tool call).** Cererea structurata prin care modelul solicita o operatie externa. Unealta este executata de mediul de lucru, nu de simpla generare a textului.

**API (Application Programming Interface).** Interfata prin care doua programe comunica. De exemplu, o aplicatie cere unui serviciu meteo temperatura pentru o localitate si primeste date structurate.

**Automatizare deterministica.** Proces in care pasii si regulile sunt stabilite explicit. Aceleasi date, in aceleasi conditii, ar trebui sa duca la acelasi rezultat.

**Backoff.** Pauza care creste intre doua reincercari ale unei operatii esuate, ca sa nu supraincarci un serviciu deja in dificultate.

**Baseline.** Masurarea situatiei initiale, folosita pentru comparatie dupa o modificare. Poate include timpul, costul, erorile si interventiile umane.

**Benchmark.** Test standardizat pentru compararea unor modele sau sisteme. Un benchmark bun precizeaza setul de sarcini, metoda de evaluare si limitarile.

**Bucla agentica.** Secventa repetata *observa, decide, actioneaza, verifica*. O bucla corecta are conditii de oprire si limita de resurse.

**Checkpoint.** Punct de salvare a starii, din care executia poate fi reluata dupa o intrerupere, fara a repeta tot procesul.

**Clasa de agenti.** Categorie logica de responsabilitati, precum Research, Development sau QA. Este un termen de proiectare folosit aici, nu neaparat o clasa din limbajul Python.

**Conector.** Integrare care face un serviciu extern accesibil unei aplicatii. Poate gestiona autentificarea, operatiile, conversia datelor si erorile.

**Context.** Informatiile furnizate modelului intr-o cerere sau sesiune, inclusiv instructiuni, mesaje, documente si rezultate ale uneltelor.

**Context engineering.** Selectarea, ordonarea si actualizarea informatiei accesibile modelului pentru o anumita sarcina.

**Contract de iesire.** Definirea explicita a rezultatului asteptat: campuri, format, conditii de validare si tratamentul erorilor.

**DAG (directed acyclic graph).** Graf orientat fara cicluri, folosit pentru a reprezenta dependentele dintre sarcini: B porneste doar dupa A, C si D pot rula in paralel.

**Embedding.** Reprezentare numerica a unui continut, utila pentru cautarea fragmentelor apropiate semantic. Asemanarea numerica nu garanteaza adevarul informatiei.

**Escalare.** Trimiterea unei situatii catre alt agent, un serviciu specializat sau un operator uman, atunci cand lipsesc datele ori sunt depasite limitele autorizate.

**Evaluare (eval).** Procedura prin care comportamentul modelului sau al sistemului este comparat cu criterii stabilite dinainte. Poate combina reguli, teste si judecata umana.

**Evaluare de regresie.** Evaluare repetata dupa o modificare, ca sa verifice ca sistemul nu a pierdut ce stia deja sa faca.

**Fallback.** Alternativa controlata folosita cand fluxul principal nu poate continua. De exemplu, o cerere merge la un operator in loc sa fie executata automat.

**Fereastra de context.** Limita de informatie, exprimata in tokeni, pe care modelul o poate procesa intr-o interactiune. Limita declarata nu garanteaza folosirea corecta a tuturor informatiilor.

**Few-shot prompting.** Metoda prin care promptul include cateva exemple de intrare si iesire. Exemplele nepotrivite pot induce o regula gresita.

**Fine-tuning.** Adaptarea unui model prin antrenare suplimentara. Este diferit de adaugarea unui document in context sau intr-o baza RAG.

**Foundation model.** Model general, antrenat pe date ample, utilizabil pentru mai multe sarcini si eventual adaptat ulterior.

**GraphRAG.** Varianta de RAG in care documentele sunt transformate intr-un graf de entitati si relatii, cu rezumate pe comunitati, utila pentru intrebari despre o colectie intreaga.

**Guardrail.** Control care limiteaza, verifica sau blocheaza comportamentul. Poate fi o regula in cod, o permisiune, o validare sau o aprobare umana.

**Halucinatie.** Continut generat care nu este sustinut de fapte sau de datele disponibile. Nu orice greseala a unui model este o halucinatie.

**Handoff.** Transferul responsabilitatii pentru o sarcina de la un agent la altul, cu un contract clar privind datele transmise si rezultatul asteptat.

**Harness.** Mediul care conecteaza modelul cu uneltele, contextul, starea, regulile si bucla de executie. Poate folosi un model local sau un API cloud.

**Harness engineering.** Proiectarea acelui mediu astfel incat executia sa fie clara, repetabila, observabila si controlabila.

**Human-in-the-loop.** Etapa in care o persoana verifica, decide sau aproba anumite actiuni. Nu inseamna ca omul supravegheaza fiecare token.

**Idempotenta.** Proprietatea unei operatii prin care repetarea aceleiasi cereri nu produce efecte suplimentare nedorite. Esentiala la plati, comenzi si operatii reluate dupa erori.

**IDP (Intelligent Document Processing).** Combinatie de extragere, clasificare si verificare a datelor din documente. Poate folosi OCR, reguli, modele de limbaj si operatori umani.

**Inferenta.** Folosirea unui model deja antrenat pentru a genera un raspuns sau o predictie. Nu trebuie confundata cu antrenarea.

**Instanta de agent.** O activare concreta a configuratiei unui agent pentru o sarcina. Mai multe instante pot folosi acelasi model partajat.

**LLM (Large Language Model).** Model de limbaj antrenat la scara mare, capabil sa produca text si, in functie de arhitectura, alte tipuri de iesiri.

**Loop engineering.** Proiectarea buclelor de executie, observatie, evaluare si corectare, cu limite si conditii de oprire.

**MCP (Model Context Protocol).** Protocol care standardizeaza integrarea dintre aplicatiile AI si sursele de date sau uneltele externe.

**Memorie persistenta.** Informatii pastrate intre sesiuni. Nu modifica automat parametrii modelului si trebuie gestionata din perspectiva provenientei si actualizarii.

**Model multimodal.** Model care proceseaza sau genereaza mai multe tipuri de informatie, de exemplu text si imagini.

**Motor de inferenta.** Program care incarca si executa modelul, de exemplu intr-un serviciu local. Nu este automat un harness agentic.

**Observabilitate.** Capacitatea de a intelege starea si comportamentul sistemului prin jurnale, metrici si trasee de executie.

**OCR (Optical Character Recognition).** Transformarea textului dintr-o imagine sau scanare in caractere procesabile de calculator.

**Orchestrator.** Componenta care aloca sarcini, coordoneaza dependente, urmareste stari si decide transferurile dintre etapele unui workflow. Poate fi cod cu reguli sau poate folosi si un model AI.

**Principiul privilegiului minim.** Regula potrivit careia fiecare componenta primeste doar accesul necesar sarcinii sale.

**Prompt.** Mesaj, instructiune sau colectie de intrari oferite unui model pentru o sarcina. Nu este acelasi lucru cu permisiunea tehnica de a executa actiuni.

**Prompt caching.** Mecanism prin care furnizorul reutilizeaza partea deja procesata a unui prompt lung si stabil, reducand costul si timpul de procesare.

**Prompt engineering.** Proiectarea si testarea instructiunilor date modelului, ca sa obtii rezultate cat mai bune pentru o sarcina.

**Prompt injection.** Atac sau situatie in care un continut cu autoritate scazuta (o pagina web, un document) incearca sa dea instructiuni agentului dincolo de scopul legitim.

**Provenienta (provenance).** Informatii despre originea unui rezultat: sursa, versiune, data, autor sau mecanism de obtinere. Este mai mult decat citarea unui link.

**RAG (Retrieval-Augmented Generation).** Metoda prin care informatia este recuperata din surse externe si furnizata modelului in momentul generarii. Nu este sinonim cu memoria si nu garanteaza exactitatea.

**Rata de succes.** Proportia executiilor care indeplinesc criteriile stabilite. Fara distributia cazurilor si gravitatea erorilor, poate induce in eroare.

**Retry.** Reluarea unei operatii dupa un esec. Se aplica in functie de efectele operatiei: nu orice esec se repara prin repetare.

**Rollback.** Revenirea la o stare anterioara. Pentru unele efecte (un email trimis) revenirea completa nu este posibila.

**RPA (Robotic Process Automation).** Automatizare care reproduce sau orchestreaza operatii repetitive din interfete si aplicatii. Poate functiona si fara LLM.

**Run.** O executie delimitata a unei sarcini, identificata printr-un cod si descrisa prin intrari, actiuni si rezultate.

**Rutare (routing).** Alegerea destinatiei unei cereri: agentul, modelul, unealta sau procesul potrivit.

**Sandbox.** Mediu izolat sau restrictionat pentru executie. Restrictiile reale depind de sistemul de operare, containere, retea, permisiuni si configuratie.

**Sesiune.** Istoric si stare legate de una sau mai multe interactiuni. Poate traversa mai multe apeluri de model, dar nu inseamna neaparat memorie permanenta.

**Shadow mode.** Mod de testare in care sistemul ruleaza procesul in paralel, fara a aplica modificari reale, iar propunerile sunt comparate cu deciziile procedurii existente.

**Sistem agentic.** Agentul impreuna cu infrastructura din jurul lui: harness, unelte, memorie, verificari, observabilitate si, uneori, orchestrare.

**Temperatura.** Parametru de decodare care influenteaza variatia raspunsurilor. O valoare mai mica reduce variatia, dar nu garanteaza exactitate.

**Timeout.** Situatia in care o operatie depaseste intervalul de asteptare stabilit.

**Token.** Unitatea in care modelul proceseaza textul, adesea un cuvant scurt, o parte de cuvant sau un simbol. Nu coincide obligatoriu cu un cuvant intreg.

**Trace.** Reconstructie a traseului unei executii prin evenimente corelate: cerere, apeluri de unelte, raspunsuri, erori si rezultate.

**Trust Score (scor de incredere).** Indicator propus pentru evaluarea unui agent intr-un domeniu concret. Nu este o proprietate universala a modelului si nu inlocuieste analiza riscului.

**Workflow.** Succesiune de etape si decizii care transforma intrari in rezultate. Poate contine reguli fixe, oameni, modele si agenti.
