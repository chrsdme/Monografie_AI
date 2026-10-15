# 22. Cum incepi propriul sistem, fara sa sari etapele

## 22.1. Alegerea sarcinii

Alege o problema care se repeta, are intrari disponibile si permite verificarea rezultatului. Exemple bune: organizarea documentelor, pregatirea unui raport, analiza unor erori, redactarea unor ciorne sau verificarea unei colectii de date. Pentru primul experiment evita operatiile ireversibile si situatiile in care nu ai cum sa recunosti un rezultat gresit.

Intreaba-te: cat de des apare problema? Cat dureaza azi? Cum arata un rezultat bun? Ce greseli sunt tolerabile? Ce greseli ar face pagube? Daca nu poti raspunde, proiectul e inca prea vag pentru automatizare.

## 22.2. Scrie contractul, nu doar promptul

Defineste intrarea, iesirea, sursele autorizate, uneltele permise, criteriile de acceptare, situatiile in care sistemul trebuie sa se opreasca si responsabilul final. Contractul poate sta pe o pagina si nu are nevoie de jargon. Din documentul asta deduci apoi prompturi, scheme si teste.

## 22.3. Construieste cea mai simpla varianta

Incepe cu un exemplu rezolvat manual intr-un chatbot. Daca metoda merge, testeaz-o pe date diferite. Adauga o unealta doar cand vezi ca e necesara: calculator pentru calcule, cautare pentru informatii actuale, documente pentru date private. Daca procesul se repeta, automatizeaza traseul fix. Introdu agenti doar acolo unde apar decizii care nu pot fi descrise rezonabil dinainte.

## 22.4. Stabileste verificarile inainte de autonomie

Nu astepta versiunea "completa" ca sa incepi evaluarea. Pastreaza exemple cu raspunsuri cunoscute, cazuri de eroare si criterii de respingere. Inregistreaza versiunea configuratiei, uneltele si rezultatele. Fara aceasta baza de comparatie nu vei sti daca o schimbare de model sau de prompt a imbunatatit ceva sau doar a produs un raspuns mai convingator.

## 22.5. Pregateste un traseu de escalare

Un sistem bun stie ce nu poate face. Cand lipsesc date, cand o unealta returneaza o eroare sau cand o operatie cere aprobare, executia trebuie sa se opreasca intr-o stare clara. Un operator trebuie sa poata vedea ce s-a intamplat si ce decizie e necesara. "Mergem mai departe cu orice pret" nu e un criteriu de performanta.

## 22.6. Extinde doar pe baza rezultatelor

Daca un workflow fix rezolva 98% dintre cazuri, iar exceptiile sunt rare, poate fi mai eficient sa lasi exceptiile unui operator sau unui singur agent specializat. Daca numarul de exceptii creste, adaugi un mecanism de analiza. Daca apar dependente intre sarcini, poti introduce orchestrare. Daca mai multe rulari au nevoie de aceeasi clasa de responsabilitati, pornesti mai multe instante, nu inventezi clase noi pentru fiecare sarcina.

## 22.7. Un plan de invatare aplicabila

In prima etapa, inveti sa formulezi o cerere verificabila si sa recunosti erorile. In a doua, lucrezi cu documente si API-uri. In a treia, construiesti un workflow cu log si validare. In a patra, implementezi un agent cu o unealta, conditii de oprire si teste. In a cincea, adaugi un al doilea rol doar daca are o responsabilitate independenta. In ultima, evaluezi intregul proces, inclusiv intreruperile si recuperarile.

Nu esti obligat sa termini fiecare etapa intr-o anumita saptamana. Important e sa nu confunzi o demonstratie reusita cu un sistem robust.

## 22.8. Ce ramane valabil chiar daca toate produsele se schimba

Modelele vor evolua, API-urile se vor modifica si vor aparea alte framework-uri. Intrebarile de proiectare raman insa surprinzator de stabile: ce problema rezolvam, ce date folosim, cine are dreptul sa faca ce, cum verificam rezultatul, cum observam erorile si cum revenim dupa un esec?

Daca retii aceste intrebari, poti evalua un produs nou fara sa o iei de la zero. Asta e scopul lucrarii: nu memorarea unor nume comerciale, ci intelegerea unui mod de lucru.

## 22.9. O metoda de alegere a proiectului pilot

O alegere buna se poate face fara framework si fara consultanti. Pentru fiecare proces candidat, acorda o nota simpla la cinci criterii: frecventa, timpul consumat azi, calitatea datelor, usurinta verificarii si impactul unei erori. Nu aduna punctele mecanic, ca si cum toate criteriile ar conta la fel. Intai excluzi operatiile periculoase sau imposibil de verificat, apoi alegi dintre cele ramase un pilot mic, repetabil si cu beneficiu masurabil. Abordarea e coerenta cu ghidurile de planificare a automatizarii de la IBM si Aliant [S17](../anexe/bibliografie.md#s17), [S19](../anexe/bibliografie.md#s19).

De exemplu, generarea unui sumar saptamanal din tichetele inchise este un pilot mai bun decat acordarea automata de credite. In primul caz, eroarea poate fi observata si corectata inainte de publicare. In al doilea, deciziile pot avea consecinte juridice si financiare si cer controale mult mai puternice.

## 22.10. Exercitiu de consolidare: procesul inaintea produsului

Alege o activitate pe care o faci cel putin o data pe saptamana. Scrie manual pasii de acum si noteaza pentru fiecare: informatia de intrare, persoana sau sistemul care decide, unealta care modifica datele si dovada ca pasul s-a incheiat corect. Marcheaza etapele care sunt doar copii de date, cele care cer interpretarea unui text si cele care produc efecte externe. Apoi proiecteaza trei variante: fara AI, asistata de AI si agentica. Compara-le dupa cost, timp, erori si capacitatea de a reveni dupa un esec.

Daca varianta fara agenti iese cea mai buna, exercitiul a reusit. Scopul nu e sa demonstrezi ca trebuie folosit un anumit tip de AI, ci sa intelegi ce arhitectura rezolva problema cu cel mai mic risc rezonabil.
