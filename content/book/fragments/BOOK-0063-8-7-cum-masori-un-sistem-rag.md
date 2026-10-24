### 8.7. Cum masori un sistem RAG

Un RAG poate gresi in doua locuri diferite, iar daca masori doar raspunsul final nu vei sti in care. Prima greseala: sistemul aduce fragmentele nepotrivite sau incomplete. A doua: fragmentele sunt bune, dar modelul scrie ceva ce ele nu sustin. Sunt probleme cu cauze diferite si cu remedii diferite.

Lucrarea RAGAS (Es, James, Espinosa Anke si Schockaert, prezentata la EACL 2024) propune evaluarea fara referinte scrise de om pe trei dimensiuni: cat de bine gaseste sistemul pasajele relevante, cat de fidel le foloseste modelul si cat de buna e generarea in sine [S27]. Documentatia actuala a bibliotecii foloseste nume de metrici pe care le vei intalni in practica: *Context Precision*, *Context Recall*, *Faithfulness* si *Response Relevancy* [S27]. Numele difera putin fata de cele din lucrare, asa ca verifica intotdeauna definitia din versiunea de documentatie pe care o folosesti.

O regula practica: porneste cu un set mic de intrebari reale (30-50 sunt un inceput rezonabil), adauga pentru fiecare fragmentul care ar trebui sa fie gasit si raspunsul asteptat, apoi masoara separat recuperarea si raspunsul. Metricile calculate de un alt model sunt un ajutor, nu o hotarare finala. Un judecator automat poate gresi, deci verifica manual un esantion din cazurile semnalate.

