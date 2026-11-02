### 8.12. Cum aflam daca recuperarea a gasit documentul potrivit

Un sistem RAG poate da un raspuns gresit din doua motive: nu a gasit dovada sau nu a folosit corect dovada gasita. Pentru primul caz, o masura practica este **Recall@k**: proportia documentelor sau pasajelor relevante cunoscute care apar in primele `k` rezultate. Metoda presupune ca am definit anterior ce rezultate sunt relevante. `Recall@5` nu spune singur daca modelul a raspuns corect.

Exemplu ilustrativ: pregatim zece intrebari, fiecare cu un document de referinta. Pentru opt dintre ele, documentul cautat apare intre primele cinci rezultate. Avem o rata de gasire de **8 din 10 cazuri** pe aceasta suita simplificata. Nu este o concluzie statistica despre toate intrebarile posibile si nici o masura de fidelitate a raspunsului. Daca exista mai multe documente relevante pentru aceeasi intrebare, calculam metricile pe seturile de referinta corespunzatoare.

**Fidelitatea fata de surse** (*faithfulness*) pune alta intrebare: fiecare afirmatie importanta din raspuns este sustinuta de fragmentele disponibile? O referinta citata care nu contine informatia pretinsa nu este o dovada valida. Metricile de evaluare RAG pot ajuta la separarea regasirii de generare, dar evaluarile automate necesita verificari pe exemple cunoscute [S27].

Pentru o prima evaluare: salvam intrebarile, raspunsurile de referinta, documentele asteptate, versiunea colectiei si configuratia cautarii. Dupa fiecare schimbare de chunking, embedding, cautare lexicala sau reranking, repetam aceleasi teste si apoi verificam cateva cazuri noi. Astfel vedem daca schimbarea a imbunatatit recuperarea sau a mutat erorile in alta parte.

