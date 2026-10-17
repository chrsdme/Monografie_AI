# Anexa B. Sabloane neutre: cum documentam sarcina, agentul si verificarile

Sabloanele de mai jos nu apartin niciunui produs. Sunt propuneri de documentare, cu campuri pe care le poti pastra intr-un fisier Markdown, intr-un tabel sau intr-o aplicatie de proiect. Nu trebuie sa completezi toate campurile pentru un exercitiu simplu. Incepi cu esentialul si adaugi detalii cand riscul le justifica.

## B.1. Brief pentru o sarcina asistata de AI

```text
Numele sarcinii:
Scopul concret:
Cine foloseste rezultatul:
Date sau documente disponibile:
Ce informatii NU sunt disponibile:
Operatii permise:
Operatii interzise:
Formatul rezultatului:
Criterii de acceptare:
Exemple de eroare:
Cine aproba:
```

**Exemplu completat.** O firma vrea un raport saptamanal de suport. Scopul este sa identifice primele cinci categorii de probleme si cererile ramase nerezolvate. Datele vin din exportul oficial al tichetelor. Sunt permise citirea CSV-ului, filtrarea si agregarea. Este interzisa modificarea starii tichetelor. Rezultatul trebuie sa contina un tabel cu numarul solicitarilor pe categorii si o explicatie de cel mult o pagina. Raportul se accepta doar daca totalul din tabel este egal cu numarul tichetelor din perioada aleasa si daca toate exemplele citate se regasesc in fisierul sursa.

Un brief ca acesta poate fi folosit intr-un chatbot obisnuit, fara niciun agent autonom.

## B.2. Fisa unei clase de agenti

```text
Clasa: Research / Development / QA / Alta
Responsabilitate: ce rezolva si ce NU rezolva
Intrari necesare: specificatii, documente, versiuni
Unelte permise: citire / scriere / executie / retea
Unelte explicit interzise:
Tipuri de date autorizate:
Forma obligatorie a rezultatului:
Dovezi cerute pentru ACCEPTAT:
Conditii pentru ESCALARE:
Conditii pentru OPRIRE:
Limite: timp, apeluri, buget, incercari
Regula de pastrare a jurnalului:
Proprietarul configuratiei si versiunea:
```

O astfel de fisa nu e un simplu personaj imaginat intr-un prompt. Devine utila doar daca uneltele si permisiunile sunt aplicate in mediul de executie. La un agent QA, o regula de tipul "nu modifica productia" e slaba daca i-ai dat totusi credentiale de administrator pentru productie.

## B.3. Contract pentru transferul dintre doua etape

Sa presupunem ca Research trebuie sa predea rezultatul catre Development. Evita transferul unui istoric lung de conversatii si foloseste un document scurt, verificabil:

```text
run_id: proiect-041
predare: Research -> Development
specificatie_aprobata: SPEC-12, revizia 3
cerinte_obligatorii: [C1, C2, C3]
decizii_confirmate: [D1, D2]
probleme_deschise: [P4]
linkuri_surse: [URL sau identificatori de fisiere]
artefacte: [calea / identificatorul documentelor]
criterii_de_acceptare: [T1, T2, T3]
stare: READY sau BLOCKED
```

Contractul trebuie sa fie suficient ca noul agent sa poata incepe, dar nu sa contina toate ipotezele si toate mesajele celui dinainte. Cand lipseste un element esential, etapa este `BLOCKED`. Nu inventezi detaliul ca sa pastrezi aparenta de progres.

## B.4. Contract minimal pentru o unealta

O unealta care modifica date are nevoie de un comportament mai precis decat "actualizeaza comanda". Un exemplu generic:

```text
Operatie: prepare_order_update
Intrari: order_id, requested_field, new_value
Permisiune: citire si pregatire, fara aplicare
Validari: comanda exista; campul este permis; noua valoare este valida
Rezultat: proposed_change_id, current_value, proposed_value
Erori: NOT_FOUND, INVALID_FIELD, INVALID_VALUE, ACCESS_DENIED
Efecte secundare: niciunul
Urmatorul pas: aprobare separata inainte de apply
```

Daca separi `prepare` de `apply`, creezi o etapa naturala de verificare. Pentru operatiile care nu se pot repeta in siguranta, foloseste si identificatori unici ai cererii, ca o reincercare sa nu produca plata sau comanda de doua ori.

## B.5. O inregistrare de executie pe care o putem audita

```text
run_id: 2026-10-13-00042
agent_class: QA
agent_config_version: 1.3
model_identifier: model/version, daca este disponibil
request_id: ticket-122
input_reference: cerere-122-rev2
context_sources: [spec-122, policy-returns-rev5]
tool_calls: [nume, argumente validate, moment]
tool_results: [status, identificator, verificari]
output_artifact: review-122.md
independent_checks: [check-schema PASS, check-total PASS]
final_status: ACCEPTED / REJECTED / ESCALATED
owner_approval: required / not_required / approved
```

Nu orice jurnal trebuie sa pastreze integral continutul sensibil al documentelor. Poti pastra referinte, hash-uri, metadate si rezultate de verificare, iar continutul brut doar daca politica de securitate si nevoia de audit il justifica. Cu cat sistemul vorbeste cu mai multe aplicatii, cu atat conteaza mai mult corelarea prin `run_id`.

## B.6. Definitia de finalizare: ce inseamna "gata"

O sarcina de implementare se declara terminata doar cand exista un rezultat identificabil si criteriile obligatorii au trecut. Exemplu: codul compileaza, testele relevante trec, modificarile au fost inspectate, versiunea finala este versionata si limitarile cunoscute sunt consemnate. Daca testul nu a putut fi rulat, statusul este "neverificat", nu "PASS". Daca era nevoie de o verificare fizica si ea nu s-a facut, un build reusit nu o inlocuieste.

Pentru o analiza, definitia poate fi alta: exista surse, datele sunt actuale, calculele se pot reproduce si incertitudinile sunt identificate. Pentru un raspuns de suport, trebuie verificate datele despre client si politica aplicabila.

**Principiul comun:** o declaratie de succes nu inlocuieste dovada pe care o cere sarcina.

## B.7. O fisa scurta pentru alegerea primului workflow

| Criteriu | Intrebare practica | Rezultat |
|---|---|---|
| Repetitie | Apare problema suficient de des? | Da / Nu |
| Intrari | Putem obtine datele necesare legal si fiabil? | Da / Nu |
| Criterii | Putem recunoaste un rezultat gresit? | Da / Nu |
| Riscuri | Ce se intampla cand sistemul greseste? | Mic / Mediu / Mare |
| Reversibilitate | Putem anula efectul unei actiuni? | Da / Partial / Nu |
| Beneficiu | Exista timp sau cost masurat initial? | Da / Nu |

Daca lipsesc datele sau metoda de verificare, nu forta introducerea unui agent. Simplifica sarcina sau lucreaza intai la infrastructura informationala. Din ghidurile de automatizare pentru companii retinem analiza procesului si definirea obiectivelor, nu obligatia de a cumpara o anumita platforma [S19](../anexe/bibliografie.md#s19), [S23](../anexe/bibliografie.md#s23).


## B.8. Specificatie de intentie: de la obiectiv la verificare

Un *Intent Spec* este un artefact de documentare, nu o functie standard a unui model. Exemplul de mai jos completeaza [studiul 21.7 despre rambursari](https://chrsdme.github.io/Monografie_AI/partea-5/21-studii-de-caz/#217-studiul-de-caz-e-acelasi-retur-prin-trei-arhitecturi); aceleasi intrebari sunt utile pentru [cei doi agenti YouTube din 21.8](https://chrsdme.github.io/Monografie_AI/partea-5/21-studii-de-caz/#218-studiul-de-caz-f-cercetare-youtube-si-productie-editoriala-cu-doi-agenti). Explicatia conceptului este in [sectiunea 6.7](https://chrsdme.github.io/Monografie_AI/partea-2/06-prompturi-instructiuni-briefuri/#67-intent-engineering-de-la-cerere-la-obiectiv-verificabil).

```yaml
intent_id: refund_resolution_v1
status: exemplu_didactic
problem: "Solicitarile trebuie solutionate corect si consecvent."
evidence: "Comanda, politica magazinului si verificari in sistem."
objective: "Rezolva cererile eligibile, fara plati duplicate sau neautorizate."
success_criteria:
  - final_state_verified_or_escalated
  - no_duplicate_refund
  - customer_notified_only_after_confirmation
constraints:
  currency: RON
  auto_refund_limit: 100
  require_verified_customer: true
priorities: [authorisation, correctness, speed]
human_approval_when: [amount_above_limit, unclear_eligibility]
stop_when: [verified_outcome, waiting_for_customer, human_escalation, budget_limit]
verification: [test_62_ron, test_350_ron, test_duplicate_refund]
owner: support_operations
```

**Interpretare:** pentru 62 RON verificam eligibilitatea si confirmarea operatiei; pentru 350 RON verificam escalarea fara plata. Pentru YouTube am inlocui limita financiara cu sursele permise, verificarea originalitatii si aprobarea versiunii exacte a videoclipului.

**Limita:** YAML-ul este ilustrativ, nu este format oficial si nu este citit automat de simulatorul din Capitolul 21. Campurile nu impun singure permisiuni, nu efectueaza tranzactii si nu verifica rezultate; aplicatia trebuie sa implementeze controalele si testele.
