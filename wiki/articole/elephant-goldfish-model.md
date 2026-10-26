# Elephant-Goldfish Model: de ce un agent cu memorie are nevoie de evaluatori fara istoric

*Publicat: 26 octombrie 2026 | Autor: chrsdme | Tema: agenti AI, proiectare software, verificare*

> **Ideea centrala:** un agent AI care cunoaste proiectul poate crea o specificatie buna, dar nu ar trebui sa fie singurul care o evalueaza. Separarea deliberata intre proiectare si critica poate descoperi probleme inainte de scrierea codului.

Pe 22 octombrie 2026, Google a prezentat public **Elephant-Goldfish Model (EGM)**, o metoda open-source de dezvoltare software bazata pe specificatii (*Spec-Driven Development*, SDD). Google afirma ca metoda este folosita intern de mii de ingineri. Aceasta cifra este o afirmatie a autorilor proiectului, nu o evaluare independenta [S45].

Ce aduce nou? Nu un model lingvistic mai mare, ci un proces in care contextul si evaluarea critica sunt administrate separat.

## 1. Problema: AI poate implementa foarte repede o idee prost definita

Un flux uzual este: cerinta -> cod generat -> test -> corectie -> cod nou. Poate functiona excelent pentru o schimbare simpla. In proiectele complexe, insa, un agent poate implementa coerent o interpretare gresita a cerintei.

Riscurile apar cand regulile raman numai in discutii, cand acelasi agent isi confirma propriile presupuneri si cand documentatia nu mai reflecta modificarile facute ulterior. Trecerea unui set de teste nu demonstreaza, singura, ca obiectivul utilizatorului a fost inteles corect.

EGM muta o parte a criticii inainte de implementare. Nu promite eliminarea defectelor. Incearca sa reduca numarul deciziilor luate prin presupunere [S45], [S47].

## 2. Trei roluri diferite

### Elephant: agentul care construieste intelegerea

**Elephant** este o sesiune AI cu acces la contextul relevant: baza de cod (*codebase*), arhitectura, documentatie, reguli, obiective si decizii anterioare. Pune intrebari, analizeaza alternative si redacteaza proiectarea. In etapa de design respecta regula **nu scrie codul functionalitatii**. Poate, in schimb, inspecta codul existent pentru a intelege constrangerile [S45], [S46].

### Goldfish: evaluatorul fara istoricul conversatiei

**Goldfish** porneste intr-o sesiune izolata. Nu primeste automat istoricul discutiilor dintre utilizator si Elephant; primeste specificatia, instructiunile de evaluare si, acolo unde este relevant, codul sau alte dovezi autorizate.

Aici, *zero-context* nu inseamna lipsa tuturor informatiilor. Inseamna lipsa contextului conversational care i-ar putea permite sa completeze tacit explicatiile inexistente in document. Daca specificatia este ambigua, evaluatorul trebuie sa semnaleze acest lucru, nu sa presupuna ce ar fi dorit autorul [S46].

### Omul: responsabil pentru deciziile finale

Dezvoltatorul accepta sau respinge constatarile, decide compromisurile si aproba implementarea. O critica produsa de AI nu este automat corecta. Agentii pot rata defecte, pot produce false alarme si pot impartasi aceleasi erori de rationament.

## 3. Cum se desfasoara fluxul de lucru

Metoda are trei faze centrale. Repository-ul oficial include si unelte auxiliare [S46], [S47].

| Etapa | Scop | Rezultat |
| --- | --- | --- |
| **Bootstrap** (optional) | Cartografiaza codul existent si regulile proiectului | Documentatie despre componente si dependinte |
| **Brainstorm** | Clarifica problema, limitele si alternativele | *Concept brief*, un rezumat al intentiei si al cerintelor |
| **Draft** | Transforma conceptul intr-o specificatie tehnica | Document de design cu arhitectura, interfete, alternative, criterii de acceptare |
| **Review** | Testeaza critic specificatia in sesiuni izolate | Constatari clasificate si decizii de corectare |
| **Implementare** | Construieste pe baza specificatiei aprobate | Cod si teste care necesita verificare reala |
| **Drift Report** (optional, ulterior) | Compara documentatia cu codul actual | Posibile abateri de analizat |

Comenzile principale documentate sunt `/egm-brainstorm`, `/egm-draft`, `/egm-review`, iar cele suplimentare includ `/egm-bootstrap` si `/egm-drift-report`. Sintaxa exacta poate diferi intre mediile de executie [S46].

### Goldfish Protocol: trei verificari distincte

**Comprehension Check.** Un agent fara istoricul discutiei explica designul in propriile cuvinte. Daca nu poate descrie corect scopul, fluxurile si dependintele, documentul poate avea lacune.

**Antagonistic Review.** Un grup de evaluatori cauta activ greseli logice, situatii limita, dependinte ascunse si alternative mai simple. Obiectivul nu este aprobarea automata.

**Implementation Readiness Check.** Un evaluator verifica daca implementatorul are informatiile concrete necesare: fisiere, interfete, structuri de date, comportamente la eroare, criterii de acceptare si teste [S45].

Constatarile se intorc la autorul specificatiei. Acesta le corecteaza sau le respinge motivat. Pentru o problema simpla, metoda poate fi aplicata partial, fara toate etapele.

## 4. Exemplu: rezervarile online

Cerinta initiala suna usor: „Utilizatorul selecteaza un loc, plateste si primeste confirmarea”.

Un agent grabit poate genera imediat pagina si API-ul. Un proces orientat spre specificatii ar trebui sa clarifice mai intai:

- Ce se intampla daca doi clienti selecteaza simultan acelasi loc?
- Cat timp este retinut un loc inainte de confirmarea platii?
- Ce se intampla daca plata este acceptata, dar serverul pierde raspunsul?
- Cum prevenim rezervarile sau incasarile duplicate la reincercarea cererii?
- Cine reconciliaza o tranzactie aflata intr-o stare neclara?

Din aceste intrebari pot rezulta reguli testabile: rezervari fara conflicte, operatii idempotente, expirarea blocarilor temporare si reconciliere dupa erori. Acestea sunt **exemple ilustrative create pentru articol**, nu rezultate ale unui experiment EGM.

Beneficiul practic nu este numarul de observatii gasite de un agent. Este transformarea observatiilor justificate in decizii si teste verificabile.

## 5. Cum aplici ideea fara sa instalezi un plugin

Principiile pot fi reproduse cu doua sesiuni AI separate.

**Sesiunea A, proiectare.** Ofera contextul proiectului, clarifica obiectivele, listeaza constrangerile, alternativele si scenariile de esec. Rezultatul trebuie sa fie un document de specificatie, nu doar un rezumat al conversatiei.

**Sesiunea B, evaluare.** Deschide o sesiune noua. Furnizeaza doar documentul final, regulile de audit si dovezile necesare. Solicita trei verificari: explicarea designului, cautarea adversariala a defectelor si evaluarea pregatirii pentru implementare.

Pentru fiecare constatare cere: pasajul afectat, motivul, consecinta posibila, severitatea si corectia propusa. Intoarce constatarile la sesiunea de proiectare si modifica specificatia doar dupa analiza.

Separarea conversatiilor reduce o sursa de contaminare a review-ului; **nu garanteaza independenta cognitiva** intre modele sau corectitudinea evaluatorilor. Testarea si revizuirea umana raman obligatorii.

## 6. Plugin oficial si medii de dezvoltare

Repository-ul [S46] documenteaza integrarea cu mai multe medii, printre care Claude Code si OpenAI Codex.

Pentru Claude Code sunt indicate comenzile:

```text
claude plugin marketplace add google/elephant-goldfish-model
claude plugin install egm@egm
```

Pentru Codex:

```text
codex plugin marketplace add google/elephant-goldfish-model
codex plugin add egm@egm
```

Acestea sunt comenzile din documentatia consultata la 26 octombrie 2026. Functionarea lor depinde de versiunea si configuratia programului folosit. Repository-ul este disponibil sub **Apache 2.0**, dar precizeaza explicit ca nu este un produs Google cu suport oficial [S46].

Nu instala automat unelte sau scripturi in proiecte importante fara sa inspectezi ce fisiere modifica si ce permisiuni solicita.

## 7. Aceeasi metafora, alta problema: memoria agentilor

Expresiile „elefant” si „pestisor de aur” sunt folosite si pentru a compara agentii care pastreaza stare cu cei fara memorie persistenta. **Acest subiect este diferit de EGM.**

In EGM, lipsa istoricului este o proprietate intentionata a evaluatorului.

In arhitectura memoriei agentilor, obiectivul este sa putem pastra si recupera informatii corecte intre sesiuni: fapte, decizii, evenimente, reguli si relatii. Un model nu obtine automat memorie persistenta doar pentru ca a primit un prompt lung.

Putem distinge trei categorii utile:

- **Memorie episodica:** ce s-a intamplat si cand, de exemplu o decizie luata intr-o sedinta.
- **Memorie semantica:** fapte, entitati si relatii consolidate.
- **Memorie procedurala:** reguli, proceduri si pasi reutilizabili.

O cautare vectoriala poate recupera fragmente apropiate semantic, folosind *embeddinguri*. Un **graf de cunostinte** poate reprezenta explicit legaturi intre persoane, proiecte, decizii si surse. Cele doua tehnici pot fi complementare, nu trebuie privite ca alternative exclusive [S26], [S48], [S49].

### De ce conteaza timpul

O informatie poate fi corecta in martie si depasita in octombrie. Memoria durabila are nevoie nu doar de relatie, ci si de **validitate temporala**: de cand pana cand era adevarata acea relatie si cand a aflat sistemul despre ea.

Lucrarea despre Zep si Graphiti prezinta o arhitectura de graf temporal pentru memoria agentilor. Rezultatele de performanta raportate de autori nu trebuie confundate cu o certificare independenta a tuturor aplicatiilor [S48].

EGM si memoria persistenta se pot combina: Elephant poate consulta o baza de cunostinte durabila, in timp ce Goldfish primeste doar specificatia si dovezile permise. Aceasta este o **posibilitate arhitecturala**, nu o cerinta obligatorie a pluginului.

## 8. Unde ajuta si unde complica lucrurile

**Poate ajuta** la modificari de arhitectura, migrari de date, integrarea mai multor servicii, autentificare, plati sau functionalitati cu efecte dificil de inversat. Clarificarea cerintelor si evaluarea separata pot reduce riscul de a implementa intentii intelese gresit.

**Poate fi excesiv** pentru o corectie locala si bine delimitata. Fiecare sesiune adauga cost, timp si constatari care trebuie evaluate. Un Goldfish poate produce false pozitive, iar mai multi evaluatori pot repeta aceeasi eroare. Documentatia poate deveni inutil de lunga.

Ghidul Google recomanda explicit folosirea selectiva a abilitatilor si evita impunerea intregului proces pentru un bug simplu [S47].

## 9. Recomandari practice

Porneste cu un document mic: obiectiv, limite, dependinte, scenarii critice, cazuri limita si criterii de acceptare. Ofera-l unui evaluator separat. Pastreaza doar observatiile cu dovezi si consecinte explicite.

Daca proiectul este complex, poti adauga fazele oficiale de brainstorm, draft, review si verificare a derivei. Daca este simplu, un singur review bine formulat poate fi suficient.

**Principiul care merita retinut:** informatiile trebuie pastrate cand ajuta continuitatea proiectului si izolate cand ar influenta nejustificat verificarea. Nici memoria, nici numarul de agenti nu inlocuiesc testele reale sau judecata dezvoltatorului.

## 10. Surse si lecturi conexe

Sursele complete sunt in [bibliografia monografiei](../anexe/bibliografie.md). Pentru acest articol:

- [S45] [Anuntul oficial Google, 22 octombrie 2026](../anexe/bibliografie.md#s45).
- [S46] [Repository-ul EGM, licenta si instructiuni](../anexe/bibliografie.md#s46).
- [S47] [Ghidul de utilizare EGM](../anexe/bibliografie.md#s47).
- [S48] [Rasmussen et al., Zep si grafurile temporale](../anexe/bibliografie.md#s48).
- [S49] [Bechberger, prezentare despre memoria pe termen lung](../anexe/bibliografie.md#s49).
- [S26] [Edge et al., GraphRAG](../anexe/bibliografie.md#s26).

Pentru conceptele introduse aici, consulta [dictionarul de termeni](../anexe/glosar.md), precum si capitolele despre [context](../partea-1/04-context.md), [RAG si memorie](../partea-2/08-rag-memorie-cunostinte.md), [orchestrare](../partea-3/14-orchestrare.md) si [evaluarea agentilor](../partea-4/17-evaluare-trust-score.md).

*Nota metodologica: afirmatia Google despre utilizarea interna este atribuita sursei primare; acest articol nu prezinta benchmark-uri proprii si nu considera rezultatele unor videoclipuri demonstrative drept dovezi independente.*
