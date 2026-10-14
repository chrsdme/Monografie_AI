# 20. Cost, viteza, calitate si alegerea unei complexitati justificate

## 20.1. Costul real depaseste factura de tokeni

Intr-un sistem cu agenti platim sau consumam resurse pentru inferenta, cautare, stocare, instrumente, executia testelor si monitorizare. Unele servicii factureaza separat intrarile, iesirile, stocarea ori apelurile instrumentelor. Un model accesat local nu elimina costurile: hardware, energie, mentenanta si timpul operatorului raman relevante. Nu exista un pret universal si nu vom construi decizii pe tarife care pot fi modificate oricand.

## 20.2. De ce mai multi agenti pot incetini sistemul

Sa presupunem ca o sarcina simpla se rezolva cu un apel de model si un test. Daca o impartim intre patru agenti, adaugam pregatirea contextului, transferuri, verificarea contractelor si sintetizarea rezultatelor. Poate fi mai lent si mai scump. Paralelizarea ajuta numai cand munca poate fi separata, exista resurse suficiente si costul coordonarii nu anuleaza castigul.

Un sistem cu sase instante care utilizeaza acelasi model pe un singur accelerator nu este automat de sase ori mai rapid. Serviciul poate procesa cererile in coada, poate imparti capacitatea sau poate atinge limitele de memorie. De aceea masuram **durata completa a workflow-ului**, nu numai viteza unui apel individual.

## 20.3. Metrici care merita urmarite

**Rata de succes verificat**, nu doar rata de raspuns. **Timpul pana la rezultat acceptat**, nu doar timpul primei iesiri. **Costul per sarcina acceptata**, nu doar costul unui apel. **Frecventa interventiilor umane**, **numarul de retry-uri**, **erorile critice** si **timpul de recuperare** sunt indicatori utili. Un model mai ieftin care produce multe reparatii poate ajunge mai scump pe rezultatul final.

## 20.4. O matrice simpla de decizie

| Situatie | Solutie de la care merita sa pornim |
|---|---|
| Intrebare sau explicatie | Chatbot, fara autonomie |
| Analiza unui document | Model + document + verificare |
| Date actuale dintr-o sursa | Tool / API cu raspuns validat |
| Proces repetitiv si fix | Script sau workflow determinist |
| Exceptii nestructurate | Agent cu instrumente limitate |
| Mai multe responsabilitati reale | Agenti specializati + orchestrare |
| Operatii cu miza mare | Controale independente, aprobare si audit |

Aceasta matrice nu este lege. Este un antidot impotriva supraingineriei. Alegem cea mai simpla solutie care satisface cerintele, apoi crestem complexitatea pe baza unor dovezi.
