# 14. Orchestrarea: cine decide, cine executa si cine verifica

## 14.1. Ce este, de fapt, orchestratorul?

Un **orchestrator** este componenta care coordoneaza un proces cu mai multe operatii, agenti sau servicii. Stabileste ordinea, dependentele, distribuirea sarcinilor, starile de lucru, regulile de acceptare si felul in care te recuperezi dupa esecuri. Poate fi un program determinist, un serviciu de workflow, un LLM care propune un plan sau o combinatie. Nu trebuie sa fie "cel mai destept model din sistem".

Orchestratorul nu face toate sarcinile. Seamana mai degraba cu un dispecer: urmareste ce trebuie facut, de catre cine, pana cand si cu ce dovezi. Daca dispecerul incepe sa execute fiecare operatie marunta, pierde avantajul separarii responsabilitatilor.

## 14.2. O cerere care devine proiect

Utilizatorul spune: "Construieste o aplicatie web cu autentificare, panou de administrare si notificari". Cererea e prea larga pentru un singur pas. Orchestratorul poate incepe cu clarificarea cerintelor, apoi cere arhitectura, creeaza sarcini de implementare, asteapta integrarea si porneste verificarile. Sarcinile pot depinde unele de altele: schema bazei de date trebuie fixata inainte ca anumite componente sa poata fi conectate corect. Figura 7 arata relatia dintre orchestrator, dependente, instante si verificare.

![Figura 7. Orchestrator, dependente, instante si verificare.](../figuri/fig07_orchestrare.svg)

*Figura 7. Orchestratorul coordoneaza si tine starea executiei.*

## 14.3. Alocarea sarcinilor si rutarea

**Rutarea** inseamna alegerea destinatiei unei cereri. Poate fi deterministica: solicitarile despre rambursari merg la procesul financiar, iar cele despre erori de aplicatie la suportul tehnic. Sau poate implica un model care clasifica o cerere ambigua. In ambele cazuri decizia trebuie inregistrata, iar situatiile neclare au nevoie de un traseu de escalare.

Un orchestrator poate alege nu doar agentul, ci si modelul, uneltele sau nivelul de autonomie. Sarcinile simple pot merge pe un model economic, iar analizele complicate pe unul mai capabil. Optimizarea are sens doar daca masori erorile de rutare si costul total, inclusiv apelurile suplimentare pentru reparatii.

## 14.4. Dependente, grafuri si stari

O sarcina poate fi `PENDING`, `READY`, `RUNNING`, `BLOCKED`, `FAILED`, `WAITING_APPROVAL` sau `DONE`. Numele exacte variaza, dar sensul trebuie definit explicit. Trecerea de la `RUNNING` la `DONE` ar trebui sa se bazeze pe conditii verificabile, nu doar pe textul "gata" generat de un agent.

Dependentele se pot reprezenta ca un graf: sarcina B porneste doar dupa A; C si D merg in paralel; E asteapta rezultatele lui C si D. Cand nu are cicluri, graful se numeste **DAG** (*directed acyclic graph*). Nu orice sistem agentic are nevoie de un DAG explicit, dar ajuta la planificarea proceselor complexe.

## 14.5. Modele de coordonare

**Secvential:** Research da specificatia, Development implementeaza, QA verifica. Simplu de urmarit, dar uneori lent.

**Paralel:** mai multi agenti lucreaza pe sarcini independente, iar rezultatele se agrega. Bun cand munca se poate imparti fara conflicte.

**Orchestrator si lucratori:** un coordonator descompune dinamic o cerere si imparte sarcini unor executanti. Potrivit cand subdiviziunile depind de problema concreta.

**Evaluator si optimizator:** o executie produce rezultatul, alta il evalueaza si da feedback, iar procesul se repeta doar cat timp exista progres verificabil.

**Handoff:** responsabilitatea pentru o sarcina trece la un specialist, cu un contract clar si un context limitat. Nu e o fraza de genul "acum se ocupa colegul"; include identitatea sarcinii, datele transmise si rezultatul asteptat.

Tiparele acestea sunt prezentate si in ghidul Anthropic despre agenti eficienti, a carui recomandare de baza am citat-o deja: complexitate doar cand aduce beneficii masurabile [S10](../anexe/bibliografie.md#s10).

Cand agentii vin de la furnizori diferiti, apare nevoia unui limbaj comun intre ei. Protocolul **A2A** (*Agent2Agent*), dezvoltat initial de Google si gazduit acum de Linux Foundation, urmareste sa standardizeze comunicarea intre agenti, iar versiunea 1.0 este prima sa specificatie stabila [S37](../anexe/bibliografie.md#s37). Ca la orice standard, avantajul real apare cand cel putin doua sisteme diferite il implementeaza si il testezi in mediul tau.

## 14.6. Acelasi model, mai multi agenti

Un serviciu de inferenta poate raspunde cererilor pentru Research, Development si QA. Fiecare configuratie trimite modelului instructiuni si contexte diferite. **Nu pornim neaparat trei copii ale greutatilor modelului.** Serviciul poate programa cererile in serie, poate face batching sau le poate procesa concurent, in limitele infrastructurii.

Ia un singur model Qwen accesibil prin API. Instanta `Research-R1` intreaba ce cerinte trebuie indeplinite. `Development-D1` foloseste acelasi endpoint ca sa propuna cod, dar are acces doar la spatiul lui de lucru. `QA-Q1` consulta specificatia si rezultatele testelor, dar nu are voie sa scrie in cod. Diferentele de rol vin din sistemul care construieste contextul si impune drepturile, nu dintr-o presupusa schimbare a greutatilor modelului.

**Acelasi model** poate insemna raspunsuri corelate si greseli asemanatoare. Pentru verificarile critice preferam date si teste independente; un alt model poate fi o masura in plus, nu un inlocuitor al dovezilor.

## 14.7. Concurenta, paralelismul si izolarea

**Concurenta** inseamna gestionarea mai multor sarcini aflate in progres. **Paralelismul** inseamna executie simultana reala. Un singur serviciu poate gestiona zece sesiuni concurente si totusi sa genereze raspunsurile pe rand, daca resursele nu permit altfel. Numarul instantelor active nu e acelasi cu numarul de procese, de modele incarcate sau de GPU-uri.

Cand doi dezvoltatori AI modifica aceleasi fisiere, apar conflicte. De aceea folosim spatii de lucru separate, ramuri de versiune, reguli de integrare si teste pe rezultatul combinat. Daca sase instante scriu fiecare cod corect in izolare, rezultatul integrat poate totusi sa nu mearga. Evaluarea sistemului trebuie sa includa si pasul acesta.

## 14.8. De ce 20 de agenti pot fi mai slabi decat trei clase bine gandite

Fiecare transfer cere informatii, verificarea contractului si uneori o conversatie in plus. Daca creezi un agent pentru citirea fiecarui log si altul pentru fiecare comanda de test, inmultesti punctele de sincronizare. La o sarcina simpla, costul coordonarii poate depasi costul muncii. O bucla interna de implementare si testare e adesea mai ieftina decat sase transferuri intre roluri separate artificial.

Asta nu inseamna ca trei agenti ajung mereu. In proiectele mari pot exista zeci de specialisti justificati. Principiul este **minimizarea transferurilor inutile**, cu separare acolo unde exista responsabilitati, permisiuni sau criterii de verificare diferite.

## 14.9. Unde intra memoria in orchestrare

Orchestratorul are nevoie de o stare comuna: sarcinile, dependentele, rezultatele, aprobarile si evaluarile. Agentii primesc doar partea relevanta pentru executia lor. Rezultatele confirmate pot intra in memoria proiectului. Logurile detaliate pot sta intr-un depozit separat, disponibil pentru investigatii. Asa eviti ca fiecare instanta sa primeasca un istoric urias.

Memoria comuna are si riscuri. O concluzie gresita a unui agent nu trebuie ridicata automat la rang de adevar al organizatiei. Inainte de publicare, datele importante au nevoie de verificare, provenienta si un responsabil clar.

## 14.10. Ce se intampla cand un agent esueaza?

Orchestratorul trebuie sa deosebeasca un esec temporar de unul logic. Un timeout poate justifica reluarea limitata a unei cereri de citire. O schema gresita poate cere corectarea datelor. O operatie financiara cu stare necunoscuta cere intai verificarea efectului, nu retrimiterea pe orbeste. Daca QA respinge implementarea, sarcina se intoarce la Development cu defectele si dovezile, nu cu un mesaj generic de tipul "mai incearca".

Un mecanism de **failsafe** poate bloca accesul, poate pune o sarcina in asteptare sau poate opri intregul workflow. Pentru operatii reversibile poate exista rollback. Pentru cele ireversibile, uneori singura masura realista e prevenirea prin permisiuni, validare si aprobare.

## 14.11. Cum evitam ca orchestratorul sa devina el insusi problema

Un orchestrator care depinde numai de o conversatie foarte lunga poate pierde starea. Unul care ia decizii fara jurnal devine greu de auditat. Unul care isi declara singur succesul nu ofera control real. Solutia practica: tranzitiile importante intr-un registru, contracte de intrare si iesire, limite impuse si verificari separate pentru actiunile cu risc.

## 14.12. Studiu practic: orchestrator, worker temporar si verificator separat

Sa presupunem ca vrem sa corectam autentificarea unei aplicatii. In loc sa incarcam toata investigatia intr-o singura conversatie, putem separa deciziile de executie:

```text
Cererea utilizatorului
        |
MAIN: cerinte, dependente, criterii
        |
Task Packet -> Worker (context nou)
        |              |
        |         cod + teste + jurnal
        |              |
        +----------> Verifier independent
                       |
               dovezi PASS / FAIL
                       |
               MAIN: accepta sau redistribuie
```

**Contractul taskului.** Orchestratorul atribuie un ID, o cerinta, fisierele si instrumentele permise, limitele de timp si resurse, plus criterii verificabile de acceptare. Un worker nu ar trebui sa primeasca istoricul complet al proiectului, ci doar acest contract si referintele necesare. Daca doi workeri modifica aceleasi fisiere, izolam modificarile si verificam rezultatul integrat.

**Workerul nu se autocertifica.** Workerul poate avea un checklist si isi poate rula singur testele. La final declara `CLAIMED_DONE`, `PARTIAL`, `BLOCKED` sau `FAILED` si trimite modificarile, dovezile si limitarile. Un verificator separat stabileste pentru fiecare criteriu `PASS`, `FAIL` sau `NOT_VERIFIED`, preferabil pe baza unor teste reproductibile. Doar MAIN poate marca cerinta `ACCEPTED`, conform politicii proiectului; `DEFERRED` cere motiv si aprobare explicita. Un rezultat general `DONE` nu ascunde cerinte ramase deschise.

**Contextul este temporar, starea nu.** La un task nou sau la reluarea unuia intrerupt, un worker porneste cu un context limitat si citeste un checkpoint persistent. De exemplu, `evidence/T-001/progress.md` poate retine concluziile si pasii urmatori, `events.jsonl` evenimentele relevante, iar `test-summary.txt` verificarile. Jurnalul trebuie sa includa provenienta si versiunile fisierelor, fara sa stocheze secrete sau dumpuri inutile. Un rezumat nu inlocuieste verificarea starii reale a fisierelor.

**Bugetul este o politica, nu o magie a SDK-ului.** Pentru un task mediu putem experimenta cu aproximativ 25 de operatii substantiale. La circa 70% din buget workerul se concentreaza pe finalizare, iar la 80% salveaza progresul si returneaza `PARTIAL` daca nu poate incheia sigur. Valorile sunt orientative si se ajusteaza dupa date: numarul de apeluri de instrumente, numarul de ture, tokenii si costul sunt metrici diferite. Operatiile independente de citire pot fi grupate cand mediul permite, fara a compromite observabilitatea.

**Ce este suportat si ce construim noi.** Claude Code foloseste configuratii de subagenti in Markdown, Codex foloseste configuratii TOML, iar OpenAI Agents SDK si Pydantic AI permit delegare programatica. LangGraph ofera mecanisme explicite de stare si checkpoint. Totusi, regulile `ACCEPTED`, contractele noastre de task, politicile de buget si izolarea reala a permisiunilor nu apar automat din simpla definire a unui agent. Un handoff poate transmite si istoric; contextul proaspat trebuie impus prin configuratie ori rulare independenta.

**Exemplu descarcabil:** [configuratii generice de orchestrare pentru Claude, Codex si SDK-uri Python](https://github.com/chrsdme/Monografie_AI/blob/main/resurse/agent_orchestration_generic_examples.zip). Sunt sabloane educationale de adaptat si validat inaintea folosirii intr-un mediu real, nu o infrastructura de productie gata de instalat.

**Concluzia capitolului:** orchestrarea nu inseamna doar delegare. Inseamna control asupra dependentelor, identitatilor, resurselor, verificarilor si recuperarii.
