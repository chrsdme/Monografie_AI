# Roadmap - dupa Editia 1.1

## Editia 1.2 - de la explicatie la operare masurabila

1. **Iesiri structurate si constrained decoding.** Diferenta dintre JSON valid, schema valida si valori corecte. Formatul garantat nu garanteaza adevarul datelor.
2. **RAG evaluat pe componente.** Retrieval, context recall/precision, faithfulness, answer relevance si calitatea/actualitatea sursei.
3. **Evals si regresii.** Golden sets, capability evals, regression suites, pass@k versus consistenta, LLM-as-a-judge si evaluare umana calibrata.
4. **Memorie operationala.** Stale memory, memory poisoning, drift, expirare si separarea dintre fapt, ipoteza, preferinta si rezultat temporar.
5. **Human-in-the-loop / on-the-loop / out-of-the-loop.** Aprobari cu checkpoint, expirarea aprobarii si reluarea executiei.
6. **Fiabilitate.** Retry cu backoff/jitter, circuit breakers, model fallback/routing, idempotency si reconcilierea efectelor necunoscute.
7. **Computer use / GUI agents.** Cand lipsesc API-urile, ce aduce interactiunea vizuala si de ce este mai fragila.
8. **Protectia datelor.** Minimizare, scop, acces, retentie si diferente intre securitate tehnica si conformitate.

## Editia 2.0 - manual de proiectare si operare a sistemelor agentice

### Partea VI - Patternuri arhitecturale
Router, planner-executor, evaluator-optimizer, research pipeline, critic/reviewer, orchestrare determinista versus orchestrare cu model si criterii de alegere.

### Partea VII - AgentOps si ciclul de viata
Prompt/configuration as code, evals in CI/CD, observabilitate distribuita, rollout progresiv, shadow mode, incidente, rollback si change management.

### Partea VIII - Guvernanta si securitate agentica
Responsabilitati organizationale, autonomy/authority separation, supply chain, tool misuse, memory/context poisoning, inter-agent trust, DLP si red teaming.

### Partea IX - Interoperabilitate
MCP aprofundat, A2A pentru colaborare agent-agent, autentificare, autorizare si contracte de transfer intre sisteme.

### Partea X - Catalog de sisteme complete
Cinci arhitecturi cap-coada: asistent personal, RAG pentru documentatie, procesare documente/facturi, suport clienti si software engineering agentic. Pentru fiecare: flux, permisiuni, date, verificari, failure modes, cost si criterii de oprire.

## Principiu editorial

1.2 adauga mecanisme verificabile fara sa rupa structura actuala. 2.0 devine schimbare de nivel: nu doar „ce este”, ci „cum proiectam, operam, masuram si guvernam”.
