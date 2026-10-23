### 15.5. Loop engineering

Intrebarea lui: **Cum proiectez iteratia dintre actiune, observatie, evaluare si corectare?** Intr-o bucla, agentul cere o actiune, primeste feedback si decide pasul urmator. Un sistem bun observa lipsa progresului, impune bugete si stie cand sa se opreasca. IBM a explicat termenul *loop engineering* intr-un material din iulie 2026 [S14]. Practicile de feedback si control al buclelor preced, desigur, eticheta.

Exemplu: un agent implementeaza o functionalitate, ruleaza testele, repara erorile si repeta pana cand verificarile trec sau pana atinge limita de iteratii. Un validator independent hotaraste daca rezultatul final poate fi acceptat.

