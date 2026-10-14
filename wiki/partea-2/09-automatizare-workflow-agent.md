# 9. Automatizare, workflow si agent: de ce diferenta conteaza

## 9.1. Automatizarea traditionala nu a disparut

Multe procese de lucru sunt predictibile: la primirea unei facturi, salveaza atasamentul; daca lipseste numarul de factura, trimite-o intr-o coada de verificare; daca exista acelasi numar si acelasi furnizor, marcheaz-o ca posibil duplicat. Aceste reguli pot fi implementate in cod clasic. A le inlocui fara motiv cu decizii ale unui LLM ar adauga cost si incertitudine.

Un **workflow** este un lant de pasi, conditionari si transferuri de date. Poate include programe clasice, modele AI sau ambele. Un workflow poate fi secvential, paralel sau conditionat. Un program care executa un workflow nu este, prin definitie, un agent autonom.

## 9.2. Ce adauga un agent

Intr-un sistem agentic, modelul poate alege urmatorul pas in functie de situatie. Daca documentul lipseste, poate cauta alta sursa permisa. Daca formatul s-a schimbat, poate propune o alta metoda de extragere. Daca regulile cer aprobare, se opreste. Agentul combina un obiectiv, un model, un set de instrumente, un context de lucru si un ciclu de actiune si feedback.

O definitie operationala utila este aceasta: **agentul este o componenta executabila care urmareste un obiectiv, poate selecta actiuni in limitele acordate si observa rezultatele pentru a decide daca continua, se corecteaza sau se opreste**. Exista definitii mai largi in literatura AI, inclusiv pentru agenti care nu folosesc LLM-uri. Pentru aceasta lucrare, cand spunem *agent AI* ne referim in principal la sistemele moderne construite in jurul unor modele si instrumente.

## 9.3. O distinctie folosita frecvent in inginerie

Anthropic propune o diferenta practica: intr-un workflow, traseul principal este stabilit de cod; intr-un agent, modelul dirijeaza dinamic utilizarea instrumentelor si succesiunea actiunilor [S10]. Delimitarea nu este absoluta. Un sistem real poate contine pasi ficsi la exterior si agenti autonomi pe anumite portiuni. Tocmai aceste combinatii ne intereseaza.

## 9.4. Comparatie pe aceeasi sarcina

**Sarcina:** dintr-un email cu o factura, pregateste o intrare in registrul contabil.

- **Chatbot:** explica utilizatorului ce campuri trebuie extrase; omul face operatiile.
- **Chatbot cu document:** citeste factura atasata si propune un tabel.
- **Workflow fix:** citeste atasamentul, extrage campuri intr-un format stabilit, aplica validari si salveaza o ciorna.
- **Agent cu instrumente:** poate investiga o factura neobisnuita, cauta o comanda asociata si explica neconcordantele.
- **Sistem cu orchestrare:** poate delega extragerea, reconcilierea si verificarea, apoi solicita aprobarea inainte de operatii sensibile.

In practica, un workflow fix poate fi preferabil pentru 95% dintre facturile standard, iar un agent poate gestiona numai exceptiile. Nu este o rusine tehnologica. Este un design eficient, pentru ca foloseste variabilitatea modelului doar acolo unde aduce un beneficiu.

## 9.5. Cat de multa autonomie are agentul?

Autonomia nu este un intrerupator cu doua pozitii. Un agent poate doar recomanda, poate pregati o ciorna, poate executa in mediu izolat, poate modifica resurse reversibile sau poate actiona asupra sistemelor de productie. Fiecare treapta cere dovezi si controale diferite. Gradul de autonomie trebuie sa depinda de risc si de evaluarile realizate, nu de cat de convingator este textul generat.

## 9.6. Intrebarea de proiectare

Daca problema poate fi descrisa in reguli clare, incepem cu reguli. Daca necesita judecati asupra textelor sau informatiilor neuniforme, adaugam modelul la pasul relevant. Daca traseul nu poate fi anticipat rezonabil, evaluam un agent. Daca exista mai multe responsabilitati independente si beneficii masurabile, discutam despre orchestrare. Complexitatea se castiga prin necesitate, nu prin entuziasm.

---

## 9.8. Cartografierea procesului inainte sa alegem tehnologia

Inainte de orice automatizare, trebuie sa descriem ce se intampla acum. Este tentant sa sarim direct la intrebarea „ce model AI folosim?”, dar o alegere tehnica nu poate repara un proces pe care nimeni nu l-a inteles. Ghidurile IBM despre workflow si materialele de automatizare operationala insista asupra definirii pasilor, a obiectivelor si a integrarii cu sistemele existente [S17, S19].

Pentru o cerere de suport intr-o firma mica, procesul real poate arata astfel: soseste mesajul, un angajat identifica clientul, verifica o comanda, consulta politica de retur, pregateste raspunsul, apoi escaladeaza situatiile exceptionale. Fiecare etapa are o intrare, o iesire, o persoana responsabila si un timp de executie. Notam si ce se intampla cand lipsesc informatii.

Abia dupa aceasta cartografiere putem decide daca este necesara inteligenta artificiala. Verificarea existentei unui numar de comanda intr-o baza de date este o interogare obisnuita. Clasificarea intentiei dintr-un mesaj liber poate beneficia de un model de limbaj. Aplicarea termenului legal pentru rambursare trebuie sa ramana o regula verificabila. Redactarea unui raspuns politicos poate folosi generare de text, dar trimiterea sa poate necesita control suplimentar.

O metoda accesibila este tabelul cu sase coloane: *pas, intrare, iesire, responsabil, eroare posibila, dovada de succes*. Nu trebuie sa fie un desen sofisticat. Important este sa expuna dependentele ascunse si locurile unde un om repara in prezent, din memorie, greselile procesului.

## 9.9. Masurarea situatiei initiale: fara ea nu stim daca am progresat

Inainte de prima schimbare, colectam un set de referinta (*baseline*): cat dureaza o cerere, cat costa, cate corectii necesita si in cate cazuri avem nevoie de un operator. Aceste cifre trebuie obtinute din propriul proces, nu imprumutate dintr-un material de marketing. Un workflow poate reduce timpul de raspuns, dar poate creste numarul de corectii. Sau poate fi mai ieftin la volume mici si mult mai scump cand avem mii de apeluri API.

Un exemplu ilustrativ: o firma rezolva manual 100 de cereri pe saptamana, in medie in 12 minute fiecare. Dupa introducerea unui sistem asistat de AI, timpul de lucru activ scade la 7 minute, dar 15 cereri necesita interventie suplimentara de 10 minute. Economia bruta ar fi 500 de minute, insa cele 150 de minute suplimentare reduc castigul net la 350 de minute. Daca am compara numai timpul mediu de generare a raspunsului AI, am obtine o imagine falsa.

In plus, trebuie sa definim ce inseamna un rezultat corect. „Clientul a primit un raspuns” nu inseamna „problema clientului s-a rezolvat”. Aceasta distinctie este utila in suport, marketing, vanzari, analiza documentelor, educatie si administratie. Ghidul practic publicat de Mersi AI pune accent pe identificarea procesului potrivit, masurarea performantei initiale si pastrarea unui traseu de recuperare [S23]. Retinem metoda, nu estimarile de eficienta neverificate pentru un proiect concret.

## 9.10. Alegerea locului unde introducem AI-ul

Un sistem mixt poate fi mai bun decat unul integral agentic. Sa luam o solicitare de schimbare a adresei de livrare. Un model poate identifica intentia si extrage adresa din mesaj. Un validator de cod poate verifica formatul codului postal si existenta comenzii. O regula poate bloca schimbarile dupa expediere. Daca solicitarea este ambigua, sistemul cere informatii suplimentare. Daca toate conditiile sunt indeplinite, se poate pregati actualizarea sau executa operatia autorizata.

Prin urmare, arhitectura nu se alege prin vot intre „automatizare veche” si „AI nou”. Se alege etapa cu etapa: reguli pentru ceea ce este exact, modele pentru ceea ce este ambiguu, verificari pentru ceea ce este important si aprobari pentru actiunile cu risc.
