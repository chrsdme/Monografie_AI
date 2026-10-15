# 22. Cum incepi propriul sistem, fara sa sari etapele

## 22.1. Alegerea sarcinii

Alege o problema care se repeta, are intrari disponibile si permite verificarea rezultatului. Exemple bune: organizarea documentelor, pregatirea unui raport, analiza unor erori, redactarea unor ciorne sau verificarea unei colectii de date. Evita pentru primul experiment operatiile ireversibile sau situatiile in care nu poti recunoaste un rezultat gresit.

Intreaba-te: de cate ori apare problema? Cat dureaza astazi? Cum arata rezultatul bun? Ce greseli sunt tolerabile? Ce greseli ar produce pagube? Daca nu poti raspunde, proiectul este inca prea vag pentru automatizare.

## 22.2. Scrie contractul, nu doar promptul

Defineste intrarea, iesirea, sursele autorizate, instrumentele permise, criteriile de acceptare, situatiile in care sistemul trebuie sa se opreasca si responsabilul final. Contractul poate incapea pe o pagina. Nu trebuie sa contina jargon. Din acest document derivam ulterior prompturi, scheme si teste.

## 22.3. Construieste cea mai simpla varianta

Incepe cu un exemplu tratat manual intr-un chatbot. Daca metoda functioneaza, testeaz-o pe date diferite. Adauga o unealta numai cand observi ca este necesara: calculator pentru calcule, cautare pentru informatii actuale, documente pentru date private. Daca procesul se repeta, automatizeaza traseul fix. Introdu agenti numai acolo unde apar decizii care nu pot fi descrise rezonabil dinainte.

## 22.4. Stabileste mecanismele de verificare inainte de autonomie

Nu astepta versiunea „completa” pentru a incepe evaluarea. Pastreaza exemple cu raspunsuri cunoscute, cazuri de eroare si criterii de respingere. Inregistreaza versiunea configuratiei, instrumentele si rezultatele. Fara aceasta baza de comparatie, nu vei sti daca o schimbare de model sau de prompt a imbunatatit ceva sau doar a produs un raspuns mai convingator.

## 22.5. Pregateste un traseu de escalare

Un sistem bun stie ce nu poate face. Cand lipsesc date, cand o unealta returneaza o eroare sau cand o operatie necesita aprobare, executia trebuie sa se opreasca intr-o stare clara. Un operator trebuie sa poata vedea ce s-a intamplat si ce decizie este necesara. „A continua cu orice pret” nu este un criteriu de performanta.

## 22.6. Extinde doar pe baza rezultatelor

Daca un workflow fix rezolva 98% dintre cazuri si exceptiile sunt rare, poate fi mai eficient sa lasam exceptiile pentru un operator sau un singur agent specializat. Daca numarul de exceptii creste, adaugam un mecanism de analiza. Daca apar dependente intre sarcini, putem introduce orchestrare. Daca mai multe executii au nevoie de aceeasi clasa de responsabilitati, pornim mai multe instante, nu inventam clase noi pentru fiecare sarcina.

## 22.7. Un plan de invatare aplicabila

In prima etapa, invata sa formulezi o cerere verificabila si sa recunosti erorile. In a doua, lucreaza cu documente si API-uri. In a treia, construieste un workflow cu log si validare. In a patra, implementeaza un agent cu un instrument, conditii de oprire si teste. In a cincea, adauga un al doilea rol numai daca are responsabilitate independenta. In ultima, evalueaza intregul proces, inclusiv intreruperile si recuperarile.

Nu este obligatoriu sa termini fiecare etapa intr-o anumita saptamana. Important este sa nu confunzi o demonstratie reusita cu un sistem robust.

## 22.8. Ce ramane valabil chiar daca toate produsele se schimba

Modelele vor evolua, API-urile se vor modifica si vor aparea alte framework-uri. Dar intrebarile de proiectare raman surprinzator de stabile: ce problema rezolvam, ce date folosim, cine are dreptul sa faca ce, cum verificam rezultatul, cum observam erorile si cum revenim dupa un esec?

Daca cititorul retine aceste intrebari, poate evalua un nou produs fara sa porneasca de la zero. Aceasta este finalitatea lucrarii: nu memorarea unor nume comerciale, ci intelegerea unui mod de lucru.


## 22.9. O metoda de selectare a proiectului pilot

O alegere buna poate fi facuta fara framework si fara consultanti. Pentru fiecare proces candidat, acordam o evaluare simpla la cinci criterii: frecventa, timpul consumat astazi, calitatea datelor, usurinta verificarii si impactul unei erori. Nu adunam mecanic punctele ca si cum toate criteriile ar avea aceeasi importanta. Mai intai excludem operatiile periculoase sau imposibil de verificat, apoi alegem dintre cele ramase un pilot mic, repetabil si cu beneficiu masurabil. Aceasta abordare este coerenta cu ghidurile de planificare a automatizarii de la IBM, Aliant si Digital Romania [S17, S19].

De exemplu, generarea unui sumar saptamanal din tichete inchise este un pilot mai bun decat acordarea automata de credite. In primul caz, eroarea poate fi observata si corectata inainte de publicare. In al doilea, deciziile pot avea consecinte juridice si financiare si necesita controale mult mai puternice.

## 22.10. Exercitiu de consolidare: procesul inaintea produsului

Alege o activitate pe care o repeti cel putin o data pe saptamana. Scrie manual pasii actuali si noteaza pentru fiecare: informatia de intrare, persoana sau sistemul care decide, instrumentul care modifica datele si dovada ca etapa s-a incheiat corect. Marcheaza etapele care sunt doar copii de date, etapele care solicita interpretarea textului si etapele care produc efecte externe. Apoi proiecteaza trei variante: fara AI, asistat de AI si agentic. Compara-le pe cost, timp, erori si capacitatea de a reveni dupa un esec.

Daca varianta fara agenti este cea mai buna, exercitiul a reusit. Scopul nu este sa dovedim ca un anumit tip de AI trebuie folosit, ci sa intelegem ce arhitectura rezolva problema cu cel mai mic risc rezonabil.
