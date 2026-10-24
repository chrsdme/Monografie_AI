### 21.2. Cazul B: dezvoltarea unei aplicatii web

**Situatia initiala.** O echipa vrea o aplicatie de programari. Clientul isi poate crea cont, alege un interval si primeste o confirmare. Administratorul vede programarile. Datele trebuie protejate, iar o rezervare nu trebuie dublata daca utilizatorul apasa de doua ori butonul.

**Nivelul 1: chat pentru a intelege cerinta.** Utilizatorul cere modelului sa explice ce componente sunt necesare. Primeste o lista: interfata, autentificare, baza de date, API, notificari si teste. E un plan de discutat, nu un sistem construit. Modelul poate omite probleme: fusuri orare, suprapuneri sau stergerea datelor. Un cititor responsabil transforma planul intr-o specificatie verificabila.

**Nivelul 2: cerinte si contracte.** Definesti ce inseamna o programare valida: serviciu disponibil, data viitoare, interval liber, utilizator autorizat. Stabilesti comportamentul la anulare si la erori. Un contract de iesire pentru rezervare poate contine `booking_id`, `status`, `slot_start` si `slot_end`. Ai deja criterii care se pot testa fara AI.

**Nivelul 3: un agent de dezvoltare.** Agentul primeste proiectul, cerintele si unelte pentru editare, build si teste. Scrie cod, ruleaza testele si corecteaza erorile. Daca o cerinta spune ca intervalele sunt de 30 de minute, poate adauga un test pentru o rezervare de 45 de minute si poate observa respingerea. In faza asta nu ai nevoie de un agent separat pentru fiecare comanda `git`, functie sau test.

**Nivelul 4: verificare independenta.** Un agent QA primeste cerintele initiale, modificarile, rezultatele testelor si acces de citire la cod. Construieste cazuri noi: dubla rezervare, doua cereri simultane, schimbarea fusului orar, utilizator neautorizat, anulare dupa termen. Nu porneste de la afirmatia dezvoltatorului "am acoperit toate cazurile". Dovezile relevante sunt testele executabile si rezultatul din baza de date.

**Nivelul 5: orchestrare.** Cand proiectul creste, orchestratorul descompune sarcina: Research analizeaza documentatia si cerintele, Development lucreaza la componente independente, QA verifica integrarea. Daca o regula de securitate nu e stabilita, sarcina care depinde de ea ramane `BLOCKED`. Daca testele nu trec, rezultatul revine la implementare cu erorile exacte.

**Nivelul 6: instante paralele, nu clase noi.** Avem trei clase: Research, Development si QA. Putem porni o instanta Research, sase instante Development si doua QA. Instantele Development lucreaza la autentificare, calendar, baza de date, notificari, frontend si integrare, fiecare cu propria sarcina. Infrastructura de inferenta poate fi partajata, deci noua instante nu inseamna noua modele incarcate. La final, rezultatul integrat trebuie verificat din nou, pentru ca modificari corecte separat pot deveni incompatibile impreuna.

