### 17.11. Cand o evaluare ne pacaleste: scurgeri, calibrare si experimente

O evaluare devine mai putin utila daca folosim aceleasi exemple de fiecare data cand schimbam promptul. Incepem sa adaptam sistemul la intrebari cunoscute, nu la problema reala. De aceea separam un set de dezvoltare de un set **rezervat** (*held-out*), pe care nu il folosim pentru ajustari curente.

**Contaminarea evaluarii** apare cand informatii din testele care ar trebui sa fie independente ajung sa influenteze dezvoltarea sau raspunsul evaluat. Nu este nevoie sa existe intentie de trisare. Un exemplu simplu: publicam toate raspunsurile de referinta in acelasi fisier pe care agentul il citeste in timpul testului. Scorul obtinut nu mai demonstreaza capacitatea cautata.

Un **LLM evaluator** poate ajuta la notarea raspunsurilor libere, dar nu trebuie sa fie singura instanta de verificare. Il **calibram** pe cazuri evaluate de oameni: vedem unde este prea indulgent, prea sever sau in dezacord cu dovezile. Pentru criteriile exacte folosim teste deterministe; pentru ambiguitati folosim rubrici si esantioane revizuite [S33].

Un **studiu de ablatie** inseamna sa eliminam sau sa modificam controlat o componenta si sa observam efectul. De exemplu, testam acelasi RAG cu si fara reranking, pastrand restul configuratiei. Daca schimbam simultan modelul, colectia de documente si promptul, nu mai stim ce a produs diferenta.

**Exemplu de fals pozitiv:** un test cauta cuvantul `shipped` intr-un raspuns si il marcheaza ca reusita. Dar si propozitia `The order is not shipped` contine cuvantul respectiv. Pentru un status de comanda, comparam valoarea structurata cu sistemul de evidenta, nu simpla prezenta a unui sir de caractere.

**De retinut:** un scor bun trebuie sa reziste la intrebarea „Ce anume a fost testat, pe ce date, prin ce criteriu si ce explicatii alternative au ramas?”.

