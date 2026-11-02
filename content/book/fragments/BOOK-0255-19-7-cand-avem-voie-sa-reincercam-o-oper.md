### 19.7. Cand avem voie sa reincercam o operatie

Un retry pare simplu: "daca nu merge, incearca din nou". In realitate, trebuie sa intelegem **de ce** a esuat si **daca operatia a produs deja un efect**.

Daca serviciul spune ca datele sunt invalide, repetarea aceleiasi cereri nu le corecteaza. Daca autentificarea a expirat, este nevoie de o decizie despre credentale, nu de o bucla rapida. Pentru erori temporare de retea, limitari de rata ori indisponibilitate a serviciului poate fi potrivita o noua incercare, cu timeout si o pauza crescatoare, eventual respectand timpul de asteptare cerut de furnizor.

Problema grea apare cand clientul nu primeste un raspuns, dar serverul a executat deja actiunea. Un exemplu este crearea unei plati: conexiunea cade dupa ce plata s-a inregistrat. O noua cerere fara control poate duplica efectul. Unele API-uri folosesc **chei de idempotenta**, care permit recunoasterea cererii repetate, dar comportamentul lor si perioada de pastrare sunt specifice furnizorului [S53].

Un workflow robust are trei stari distincte: `confirmed`, `failed` si `unknown`. In starea `unknown`, procesul verifica sistemul de evidenta inainte sa reaplice operatia. Pentru evenimente, identificatorii procesati trebuie pastrati intr-un mecanism durabil, nu doar intr-o lista temporara din memoria programului.

**De retinut:** siguranta unei reincercari depinde de semantica operatiei si de mecanismul care previne duplicatele, nu de numarul de retry-uri.

