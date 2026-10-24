### 14.5. Modele de coordonare

**Secvential:** Research da specificatia, Development implementeaza, QA verifica. Simplu de urmarit, dar uneori lent.

**Paralel:** mai multi agenti lucreaza pe sarcini independente, iar rezultatele se agrega. Bun cand munca se poate imparti fara conflicte.

**Orchestrator si lucratori:** un coordonator descompune dinamic o cerere si imparte sarcini unor executanti. Potrivit cand subdiviziunile depind de problema concreta.

**Evaluator si optimizator:** o executie produce rezultatul, alta il evalueaza si da feedback, iar procesul se repeta doar cat timp exista progres verificabil.

**Handoff:** responsabilitatea pentru o sarcina trece la un specialist, cu un contract clar si un context limitat. Nu e o fraza de genul "acum se ocupa colegul"; include identitatea sarcinii, datele transmise si rezultatul asteptat.

Tiparele acestea sunt prezentate si in ghidul Anthropic despre agenti eficienti, a carui recomandare de baza am citat-o deja: complexitate doar cand aduce beneficii masurabile [S10].

Cand agentii vin de la furnizori diferiti, apare nevoia unui limbaj comun intre ei. Protocolul **A2A** (*Agent2Agent*), dezvoltat initial de Google si gazduit acum de Linux Foundation, urmareste sa standardizeze comunicarea intre agenti, iar versiunea 1.0 este prima sa specificatie stabila [S37]. Ca la orice standard, avantajul real apare cand cel putin doua sisteme diferite il implementeaza si il testezi in mediul tau.

