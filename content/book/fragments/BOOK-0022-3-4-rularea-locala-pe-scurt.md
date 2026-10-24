### 3.4. Rularea locala, pe scurt

Unele modele pot rula pe echipamente proprii cu ajutorul unui **motor de inferenta**. llama.cpp, Ollama si vLLM sunt exemple din aceasta categorie, cu roluri si moduri de lucru diferite. Motorul incarca modelul, face calculul si poate expune un API. Hardware-ul, formatul greutatilor, memoria si configuratia limiteaza ce poti rula. Uneori merge pe CPU, alteori pe GPU sau pe hardware specializat.

Aplicatia sau harness-ul nu trebuie sa fie pe aceeasi masina cu motorul. Un program local poate apela un model din cloud. Invers, un agent pornit de pe alt calculator poate folosi un model servit de masina ta. Fiecare varianta schimba costurile, confidentialitatea, latenta si munca de administrare.

