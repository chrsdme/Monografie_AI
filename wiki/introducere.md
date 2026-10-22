# Introducere

## Nota editoriala

Aceasta lucrare nu cere experienta de programare si nu face reclama niciunei platforme. Poti folosi un chatbot in browser, o aplicatie instalata, o linie de comanda sau un sistem construit prin API. Principiile raman aceleasi. Se schimba doar interfetele, permisiunile, costurile si uneltele la indemana.

Textul este scris intentionat fara diacritice, in romana de zi cu zi. Termenii englezesti raman acolo unde o traducere i-ar face greu de recunoscut in documentatie. Fiecare este explicat la prima aparitie si reluat in glosar. Exemplele de sisteme si rezultatele de test sunt ilustrative: nu sunt rapoarte despre o implementare reala, iar acolo unde ceva este simulare, o spunem. Afirmatiile istorice si tehnice trimit la surse care pot fi verificate, marcate cu [S01](anexe/bibliografie.md#s01), [S02](anexe/bibliografie.md#s02) si asa mai departe, iar lista lor completa se afla la final.

Nu vrem sa prezentam AI-ul ca pe un angajat perfect si nici ca pe un pericol inevitabil. Ne intereseaza ce poate face, ce nu poate dovedi singur si cum construim mecanisme care transforma o demonstratie reusita intr-un proces pe care te poti baza.

Pe langa materialele documentate si citate, in aceasta lucrare au intrat si materiale personale, nepublicate, folosite doar ca parte de context. Pentru ele nu oferim nume sau surse exacte.

## Cum se citeste aceasta carte

Partile se construiesc una peste alta. **Partea I** explica modelul si contextul. **Partea II** aduce informatii externe, instrumente si primele automatizari. **Partea III** construieste arhitectura, pana la orchestrarea mai multor agenti. **Partea IV** arata cum verificam, securizam si operam sistemul. **Partea V** prezinta studii de caz despre proiectarea si evaluarea sistemelor AI, inclusiv rambursari si productie editoriala, si arata cum citim critic exemplele publice. Anexele dau definitii, sabloane si un protocol de evaluare pe care le poti copia.

Poti sari la un capitol, dar ordinea e gandita pentru invatare. Nu are rost sa te ocupi de un protocol nou inainte sa fi inteles ce este o cerere HTTP, nici de un orchestrator inainte sa fi vazut un agent care foloseste o singura unealta.

**Conventii.** Cand spunem *model*, ne referim la componenta care produce predictii sau genereaza continut. *Aplicatia* este produsul care il pune la dispozitie. *Agentul* este o configuratie executabila care urmareste un obiectiv prin actiuni si feedback. Un *sistem agentic* include si infrastructura din jurul agentului. Figurile sunt numerotate in ordinea in care apar (Figura 1 pana la Figura 8), iar fiecare are o legenda sub ea.

**Ce este nou fata de editia 1.2.1.** Modificarile sunt descrise in Anexa E.6; vezi istoricul E.6 pentru provenienta commitului si domeniile afectate.
