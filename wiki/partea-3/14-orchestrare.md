# 14. Orchestrarea: cine decide, cine executa si cine verifica



## 14.1. Ce este, de fapt, orchestratorul?

Un **orchestrator** este componenta care coordoneaza executia unui proces cu mai multe operatii, agenti sau servicii. El stabileste ordinea, dependentele, distribuirea sarcinilor, starile de lucru, regulile de acceptare si modul de recuperare dupa esecuri. Poate fi un program determinist, un serviciu de workflow, un LLM care propune un plan sau o combinatie dintre acestea. Nu este obligatoriu sa fie „cel mai inteligent model din sistem”.

Orchestratorul nu trebuie sa faca toate sarcinile. Rolul lui seamana cu cel al unui dispecer: urmareste ce trebuie facut, de cine, pana cand si cu ce dovezi. Daca dispecerul incepe sa execute fiecare operatie marunta, pierde avantajul separarii responsabilitatilor.

## 14.2. O cerere care devine proiect

Utilizatorul spune: „Construieste o aplicatie web cu autentificare, panou de administrare si notificari”. Cererea este prea larga pentru un singur pas. Orchestratorul poate incepe cu clarificarea cerintelor, apoi solicita arhitectura, creeaza sarcini de implementare, asteapta integrarea si porneste verificari. Un proiect poate avea sarcini care depind unele de altele: schema bazei de date trebuie stabilita inainte ca anumite componente sa poata fi conectate corect.


## 14.3. Alocarea sarcinilor si rutarea

**Rutarea** inseamna alegerea destinatiei unei cereri. Poate fi determinista: solicitarile despre rambursari merg spre procesul financiar; cele despre erori de aplicatie merg spre suport tehnic. Sau poate implica un model care clasifica o cerere ambigua. In ambele cazuri, decizia ar trebui inregistrata, iar situatiile neclare trebuie sa aiba un traseu de escalare.

Un orchestrator poate alege nu doar agentul, ci si modelul, instrumentele sau nivelul de autonomie. De exemplu, sarcinile simple pot folosi un model economic, iar analizele complicate unul mai competent. Aceasta optimizare are sens numai daca masuram erorile de rutare si costul total, inclusiv apelurile suplimentare pentru reparatii.

## 14.4. Dependente, grafuri si stari

O sarcina poate fi `PENDING`, `READY`, `RUNNING`, `BLOCKED`, `FAILED`, `WAITING_APPROVAL` sau `DONE`. Numele exacte variaza, dar sensul trebuie definit explicit. Trecerea de la `RUNNING` la `DONE` ar trebui sa se bazeze pe conditii verificabile, nu numai pe textul „gata” generat de un agent.

Dependentele pot fi reprezentate ca un graf: sarcina B poate porni numai dupa A; C si D pot merge in paralel; E trebuie sa astepte rezultatele C si D. Aceasta metoda este adesea numita **DAG**, *directed acyclic graph*, atunci cand nu contine cicluri. Nu orice sistem agentic necesita un DAG explicit, dar acesta ajuta la planificarea unor procese complexe.

## 14.5. Modele de coordonare

**Secvential:** Research furnizeaza specificatia; Development implementeaza; QA verifica. Simplu de urmarit, dar uneori lent.

**Paralel:** mai multi agenti prelucreaza sarcini independente si rezultatele sunt agregate. Bun cand munca se poate imparti fara conflicte.

**Orchestrator-workers:** un coordonator descompune dinamic o cerere si distribuie sarcini unor executanti. Potrivit cand subdiviziunile depind de problema concreta.

**Evaluator-optimizer:** o executie produce rezultatul, alta evalueaza si ofera feedback, iar procesul se repeta numai cat timp exista progres verificabil.

**Handoff:** responsabilitatea unei sarcini este transferata unui specialist, cu un contract clar si un context limitat. Transferul nu este doar o fraza „acum se ocupa colegul”; include identitatea sarcinii, datele transmise si rezultatul asteptat.

Aceste tipare sunt prezentate si in ghidul Anthropic despre construirea agentilor eficienti. Recomandarea de baza a acelui material este sa adaugam complexitate doar cand aduce beneficii masurabile [S10].

## 14.6. Acelasi model, mai multi agenti

Un serviciu de inferenta poate raspunde cererilor pentru Research, Development si QA. Fiecare configuratie ii transmite modelului instructiuni si contexte diferite. **Nu pornim obligatoriu trei copii ale greutatilor modelului**. Serviciul poate programa cererile in serie, poate face batching sau poate procesa concurent in limitele infrastructurii.

Sa luam un singur model Qwen accesibil prin API. Instanta `Research-R1` intreaba ce cerinte trebuie indeplinite. `Development-D1` foloseste acelasi endpoint pentru a propune cod, dar primeste acces numai la spatiul sau de lucru. `QA-Q1` consulta specificatia si rezultatele testelor, dar nu are permisiune de scriere in cod. Diferentele de rol apar din sistemul care construieste contextul si impune drepturile, nu dintr-o presupusa schimbare a greutatilor modelului.

**Acelasi model** poate insemna raspunsuri corelate si greseli similare. Pentru verificari critice, preferam date si teste independente; folosirea altui model poate fi o masura suplimentara, nu un substitut pentru dovezi.

## 14.7. Concurenta, paralelismul si izolarea

**Concurenta** inseamna gestionarea mai multor sarcini aflate in progres. **Paralelismul** inseamna executie simultana reala. Un singur serviciu poate gestiona zece sesiuni concurente, dar poate genera efectiv raspunsurile secvential daca resursele nu permit altceva. Numarul instantelor active nu este acelasi cu numarul de procese, modele incarcate sau GPU-uri.

Cand doi dezvoltatori AI modifica aceleasi fisiere, apar conflicte. De aceea folosim spatii de lucru separate, ramuri de versiune, reguli de integrare si teste pe rezultatul combinat. Daca sase instante produc fiecare cod corect in izolare, rezultatul integrat poate totusi sa nu functioneze. Evaluarea sistemului trebuie sa includa si aceasta etapa.

## 14.8. De ce 20 de agenti pot fi mai slabi decat trei clase bine gandite

Fiecare transfer necesita informatii, verificarea contractului si uneori o conversatie suplimentara. Daca cream un agent pentru citirea fiecarui log si altul pentru fiecare comanda de test, inmultim punctele de sincronizare. La o sarcina simpla, costul coordonarii poate depasi costul muncii. O bucla interna de implementare si testare este adesea mai ieftina decat sase transferuri intre roluri artificial separate.

Asta nu inseamna ca „trei agenti” sunt intotdeauna suficienti. In proiecte mari pot exista zeci de specialisti justificati. Principiul este **minimizarea transferurilor inutile**, pastrand separarea acolo unde exista responsabilitati, permisiuni sau criterii de verificare diferite.

## 14.9. Unde intra memoria in orchestrare

Orchestratorul are nevoie de o stare comuna: sarcinile, dependentele, artefactele, aprobarile si evaluarile. Agentii primesc numai partea relevanta pentru executia lor. Rezultatele confirmate pot intra in memoria proiectului. Logurile detaliate pot ramane intr-un depozit separat, disponibil pentru investigatii. In acest mod evitam ca fiecare instanta sa primeasca o conversatie istorica uriasa.

Memoria comuna are si riscuri. O concluzie gresita a unui agent nu trebuie promovata automat la nivel de adevar organizational. Inainte de publicare, datele importante au nevoie de verificare, provenienta si responsabil clar.

## 14.10. Ce se intampla cand un agent esueaza?

Orchestratorul trebuie sa distinga intre un esec temporar si unul logic. Un timeout poate justifica reluarea limitata a unei cereri de citire. O schema gresita poate cere corectarea datelor. O operatie financiara cu stare necunoscuta necesita mai intai verificarea efectului, nu retrimiterea oarba. Daca QA respinge implementarea, sarcina revine la Development cu defectele si dovezile, nu cu un mesaj generic „mai incearca”.

Un mecanism de **failsafe** poate bloca accesul, poate pune o sarcina in asteptare sau poate opri intregul workflow. Pentru operatii reversibile, poate exista rollback. Pentru operatii ireversibile, uneori singura masura realista este prevenirea prin permisiuni, validare si aprobare.

## 14.11. Cum evitam ca orchestratorul sa devina el insusi problema

Un orchestrator care depinde exclusiv de o conversatie foarte lunga poate pierde starea. Unul care ia decizii fara jurnal devine greu de auditat. Unul care isi inventeaza singur succesul nu ofera control real. Solutia practica este sa pastram tranzitiile importante intr-un registru, sa definim contracte de intrare si iesire, sa impunem limite si sa verificam separat actiunile cu risc.

**Concluzia capitolului:** orchestrarea nu inseamna doar delegare. Inseamna control asupra dependentelor, identitatilor, resurselor, verificarilor si recuperarii.
