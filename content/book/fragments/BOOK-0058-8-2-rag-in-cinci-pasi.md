### 8.2. RAG in cinci pasi

1. Ai o colectie de documente sau inregistrari, de exemplu regulile unei firme.
2. Sistemul le pregateste pentru cautare: extrage textul, il imparte in fragmente, retine metadate si, eventual, calculeaza reprezentari numerice.
3. Utilizatorul pune o intrebare, de pilda "Care este termenul de retur pentru produsul X?".
4. Sistemul cauta fragmentele relevante si le trimite modelului impreuna cu intrebarea.
5. Modelul redacteaza raspunsul pe baza materialului recuperat, de preferat cu indicarea sursei.

![Figura 1. Din intrebare, cautare si surse recuperate se formeaza raspunsul verificabil.](Monografie_AI_figuri/fig01_rag.svg)

*Figura 1. RAG: colectie de documente, recuperare si raspuns cu surse. Cautarea poate fi vectoriala, dupa cuvinte-cheie sau mixta.*

Un **embedding** este o reprezentare numerica a continutului, utila in unele sisteme de cautare semantica. O **baza vectoriala** poate pastra astfel de reprezentari si cauta vecinii cei mai apropiati. RAG nu cere insa obligatoriu o baza vectoriala: cautarea dupa cuvinte-cheie, SQL sau o combinatie pot fi suficiente, uneori chiar mai potrivite.

