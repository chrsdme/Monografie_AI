# Introducere

**O introducere graduala in modele, context, instrumente, memorie, harness, agenti, orchestrare si evaluare**

*Editia 1.1 | 15 octombrie 2026 | Material educational, fara afiliere comerciala*

> De la primul mesaj intr-un chatbot pana la proiectarea unui sistem in care mai multi specialisti AI colaboreaza, isi verifica rezultatele si primesc autonomie numai atunci cand aceasta poate fi justificata.

## Nota editoriala

Aceasta lucrare nu presupune experienta in programare si nu promoveaza o platforma anume. Cititorul poate utiliza un chatbot intr-un browser, o aplicatie instalata pe calculator, o interfata de linie de comanda sau un sistem construit prin API. Principiile raman aceleasi; difera interfetele, permisiunile, costurile si instrumentele disponibile.

Textul este intentionat scris fara diacritice, intr-o romana accesibila. Termenii englezesti sunt pastrati acolo unde traducerea i-ar face mai greu de recunoscut in documentatie. Termenii centrali sunt explicati la prima utilizare relevanta si reuniti in glosar. Exemplele de sisteme si rezultatele de test sunt ilustrative, nu rapoarte despre o implementare deja executata. Pentru afirmatiile istorice si tehnice exista trimiteri catre surse verificabile; pentru exemplele didactice este indicat ca sunt simulari.

**Nota privind realizarea materialului.** Lucrarea a fost generata integral cu asistenta AI, pornind de la idei, discutii si exemple personale, completate cu documentatie oficiala, lucrari de cercetare si alte surse externe. Continutul a fost revizuit, verificat si adaptat pentru a ramane inteligibil unui public fara experienta tehnica. Folosirea AI nu transforma automat textul sau sursele in dovezi; afirmatiile importante trebuie sa ramana verificabile independent.

**Versiune, erori si contributii.** Editia web, istoricul modificarilor si mecanismul de contributie sunt publice la https://chrsdme.github.io/Monografie_AI/ si https://github.com/chrsdme/Monografie_AI. Corecturile pot fi propuse prin Pull Request sau GitHub Issue. Repository-ul este publicat sub licenta MIT; materialele externe citate isi pastreaza propriile licente si drepturi.

Scopul nu este sa prezentam AI-ul drept un angajat perfect, nici drept un pericol inevitabil. Ne intereseaza ce poate face, ce nu poate demonstra singur si cum construim mecanisme care transforma o demonstratie reusita intr-un proces repetabil.

## Cum se citeste aceasta carte

Partile sunt progresive. **Partea I** explica modelul si contextul. **Partea II** introduce informatii externe, instrumente si primele automatizari. **Partea III** construieste arhitectura, pana la orchestrarea mai multor agenti. **Partea IV** arata cum verificam, securizam si operam sistemul. **Partea V** urmareste doua proiecte principale si doua exemple complementare, de la cerere pana la verificarea rezultatului. Anexele ofera definitii si sabloane reutilizabile.

Cititorul poate sari la un capitol, dar ordinea este gandita pentru invatare. Nu este nevoie sa inteleaga un protocol nou inainte sa fi inteles o cerere HTTP, nici un orchestrator inainte sa fi vazut un agent care foloseste un instrument.

**Conventii:** cand spunem *model* ne referim la componenta care produce predictii sau genereaza continut. Cand spunem *aplicatie* ne referim la produsul care il pune la dispozitie. Pentru *agent* folosim in aceasta lucrare o definitie operationala: o configuratie executabila care urmareste un obiectiv prin actiuni si feedback. Cand spunem *sistem agentic*, includem si infrastructura din jurul agentului.
