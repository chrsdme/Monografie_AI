# 10. Harness-ul: mediul care transforma modelul intr-un executant

Figura 2 arata imaginea de ansamblu a acestei parti: modelul nu sta singur, ci in spatele unei aplicatii si al unui harness care ii dau context si unelte.

![Figura 2. Aplicatia si harness-ul coordoneaza contextul si instrumentele; modelul genereaza raspunsul.](../figuri/fig02_model_aplicatie.svg)

*Figura 2. Model, aplicatie, instrumente si infrastructura de inferenta. Schema este logica si valabila atat pentru cloud, cat si pentru modele locale.*

## 10.1. Ce problema rezolva

Sa zicem ca un model poate scrie un program Python. Utilizatorul ii cere sa modifice o aplicatie, iar modelul propune un fragment de cod. Bun. Dar cine deschide proiectul? Cine citeste fisierul corect, aplica modificarea, ruleaza testele, prinde erorile, compara rezultatul cu cerinta si il aduce pe model inapoi in discutie? Fara toate astea, modelul ramane mai ales un consultant care genereaza text.

**Harness** este numele tot mai folosit pentru infrastructura operationala din jurul modelului, cea care il lasa sa execute sarcini intr-un mod repetabil. Nu exista o definitie oficiala acceptata de toti furnizorii. Aici folosim termenul pentru ansamblul care gestioneaza sesiuni, instructiuni, contexte, unelte, permisiuni, bucle de executie, jurnale si puncte de verificare. Unele produse includ si orchestrarea; alte arhitecturi o tin separat.

Gandeste-te la un meserias foarte priceput care ajunge intr-un atelier gol. Stie sa lucreze, dar nu are scule, planuri, materiale sau cineva care sa verifice lucrarea. Harness-ul este atelierul pregatit: uneltele potrivite, regulile de acces, registrul operatiilor si procesul prin care vedem daca produsul final se potriveste cu planul. Analogia are limite, dar arata de ce modelul si mediul lui trebuie evaluate separat.

## 10.2. Componentele practice ale unui harness

Un harness poate avea un **manager de sesiune**, care tine istoricul si starea curenta; un **constructor de context**, care alege instructiuni, fisiere si rezultate; un **registru de unelte**, care descrie functiile disponibile; un **executor**, care le ruleaza; un **manager de permisiuni**, care decide ce operatii sunt admise; un **controlor al buclei**, care gestioneaza continuarea, oprirea si limitele; si un sistem de **observabilitate**, care pastreaza evenimentele relevante.

Nu trebuie sa fie procese separate. Un script Python de cateva sute de linii poate implementa o parte din ele, iar un produs complex poate imparti aceleasi functii pe mai multe servicii. Diferenta sta in responsabilitati, nu in numarul de fisiere sau in numele framework-ului.

## 10.3. Harness si motor de inferenta

Confuzia apare des cand cineva instaleaza un motor pentru modele locale si vede ca acesta raspunde printr-un API. **Motorul de inferenta** incarca modelul si face calculul necesar generarii. **Harness-ul** gestioneaza sarcina, contextul, uneltele si procesul de executie. Un motor poate include functii de servire, de gestionare a cererilor sau de apeluri structurate, dar asta nu inseamna ca ruleaza un workflow complet de dezvoltare software. Figura 3 separa cele doua roluri.

![Figura 3. Motorul genereaza; harness-ul gestioneaza executia si controlul.](../figuri/fig03_harness.svg)

*Figura 3. Responsabilitatile motorului de inferenta si ale harness-ului.*

Exemplu local: un serviciu de inferenta primeste intrebarea si returneaza text. Un harness separat ii trimite cerintele, ii ofera fisierele relevante, interpreteaza cererea de rulare a testelor si inapoiaza rezultatul. Exemplu cloud: acelasi harness poate folosi un API administrat de un furnizor. Din perspectiva proiectului, responsabilitatile de context si executie raman asemanatoare. Furnizorul poate oferi insa propriul harness administrat, caz in care o parte din responsabilitati se muta in serviciul extern.

## 10.4. Ce este bucla agentului

Un harness poate controla un ciclu ca acesta:

```text
Primeste obiectivul
  -> construieste contextul relevant
  -> cere modelului urmatorul pas
  -> valideaza actiunea propusa
  -> cere aprobare, daca este necesar
  -> executa unealta permisa
  -> inregistreaza rezultatul real
  -> verifica daca obiectivul a fost atins
  -> continua, corecteaza, escaladeaza sau se opreste
```

Bucla nu are voie sa mearga la nesfarsit. Ai nevoie de un numar maxim de pasi, de un buget de timp sau de cost, de conditii de oprire la eroare si de reguli pentru actiunile care nu se pot repeta fara efecte secundare. Un mecanism care poate retrimite de zece ori o cerere de rambursare este un exemplu limpede de design prost.

Anthropic subliniaza si un alt detaliu: agentii trebuie sa primeasca "ground truth" din mediu la fiecare pas, de exemplu rezultatele uneltelor sau ale executiei de cod [S10](../anexe/bibliografie.md#s10). Cu alte cuvinte, bucla se sprijina pe ce s-a intamplat cu adevarat, nu pe ce spune modelul ca s-a intamplat.

## 10.5. Cum recunoastem un harness bun

Un harness bun face sistemul **inteligibil**. Cand o sarcina esueaza, poti afla ce a primit modelul, ce unelte avea, ce a cerut, ce s-a executat si de ce s-a oprit. Daca rezultatele bune apar doar in demonstratii si nu se pot reproduce, vina poate fi a mediului, nu doar a modelului.

Mai multe proiecte moderne de agenti pentru programare se concentreaza pe aceasta parte. Eseul OpenAI despre *harness engineering*, din februarie 2026, descrie atentia acordata vizibilitatii sistemului, regulilor din repository, mecanismelor de verificare si cresterii controlate a autonomiei [S11](../anexe/bibliografie.md#s11). Nu extindem automat experienta acelui proiect la toate industriile. O folosim ca sa ilustram ca ingineria mediului devine la fel de importanta ca alegerea modelului.

## 10.6. Cum lucreaza un harness cu mai multe modele

Un harness poate avea o interfata generica pentru servicii de inferenta. Pentru un raport simplu alege un model economic, pentru programare unul mai capabil, iar pentru imagini unul multimodal. Rutarea poate fi o regula fixa sau o decizie luata de alta componenta. E o optiune de arhitectura, nu o garantie de economie: o rutare gresita si transferurile repetate pot scumpi sistemul.

Important: **schimbarea modelului nu trebuie sa schimbe automat permisiunile agentului**. Daca agentul are drept de citire, faptul ca foloseste un model mai bun nu ii da drept de stergere. Si invers, un model slab nu trebuie lasat sa execute actiuni periculoase doar pentru ca a formulat o cerere convingatoare.

## 10.7. Ce nu rezolva harness-ul singur

Un harness poate rula corect o comanda gresita. Poate arhiva impecabil un raspuns fals. Poate relua cu disciplina un plan prost. De aceea ai nevoie de criterii de acceptare, evaluatori si mecanisme externe de control. Harness-ul da cadrul de executie, iar corectitudinea sarcinii se demonstreaza prin verificari.
