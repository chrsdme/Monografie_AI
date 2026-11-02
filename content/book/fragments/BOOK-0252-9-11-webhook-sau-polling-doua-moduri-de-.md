### 9.11. Webhook sau polling: doua moduri de a incepe acelasi proces

Nu orice automatizare trebuie sa inceapa printr-un mesaj trimis de un om. Un magazin online poate primi o comanda, un formular poate fi completat, iar un sistem de suport poate inregistra un tichet. Aceste evenimente pot declansa un workflow.

La **polling**, aplicatia intreaba periodic un serviciu daca a aparut ceva nou. La un **webhook**, serviciul trimite o notificare catre un endpoint configurat, cand apare un anumit eveniment. Prima metoda este usor de inteles, dar poate face multe interogari fara rezultat. A doua reduce nevoia de verificari repetate, dar introduce cerinte de securitate si gestionare a livrarilor.

Un webhook primit nu este automat de incredere. Programul verifica provenienta sau semnatura, tipul evenimentului, identitatea si permisiunile, apoi decide daca evenimentul trebuie procesat. Acelasi eveniment poate fi transmis din nou, de exemplu cand confirmarea de primire a esuat. Documentatia Stripe ofera un exemplu concret de mecanism de evenimente, semnaturi si re-livrari; regulile exacte depind de furnizor [S54].

Sa luam clasificarea unui tichet. **Evenimentul** il porneste, **codul** valideaza intrarea, **modelul** poate propune categoria, iar **workflow-ul** hotaraste rutarea. Un mesaj destinat clientului poate ramane ciorna pana la aprobarea unui operator. A numi intregul proces „agent” nu il face mai bun. In multe cazuri, un workflow cu un singur pas LLM este suficient.

