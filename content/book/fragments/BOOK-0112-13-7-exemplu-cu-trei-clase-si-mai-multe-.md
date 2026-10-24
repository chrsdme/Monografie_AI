### 13.7. Exemplu cu trei clase si mai multe instante

Putem defini clasele Research, Development si QA. Intr-un workflow, orchestratorul poate porni 2 instante Research, 3 Development si 2 QA, ca in Figura 6. Rezulta **3 clase** si **7 instante**, nu 7 modele diferite. Instantele pot folosi unul sau mai multe modele partajate si pot rula in paralel doar in masura in care sarcinile si resursele permit. La scara mai mare, acelasi principiu da, de pilda, 3 clase si 20 de instante.

![Figura 6. Trei clase de agenti si mai multe instante, cu motor partajat.](Monografie_AI_figuri/fig06_clase_instante.svg)

*Figura 6. Clasele descriu roluri; instantele executa sarcini si pot partaja un motor de inferenta.*

Distinctia are valoare economica si operationala: actualizarile unei configuratii comune pot influenta rularile viitoare ale clasei respective, iar rezultatele se pot analiza pe responsabilitati. In acelasi timp, fiecare instanta are propria identitate in jurnal, ca sa poti reconstitui un esec concret.

