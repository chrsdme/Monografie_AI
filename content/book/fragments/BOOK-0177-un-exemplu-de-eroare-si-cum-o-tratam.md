#### Un exemplu de eroare si cum o tratam

Factura spune total 1.260,00 si are doua linii de cate 500,00 plus TVA 260,00. Modelul extrage 1.620,00 dintr-o imagine neclara. Validatorul numeric constata ca suma extrasa nu corespunde totalului calculat din linii. Documentul nu e aprobat. Agentul poate incerca alta metoda de extragere, dar dupa un numar limitat de incercari il trimite unui operator. **Sistemul a functionat corect chiar daca modelul a gresit**, pentru ca eroarea a fost prinsa inainte sa produca un efect extern.

