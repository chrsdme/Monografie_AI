### 12.3. Starea si sesiunile

O **sesiune** poate pastra conversatia si rezultatele relevante. Un **run** este o executie concreta a unei sarcini. Un **task** este o unitate de lucru cu obiectiv si criterii de finalizare. Un run poate contine mai multe apeluri de model si de unelte. O sesiune poate avea mai multe run-uri, iar un workflow poate cuprinde sarcini si sesiuni diferite. Terminologia exacta variaza intre produse; aici o folosim consecvent, pentru claritate.

De exemplu, "revizuieste documentele de azi" poate produce un run care citeste 30 de documente si returneaza 30 de rezultate. Daca agentul se intrerupe dupa al cincisprezecelea, o reluare corecta cere sa stii ce documente au fost deja procesate si care operatii au efecte secundare. Starea asta trebuie pastrata in afara povestii pe care modelul o spune despre ce a facut.

