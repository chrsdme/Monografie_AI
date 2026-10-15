# 9. Automatizare, workflow si agent: de ce diferenta conteaza

## 9.1. Automatizarea clasica nu a disparut

Multe procese sunt previzibile: cand soseste o factura, salveaza atasamentul; daca lipseste numarul facturii, trimite-o intr-o coada de verificare; daca exista acelasi numar si acelasi furnizor, marcheaz-o ca posibil duplicat. Regulile astea se scriu in cod obisnuit. Sa le inlocuiesti fara motiv cu decizii ale unui LLM inseamna cost si incertitudine in plus.

Un **workflow** este un lant de pasi, conditii si transferuri de date. Poate include programe clasice, modele AI sau pe amandoua si poate fi secvential, paralel sau conditionat. Un program care ruleaza un workflow nu este, prin definitie, un agent autonom.

## 9.2. Ce adauga un agent

Intr-un sistem agentic, modelul poate alege pasul urmator in functie de situatie. Daca lipseste documentul, cauta alta sursa permisa. Daca formatul s-a schimbat, propune alta metoda de extragere. Daca regulile cer aprobare, se opreste. Agentul combina un obiectiv, un model, un set de unelte, un context de lucru si un ciclu de actiune si feedback.

O definitie operationala utila: **agentul este o componenta executabila care urmareste un obiectiv, poate alege actiuni in limitele acordate si observa rezultatele ca sa decida daca continua, se corecteaza sau se opreste**. Literatura AI are definitii mai largi, inclusiv pentru agenti care nu folosesc LLM-uri. In aceasta lucrare, "agent AI" inseamna in principal sistemele moderne construite in jurul unor modele si unelte.

## 9.3. O distinctie folosita des in inginerie

Anthropic propune o diferenta practica. Despre workflow-uri spune ca sunt "systems where LLMs and tools are orchestrated through predefined code paths" [S10](../anexe/bibliografie.md#s10). In schimb, la un agent modelul conduce dinamic folosirea uneltelor si ordinea actiunilor. Granita nu e absoluta: un sistem real poate avea pasi fixi la exterior si agenti autonomi pe anumite portiuni. Tocmai aceste combinatii ne intereseaza.

## 9.4. Aceeasi sarcina, cinci abordari

**Sarcina:** dintr-un email cu o factura, pregateste o intrare in registrul contabil.

- **Chatbot:** explica utilizatorului ce campuri trebuie extrase; omul face operatiile.
- **Chatbot cu document:** citeste factura atasata si propune un tabel.
- **Workflow fix:** citeste atasamentul, extrage campurile intr-un format stabilit, aplica validari si salveaza o ciorna.
- **Agent cu unelte:** poate investiga o factura neobisnuita, cauta o comanda asociata si explica diferentele.
- **Sistem cu orchestrare:** poate delega extragerea, reconcilierea si verificarea, apoi cere aprobare inainte de operatiile sensibile.

In practica, un workflow fix poate fi preferabil pentru marea majoritate a facturilor standard, iar un agent poate lua doar exceptiile. Nu e o rusine tehnologica. E un design eficient, pentru ca foloseste variabilitatea modelului numai acolo unde aduce un beneficiu.

## 9.5. Cata autonomie are agentul?

Autonomia nu e un intrerupator cu doua pozitii. Un agent poate doar recomanda, poate pregati o ciorna, poate rula intr-un mediu izolat, poate modifica resurse reversibile sau poate actiona direct asupra sistemelor de productie. Fiecare treapta cere alte dovezi si alte controale. Gradul de autonomie trebuie sa depinda de risc si de evaluarile facute, nu de cat de convingator suna textul generat.

## 9.6. Intrebarea de proiectare

Daca problema se poate descrie in reguli clare, incepi cu reguli. Daca ai de judecat texte sau informatii neuniforme, adaugi modelul la pasul respectiv. Daca traseul nu poate fi anticipat rezonabil, evaluezi un agent. Daca exista mai multe responsabilitati independente si beneficii masurabile, discuti despre orchestrare. Complexitatea se castiga prin necesitate, nu prin entuziasm.

Anthropic spune acelasi lucru, intr-o fraza: "we recommend finding the simplest solution possible, and only increasing complexity when needed" [S10](../anexe/bibliografie.md#s10).

## 9.7. Cinci tipare de workflow de incercat inainte de un agent

Intre "un singur apel la model" si "un agent liber" exista un teren larg. Ghidul Anthropic descrie cinci tipare de workflow, utile ca vocabular comun [S10](../anexe/bibliografie.md#s10):

- **Inlantuire de prompturi** (*prompt chaining*): o sarcina se imparte in pasi, iar rezultatul unuia intra in urmatorul, cu verificari intre ei. Exemplu: extragi datele facturii, apoi le validezi, apoi redactezi nota.
- **Rutare** (*routing*): clasifici cererea si o trimiti pe traseul potrivit. Exemplu: mesajele despre facturi merg la un traseu, cele despre retururi la altul.
- **Paralelizare** (*parallelization*): mai multe verificari independente ruleaza in acelasi timp, iar rezultatele se compara sau se voteaza.
- **Orchestrator si lucratori** (*orchestrator-workers*): un model imparte sarcina in subsarcini care nu pot fi cunoscute dinainte si le da altor modele.
- **Evaluator si optimizator** (*evaluator-optimizer*): un model produce, altul critica, si se repeta pana cand criteriile sunt indeplinite.

Primele trei se pot construi si cu cod obisnuit, fara sa lasi modelul sa decida traseul. Ultimele doua se apropie de comportamentul agentic. Regula practica: ia cea mai simpla varianta care trece testele tale, apoi masoara daca urmatoarea chiar aduce ceva.

## 9.8. Cartografierea procesului inainte sa alegem tehnologia

Inainte de orice automatizare, descrie ce se intampla acum. E tentant sa sari direct la "ce model AI folosim?", dar o alegere tehnica nu repara un proces pe care nu l-a inteles nimeni. Ghidurile IBM despre workflow si materialele de automatizare operationala insista pe definirea pasilor, a obiectivelor si a integrarii cu sistemele existente [S17](../anexe/bibliografie.md#s17), [S19](../anexe/bibliografie.md#s19).

Pentru o cerere de suport intr-o firma mica, procesul real poate arata asa: soseste mesajul, un angajat identifica clientul, verifica o comanda, consulta politica de retur, pregateste raspunsul, apoi escaladeaza cazurile speciale. Fiecare etapa are o intrare, o iesire, un responsabil si un timp de executie. Noteaza si ce se intampla cand lipsesc informatii.

Abia dupa harta poti decide daca ai nevoie de AI. Verificarea unui numar de comanda intr-o baza de date e o interogare obisnuita. Clasificarea intentiei dintr-un mesaj liber poate profita de un model de limbaj. Termenul legal pentru rambursare trebuie sa ramana o regula verificabila. Un raspuns politicos poate fi generat, dar trimiterea lui poate cere control suplimentar.

O metoda accesibila este tabelul cu sase coloane: *pas, intrare, iesire, responsabil, eroare posibila, dovada de succes*. Nu trebuie sa fie un desen sofisticat. Conteaza sa scoata la lumina dependentele ascunse si locurile unde un om repara azi, din memorie, greselile procesului.

## 9.9. Masurarea situatiei initiale: fara ea nu stim daca am progresat

Inainte de prima schimbare, strange un set de referinta (*baseline*): cat dureaza o cerere, cat costa, cate corectii cere si in cate cazuri e nevoie de un operator. Cifrele trebuie luate din procesul tau, nu imprumutate dintr-un material de marketing. Un workflow poate reduce timpul de raspuns si, in acelasi timp, creste numarul de corectii. Sau poate fi mai ieftin la volume mici si mult mai scump la mii de apeluri API.

Un exemplu ilustrativ: o firma rezolva manual 100 de cereri pe saptamana, in medie 12 minute fiecare. Dupa introducerea unui sistem asistat de AI, timpul activ scade la 7 minute, dar 15 cereri cer o interventie suplimentara de cate 10 minute. Economia bruta ar fi de 500 de minute, iar cele 150 de minute in plus aduc castigul net la 350. Daca ai fi comparat doar timpul de generare a raspunsului AI, ai fi obtinut o imagine falsa.

Mai trebuie sa definesti ce inseamna un rezultat corect. "Clientul a primit un raspuns" nu inseamna "problema clientului s-a rezolvat". Distinctia conteaza in suport, marketing, vanzari, analiza documentelor, educatie si administratie. Ghidul practic Mersi AI pune accent pe alegerea procesului potrivit, pe masurarea performantei initiale si pe pastrarea unui traseu de recuperare [S23](../anexe/bibliografie.md#s23). Retinem metoda, nu estimarile de eficienta pentru un proiect anume.

## 9.10. Alegerea locului unde introducem AI-ul

Un sistem mixt poate fi mai bun decat unul complet agentic. Ia cererea de schimbare a adresei de livrare. Un model poate identifica intentia si poate extrage adresa din mesaj. Un validator scris in cod verifica formatul codului postal si existenta comenzii. O regula blocheaza schimbarile dupa expediere. Daca cererea e ambigua, sistemul cere clarificari. Daca toate conditiile sunt indeplinite, pregateste actualizarea sau executa operatia autorizata.

Asadar arhitectura nu se alege prin vot intre "automatizare veche" si "AI nou". Se alege pas cu pas: reguli pentru ce e exact, modele pentru ce e ambiguu, verificari pentru ce e important si aprobari pentru actiunile cu risc.
