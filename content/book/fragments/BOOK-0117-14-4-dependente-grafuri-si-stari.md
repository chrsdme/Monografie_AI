### 14.4. Dependente, grafuri si stari

O sarcina poate fi `PENDING`, `READY`, `RUNNING`, `BLOCKED`, `FAILED`, `WAITING_APPROVAL` sau `DONE`. Numele exacte variaza, dar sensul trebuie definit explicit. Trecerea de la `RUNNING` la `DONE` ar trebui sa se bazeze pe conditii verificabile, nu doar pe textul "gata" generat de un agent.

Dependentele se pot reprezenta ca un graf: sarcina B porneste doar dupa A; C si D merg in paralel; E asteapta rezultatele lui C si D. Cand nu are cicluri, graful se numeste **DAG** (*directed acyclic graph*). Nu orice sistem agentic are nevoie de un DAG explicit, dar ajuta la planificarea proceselor complexe.

