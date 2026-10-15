# Anexa B. Sabloane neutre: cum documentam sarcina, agentul si verificarile

Aceste sabloane nu apartin unui produs. Sunt propuneri de documentare, cu campuri care pot fi pastrate intr-un fisier Markdown, intr-un tabel ori intr-o aplicatie de proiect. Nu toate campurile trebuie folosite pentru un exercitiu simplu; incepem cu esentialul si adaugam detaliile justificate de risc.

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

**Exemplu completat.** O firma doreste un raport saptamanal de suport. Scopul este sa identifice primele cinci categorii de probleme si cererile ramase nerezolvate. Datele provin din exportul oficial al tichetelor. Sunt permise citirea CSV-ului, filtrarea si agregarea. Este interzisa modificarea starii tichetelor. Rezultatul trebuie sa contina un tabel cu numarul solicitarilor pe categorii si o explicatie de maximum o pagina. Acceptarea se face numai daca totalul din tabel este egal cu numarul tichetelor din perioada aleasa si daca toate exemplele citate pot fi regasite in fisierul sursa.

Acest brief poate fi folosit intr-un chatbot obisnuit, fara niciun agent autonom.

## B.2. Fisa unei clase de agenti

```text
Clasa: Research / Development / QA / Alta
Responsabilitate: ce rezolva si ce NU rezolva
Intrari necesare: specificatii, documente, versiuni
Instrumente permise: citire / scriere / executie / retea
Instrumente explicit interzise:
Tipuri de date autorizate:
Forma obligatorie a rezultatului:
Dovezi cerute pentru ACCEPTAT:
Conditii pentru ESCALARE:
Conditii pentru OPRIRE:
Limite: timp, apeluri, buget, incercari
Regula de pastrare a jurnalului:
Proprietarul configuratiei si versiunea:
```

O astfel de fisa nu este un simplu personaj imaginat intr-un prompt. Ea devine utila numai daca instrumentele si permisiunile sunt aplicate in mediul de executie. Pentru un agent QA, o regula de tip „nu modifica productia” este slaba daca i-am oferit totusi credentiale de administrator pentru productie.

## B.3. Contract pentru transferul dintre doua etape

Sa presupunem ca Research trebuie sa predea rezultatul catre Development. Evitam transferul unui istoric lung de conversatii si folosim un document scurt, verificabil:

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

Acest contract trebuie sa fie suficient pentru ca noul agent sa poata incepe, dar nu trebuie sa contina toate ipotezele si toate mesajele celui anterior. Cand lipseste un element esential, etapa este `BLOCKED`; nu se inventeaza detaliul pentru a pastra aparentele de progres.

## B.4. Contract minimal pentru un instrument

Un instrument care modifica date trebuie sa aiba un comportament mai precis decat „actualizeaza comanda”. Un exemplu generic ar putea fi:

```text
Operatie: prepare_order_update
Intrari: order_id, requested_field, new_value
Permisiune: citire si pregatire, fara aplicare
Validari: comanda exista; campul este permis; noua valoare este valida
Rezultat: proposed_change_id, current_value, proposed_value
Erori: NOT_FOUND, INVALID_FIELD, INVALID_VALUE, ACCESS_DENIED
Efecte secundare: salveaza o propunere interna; nu modifica datele comenzii si nu declanseaza actiuni externe
Urmatorul pas: aprobare separata inainte de apply
```

Separand `prepare` de `apply` putem crea o etapa naturala de verificare. Pentru operatii care nu se pot repeta in siguranta, folosim si identificatori unici ai cererii, astfel incat o reincercare sa nu produca plata sau comanda de doua ori.

## B.5. O inregistrare de executie pe care o putem audita

```text
run_id: 2026-10-13-00042
agent_class: QA
agent_config_version: 1.3
model_identifier: model/version, daca disponibil
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

Nu orice jurnal trebuie sa pastreze integral continutul sensibil al documentelor. Putem pastra referinte, hash-uri, metadate si rezultate de verificare, iar continutul brut numai daca politica de securitate si necesitatea auditului il justifica. Cu cat sistemul interactioneaza cu mai multe aplicatii, cu atat devine mai importanta corelarea prin `run_id`.

## B.6. Definitia de finalizare: ce inseamna „gata”

O sarcina de implementare poate fi declarata finalizata numai cand exista un rezultat identificabil si criteriile obligatorii au trecut. Exemplu: codul se compileaza, testele relevante trec, modificarile au fost inspectate, varianta finala este versionata si limitarile cunoscute sunt consemnate. Daca testul nu a putut fi rulat, statusul trebuie sa fie „neverificat”, nu „PASS”. Daca verificarea fizica este necesara si nu s-a produs, build-ul reusit nu o inlocuieste.

Pentru o analiza, definitia de finalizare poate fi diferita: exista surse, datele sunt actuale, calculele se pot reproduce si incertitudinile sunt identificate. Pentru un raspuns de suport, este necesara o verificare a datelor despre client si a politicii aplicabile.

**Principiul comun:** o declaratie de succes nu este un substitut pentru dovada ceruta de sarcina.

## B.7. O fisa scurta pentru selectarea primului workflow

| Criteriu | Intrebare practica | Rezultat |
|---|---|---|
| Repetitie | Apare problema suficient de des? | Da / Nu |
| Intrari | Putem obtine datele necesare legal si fiabil? | Da / Nu |
| Criterii | Putem recunoaste un rezultat gresit? | Da / Nu |
| Riscuri | Ce se intampla cand sistemul greseste? | Mic / Mediu / Mare |
| Reversibilitate | Putem anula efectul unei actiuni? | Da / Partial / Nu |
| Beneficiu | Exista timp ori cost masurat initial? | Da / Nu |

Daca lipsesc datele sau metoda de verificare, nu fortam introducerea unui agent. Simplificam sarcina ori lucram mai intai la infrastructura informationala. Din ghidurile de automatizare pentru companii retinem analiza procesului si definirea obiectivelor, nu obligatia de a cumpara o anumita platforma [S19, S23].
