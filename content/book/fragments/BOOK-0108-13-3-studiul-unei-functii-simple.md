### 13.3. Studiul unei functii simple

Cerinta: "Transportul este gratuit doar cand valoarea comenzii este **mai mare de** 50 de lire". Agentul de dezvoltare scrie `total >= 50`, apoi isi ruleaza testele pe valorile 30 si 70. Ambele trec. Dar pentru 50 rezultatul e gresit. Este un esec al cazurilor de test, nu neaparat al rularii lor.

Am putea crea sase agenti: unul scrie functia, unul ruleaza `pytest`, unul citeste logul, altul corecteaza, unul face commit si ultimul scrie raportul. Ar fi o fragmentare exagerata. Toate operatiile astea pot face parte din responsabilitatea fireasca a agentului de Development, iar transferurile intre sase entitati ar adauga complexitate si riscul sa se piarda informatie pe drum.

Un **agent QA separat** are sens pentru ca are alta responsabilitate: verifica implementarea fata de cerinta initiala. Poate construi teste fix la pragul de 50, poate inspecta modificarile si poate refuza acceptarea. Ideal, evaluarea lui porneste din specificatia originala si din dovezi reale, nu doar din afirmatia dezvoltatorului ca "totul e gata".

