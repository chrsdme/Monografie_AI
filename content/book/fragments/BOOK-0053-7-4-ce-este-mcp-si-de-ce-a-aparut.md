### 7.4. Ce este MCP si de ce a aparut

**Model Context Protocol** (MCP) este un protocol pentru conectarea aplicatiilor AI la unelte si surse de context prin interfete standardizate. In loc sa construiesti o integrare diferita pentru fiecare pereche aplicatie-serviciu, folosesti componente interoperabile. Documentatia descrie rolurile de host, client si server, precum si conceptele *tools*, *resources* si *prompts* [S07].

Documentatia insasi spune cu precizie ce acopera protocolul: "MCP focuses solely on the protocol for context exchange", adica nu dicteaza cum folosesc aplicatiile modelele sau cum isi gestioneaza contextul [S07]. Un server MCP pentru un sistem de fisiere ar putea expune citirea unui document. Un server pentru o baza de date ar putea oferi cautari autorizate si informatii despre schema. MCP nu garanteaza insa siguranta, calitatea datelor sau dreptul de acces. Acestea depind de configuratia hostului, de autentificare, de autorizare si de felul in care sunt scrise uneltele.

Pe 9 decembrie 2025, Anthropic a donat MCP catre Agentic AI Foundation, un fond gazduit de Linux Foundation, alaturi de alte doua proiecte (goose si AGENTS.md), ca sa ramana deschis si neutru fata de furnizori [S40]. Asta nu face protocolul perfect, dar schimba cine decide evolutia lui.

Specificatia evolueaza. Versiunea de protocol 2026-07-28 marcheaza, de exemplu, mecanismele *sampling* si *logging* ca depreciate [S07]. Pentru un sistem real, verifica versiunea pe care o implementezi.

MCP nu este nici obligatoriu. O functie Python apelata direct poate fi cea mai simpla unealta pentru un proiect mic. Protocolul isi arata valoarea cand ai nevoie de interoperabilitate intre aplicatii si servicii.

