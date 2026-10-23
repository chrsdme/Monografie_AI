### 7.1. De la raspuns text la un apel concret

Intreaba un model "Cat e afara acum la Brasov?". Poate sti cum e clima orasului, dar nu stie temperatura reala din minutul acela. Pentru informatii actuale are nevoie de o sursa externa. O **unealta** (*tool*) poate fi o functie meteo, un calculator, o cautare, un program care citeste un fisier sau o operatie intr-un sistem de gestiune.

La **tool calling**, modelul propune un apel structurat, de exemplu `get_weather(city="Brasov", country="RO")`. O componenta a aplicatiei il interpreteaza, verifica permisiunile si argumentele, ruleaza unealta si trimite rezultatul inapoi. Abia apoi modelul formuleaza raspunsul final. In schemele obisnuite, modelul nu executa codul doar pentru ca a scris un text care seamana cu o comanda. Executia apartine runtime-ului care are acces la unealta [S06].

