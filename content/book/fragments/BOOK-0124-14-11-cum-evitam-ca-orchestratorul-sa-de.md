### 14.11. Cum evitam ca orchestratorul sa devina el insusi problema

Un orchestrator care depinde numai de o conversatie foarte lunga poate pierde starea. Unul care ia decizii fara jurnal devine greu de auditat. Unul care isi declara singur succesul nu ofera control real. Solutia practica: tranzitiile importante intr-un registru, contracte de intrare si iesire, limite impuse si verificari separate pentru actiunile cu risc.

