# 7. Cum ajunge AI-ul sa foloseasca instrumente

## 7.1. De la raspunsul text la un apel concret

Un model care primeste intrebarea „Care este vremea acum la Brasov?” poate cunoaste clima orasului, dar nu stie automat temperatura reala din minutul respectiv. Pentru informatie actuala are nevoie de o sursa externa. Un **instrument** (*tool*) poate fi o functie de verificare meteo, un calculator, o cautare, un program care citeste un fisier sau o operatiune intr-un sistem de gestiune.

La **tool calling**, modelul poate propune un apel structurat, de exemplu `get_weather(city="Brasov", country="RO")`. O componenta a aplicatiei interpreteaza aceasta cerere, verifica permisiunile si argumentele, executa instrumentul si returneaza rezultatul. Modelul poate apoi formula raspunsul final. In schemele obisnuite, modelul nu executa el insusi codul doar pentru ca a generat un text care seamana cu o comanda. Executia apartine runtime-ului care dispune de acces la instrument [S06].

## 7.2. O trasare completa a operatiei meteo

Sa presupunem ca utilizatorul solicita: „Cat de cald este la Paris, Franta?”. Sistemul poate produce un jurnal simplificat:

```text
run_id: meteo-104
cerere: "Paris, Franta, acum"
tool_call: geocode(city="Paris", country="FR")
tool_result: latitude=48.86, longitude=2.35
tool_call: weather(latitude=48.86, longitude=2.35)
tool_result: temperature=18.2, observed_at=...
raspuns_final: "La Paris sunt 18,2 grade..."
validare: orasul corespunde; valoarea se potriveste; sursa este recenta
```

Valorile sunt ilustrative, nu reprezinta o observatie meteorologica reala. Ideea este ca fiecare veriga poate fi inspectata. Daca raspunsul este gresit, putem identifica daca s-a ales Paris din Texas, daca serviciul a returnat date vechi sau daca modelul a transcris gresit temperatura.

## 7.3. Un API nu este acelasi lucru cu un conector

API-ul defineste cum se solicita functii unui serviciu. Un **conector** este o integrare care adapteaza un serviciu pentru o anumita aplicatie: autentificare, lista de operatii, conversia datelor, gestiunea erorilor. De exemplu, un conector pentru email poate oferi operatiile „cauta mesaje”, „citeste mesaj” si „pregateste raspuns”. Nu este obligatoriu ca utilizatorul sa cunoasca endpointurile HTTP pe care le foloseste conectorul in fundal.

Un conector nu inseamna automat acces complet. Permisiunile pot fi numai de citire sau pot include scriere, stergere si trimitere. Vom trata aceste diferente ca parte a arhitecturii, nu ca un detaliu decorativ.

## 7.4. Ce este MCP si de ce a aparut

**Model Context Protocol** (MCP) este un protocol pentru conectarea aplicatiilor AI la instrumente si surse de context prin interfete standardizate. In loc sa implementeze o integrare complet diferita pentru fiecare combinatie de aplicatie si serviciu, dezvoltatorii pot folosi componente interoperabile. Documentatia protocolului descrie concepte precum *tools*, *resources* si *prompts*, precum si rolurile de host, client si server [S07].

Un server MCP pentru un sistem de fisiere ar putea expune operatia de citire a unui document. Un server pentru o baza de date ar putea oferi cautari autorizate si informatii despre schema. Dar MCP nu garanteaza siguranta, calitatea datelor sau dreptul de acces. Acestea depind de configuratia hostului, autentificare, autorizare si felul in care sunt implementate instrumentele.

Nici MCP nu este obligatoriu. O functie Python apelata direct poate fi cea mai simpla unealta posibila pentru un proiect mic. Protocolul devine util cand avem nevoie de interoperabilitate intre aplicatii si servicii.

## 7.5. Instrumente numai de citire si instrumente care modifica lumea

Cautarea documentelor este diferita de stergerea lor. Citirea unei facturi este diferita de emiterea unei plati. Intr-un sistem controlat, fiecare unealta trebuie sa aiba un nume inteligibil, o schema pentru argumente, permisiuni minime si rezultate usor de inspectat. Pentru actiunile cu efecte ireversibile sau financiare avem nevoie de aprobari si verificari suplimentare.

Exemplu: `draft_email(recipient, body)` poate salva o ciorna fara s-o trimita. `send_email(recipient, body)` produce un efect extern. Chiar daca ambele folosesc acelasi model pentru compunerea textului, riscul operational nu este acelasi.

## 7.6. Tool choice: cine decide daca unealta este folosita?

Intr-o configuratie de tip `auto`, modelul poate avea libertatea sa decida daca solicita instrumentul, in functie de API si instructiuni. Daca unealta este obligatorie pentru sarcina, aplicatia ar trebui sa impuna acest lucru sau sa verifice in cod ca a avut loc apelul necesar. Un prompt de tip „nu inventa vremea” ajuta, dar nu este suficient drept garantie daca runtime-ul accepta raspunsuri fara apelul sursei.

**De retinut:** calitatea unui agent cu instrumente depinde cel putin de trei lucruri: decizia de a folosi unealta, argumentele transmise si interpretarea rezultatului. Fiecare se evalueaza separat.
