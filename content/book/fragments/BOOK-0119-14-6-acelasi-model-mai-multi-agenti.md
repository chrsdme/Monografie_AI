### 14.6. Acelasi model, mai multi agenti

Un serviciu de inferenta poate raspunde cererilor pentru Research, Development si QA. Fiecare configuratie trimite modelului instructiuni si contexte diferite. **Nu pornim neaparat trei copii ale greutatilor modelului.** Serviciul poate programa cererile in serie, poate face batching sau le poate procesa concurent, in limitele infrastructurii.

Ia un singur model Qwen accesibil prin API. Instanta `Research-R1` intreaba ce cerinte trebuie indeplinite. `Development-D1` foloseste acelasi endpoint ca sa propuna cod, dar are acces doar la spatiul lui de lucru. `QA-Q1` consulta specificatia si rezultatele testelor, dar nu are voie sa scrie in cod. Diferentele de rol vin din sistemul care construieste contextul si impune drepturile, nu dintr-o presupusa schimbare a greutatilor modelului.

**Acelasi model** poate insemna raspunsuri corelate si greseli asemanatoare. Pentru verificarile critice preferam date si teste independente; un alt model poate fi o masura in plus, nu un inlocuitor al dovezilor.

