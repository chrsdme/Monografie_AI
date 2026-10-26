# Anexa A. Dictionar de termeni: de la vocabularul de baza la arhitecturi agentice

Glosarul este in ordine alfabetica, nu in ordinea aparitiei. Explicatiile complete se gasesc in capitolele corespunzatoare. Definitii generale pot fi consultate si in glosarul Stanford HAI [S18]. Cand un termen are sensuri diferite in produse diferite, am ales intelesul operational folosit in aceasta carte.

**Audit adversarial (antagonistic review).** Revizuire care cauta activ greseli, ambiguitati, dependente ascunse si cazuri limita, in loc sa urmareasca aprobarea automata a planului.

**Bootstrap (cartografiere initiala).** Etapa de inventariere a structurii si regulilor unui proiect existent, pentru ca un agent sa poata lucra pe baza unor informatii explicite.

**Cautare vectoriala.** Recuperarea continutului prin compararea reprezentarilor numerice (embeddinguri). Ajuta la gasirea textelor similare semantic, nu garanteaza corectitudinea lor.

**Codebase (baza de cod).** Ansamblul codului sursa, configuratiilor si componentelor unui proiect software.

**Comprehension Check.** Verificare in care un evaluator fara istoricul discutiilor explica o specificatie pentru a descoperi parti ambigue sau neintelese.

**Concept brief.** Document scurt care fixeaza scopul, cerintele, constrangerile, intrebarile deschise si directia propusa inaintea specificatiei detaliate.

**Design draft.** Prima versiune structurata a proiectarii tehnice, supusa completarii, revizuirii si aprobarii inainte de implementare.

**Drift Report.** Raport care compara documentatia aprobata cu implementarea actuala pentru a identifica abateri posibile. Diferentele necesita analiza, nu sunt automat defecte.

**Elephant-Goldfish Model (EGM).** Metoda deschisa de proiectare software asistata de AI in care un agent cu context redacteaza specificatii, iar evaluatori izolati conversational le critica inaintea implementarii.

**Elephant (rol EGM).** Agentul de proiectare cu context amplu despre proiect; clarifica intentia, alternativele si specificatia, fara sa implementeze cod in faza de design.

**Goldfish Protocol.** Secventa de verificare EGM care testeaza intelegerea specificatiei, cauta activ defecte si evalueaza pregatirea pentru implementare.

**Goldfish (rol EGM).** Evaluator AI lansat intr-o sesiune izolata de istoricul proiectarii. Primeste specificatia si dovezile autorizate, nu explicatiile nescrise din conversatia cu Elephant.

**Graf de cunostinte (knowledge graph).** Structura de date cu entitati si relatii explicite intre ele; relatiile pot avea surse, proprietati si intervale de valabilitate.

**Implementation Readiness Check.** Verificare daca specificatia contine suficiente detalii pentru implementare si testare, inclusiv interfete, structuri de date, comportamente la eroare si criterii de acceptare.

**Izolare de context.** Separarea controlata a istoricului si instructiunilor dintre sesiuni ori agenti, pentru a reduce influenta informatiilor care nu trebuie folosite intr-o evaluare.

**Memorie episodica.** Memorie care pastreaza evenimente si interactiuni datate, de exemplu ce a fost decis intr-o anumita sesiune.

**Memorie procedurala.** Memorie care descrie reguli si moduri de lucru: proceduri, pasi, politici si abilitati reutilizabile.

**Memorie semantica.** Memorie structurata despre concepte, fapte si relatii, distincta de istoricul brut al interactiunilor.

**Resursa externa complementara:** [Lexiconul agentilor AI - Ovidiu Boticiu](https://ovidiuboticiu.github.io/lexiconul-agentilor-ai/index.html), cu 361 de intrari EN-RO. Este un proiect independent (text CC BY-NC 4.0; cod fara licenta de reutilizare). Definitiile din aceasta carte sunt formulate independent, nu copiate din lexicon; aceasta recomandare nu certifica toate cele 361 de intrari.

**A2A (Agent2Agent).** Protocol deschis pentru comunicarea dintre agenti de la furnizori diferiti, dezvoltat initial de Google si gazduit acum de Linux Foundation.

**Agent AI.** Componenta software care urmareste un obiectiv si poate decide, in limite definite, ce actiune sa execute si cum sa foloseasca rezultatul. Nu orice chatbot este automat un agent.

**AI Employee (angajat digital).** Eticheta operationala/comerciala pentru un sistem care gestioneaza responsabilitati recurente, cu automatizari si eventual agenti. Nu este un standard tehnic sau un nou tip de model.

**Apel de unealta (tool call).** Cererea structurata prin care modelul solicita o operatie externa. Unealta este executata de mediul de lucru, nu de simpla generare a textului.

**API (Application Programming Interface).** Interfata prin care doua programe comunica. De exemplu, o aplicatie cere unui serviciu meteo temperatura pentru o localitate si primeste date structurate.

**Artefact.** Rezultat identificabil si versionabil al unui proces, precum un raport, un scenariu ori un fisier video. Aprobarile trebuie legate de o versiune concreta.

**Autentificare.** Verificarea identitatii utilizatorului sau serviciului care solicita o operatie.

**Autorizare.** Verificarea dreptului unei identitati de a consulta date ori executa o operatie. Un prompt nu poate inlocui verificarea tehnica.

**Automatizare deterministica.** Proces in care pasii si regulile sunt stabilite explicit. Aceleasi date, in aceleasi conditii, ar trebui sa duca la acelasi rezultat.

**Backoff.** Pauza care creste intre doua reincercari ale unei operatii esuate, ca sa nu supraincarci un serviciu deja in dificultate.

**Baseline.** Masurarea situatiei initiale, folosita pentru comparatie dupa o modificare. Poate include timpul, costul, erorile si interventiile umane.

**Benchmark.** Test standardizat pentru compararea unor modele sau sisteme. Un benchmark bun precizeaza setul de sarcini, metoda de evaluare si limitarile.

**Bucla agentica.** Secventa repetata *observa, decide, actioneaza, verifica*. O bucla corecta are conditii de oprire si limita de resurse.

**Checkpoint.** Punct de salvare a starii, din care executia poate fi reluata dupa o intrerupere, fara a repeta tot procesul.

**Cheie de idempotenta.** Identificator unic al unei cereri cu efecte externe, folosit pentru a recunoaste reincercarile si a evita duplicatele, de exemplu la rambursari.

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

**Fixture.** Date de test pregatite in avans, cu rezultate cunoscute, care permit verificari repetabile fara servicii reale.

**Foundation model.** Model general, antrenat pe date ample, utilizabil pentru mai multe sarcini si eventual adaptat ulterior.

**GraphRAG.** Varianta de RAG in care documentele sunt transformate intr-un graf de entitati si relatii, cu rezumate pe comunitati, utila pentru intrebari despre o colectie intreaga.

**Guardrail.** Control care limiteaza, verifica sau blocheaza comportamentul. Poate fi o regula in cod, o permisiune, o validare sau o aprobare umana.

**Halucinatie.** Continut generat care nu este sustinut de fapte sau de datele disponibile. Nu orice greseala a unui model este o halucinatie.

**Handoff.** Transferul responsabilitatii pentru o sarcina de la un agent la altul, cu un contract clar privind datele transmise si rezultatul asteptat.

**Harness.** Mediul care conecteaza modelul cu uneltele, contextul, starea, regulile si bucla de executie. Poate folosi un model local sau un API cloud.

**Harness engineering.** Proiectarea acelui mediu astfel incat executia sa fie clara, repetabila, observabila si controlabila.

**Hash.** Amprenta calculata din continutul unui fisier, utila pentru compararea versiunilor. Nu dovedeste singura autenticitatea.

**Health Metric (indicator de protectie).** Masura care verifica daca atingerea unui obiectiv degradeaza alte rezultate importante, de exemplu rata redeschiderii tichetelor.

**Human-in-the-loop.** Etapa in care o persoana verifica, decide sau aproba anumite actiuni. Nu inseamna ca omul supravegheaza fiecare token.

**Idempotenta.** Proprietatea unei operatii prin care repetarea aceleiasi cereri nu produce efecte suplimentare nedorite. Esentiala la plati, comenzi si operatii reluate dupa erori.

**IDP (Intelligent Document Processing).** Combinatie de extragere, clasificare si verificare a datelor din documente. Poate folosi OCR, reguli, modele de limbaj si operatori umani.

**Inferenta.** Folosirea unui model deja antrenat pentru a genera un raspuns sau o predictie. Nu trebuie confundata cu antrenarea.

**Instanta de agent.** O activare concreta a configuratiei unui agent pentru o sarcina. Mai multe instante pot folosi acelasi model partajat.

**Intent Drift (abatere fata de intentie).** Diferenta dintre obiectivul aprobat si directia efectiva a executiei sau a modificarilor ulterioare.

**Intent Engineering (ingineria intentiei).** Abordare emergenta ce leaga problema, obiectivele, dovezile, constrangerile si verificarea rezultatului unui sistem AI. Nu este un standard unic.

**Intent Specification (Intent Spec).** Document structurat si versionabil care descrie obiectivul, criteriile de succes, limitele, aprobarile si dovezile necesare. Nu impune singur reguli tehnice.

**Intentie operationala.** Scopul unui proces si limitele in care trebuie realizat; diferit de identificarea intentiei dintr-un mesaj individual.

**JSON (JavaScript Object Notation).** Format text structurat pentru date, folosit de API-uri si jurnale. Structura si sintaxa pot fi validate automat.

**LLM (Large Language Model).** Model de limbaj antrenat la scara mare, capabil sa produca text si, in functie de arhitectura, alte tipuri de iesiri.

**Loop engineering.** Proiectarea buclelor de executie, observatie, evaluare si corectare, cu limite si conditii de oprire.

**MCP (Model Context Protocol).** Protocol care standardizeaza integrarea dintre aplicatiile AI si sursele de date sau uneltele externe.

**Memorie persistenta.** Informatii pastrate intre sesiuni. Nu modifica automat parametrii modelului si trebuie gestionata din perspectiva provenientei si actualizarii.

**Metadate.** Informatii care descriu un obiect, de exemplu titlu, autor, data publicarii si identificator. Nu sunt echivalente cu continutul integral.

**Mock.** Componenta simulata care inlocuieste un serviciu sau model real intr-un test. Testarea cu mock nu verifica integrarea externa.

**Model multimodal.** Model care proceseaza sau genereaza mai multe tipuri de informatie, de exemplu text si imagini.

**Motor de inferenta.** Program care incarca si executa modelul, de exemplu intr-un serviciu local. Nu este automat un harness agentic.

**OAuth.** Protocol pentru autorizare delegata: o aplicatie poate primi acces limitat la resurse fara sa primeasca parola utilizatorului.

**Observabilitate.** Capacitatea de a intelege starea si comportamentul sistemului prin jurnale, metrici si trasee de executie.

**OCR (Optical Character Recognition).** Transformarea textului dintr-o imagine sau scanare in caractere procesabile de calculator.

**Orchestrator.** Componenta care aloca sarcini, coordoneaza dependente, urmareste stari si decide transferurile dintre etapele unui workflow. Poate fi cod cu reguli sau poate folosi si un model AI.

**Outcome (rezultat efectiv).** Starea reala verificata dupa executie, distincta de afirmatia agentului ca a finalizat sarcina.

**Permisiuni.** Drepturi tehnice acordate unei componente pentru citire, scriere sau actiuni. Se aplica in mediul de executie, nu doar in instructiuni.

**Principiul privilegiului minim.** Regula potrivit careia fiecare componenta primeste doar accesul necesar sarcinii sale.

**Prompt.** Mesaj, instructiune sau colectie de intrari oferite unui model pentru o sarcina. Nu este acelasi lucru cu permisiunea tehnica de a executa actiuni.

**Prompt caching.** Mecanism prin care furnizorul reutilizeaza partea deja procesata a unui prompt lung si stabil, reducand costul si timpul de procesare.

**Prompt engineering.** Proiectarea si testarea instructiunilor date modelului, ca sa obtii rezultate cat mai bune pentru o sarcina.

**Prompt injection.** Atac sau situatie in care un continut cu autoritate scazuta (o pagina web, un document) incearca sa dea instructiuni agentului dincolo de scopul legitim.

**Provenienta (provenance).** Informatii despre originea unui rezultat: sursa, versiune, data, autor sau mecanism de obtinere. Este mai mult decat citarea unui link.

**RAG (Retrieval-Augmented Generation).** Metoda prin care informatia este recuperata din surse externe si furnizata modelului in momentul generarii. Nu este sinonim cu memoria si nu garanteaza exactitatea.

**Rata de succes.** Proportia executiilor care indeplinesc criteriile stabilite. Fara distributia cazurilor si gravitatea erorilor, poate induce in eroare.

**Reconciliere.** Compararea rezultatului asteptat cu starea reala, mai ales dupa erori sau timeouts, inainte de a repeta operatii cu efect extern.

**Retry.** Reluarea unei operatii dupa un esec. Se aplica in functie de efectele operatiei: nu orice esec se repara prin repetare.

**Review independent.** Evaluare facuta separat de autorul planului, pe baza unei specificatii si a unor dovezi delimitate; izolarea conversatiei nu elimina automat erorile comune ale modelelor.

**Rollback.** Revenirea la o stare anterioara. Pentru unele efecte (un email trimis) revenirea completa nu este posibila.

**RPA (Robotic Process Automation).** Automatizare care reproduce sau orchestreaza operatii repetitive din interfete si aplicatii. Poate functiona si fara LLM.

**Run.** O executie delimitata a unei sarcini, identificata printr-un cod si descrisa prin intrari, actiuni si rezultate.

**Rutare (routing).** Alegerea destinatiei unei cereri: agentul, modelul, unealta sau procesul potrivit.

**Sandbox.** Mediu izolat sau restrictionat pentru executie. Restrictiile reale depind de sistemul de operare, containere, retea, permisiuni si configuratie.

**Scheduler (planificator).** Mecanism care porneste sarcini la ore ori intervale stabilite. Poate declansa un agent fara sa fie el insusi un agent.

**Sesiune.** Istoric si stare legate de una sau mai multe interactiuni. Poate traversa mai multe apeluri de model, dar nu inseamna neaparat memorie permanenta.

**Shadow mode.** Mod de testare in care sistemul ruleaza procesul in paralel, fara a aplica modificari reale, iar propunerile sunt comparate cu deciziile procedurii existente.

**Sistem agentic.** Agentul impreuna cu infrastructura din jurul lui: harness, unelte, memorie, verificari, observabilitate si, uneori, orchestrare.

**Spec-Driven Development (SDD).** Dezvoltare pornind de la specificatii explicite, versionate si verificabile, care ghideaza implementarea si testarea.

**Specificatie tehnica.** Document care descrie comportamentele, interfetele, constrangerile, scenariile si criteriile de acceptare ale unei functionalitati.

**Stateful (cu stare).** Sistem care pastreaza si reutilizeaza informatii despre interactiuni sau executii intre operatii, prin mecanisme explicite de gestionare a starii.

**Stateless (fara stare).** Sistem sau operatie care nu retine implicit datele unei interactiuni anterioare; contextul necesar trebuie furnizat explicit.

**Subagent.** Instanta de agent care primeste o sarcina delimitata de la un agent coordonator; poate avea propriul context, propriile unelte si propriile limite.

**Sursa de adevar (source of truth).** Inregistrarea sau sistemul autoritativ din care se verifica o informatie operationala, cum ar fi suma comenzii in baza magazinului.

**Temperatura.** Parametru de decodare care influenteaza variatia raspunsurilor. O valoare mai mica reduce variatia, dar nu garanteaza exactitate.

**Timeout.** Situatia in care o operatie depaseste intervalul de asteptare stabilit.

**Token.** Unitatea in care modelul proceseaza textul, adesea un cuvant scurt, o parte de cuvant sau un simbol. Nu coincide obligatoriu cu un cuvant intreg.

**Trace.** Reconstructie a traseului unei executii prin evenimente corelate: cerere, apeluri de unelte, raspunsuri, erori si rezultate.

**Trade-off (compromis intre obiective).** Alegerea unei prioritati cand cerintele intra in conflict, de exemplu intre corectitudine, cost, viteza si siguranta.

**Trust Score (scor de incredere).** Indicator propus pentru evaluarea unui agent intr-un domeniu concret. Nu este o proprietate universala a modelului si nu inlocuieste analiza riscului.

**Validitate temporala.** Perioada in care o informatie sau o relatie a fost adevarata; nu trebuie confundata cu data la care sistemul a aflat informatia.

**Workflow.** Succesiune de etape si decizii care transforma intrari in rezultate. Poate contine reguli fixe, oameni, modele si agenti.

**YAML.** Format text pentru configuratii structurate, bazat pe indentare. Exemplele YAML din carte nu sunt o schema universala de framework.

