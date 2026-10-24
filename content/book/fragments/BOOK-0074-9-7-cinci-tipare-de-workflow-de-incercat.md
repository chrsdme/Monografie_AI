### 9.7. Cinci tipare de workflow de incercat inainte de un agent

Intre "un singur apel la model" si "un agent liber" exista un teren larg. Ghidul Anthropic descrie cinci tipare de workflow, utile ca vocabular comun [S10]:

- **Inlantuire de prompturi** (*prompt chaining*): o sarcina se imparte in pasi, iar rezultatul unuia intra in urmatorul, cu verificari intre ei. Exemplu: extragi datele facturii, apoi le validezi, apoi redactezi nota.
- **Rutare** (*routing*): clasifici cererea si o trimiti pe traseul potrivit. Exemplu: mesajele despre facturi merg la un traseu, cele despre retururi la altul.
- **Paralelizare** (*parallelization*): mai multe verificari independente ruleaza in acelasi timp, iar rezultatele se compara sau se voteaza.
- **Orchestrator si lucratori** (*orchestrator-workers*): un model imparte sarcina in subsarcini care nu pot fi cunoscute dinainte si le da altor modele.
- **Evaluator si optimizator** (*evaluator-optimizer*): un model produce, altul critica, si se repeta pana cand criteriile sunt indeplinite.

Primele trei se pot construi si cu cod obisnuit, fara sa lasi modelul sa decida traseul. Ultimele doua se apropie de comportamentul agentic. Regula practica: ia cea mai simpla varianta care trece testele tale, apoi masoara daca urmatoarea chiar aduce ceva.

