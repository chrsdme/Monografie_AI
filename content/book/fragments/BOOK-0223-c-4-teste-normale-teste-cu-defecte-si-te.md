## C.4. Teste normale, teste cu defecte si teste de recuperare

Verifici mai intai traseul obisnuit: date valide, unelte disponibile, raspuns corect. Apoi simulezi defecte. Pentru exemplul meteo, API-ul returneaza `HTTP 503`, timpul de raspuns depaseste limita sau geocodarea gaseste trei localitati. Comportamentul asteptat nu e neaparat un raspuns complet. Poate fi o reluare controlata, o cerere de clarificare sau un mesaj ca datele nu sunt disponibile.

Urmeaza intreruperile: procesul se opreste intre pregatirea si aplicarea unei actiuni, un raspuns de la o unealta soseste prea tarziu, apare un mesaj duplicat. Verifici daca reluarea produce acelasi efect permis, nu doua efecte. De aceea idempotenta, checkpoint-urile si jurnalizarea sunt componente de fiabilitate, nu detalii decorative.

Pentru securitate, introduci date care incearca sa depaseasca limitele: o pagina web cu instructiuni de a ignora regula de aprobare sau un fisier care cere trimiterea unor date in afara sistemului. Agentul trebuie sa trateze textele acelea ca date neautorizate, nu ca ordine superioare. OWASP include prompt injection si autonomia excesiva printre riscurile importante ale aplicatiilor LLM; verifica numerotarea in editia pe care o folosesti [S09, S16].

