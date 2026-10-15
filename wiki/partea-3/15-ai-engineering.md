# 15. Patru perspective de inginerie: prompt, context, harness si loop

## 15.1. De ce au aparut denumiri diferite

Pe masura ce aplicatiile cu LLM-uri au trecut de la un singur raspuns la procese care dureaza, atentia inginerilor s-a mutat spre probleme mai largi. Mai intai optimizam cererea. Apoi ne-am intrebat ce context trebuie transmis. Apoi ce mediu ii oferim modelului, cum controlam actiunile si cum verificam ciclurile repetate. Termenii **prompt engineering**, **context engineering**, **harness engineering** si **loop engineering** descriu niveluri care se suprapun partial; nu sunt patru faze istorice oficiale prin care trebuie sa treaca fiecare proiect.

## 15.2. Prompt engineering

Intrebarea lui este: **Cum formulez instructiunile?** Stabilim rolul, scopul, exemplele, formatul si conditiile de raspuns. Un prompt mai bun poate reduce ambiguitatea, dar nu aduce automat date actuale sau posibilitatea de executie. Termenul s-a popularizat odata cu dezvoltarea modelelor generative accesibile publicului; practica de a formula si testa intrari este mai veche decat denumirea actuala [S04].

Exemplu: in loc sa spunem „fa o analiza buna”, cerem compararea a trei variante dupa cost, risc si timpul de implementare, folosind sursele indicate.

## 15.3. Context engineering

Intrebarea lui este: **Ce vede modelul, in ce ordine si cu ce provenienta?** Selectam instructiunile stabile, documentele, rezultatele instrumentelor si istoricul util. Decidem ce nu includem, ce recuperam la cerere si ce pastram intre rulari. Anthropic a formulat explicit aceasta perspectiva intr-un articol din septembrie 2025 [S03]. Practicile de gestionare a informatiei exista, desigur, de mai mult timp.

Exemplu: un agent care depaneaza o aplicatie primeste versiunea curenta, eroarea si fisierele implicate, nu 50 de conversatii vechi fara legatura cu incidentul.

## 15.4. Harness engineering

Intrebarea lui este: **In ce mediu executa agentul sarcina si ce constrangeri tehnice il fac controlabil?** Pregatim instrumente, permisiuni, jurnal, teste, recuperare si limite. Termenul a devenit proeminent in discutii publice despre dezvoltarea asistata de agenti in 2026; eseul OpenAI din februarie este un reper documentat, nu dovada ca metoda a fost inventata atunci [S11].

Exemplu: modelul primeste acces la o copie izolata a proiectului, poate executa testele, dar nu poate publica direct in productie fara o verificare si o aprobare.

## 15.5. Loop engineering

Intrebarea lui este: **Cum proiectez iteratia dintre actiune, observatie, evaluare si corectare?** Intr-o bucla, agentul solicita o actiune, primeste feedback si decide pasul urmator. Un sistem bun identifica lipsa progresului, impune bugete si stie cand sa se opreasca. IBM a explicat termenul *loop engineering* intr-un material publicat in iulie 2026 [S14]. Practicile de feedback si control al buclelor preced, evident, aceasta eticheta.

Exemplu: un agent implementeaza o functionalitate, ruleaza testele, repara erorile si repeta pana cand verificarile trec sau pana atinge limita de iteratii. Un validator independent stabileste daca rezultatul final poate fi acceptat.

## 15.6. Cum functioneaza impreuna

Intr-un workflow de dezvoltare software, **prompt engineering** defineste sarcina, **context engineering** selecteaza fisierele, **harness engineering** pune la dispozitie editorul si testele cu permisiuni, iar **loop engineering** gestioneaza succesiunea implementare-test-corectare. Orchestratorul poate coordona mai multe astfel de bucle si poate decide cand este necesara verificarea independenta.

Niciuna dintre cele patru discipline nu repara singura un sistem prost proiectat. Un prompt impecabil nu compenseaza lipsa autorizarii. Un context excelent nu garanteaza ca un instrument returneaza date corecte. O bucla rapida poate repeta o eroare de o mie de ori daca nu exista o conditie de oprire.

## 15.7. Relatia cu ingineria software obisnuita

Versionarea, testele automate, izolarea, monitorizarea, permisiunile si recuperarea dupa esec nu au aparut odata cu agentii AI. Ele sunt principii solide ale ingineriei software. Noutatea este combinarea lor cu componente care genereaza raspunsuri variabile si pot propune dinamic actiuni. Tocmai de aceea trebuie sa adaptam disciplina existenta la o sursa suplimentara de incertitudine, nu sa reconstruim totul de la zero.
