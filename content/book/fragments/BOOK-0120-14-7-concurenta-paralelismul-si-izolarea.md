### 14.7. Concurenta, paralelismul si izolarea

**Concurenta** inseamna gestionarea mai multor sarcini aflate in progres. **Paralelismul** inseamna executie simultana reala. Un singur serviciu poate gestiona zece sesiuni concurente si totusi sa genereze raspunsurile pe rand, daca resursele nu permit altfel. Numarul instantelor active nu e acelasi cu numarul de procese, de modele incarcate sau de GPU-uri.

Cand doi dezvoltatori AI modifica aceleasi fisiere, apar conflicte. De aceea folosim spatii de lucru separate, ramuri de versiune, reguli de integrare si teste pe rezultatul combinat. Daca sase instante scriu fiecare cod corect in izolare, rezultatul integrat poate totusi sa nu mearga. Evaluarea sistemului trebuie sa includa si pasul acesta.

