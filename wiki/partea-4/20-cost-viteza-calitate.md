# 20. Cost, viteza, calitate si alegerea unei complexitati justificate

## 20.1. Costul real depaseste factura de tokeni

Intr-un sistem cu agenti consumi resurse pentru inferenta, cautare, stocare, unelte, rularea testelor si monitorizare. Unele servicii factureaza separat intrarile, iesirile, stocarea sau apelurile de unelte. Un model local nu elimina costurile: hardware-ul, energia, mentenanta si timpul operatorului raman relevante. Nu exista un pret universal si nu construim decizii pe tarife care se pot schimba oricand.

Un detaliu mai putin cunoscut: acelasi text poate cere un numar diferit de tokeni in limbi diferite. Un studiu din 2023 a constatat ca acelasi continut poate necesita pana la circa 15 ori mai multi tokeni in unele limbi fata de altele, ceea ce afecteaza si costul, si cat context incape [S38](../anexe/bibliografie.md#s38). Nu avem aici o cifra verificata pentru romana, deci masoara pe textele tale reale cu tokenizatorul modelului pe care il folosesti.

## 20.2. De ce mai multi agenti pot incetini sistemul

Sa zicem ca o sarcina simpla se rezolva cu un apel de model si un test. Daca o imparti intre patru agenti, adaugi pregatirea contextului, transferuri, verificarea contractelor si sintetizarea rezultatelor. Poate iesi mai lent si mai scump. Paralelizarea ajuta doar cand munca se poate separa, exista resurse suficiente si costul coordonarii nu anuleaza castigul.

Un sistem cu sase instante care folosesc acelasi model pe un singur accelerator nu e automat de sase ori mai rapid. Serviciul poate pune cererile la coada, poate imparti capacitatea sau poate atinge limitele de memorie. De aceea masori **durata completa a workflow-ului**, nu doar viteza unui apel individual.

## 20.3. Metrici care merita urmarite

**Rata de succes verificat**, nu doar rata de raspuns. **Timpul pana la rezultatul acceptat**, nu doar timpul primei iesiri. **Costul pe sarcina acceptata**, nu doar costul unui apel. **Frecventa interventiilor umane**, **numarul de retry-uri**, **erorile critice** si **timpul de recuperare** sunt indicatori utili. Un model mai ieftin care produce multe reparatii poate ajunge mai scump pe rezultatul final.

## 20.4. O matrice simpla de decizie

| Situatie | Solutie de la care merita sa pornim |
|---|---|
| Intrebare sau explicatie | Chatbot, fara autonomie |
| Analiza unui document | Model + document + verificare |
| Date actuale dintr-o sursa | Tool / API cu raspuns validat |
| Proces repetitiv si fix | Script sau workflow determinist |
| Exceptii nestructurate | Agent cu unelte limitate |
| Mai multe responsabilitati reale | Agenti specializati + orchestrare |
| Operatii cu miza mare | Controale independente, aprobare si audit |

Matricea nu e lege. E un antidot impotriva supraingineriei. Alegi cea mai simpla solutie care satisface cerintele, apoi cresti complexitatea pe baza dovezilor.

## 20.5. Doua parghii concrete de cost

Cand promptul tau are o parte lunga si stabila (instructiuni, documentatie, exemple), poti folosi *prompt caching*, un mecanism prin care furnizorul reutilizeaza partea deja procesata. Documentatia Anthropic spune ca asta "significantly reduces processing time and costs for repetitive tasks or prompts with consistent elements" si indica, pentru cache-ul de 5 minute, o scriere la 1,25 ori pretul de baza al tokenilor de intrare si o citire la 0,1 ori acel pret [S39](../anexe/bibliografie.md#s39). Sunt cifre ale unui furnizor, valabile la data consultarii, cu exceptii pe model. Verifica tarifele curente si masoara pe traficul tau.

A doua parghie este rutarea: sarcinile simple merg pe un model mai ieftin, cele grele pe unul mai capabil, cu masurarea erorilor de rutare (sectiunea 14.3). Ambele functioneaza doar daca ai o evaluare care iti spune ca se pastreaza calitatea.
