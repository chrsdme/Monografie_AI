# 10. Harness-ul: mediul care transforma modelul intr-un executant

![Figura 1. Aplicatia si harness-ul coordoneaza contextul si instrumentele; modelul genereaza raspunsul.](../../assets/figuri/model_aplicatie.svg)

*Figura 1 — Model, aplicatie, instrumente si infrastructura de inferenta. Este o schema logica, valabila atat pentru cloud, cat si pentru modele locale.*

## 10.1. Ce problema rezolva

Sa presupunem ca un model poate scrie un program Python. Utilizatorul ii cere sa modifice o aplicatie. Modelul propune un fragment de cod. Cine deschide proiectul? Cine citeste fisierul corect, aplica modificarea, ruleaza testele, captureaza erorile, compara rezultatul cu cerinta si il readuce pe model in discutie? Fara aceste componente, modelul ramane in mare parte un consultant care genereaza text.

**Harness** este numele utilizat tot mai des pentru infrastructura operationala care inconjoara modelul si ii permite sa execute sarcini intr-un mod repetabil. Nu exista o singura definitie oficiala acceptata de toti furnizorii. In aceasta carte folosim termenul pentru ansamblul care gestioneaza sesiuni, instructiuni, contexte, instrumente, permisiuni, bucle de executie, jurnale si puncte de verificare. Unele produse includ si orchestrarea. Alte arhitecturi tin orchestratorul separat.

Imagineaza-ti un muncitor foarte priceput care este adus intr-un atelier gol. Are cunostinte, dar nu are scule, planuri, materiale sau un sistem de verificare a lucrarii. Harness-ul este atelierul pregatit: instrumentele potrivite, regulile de acces, registrul operatiilor si procesul prin care vedem daca produsul final corespunde planului. Analogia are limite, dar explica de ce modelul si mediul lui trebuie evaluate separat.

## 10.2. Componentele practice ale unui harness

Un harness poate avea un **manager de sesiune**, care pastreaza istoricul si starea curenta; un **constructor de context**, care selecteaza instructiuni, fisiere si rezultate; un **registru de instrumente**, care descrie functiile disponibile; un **executor**, care le ruleaza efectiv; un **manager de permisiuni**, care decide ce operatii sunt admise; un **controlor al buclei**, care gestioneaza continuarea, oprirea si limitele; si un sistem de **observabilitate**, care pastreaza evenimentele relevante.

Nu toate aceste componente trebuie sa fie procese independente. Un script Python de cateva sute de linii poate implementa o parte din ele. Un produs complex poate distribui aceleasi functii pe mai multe servicii. Diferenta sta in responsabilitati, nu in numarul de fisiere sau in numele framework-ului.

## 10.3. Harness versus motor de inferenta

Confuzia apare frecvent cand cineva instaleaza un motor pentru modele locale si observa ca acesta poate raspunde prin API. **Motorul de inferenta** incarca modelul si efectueaza calculul necesar generarii. **Harness-ul** gestioneaza sarcina, contextul, instrumentele si procesul de executie. Un motor poate include unele functii de servire, gestionare a cererilor sau apeluri structurate, dar asta nu inseamna automat ca executa un workflow complet de dezvoltare software.

Exemplu local: un serviciu de inferenta primeste intrebarea si returneaza text. Un harness separat ii trimite cerinte, ii ofera fisierele relevante, interpreteaza o solicitare de rulare a testelor si transmite rezultatul. Exemplu cloud: acelasi harness poate folosi un API administrat de un furnizor. Din perspectiva proiectului, responsabilitatile de context si executie raman asemanatoare. Furnizorul poate insa oferi propriul harness administrat, caz in care o parte din responsabilitati se muta in serviciul extern.

## 10.4. Ce este bucla agentului

Un harness poate controla urmatorul ciclu:

```text
Primeste obiectivul
  -> construieste contextul relevant
  -> cere modelului urmatorul pas
  -> valideaza actiunea propusa
  -> solicita aprobarea, daca este necesar
  -> executa instrumentul permis
  -> inregistreaza rezultatul real
  -> verifica daca obiectivul a fost atins
  -> continua, corecteaza, escaladeaza sau se opreste
```

Bucla nu trebuie sa continue nelimitat. Avem nevoie de numar maxim de pasi, buget de timp sau cost, conditii de oprire la eroare si reguli pentru actiunile care nu se pot repeta fara efecte secundare. Un mecanism care poate retrimite de zece ori o cerere de rambursare este un exemplu evident de design gresit.

## 10.5. Cum recunoastem un harness bun

Un harness bun face sistemul **inteligibil**. Cand o sarcina esueaza, putem afla ce a primit modelul, ce unelte avea, ce a solicitat, ce s-a executat si de ce a fost oprit. Daca rezultatele bune apar doar in demonstratii, dar nu pot fi reproduse, problema poate tine de mediu, nu numai de calitatea modelului.

Mai multe proiecte moderne de agenti pentru programare se concentreaza pe aceasta parte. Eseul OpenAI despre *harness engineering* din februarie 2026 descrie atentia acordata vizibilitatii sistemului, regulilor din repository, mecanismelor de verificare si cresterii controlate a autonomiei [S11]. Nu vom extrapola automat experienta acelui proiect la toate industriile; o folosim pentru a ilustra faptul ca ingineria mediului devine la fel de importanta ca alegerea modelului.

## 10.6. Cum functioneaza un harness cu mai multe modele

Un harness poate avea o interfata generica pentru servicii de inferenta. Pentru un raport simplu alege un model economic, pentru o sarcina de programare alege unul mai competent, iar pentru analiza unor imagini alege unul multimodal. Rutarea poate fi o regula fixa sau o decizie controlata de un alt component. Aceasta este o optiune de arhitectura, nu o garantie de economie: rutarea gresita si transferurile repetate pot creste costul.

Important este ca **schimbarea modelului nu trebuie sa schimbe automat permisiunile agentului**. Daca agentul are drept de citire, faptul ca utilizeaza un model mai performant nu ii confera drept de stergere. Invers, un model slab nu trebuie lasat sa execute actiuni periculoase doar pentru ca a formulat o cerere convingatoare.

## 10.7. Ce nu rezolva harness-ul singur

Un harness poate rula corect o comanda gresita. Poate arhiva impecabil un raspuns fals. Poate relua cu disciplina un plan prost. De aceea avem nevoie de criterii de acceptare, evaluatori si mecanisme externe de control. Harness-ul ofera cadrul de executie; corectitudinea sarcinii se demonstreaza prin verificari.
