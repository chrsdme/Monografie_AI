# Roadmap editorial: 1.2 si 2.0

Acest document este o propunere, nu o promisiune de calendar.

## Editia 1.2 — Robustete operationala

Scop: pastram structura actuala, dar facem trecerea de la explicatia conceptelor la mecanismele care fac un sistem mic masurabil si robust.

### 1. Retrieval hibrid si reranking

Extinderea capitolului 8 cu:

- keyword/BM25 pentru identificatori, coduri si termeni exacti;
- cautare vectoriala pentru similaritate semantica;
- reranking pentru ordonarea candidatilor;
- cand GraphRAG este justificat pentru intrebari globale si cand este excesiv.

### 2. Generare structurata si constrained decoding

Extinderea capitolului 7:

- JSON Schema si contracte de iesire;
- diferenta dintre schema validata si continut corect;
- constrained decoding / grammar-guided generation;
- validare semantica dupa decodare.

### 3. Prompt caching, KV cache si economia contextului

Extinderea capitolelor 4 si 20:

- ce parte din context se repeta intre apeluri;
- caching la nivel de furnizor sau motor de inferenta;
- efectul asupra costului si latentei;
- ce nu garanteaza caching-ul.

### 4. Retry, fallback si circuit breakers

Extinderea capitolului 19:

- retry cu backoff;
- diferenta dintre retry sigur si retry periculos;
- model/provider fallback;
- circuit breaker;
- bugete maxime de timp, apeluri si cost per run.

### 5. Evals in CI/CD

Extinderea capitolului 17:

- golden datasets;
- regression tests dupa modificarea modelului, promptului sau tool-ului;
- praguri eliminatorii;
- rularea evaluarii intr-un pipeline de tip GitHub Actions;
- blocarea promovarii daca performanta sau siguranta regreseaza.

### 6. Human-in-the-loop, human-on-the-loop si intreruperi persistente

Extinderea capitolelor 14 si 17:

- aprobare inaintea actiunii;
- supraveghere cu posibilitate de interventie;
- checkpoint + WAITING_APPROVAL + reluare;
- ce context trebuie sa vada omul pentru o aprobare reala.

### 7. Computer use / agenti GUI

Subcapitol scurt, nu schimbare de directie:

- cand UI automation este necesara pentru sisteme fara API;
- fragilitatea la schimbarea interfetei;
- verificarea efectului, nu doar a click-ului;
- izolarea credentialelor si a sesiunii.

## Editia 2.0 — Manual de proiectare si operare

Scop: trecerea de la „ce sunt componentele” la „cum proiectam, evaluam si operam sisteme complete”.

### Partea VI. Patternuri arhitecturale

Catalog neutru de patternuri:

- router;
- sequential workflow;
- parallel fan-out / fan-in;
- planner-executor;
- evaluator-optimizer;
- research -> verify -> synthesize;
- specialist + independent reviewer;
- multi-agent numai cand exista responsabilitati reale separate.

Fiecare pattern: problema, schema, cand ajuta, cand nu ajuta, failure modes, cost si evaluare.

### Partea VII. AgentOps si ciclu de viata

- prompt/config-as-code;
- versionarea modelului, tool schema, memorie si permisiuni;
- deployments si rollback;
- incident response;
- post-mortem;
- drift de date, politici si surse;
- observabilitate OpenTelemetry;
- cost per accepted task.

### Partea VIII. Failure modes si red teaming

Un capitol sistematic care unifica:

- hallucination/confabulation;
- stale context;
- stale memory;
- memory poisoning;
- indirect prompt injection;
- tool misuse;
- privilege escalation;
- orchestration failure;
- evaluator failure;
- correlated errors intre agenti;
- bucle fara progres.

### Partea IX. Interoperabilitate

- MCP in profunzime: host/client/server, capabilitati, permisiuni si securitate;
- A2A pentru colaborarea dintre agenti;
- autentificare, autorizare si identitate intre sisteme;
- handoff-uri cu schema si provenienta.

Nu tratam protocoalele emergente drept garantii de securitate sau standarde imuabile.

### Partea X. Guvernanta si conformitate

Fara consultanta juridica:

- NIST AI RMF si NIST AI 600-1;
- EU AI Act: transparenta, documentatie si obligatii relevante in functie de rol si risc;
- GDPR si minimizarea datelor;
- cine poate modifica promptul, memoria, permisiunile si nivelul de autonomie;
- separarea competentei de autoritate.

### Studii de caz 2.0

Studiile existente devin reproductibile si masurabile:

- configuratie versionata;
- dataset de test;
- trace;
- cost;
- timp;
- interventii umane;
- defecte;
- criterii de acceptare;
- rerun dupa schimbarea modelului.

Un benchmark util ar compara aceeasi sarcina in patru configuratii: agent generalist, workflow determinist + model, specialisti cu routing fix si sistem orchestrat dinamic.

## Ce NU ar trebui sa devina 2.0

- catalog de framework-uri;
- clasament de modele care expira lunar;
- colectie de promisiuni comerciale;
- „swarm” folosit pentru orice problema;
- tutorial specific unui singur furnizor;
- capitole de fine-tuning disproportionate fata de publicul tinta.

Principiul ramane: arhitectura trebuie justificata prin rezultate, nu prin numarul de componente.
