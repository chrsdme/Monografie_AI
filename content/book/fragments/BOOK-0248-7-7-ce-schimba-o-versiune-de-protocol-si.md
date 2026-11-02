### 7.7. Ce schimba o versiune de protocol si ce nu schimba

Un protocol este un contract intre componente, nu o garantie ca rezultatul final va fi bun. Specificatia MCP din 28 iulie 2026 descrie un nucleu de cereri fara stare implicita (*stateless*), negocierea capabilitatilor si extensii optionale, pe langa uneltele, resursele si prompturile deja prezentate [S57]. In acest context, „fara stare” se refera la schimbul de cereri al protocolului, nu inseamna ca aplicatia ta nu poate avea sesiuni sau memorie persistenta.

Sa luam un server MCP care expune o functie de citire a unei facturi. Protocolul poate ajuta clientul sa descopere unealta si sa transmita argumentele intr-o forma comuna. Dar **nu decide singur** daca utilizatorul are dreptul la factura, daca documentul este versiunea corecta sau daca informatiile obtinute pot fi trimise altui serviciu. Aceste verificari raman la implementare, autentificare, autorizare si politica aplicatiei. Nici descrierea unei unelte externe nu trebuie tratata ca instructiune de incredere implicita [S57].

Aceeasi disciplina se aplica raspunsurilor din API-ul modelului. Intr-un flux cu unelte, trebuie deosebit un raspuns final de o oprire cauzata de limita de tokeni, de o suspendare ori de un refuz. Un motiv de oprire care nu cere unealta **nu echivaleaza automat cu succesul** [S59]. In jurnalul unui agent, starea `completed` se acorda dupa verificarea rezultatului, nu dupa simpla iesire din bucla.

**De retinut:** interoperabilitatea reduce munca de integrare. Permisiunile, validarea, limitele si dovada finalizarii raman responsabilitatea sistemului construit peste protocol.

