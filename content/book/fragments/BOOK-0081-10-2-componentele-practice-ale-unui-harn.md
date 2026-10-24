### 10.2. Componentele practice ale unui harness

Un harness poate avea un **manager de sesiune**, care tine istoricul si starea curenta; un **constructor de context**, care alege instructiuni, fisiere si rezultate; un **registru de unelte**, care descrie functiile disponibile; un **executor**, care le ruleaza; un **manager de permisiuni**, care decide ce operatii sunt admise; un **controlor al buclei**, care gestioneaza continuarea, oprirea si limitele; si un sistem de **observabilitate**, care pastreaza evenimentele relevante.

Nu trebuie sa fie procese separate. Un script Python de cateva sute de linii poate implementa o parte din ele, iar un produs complex poate imparti aceleasi functii pe mai multe servicii. Diferenta sta in responsabilitati, nu in numarul de fisiere sau in numele framework-ului.

