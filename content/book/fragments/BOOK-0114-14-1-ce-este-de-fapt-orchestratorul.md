### 14.1. Ce este, de fapt, orchestratorul?

Un **orchestrator** este componenta care coordoneaza un proces cu mai multe operatii, agenti sau servicii. Stabileste ordinea, dependentele, distribuirea sarcinilor, starile de lucru, regulile de acceptare si felul in care te recuperezi dupa esecuri. Poate fi un program determinist, un serviciu de workflow, un LLM care propune un plan sau o combinatie. Nu trebuie sa fie "cel mai destept model din sistem".

Orchestratorul nu face toate sarcinile. Seamana mai degraba cu un dispecer: urmareste ce trebuie facut, de catre cine, pana cand si cu ce dovezi. Daca dispecerul incepe sa execute fiecare operatie marunta, pierde avantajul separarii responsabilitatilor.

