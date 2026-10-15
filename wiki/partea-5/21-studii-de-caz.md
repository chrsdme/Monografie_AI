# 21. Studii de caz: facturi, aplicatii web, suport si documente scanate

Cele doua studii sunt **simulari didactice**, nu sisteme implementate si masurate in cadrul acestei lucrari. Ne intereseaza sa intelegem de ce am alege o arhitectura, ce rezultate vrem sa verificam si ce se modifica atunci cand acordam mai multa autonomie. Vom parcurge aceleasi trepte: chat, documente, instrumente, workflow si, numai daca exista motive, orchestrare intre agenti.

## 21.1. Cazul A: procesarea facturilor unei firme mici

**Situatia initiala.** O firma primeste lunar intre 50 si 150 de facturi, prin email si intr-un portal. Unele sunt PDF-uri text, altele scanari. O persoana trebuie sa identifice furnizorul, numarul, suma, moneda si scadenta, sa compare cu registrul si sa semnaleze dublurile. Volumul nu este enorm, dar operatiile repetitive consuma timp.

**Nivelul 1 — Chat.** Utilizatorul intreaba un model ce campuri sunt importante intr-o factura si solicita o lista de verificare. Modelul explica, eventual redacteaza un sablon de tabel. Nu citeste automat niciun document. Beneficiul este cognitiv: omul intelege procesul mai repede.

**Nivelul 2 — Lucrul cu documente.** Utilizatorul incarca cinci facturi si cere extragerea campurilor. Modelul returneaza un tabel. Omul compara valorile cu documentele, mai ales sumele, numerele si datele. Daca un scan este ilizibil, o reactie buna este marcarea campului ca necunoscut, nu inventarea lui. Criteriul de acceptare este corespondenta dintre sursa si tabel.

**Nivelul 3 — Instrumente.** Aplicatia poate citi atasamente printr-un conector autorizat, poate apela un serviciu de extragere a textului si poate cauta furnizorul intr-un registru. Modelul contribuie la interpretarea formatelor variabile. In schimb, validarea campurilor obligatorii si calculele de total pot fi realizate prin cod. Un jurnal inregistreaza documentul, rezultatul extragerii si orice diferenta. Nu este necesara autonomie completa.

**Nivelul 4 — Workflow fix.** La sosirea unui email de la un expeditor permis, sistemul salveaza atasamentul, identifica tipul documentului, extrage campurile, compara cu registrul si pregateste o inregistrare. Cand gaseste o diferenta, o trimite intr-o coada de verificare. Procesul este determinist la exterior, cu AI numai in componenta care interpreteaza documentul. Daca arata bine in testele reprezentative, acesta poate fi deja sistemul final.

**Nivelul 5 — Agent pentru exceptii.** Sa presupunem ca furnizorii trimit formate foarte diferite si unele facturi fac referire la comenzi care trebuie cautate in alt sistem. Agentul poate cerceta neconcordanta cu instrumente de citire, poate propune o explicatie si poate pregati un dosar pentru operator. Nu i se acorda dreptul de plata. O plata necesita un flux separat cu autentificare si aprobare.

**Nivelul 6 — Orchestrare justificata.** Daca procesul se extinde la sute de documente zilnic si include verificari fiscale, contracte si comenzi de achizitie, putem avea un orchestrator care distribuie extragerea, reconcilierea si verificarea. Diferitele operatii ar avea contexte si drepturi separate. Dar nu am crea in mod automat un agent pentru fiecare camp din factura.

### Ce ar trebui sa contina un run verificabil

```text
invoice_run_id
source_document_id + hash
source_received_at
extraction_model_or_method + version
fields_extracted + confidence_or_unknown
arithmetic_checks
supplier_registry_check
potential_duplicate_check
human_review_status
final_record_id (only after acceptance)
```

Nu toate campurile trebuie logate ca text integral. Unele pot fi referinte catre documente protejate. Important este sa putem reconstitui ce sursa a produs fiecare valoare.

### Un exemplu de eroare si cum o tratam

Factura spune total 1.260,00 si contine doua linii de 500,00 si TVA 260,00. Modelul extrage 1.620,00 dintr-o imagine neclara. Validatorul numeric constata ca suma extrasa nu corespunde totalului calculat din linii. Documentul nu este aprobat. Agentul poate incerca o alta metoda de extragere, dar dupa un numar limitat de incercari il transmite unui operator. **Sistemul a functionat corect chiar daca modelul a gresit**, fiindca eroarea a fost identificata inainte sa produca un efect extern.

### De ce un al doilea agent nu este prima solutie

Daca verificam numai egalitatea dintre doua numere, un program clasic este mai simplu si mai sigur decat un al doilea LLM. Un evaluator AI devine util cand trebuie sa stabilim daca o clauza contractuala permite o exceptie sau daca o descriere ambigua corespunde unei comenzi. Chiar si atunci, justificarea trebuie legata de documentele efectiv consultate.

## 21.2. Cazul B: dezvoltarea unei aplicatii web

**Situatia initiala.** O echipa doreste o aplicatie de programari. Clientul poate crea cont, poate alege un interval si primeste o confirmare. Administratorul poate vedea programarile. Datele trebuie sa fie protejate, iar o rezervare nu trebuie dublata daca utilizatorul apasa butonul de doua ori.

**Nivelul 1 — Chat pentru intelegerea cerintei.** Utilizatorul cere modelului sa explice ce componente sunt necesare. Primeste o lista: interfata, autentificare, baza de date, API, notificari si teste. Este un plan de discutat, nu un sistem construit. Modelul poate omite probleme: fuse orare, suprapuneri sau stergerea datelor. Un cititor responsabil transforma planul intr-o specificatie verificabila.

**Nivelul 2 — Cerinte si contracte.** Definim ce inseamna o programare valida: serviciu disponibil, data viitoare, interval liber, utilizator autorizat. Stabilim comportamentul pentru anulare si erori. Un contract de iesire pentru rezervare poate contine `booking_id`, `status`, `slot_start` si `slot_end`. Deja avem criterii care pot fi testate fara AI.

**Nivelul 3 — Un agent de dezvoltare.** Agentul primeste proiectul, cerintele si instrumente pentru editare, build si teste. Scrie cod, ruleaza testele si corecteaza erorile. Daca o cerere spune ca intervalele sunt de 30 de minute, agentul poate introduce un test pentru rezervari de 45 de minute si poate observa respingerea. In aceasta faza nu este nevoie de un agent separat pentru fiecare comanda `git`, fiecare functie ori fiecare test.

**Nivelul 4 — Verificare independenta.** Un agent QA primeste cerintele initiale, modificarile, rezultatele testelor si acces de citire la implementarea evaluata. Poate crea si executa teste intr-un spatiu separat, cu drepturi limitate asupra fisierelor si datelor de test, fara acces de scriere in productie. Construieste cazuri noi: dubla rezervare, doua cereri simultane, schimbarea fusului orar, utilizator neautorizat, anulare dupa termen. Nu porneste de la afirmatia dezvoltatorului „am acoperit toate cazurile”. Testele executabile si rezultatul din baza de date constituie dovezile relevante.

**Nivelul 5 — Orchestrare.** Cand proiectul creste, orchestratorul descompune sarcina: Research poate analiza documentatia si cerintele, Development poate lucra la componente independente, QA verifica integrarea. Daca o regula de securitate nu este stabilita, sarcina care depinde de ea ramane `BLOCKED`. Daca testele nu trec, rezultatul revine la implementare cu erorile exacte.

**Nivelul 6 — Instante paralele, nu clase noi.** Sa presupunem ca avem trei clase: Research, Development si QA. Putem porni o instanta Research, sase instante Development si doua QA. Instantele Development lucreaza la autentificare, calendar, baza de date, notificari, frontend si integrare. Fiecare are propria sarcina. Infrastructura de inferenta poate fi partajata, deci noua instante nu implica noua modele incarcate. La final, rezultatul integrat trebuie verificat din nou, fiindca modificarile corecte separat pot deveni incompatibile impreuna.

### De ce avem nevoie de spatii de lucru izolate

Daca doua instante modifica simultan acelasi fisier, pot suprascrie schimbarile sau pot produce conflicte. O strategie este folosirea unor directoare de lucru separate, de exemplu clone sau Git worktrees, asociate unor ramuri distincte. Ramurile organizeaza modificarile, iar directoarele separate evita editarea concurenta a aceleiasi copii de lucru. Aceasta izolare protejeaza procesul de lucru asupra fisierelor; nu este, singura, o bariera de securitate. Orchestratorul urmareste ce spatiu de lucru apartine fiecarui task si impune o etapa de integrare. Un test trecut intr-o ramura nu echivaleaza cu o verificare pe versiunea finala integrata.

### Un exemplu de defect introdus fara intentie

Cerinta spune ca doua rezervari nu pot utiliza acelasi interval. Un dezvoltator verifica disponibilitatea, apoi salveaza rezervarea. In timpul dintre verificare si salvare, o alta cerere poate ocupa acelasi interval. Ambele teste individuale trec, dar doua cereri concurente pot produce dublarea rezervarii. QA trebuie sa testeze concurenta, iar sistemul are nevoie de o constrangere in baza de date sau de o tranzactie potrivita. Un prompt de tip „nu permite rezervari duble” nu rezolva problema la nivel de integritate a datelor.

### Ce ar trebui sa blocheze publicarea

Publicarea nu ar trebui sa depinda de „QA spune PASS” ca text liber. Un contract de acceptare poate cere: build reusit, teste obligatorii trecute, verificari de securitate fara defecte critice cunoscute, backup sau metoda de revenire, artefact versionat si aprobare pentru productie. Unele verificari se executa automat. Altele necesita decizie umana. Orchestratorul poate colecta dovezile, dar nu trebuie sa inlocuiasca politica de livrare.

## 21.3. Ce invatam din comparatie

In cazul facturilor, valoarea principala vine din extragerea datelor si gestionarea exceptiilor. In cazul aplicatiei web, valoarea apare din implementare si iteratie. Ambele beneficiaza de instrumente si verificari. Dar nu toate au nevoie de multi-agent, nici toate sarcinile nu trebuie rulate autonom. Arhitectura corecta porneste de la procesul real, nu de la posibilitatea de a crea un numar mare de agenti.


## 21.4. Studiul de caz C: triajul solicitarilor de suport

Pentru a vedea ca aceleasi principii sunt valabile si in afara dezvoltarii software, urmarim un al treilea exemplu, mai scurt. O firma primeste emailuri despre livrari, retururi, facturi si probleme tehnice. Nu incepem prin a construi cinci agenti. Incepem prin a observa cum sunt rezolvate cererile si unde se pierde timpul.

**Versiunea asistata.** Un angajat copiaza mesajul intr-un chatbot si cere un rezumat plus o propunere de raspuns. Verifica datele si trimite personal raspunsul. Castigul posibil este in redactare, nu in executia completa.

**Versiunea conectata.** Aplicatia primeste un mesaj, identifica limba si categoria probabila, apoi consulta printr-un API starea comenzii. Accesul la politica actualizata de retur se face dintr-o baza documentara, cu citarea sursei. Daca numarul de comanda lipseste, sistemul nu inventeaza unul. Cere completari.

**Versiunea cu automatizare fixa.** Daca este doar o intrebare despre status si identitatea clientului este verificata, programul construieste un raspuns din datele comenzii. Daca mesajul contine o contestatie, informatie contradictorie sau o solicitare financiara, trece la operator. Niciun LLM nu decide singur asupra unei rambursari.

**Versiunea agentica.** Pentru solicitarile complexe, un agent specializat poate planifica verificarea mai multor surse, dar executa numai actiunile permise. Un orchestrator urmareste dependentele si impune un numar maxim de incercari. Fiecare raspuns final include un rezumat al datelor consultate si tipul de verificare efectuata. Pentru cazurile sensibile, rezultatul ramane ciorna pana la aprobare.

**Cum evaluam.** Separat, masuram clasificarea corecta a categoriei, utilizarea datelor de comanda reale, rata de escaladare justificata, timpul pana la rezolvare si numarul de actiuni neautorizate. Nu confundam un raspuns politicos cu rezolvarea solicitarii. Acest exemplu combina tipurile de aplicatii prezentate in IBM AI Workflow si recomandarile pentru suport asistat de AI din surse practice romanesti, fara a prelua produse sau promisiuni comerciale [S17, S22].

## 21.5. Studiul de caz D: dintr-un PDF scanat intr-o inregistrare verificata

Procesarea inteligenta a documentelor, denumita adesea **IDP** (*Intelligent Document Processing*), combina operatii precum recunoasterea textului, clasificarea documentelor, extragerea campurilor si verificarea lor. Este mai mult decat OCR. OCR transforma imaginea literelor in text. IDP urmareste un rezultat operational: de exemplu, date de factura pregatite pentru sistemul contabil [S20].

O factura scanata poate fi procesata astfel: sistemul identifica paginile, recunoaste textul, gaseste furnizorul, moneda, totalul, data si numarul facturii, verifica aritmetic subtotalul si taxele, compara furnizorul cu registrul si marcheaza neconcordantele. Un model multimodal poate ajuta la documente cu layout neobisnuit, dar calculele aritmetice si identificarea duplicatelor trebuie efectuate prin reguli verificabile.

Din punct de vedere al increderii, exista trei intrebari diferite: **a citit corect textul?**, **a extras campurile corecte?**, **avem dreptul sa facem operatia urmatoare?** Un rezultat bun la primele doua nu este autorizatie de plata. Aprobarea, jurnalul si controalele de duplicat raman in sistemul operational. Acest caz ajuta cititorul sa inteleaga de ce un workflow poate integra AI fara ca toate etapele sa fie delegate unui agent autonom.
