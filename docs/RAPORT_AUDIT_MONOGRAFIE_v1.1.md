# Raport de audit - Editia 1.1

**Data:** 15 octombrie 2026

Auditul a comparat sursa Markdown, versiunea web si observatiile produse independent de mai multi agenti. Recomandarile lor nu au fost acceptate automat: fiecare modificare inclusa in editia 1.1 a fost verificata fata de textul real si, pentru afirmatiile tehnice importante, fata de surse publice.

## Verdict

Structura conceptuala a editiei 1.0 este solida. Nu a fost identificata o eroare fundamentala care sa impuna rescrierea lucrarii, dar existau probleme editoriale certe, cateva formulari prea largi si referinte care necesitau actualizare.

## Corecturi aplicate

- numerotarea capitolelor 8 si 9 a fost reparata;
- au fost corectate typo-uri precum `un incantatie`, `Instruciuni`, `linkuri_surze` si `pasi ficsi`;
- explicatia despre next-token prediction a fost limitata explicit la modelele autoregresive;
- formularea despre rationament a fost nuantata;
- MCP este raportat la revizia 2026-07-28;
- idempotenta este explicata ca proprietate sustinuta de serviciul care aplica efectul, nu doar de existenta unui ID;
- QA read-only este definit fata de implementarea evaluata si productie, nu fata de orice fisier temporar;
- ramurile Git nu mai sunt prezentate ca echivalent al unor spatii de lucru izolate;
- prompt injection direct si indirect sunt diferentiate;
- Trust Score este marcat explicit drept construct didactic intern, nu standard industrial;
- exemplul de observabilitate cu 24 de documente nu mai sugereaza o concluzie numerica ambigua;
- estimarea statistica este separata de reprezentativitatea setului de teste;
- bibliografia a fost actualizata pentru MCP, OWASP, OpenTelemetry, Lost in the Middle si Kuse;
- glosarul a fost reordonat alfabetic;
- Partea V descrie corect doua studii principale si doua exemple complementare.

## Recomandari ale agentilor pe care NU le-am preluat ca fapte

Unele propuneri erau utile ca directie, dar formularea initiala era prea categorica. Exemple:

- GraphRAG nu este o inlocuire universala pentru RAG; este potrivit pentru anumite intrebari globale si relationale.
- RAGAS Context Precision masoara ordonarea/ranking-ul contextelor relevante, nu simplu faptul ca informatia utila este „la inceputul promptului”.
- Reflexion nu trebuie descris generic ca rescriere automata permanenta a system prompt-ului.
- „50-90% economie prin prompt caching” nu poate fi afirmata universal.
- fallrouting nu este un termen standard pe care merita sa construim vocabularul; folosim model routing/fallback.
- test-time compute nu trebuie redus la „mii de hidden thinking tokens”; implementarile difera.
- cifrele ROI ale furnizorilor raman rezultate raportate de furnizori, nu dovezi generale.

## Surse prioritare pentru editie

Au fost preferate lucrarile academice, specificatiile si documentatia oficiala. Sursele practice sau comerciale raman utile pentru exemple, dar nu sustin singure afirmatii universale de performanta.

## Ce ramane pentru 1.2

Editia 1.1 este o revizie de fundatie. Extinderile majore - structured outputs, evaluarea RAG, evals de regresie, memory failure modes, human oversight, retry/circuit breakers si computer use - sunt mutate intentionat in roadmap pentru a evita transformarea unei editii de corectura intr-o rescriere necontrolata.
