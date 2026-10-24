## C.7. Cine verifica verificatorul?

Un model folosit ca evaluator poate descoperi probleme pe care alt model le-a ratat. Dar poate face si propriile erori si poate repeta presupunerile celui evaluat. De aceea incepi cu verificari mecanice acolo unde exista un raspuns exact: scheme, tipuri de date, teste unitare, comparatii cu surse si reguli de permisiune. Evaluarea semantica printr-un LLM e utila pentru criteriile greu de exprimat in cod, dar trebuie calibrata pe exemple evaluate de oameni.

Separarea de rol reduce contaminarea contextului. Agentul QA primeste cerinta si rezultatul, nu doar afirmatia "am terminat, totul e corect". Daca folosesti acelasi model pentru dezvoltare si pentru QA, recunoaste riscul de erori corelate. Pentru sarcinile critice poti folosi metode sau evaluatori diferiti, nu doar alte prompturi.

