# Audit editorial si tehnic pentru editia 1.1

Data: 15 octombrie 2026

## Verdict

Editia 1.0 nu continea erori conceptuale majore care sa invalideze structura lucrarii. Au fost identificate probleme editoriale certe, cateva formulari tehnice care meritau restranse si cateva ambiguitati operationale.

## Corectii aplicate

- numerotarea capitolelor 8 si 9;
- greselile `un/o incantatie`, `Instruciuni/Instructiuni`, `linkuri_surze/linkuri_surse`, `O/Un embedding`;
- domeniul afirmatiei despre predictia urmatorului token, restrans la modelele autoregresive;
- formularea despre rationament, prezentata ca comportament observabil si nu ca echivalenta cu rationamentul uman;
- izolarea Git: ramurile nu sunt confundate cu directoarele de lucru sau cu izolarea de securitate;
- idempotenta: cheia trebuie reutilizata si verificata de serviciul care aplica efectul;
- QA: citire asupra implementarii evaluate, dar posibilitatea de a crea si executa teste intr-un mediu separat;
- exemplul de trace din capitolul 16;
- formularea statistica despre marimea esantionului;
- bibliografia OWASP, OpenTelemetry si Kuse.

## Imbunatatiri de continut

Au fost adaugate:

- iesiri structurate si diferenta dintre validarea formei si validarea continutului;
- competenta demonstrata versus autoritate acordata;
- evaluarea RAG pe componente;
- consensul multi-agent versus independenta dovezilor;
- distinctia dintre prompt injection directa si indirecta.

## Ce nu a fost introdus in 1.1

GraphRAG, A2A, computer use, test-time compute, prompt caching, constrained decoding avansat, AgentOps si capitole de conformitate au fost pastrate pentru o editie ulterioara. Sunt subiecte valide, dar introducerea tuturor intr-o revizie de corectura ar schimba prea mult curba pedagogica a editiei 1.x.

## Principiu editorial

Editia 1.1 ramane independenta de furnizor. Exemplele comerciale sunt utilizate numai pentru a ilustra mecanisme verificabile si nu ca dovada generala de performanta.
