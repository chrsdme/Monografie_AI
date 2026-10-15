# 15. Cele patru discipline de inginerie: prompt, context, harness si loop

## 15.1. De ce au aparut denumiri diferite

Pe masura ce aplicatiile cu LLM-uri au trecut de la un singur raspuns la procese care dureaza, atentia inginerilor s-a mutat spre probleme mai largi. Intai am optimizat cererea. Apoi ne-am intrebat ce context trebuie trimis. Apoi ce mediu ii dam modelului, cum controlam actiunile si cum verificam ciclurile repetate. Termenii **prompt engineering**, **context engineering**, **harness engineering** si **loop engineering** descriu niveluri care se suprapun partial. Nu sunt patru etape istorice oficiale prin care trece fiecare proiect.

## 15.2. Prompt engineering

Intrebarea lui: **Cum formulez instructiunile?** Stabilesti rolul, scopul, exemplele, formatul si conditiile de raspuns. Un prompt mai bun poate reduce ambiguitatea, dar nu aduce date actuale si nici posibilitatea de executie. Termenul s-a raspandit odata cu modelele generative accesibile publicului; practica de a formula si testa intrari e mai veche decat denumirea [S04](../anexe/bibliografie.md#s04).

Exemplu: in loc de "fa o analiza buna", ceri compararea a trei variante dupa cost, risc si timpul de implementare, pe baza surselor indicate.

## 15.3. Context engineering

Intrebarea lui: **Ce vede modelul, in ce ordine si cu ce provenienta?** Alegi instructiunile stabile, documentele, rezultatele uneltelor si istoricul util. Decizi ce nu incluzi, ce recuperezi la cerere si ce pastrezi intre rulari. Anthropic a formulat explicit perspectiva asta intr-un articol din septembrie 2025 [S03](../anexe/bibliografie.md#s03). Practicile de gestionare a informatiei exista, evident, de mai mult timp.

Exemplu: un agent care depaneaza o aplicatie primeste versiunea curenta, eroarea si fisierele implicate, nu 50 de conversatii vechi fara legatura cu incidentul.

## 15.4. Harness engineering

Intrebarea lui: **In ce mediu lucreaza agentul si ce constrangeri tehnice il fac controlabil?** Pregatesti unelte, permisiuni, jurnal, teste, recuperare si limite. Termenul a devenit vizibil in discutiile publice despre dezvoltarea asistata de agenti in 2026; eseul OpenAI din februarie este un reper documentat, nu o dovada ca metoda a fost inventata atunci [S11](../anexe/bibliografie.md#s11).

Exemplu: modelul primeste acces la o copie izolata a proiectului, poate rula testele, dar nu poate publica direct in productie fara verificare si aprobare.

## 15.5. Loop engineering

Intrebarea lui: **Cum proiectez iteratia dintre actiune, observatie, evaluare si corectare?** Intr-o bucla, agentul cere o actiune, primeste feedback si decide pasul urmator. Un sistem bun observa lipsa progresului, impune bugete si stie cand sa se opreasca. IBM a explicat termenul *loop engineering* intr-un material din iulie 2026 [S14](../anexe/bibliografie.md#s14). Practicile de feedback si control al buclelor preced, desigur, eticheta.

Exemplu: un agent implementeaza o functionalitate, ruleaza testele, repara erorile si repeta pana cand verificarile trec sau pana atinge limita de iteratii. Un validator independent hotaraste daca rezultatul final poate fi acceptat.

## 15.6. Cum lucreaza impreuna

Intr-un workflow de dezvoltare software, **prompt engineering** defineste sarcina, **context engineering** alege fisierele, **harness engineering** pune la dispozitie editorul si testele cu permisiuni, iar **loop engineering** gestioneaza succesiunea implementare-test-corectare. Orchestratorul poate coordona mai multe asemenea bucle si poate decide cand e nevoie de verificare independenta.

Niciuna dintre cele patru discipline nu repara singura un sistem prost proiectat. Un prompt impecabil nu compenseaza lipsa autorizarii. Un context excelent nu garanteaza ca o unealta returneaza date corecte. O bucla rapida poate repeta o eroare de o mie de ori daca nu are conditie de oprire.

## 15.7. Legatura cu ingineria software obisnuita

Versionarea, testele automate, izolarea, monitorizarea, permisiunile si recuperarea dupa esec nu au aparut odata cu agentii AI. Sunt principii solide de inginerie software. Noutatea e ca le combini cu componente care genereaza raspunsuri variabile si pot propune dinamic actiuni. Tocmai de aceea adaptam disciplina existenta la o sursa in plus de incertitudine, nu reconstruim totul de la zero.
