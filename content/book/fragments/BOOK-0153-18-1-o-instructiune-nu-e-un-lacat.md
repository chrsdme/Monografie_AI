### 18.1. O instructiune nu e un lacat

Un agent poate primi instructiunea "nu sterge fisiere". Reduce probabilitatea unor actiuni nepotrivite, dar nu e o bariera de securitate. Daca unealta expune o functie capabila sa stearga un director, iar agentul are credentialele necesare, riscul e real. Solutia e sa controlezi drepturile in sistemul de fisiere, in API si in mediul de executie.

**Principiul privilegiului minim** spune ca o componenta trebuie sa aiba doar accesul necesar sarcinii ei. Un agent Research care consulta documentatie nu are nevoie de token pentru publicarea in productie. Un agent QA poate primi acces de citire la cod si la rezultatele testelor, fara posibilitatea de a modifica implementarea pe care o verifica.

