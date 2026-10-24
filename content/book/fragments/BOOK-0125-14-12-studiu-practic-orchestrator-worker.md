### 14.12. Studiu practic: orchestrator, worker temporar si verificator separat

Sa presupunem ca vrem sa corectam autentificarea unei aplicatii. In loc sa incarcam toata investigatia intr-o singura conversatie, putem separa deciziile de executie:

```text
Cererea utilizatorului
        |
MAIN: cerinte, dependente, criterii
        |
Task Packet -> Worker (context nou)
        |              |
        |         cod + teste + jurnal
        |              |
        +----------> Verifier independent
                       |
               dovezi PASS / FAIL
                       |
               MAIN: accepta sau redistribuie
```

**Contractul taskului.** Orchestratorul atribuie un ID, o cerinta, fisierele si instrumentele permise, limitele de timp si resurse, plus criterii verificabile de acceptare. Un worker nu ar trebui sa primeasca istoricul complet al proiectului, ci doar acest contract si referintele necesare. Daca doi workeri modifica aceleasi fisiere, izolam modificarile si verificam rezultatul integrat.

**Workerul nu se autocertifica.** Workerul poate avea un checklist si isi poate rula singur testele. La final declara `CLAIMED_DONE`, `PARTIAL`, `BLOCKED` sau `FAILED` si trimite modificarile, dovezile si limitarile. Un verificator separat stabileste pentru fiecare criteriu `PASS`, `FAIL` sau `NOT_VERIFIED`, preferabil pe baza unor teste reproductibile. Doar MAIN poate marca cerinta `ACCEPTED`, conform politicii proiectului; `DEFERRED` cere motiv si aprobare explicita. Un rezultat general `DONE` nu ascunde cerinte ramase deschise.

**Contextul este temporar, starea nu.** La un task nou sau la reluarea unuia intrerupt, un worker porneste cu un context limitat si citeste un checkpoint persistent. De exemplu, `evidence/T-001/progress.md` poate retine concluziile si pasii urmatori, `events.jsonl` evenimentele relevante, iar `test-summary.txt` verificarile. Jurnalul trebuie sa includa provenienta si versiunile fisierelor, fara sa stocheze secrete sau dumpuri inutile. Un rezumat nu inlocuieste verificarea starii reale a fisierelor.

**Bugetul este o politica, nu o magie a SDK-ului.** Pentru un task mediu putem experimenta cu aproximativ 25 de operatii substantiale. La circa 70% din buget workerul se concentreaza pe finalizare, iar la 80% salveaza progresul si returneaza `PARTIAL` daca nu poate incheia sigur. Valorile sunt orientative si se ajusteaza dupa date: numarul de apeluri de instrumente, numarul de ture, tokenii si costul sunt metrici diferite. Operatiile independente de citire pot fi grupate cand mediul permite, fara a compromite observabilitatea.

**Ce este suportat si ce construim noi.** Claude Code foloseste configuratii de subagenti in Markdown, Codex foloseste configuratii TOML, iar OpenAI Agents SDK si Pydantic AI permit delegare programatica. LangGraph ofera mecanisme explicite de stare si checkpoint. Totusi, regulile `ACCEPTED`, contractele noastre de task, politicile de buget si izolarea reala a permisiunilor nu apar automat din simpla definire a unui agent. Un handoff poate transmite si istoric; contextul proaspat trebuie impus prin configuratie ori rulare independenta.

**Exemplu descarcabil:** [configuratii generice de orchestrare pentru Claude, Codex si SDK-uri Python](https://github.com/chrsdme/Monografie_AI/blob/main/resurse/agent_orchestration_generic_examples.zip). Sunt sabloane educationale de adaptat si validat inaintea folosirii intr-un mediu real, nu o infrastructura de productie gata de instalat.

**Concluzia capitolului:** orchestrarea nu inseamna doar delegare. Inseamna control asupra dependentelor, identitatilor, resurselor, verificarilor si recuperarii.

