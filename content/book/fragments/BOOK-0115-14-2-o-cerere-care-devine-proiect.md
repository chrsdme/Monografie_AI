### 14.2. O cerere care devine proiect

Utilizatorul spune: "Construieste o aplicatie web cu autentificare, panou de administrare si notificari". Cererea e prea larga pentru un singur pas. Orchestratorul poate incepe cu clarificarea cerintelor, apoi cere arhitectura, creeaza sarcini de implementare, asteapta integrarea si porneste verificarile. Sarcinile pot depinde unele de altele: schema bazei de date trebuie fixata inainte ca anumite componente sa poata fi conectate corect. Figura 7 arata relatia dintre orchestrator, dependente, instante si verificare.

![Figura 7. Orchestrator, dependente, instante si verificare.](Monografie_AI_figuri/fig07_orchestrare.svg)

*Figura 7. Orchestratorul coordoneaza si tine starea executiei.*

