# Orchestrare multi-agent: configuratii si exemplu practic

Dintr-o cerere larga nu trebuie sa rezulte o singura sesiune care citeste tot, modifica tot si isi valideaza singura munca. Exemplul de aici separa coordonarea, executia si verificarea, pastrand dovezile intre instante.

[:material-download: Descarca exemplele de agenti (ZIP)](https://github.com/chrsdme/Monografie_AI/raw/main/resurse/agent_orchestration_generic_examples.zip){ .md-button .md-button--primary }
[:material-book-open-variant: Citeste explicatia din Capitolul 14](../partea-3/14-orchestrare.md#1412-studiu-practic-orchestrator-worker-temporar-si-verificator-separat){ .md-button }

## Fluxul propus

```text
Utilizator -> MAIN / Orchestrator -> Task Packet
                                    |
                              Worker izolat
                                    |
                           fisiere + checkpoint
                                    |
                             Verifier separat
                                    |
                        PASS / FAIL / NOT_VERIFIED
                                    |
                       MAIN: ACCEPTED / BLOCKED
```

MAIN pastreaza registrul cerintelor si dependentele. Workerul primeste doar informatia necesara taskului. Un worker care a terminat poate fi inchis; un alt worker citeste checkpointul pentru continuare. MAIN nu inghite automat intregul transcript al workerului.

## Contractul unui task

| Camp | Exemplu |
| --- | --- |
| ID | `T-001` |
| Obiectiv | Corecteaza validarea inputului pentru login |
| Fisiere permise | `src/auth/`, `tests/auth/` |
| Interdictii | Fara deploy, secrete sau migrari |
| Acceptare | Testele existente si cazurile negative trec |
| Dovezi | `evidence/T-001/` |
| Buget | Limite explicite de ture, tokeni si timp |

Workerul isi face verificari locale si trimite `CLAIMED_DONE`, `PARTIAL`, `BLOCKED` sau `FAILED`. Verifierul raporteaza `PASS`, `FAIL` sau `NOT_VERIFIED` pentru fiecare criteriu. Numai orchestratorul aplica politica de acceptare. `DEFERRED` necesita motiv si aprobare, iar un task deschis nu devine `DONE` doar pentru ca agentul a spus ca a terminat.

## Stare persistenta, nu conversatii gigantice

```text
evidence/T-001/
  progress.md       # ce s-a incercat, ce ramane
  events.jsonl      # evenimente relevante, cu provenienta
  test-summary.txt  # teste si rezultate verificabile
```

Un agent nou trebuie sa confirme starea curenta a fisierelor si testelor, nu sa considere automat adevarat tot ce a scris agentul precedent. Evita salvarea credentialelor, prompturilor cu secrete sau logurilor brute nefiltrate.

## Platforme si configuratii

| Platforma | Mecanism | Limita de retinut |
| --- | --- | --- |
| Claude Code | Markdown + YAML in `.claude/agents/` | `maxTurns` nu este buget de operatii |
| Codex | TOML in `.codex/agents/` | Optiunile nu sunt identice cu cele Claude |
| Anthropic Agent SDK | Configuratie programatica a subagentilor | Permisiunile reale trebuie verificate |
| OpenAI Agents SDK | Manager, agents as tools, handoffs | Handofful poate transmite contextul anterior |
| Pydantic AI | Agenti tipizati, delegare Python, limite de utilizare | Workflowul de acceptare se implementeaza separat |
| LangGraph | Grafuri de stare si checkpointuri | Criteriile si permisiunile raman decizii de arhitectura |

Pachetul ZIP contine demonstratii si configuratii generice, **nu un sistem gata de productie**. Exemplele trebuie adaptate la versiunile instalate ale SDK-urilor si la politica de securitate a proiectului.

## Ordinea recomandata

1. Defineste cerinta si criteriile de acceptare.
2. Incepe cu un singur worker si un verificator, nu cu zece roluri artificiale.
3. Fa checkpoint dupa rezultate relevante si inainte de epuizarea bugetului.
4. Masoara rata de acceptare, reluarile, tokenii si costul total.
5. Adauga paralelism numai cand taskurile sunt independente si integrarea este testata.

**Intrebarea importanta nu este cati agenti avem, ci daca unul poate fi inlocuit fara sa pierdem progresul si dovezile.**

## Documentatie oficiala

- [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents)
- [Codex: multi-agent](https://developers.openai.com/codex/multi-agent)
- [OpenAI Agents SDK: orchestrare](https://openai.github.io/openai-agents-python/multi_agent/)
- [Pydantic AI: multi-agent applications](https://pydantic.dev/docs/ai/guides/multi-agent-applications/)
- [LangGraph: persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
