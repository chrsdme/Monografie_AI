# 7. Cum ajunge AI-ul sa foloseasca instrumente

## 7.1. De la raspuns text la un apel concret

Intreaba un model "Cat e afara acum la Brasov?". Poate sti cum e clima orasului, dar nu stie temperatura reala din minutul acela. Pentru informatii actuale are nevoie de o sursa externa. O **unealta** (*tool*) poate fi o functie meteo, un calculator, o cautare, un program care citeste un fisier sau o operatie intr-un sistem de gestiune.

La **tool calling**, modelul propune un apel structurat, de exemplu `get_weather(city="Brasov", country="RO")`. O componenta a aplicatiei il interpreteaza, verifica permisiunile si argumentele, ruleaza unealta si trimite rezultatul inapoi. Abia apoi modelul formuleaza raspunsul final. In schemele obisnuite, modelul nu executa codul doar pentru ca a scris un text care seamana cu o comanda. Executia apartine runtime-ului care are acces la unealta [S06](../anexe/bibliografie.md#s06).

## 7.2. Urmarirea completa a unei operatii meteo

Sa zicem ca utilizatorul intreaba: "Cat e de cald la Paris, Franta?". Sistemul poate produce un jurnal simplificat:

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

Valorile sunt ilustrative, nu o observatie meteo reala. Ideea e ca fiecare veriga se poate inspecta. Daca raspunsul iese gresit, poti vedea daca s-a ales Paris din Texas, daca serviciul a returnat date vechi sau daca modelul a copiat prost temperatura.

## 7.3. API si conector nu sunt acelasi lucru

API-ul defineste cum ceri functii de la un serviciu. Un **conector** este o integrare care adapteaza serviciul pentru o anumita aplicatie: autentificare, lista de operatii, conversia datelor, tratarea erorilor. Un conector pentru email poate oferi operatiile "cauta mesaje", "citeste mesaj" si "pregateste raspuns". Utilizatorul nu trebuie sa cunoasca endpointurile HTTP pe care conectorul le foloseste in fundal.

Un conector nu inseamna automat acces complet. Permisiunile pot fi doar de citire sau pot include scriere, stergere si trimitere. Aceste diferente fac parte din arhitectura, nu sunt un detaliu de decor.

## 7.4. Ce este MCP si de ce a aparut

**Model Context Protocol** (MCP) este un protocol pentru conectarea aplicatiilor AI la unelte si surse de context prin interfete standardizate. In loc sa construiesti o integrare diferita pentru fiecare pereche aplicatie-serviciu, folosesti componente interoperabile. Documentatia descrie rolurile de host, client si server, precum si conceptele *tools*, *resources* si *prompts* [S07](../anexe/bibliografie.md#s07).

Documentatia insasi spune cu precizie ce acopera protocolul: "MCP focuses solely on the protocol for context exchange", adica nu dicteaza cum folosesc aplicatiile modelele sau cum isi gestioneaza contextul [S07](../anexe/bibliografie.md#s07). Un server MCP pentru un sistem de fisiere ar putea expune citirea unui document. Un server pentru o baza de date ar putea oferi cautari autorizate si informatii despre schema. MCP nu garanteaza insa siguranta, calitatea datelor sau dreptul de acces. Acestea depind de configuratia hostului, de autentificare, de autorizare si de felul in care sunt scrise uneltele.

Pe 9 decembrie 2025, Anthropic a donat MCP catre Agentic AI Foundation, un fond gazduit de Linux Foundation, alaturi de alte doua proiecte (goose si AGENTS.md), ca sa ramana deschis si neutru fata de furnizori [S40](../anexe/bibliografie.md#s40). Asta nu face protocolul perfect, dar schimba cine decide evolutia lui.

Specificatia evolueaza. Versiunea de protocol 2026-07-28 marcheaza, de exemplu, mecanismele *sampling* si *logging* ca depreciate [S07](../anexe/bibliografie.md#s07). Pentru un sistem real, verifica versiunea pe care o implementezi.

MCP nu este nici obligatoriu. O functie Python apelata direct poate fi cea mai simpla unealta pentru un proiect mic. Protocolul isi arata valoarea cand ai nevoie de interoperabilitate intre aplicatii si servicii.

## 7.5. Unelte care doar citesc si unelte care schimba lumea

Cautarea documentelor nu e acelasi lucru cu stergerea lor. Citirea unei facturi e altceva decat emiterea unei plati. Intr-un sistem controlat, fiecare unealta are un nume clar, o schema pentru argumente, permisiuni minime si rezultate usor de inspectat. Pentru actiunile cu efecte ireversibile sau financiare ai nevoie de aprobari si verificari in plus.

Exemplu: `draft_email(recipient, body)` poate salva o ciorna fara sa o trimita. `send_email(recipient, body)` produce un efect in lumea reala. Chiar daca ambele apeleaza acelasi model pentru text, riscul operational nu e acelasi.

## 7.6. Tool choice: cine hotaraste daca se foloseste unealta?

In modul `auto`, modelul poate decide singur daca cere unealta, in functie de API si de instructiuni. Daca unealta e obligatorie pentru sarcina, aplicatia trebuie sa o impuna sau sa verifice in cod ca apelul necesar a avut loc. Un prompt ca "nu inventa vremea" ajuta, dar nu ajunge ca garantie daca runtime-ul accepta raspunsuri fara apelul la sursa.

**De retinut:** calitatea unui agent cu unelte depinde cel putin de trei lucruri: decizia de a folosi unealta, argumentele trimise si interpretarea rezultatului. Fiecare se evalueaza separat.
