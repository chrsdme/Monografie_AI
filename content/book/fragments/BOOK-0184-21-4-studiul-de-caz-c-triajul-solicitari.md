### 21.4. Studiul de caz C: triajul solicitarilor de suport

Ca sa vezi ca aceleasi principii merg si in afara dezvoltarii software, luam un al treilea exemplu, mai scurt. O firma primeste emailuri despre livrari, retururi, facturi si probleme tehnice. Nu incepem prin a construi cinci agenti. Incepem prin a observa cum se rezolva acum cererile si unde se pierde timp.

**Versiunea asistata.** Un angajat copiaza mesajul intr-un chatbot si cere un rezumat si o propunere de raspuns. Verifica datele si trimite el raspunsul. Castigul posibil e la redactare, nu la executia completa.

**Versiunea conectata.** Aplicatia primeste un mesaj, identifica limba si categoria probabila, apoi consulta printr-un API starea comenzii. Politica actualizata de retur vine dintr-o baza documentara, cu sursa citata. Daca lipseste numarul comenzii, sistemul nu inventeaza unul, ci cere completari.

**Versiunea cu automatizare fixa.** Daca e doar o intrebare despre status si identitatea clientului e verificata, programul construieste un raspuns din datele comenzii. Daca mesajul contine o contestatie, informatii contradictorii sau o cerere financiara, trece la operator. Niciun LLM nu decide singur asupra unei rambursari.

**Versiunea agentica.** Pentru cererile complexe, un agent specializat poate planifica verificarea mai multor surse, dar executa doar actiunile permise. Un orchestrator urmareste dependentele si impune un numar maxim de incercari. Fiecare raspuns final include un rezumat al datelor consultate si tipul de verificare facuta. La cazurile sensibile, rezultatul ramane ciorna pana la aprobare.

**Cum evaluam.** Masuram separat clasificarea corecta a categoriei, folosirea datelor reale ale comenzii, rata de escaladare justificata, timpul pana la rezolvare si numarul de actiuni neautorizate. Nu confundam un raspuns politicos cu rezolvarea cererii. Exemplul combina tipurile de aplicatii din ghidul IBM despre AI workflow si recomandarile pentru suport asistat din surse practice romanesti, fara a prelua produse sau promisiuni comerciale [S17, S22, S36].

