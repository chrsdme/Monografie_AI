### 8.8. Cand RAG-ul simplu nu ajunge

RAG-ul obisnuit se descurca bine la intrebari precum "Care e termenul de retur pentru produsul X?", pentru ca raspunsul sta intr-unul sau doua fragmente. Se impiedica la intrebari globale: "Care sunt temele principale din toate rapoartele noastre de anul trecut?". Niciun fragment singur nu contine raspunsul, iar cautarea dupa similaritate aduce doar cateva bucati.

Pentru astfel de cazuri, Edge si colegii au propus *GraphRAG*: sistemul extrage entitati si relatii din documente, le grupeaza in comunitati, scrie rezumate pentru fiecare grup si le foloseste la intrebari care privesc intreaga colectie [S26]. Costul e real, pentru ca indexarea cere multe apeluri la model. Alege o astfel de abordare doar dupa ce ai observat, pe cazuri reale, ca recuperarea simpla nu raspunde la intrebarile utilizatorilor tai.

Pana atunci, o varianta ieftina e combinarea cautarii dupa cuvinte-cheie cu cea semantica si adaugarea de metadate (data, versiune, tip de document) pentru filtrare. Nu e spectaculos, dar rezolva multe dintre problemele din sectiunea 8.3.

