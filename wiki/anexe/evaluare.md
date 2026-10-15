# Anexa C. Un protocol de evaluare progresiva si acordare a autonomiei

Aceasta anexa descrie o metoda generica. Nu pretinde ca exista un scor standard de industrie care garanteaza „increderea in AI”. Obiectivul este sa putem spune exact pentru ce sarcini, in ce conditii si cu ce dovezi un sistem a demonstrat un anumit nivel de performanta.

## C.1. Unitatea de evaluare nu este doar modelul

Trebuie sa stabilim ce anume testam: un model izolat, o configuratie de agent cu instrumente sau intregul workflow. Daca schimbam promptul, serviciul de inferenta, biblioteca unei unelte sau sursa documentelor, se poate schimba si rezultatul final. Din acest motiv, un raport de evaluare ar trebui sa noteze versiunile tuturor componentelor relevante.

Putem evalua aceeasi clasa de agenti in mai multe configuratii. Spre exemplu, QA poate utiliza acelasi model cu acces numai de citire sau cu instrumente suplimentare de executie a testelor. Performanta demonstrata intr-o configuratie nu se transfera automat celeilalte.

## C.2. Construieste setul de cazuri inainte de a modifica agentul

Pornim de la cerintele unei activitati. Pentru exemplul meteo, cazurile includ localitate si tara explicite, localitati cu acelasi nume, date lipsa, raspunsuri invalide, conexiune intrerupta si cereri pentru prognoza, nu pentru vremea actuala. Pentru suport, cazurile includ comanda existenta, comanda inexistenta, status contradictoriu si solicitare de rambursare neautorizata.

Setul trebuie sa contina situatii obisnuite, limite, erori de integrare si cazuri care necesita refuz sau escalare. Impartim exemplele intre un set folosit pentru dezvoltare si un set pastrat separat pentru verificarea finala. Daca adaptam agentul dupa fiecare rezultat din setul ascuns, setul nu mai este independent.

Un sistem care trece doar testele pe care le-a vazut poate fi perfect ajustat pentru demonstratie si slab in productie. Pentru a reduce acest risc, includem date noi si perturbari care nu schimba sensul cererii, precum reformulari, ordini diferite ale campurilor sau mici intarzieri la instrumente.

## C.3. Ce masuram si cum evitam cifrele inselatoare

Rata de succes este utila, dar insuficienta. O prezentam impreuna cu numarul executarilor si cu tipurile de eroare. La zece teste, noua reusite inseamna 90%; la o mie de teste, 900 de reusite inseamna tot 90%. Un esantion mai mare poate reduce incertitudinea statistica daca observatiile sunt colectate in conditii adecvate, dar varietatea si reprezentativitatea cazurilor trebuie evaluate separat: ele nu cresc automat odata cu numarul executarilor. Pentru rapoarte serioase putem adauga intervale de incredere si rezultate separate pe categorii.

Indicatori recomandati:

- **Corectitudine:** rezultatul respecta datele si cerintele initiale.
- **Conformitate a actiunilor:** au fost folosite numai instrumente si operatii autorizate.
- **Trasabilitate:** exista dovezi suficiente pentru reconstructia executiei.
- **Recuperare:** intreruperile sunt tratate fara dublarea operatiilor sau pierderea necontrolata a starii.
- **Escalare:** sistemul se opreste sau solicita ajutor atunci cand este necesar.
- **Cost si timp:** numarul de apeluri, durata si resursele consumate.
- **Severitatea defectelor:** separata de numarul simplu al erorilor.

Un agent care a produs 990 de raspunsuri corecte din 1.000, dar a executat o singura plata neautorizata, nu este „99% sigur” pentru tranzactii financiare. Evaluarea riscului necesita reguli de acceptare distincte de media performantelor.

## C.4. Teste normale, teste cu defecte si teste de recuperare

Mai intai verificam traseul obisnuit: date valide, instrumente disponibile, raspuns corect. Apoi simulam defecte. Pentru exemplul meteo, API-ul returneaza `HTTP 503`, timpul de raspuns depaseste limita sau geocodarea gaseste trei localitati. Comportamentul asteptat nu este neaparat un raspuns complet. Poate fi o reluare controlata, o cerere de clarificare sau un mesaj ca datele nu sunt disponibile.

Urmeaza intreruperile: procesul se opreste intre pregatirea si aplicarea unei actiuni, un raspuns de instrument soseste prea tarziu, apare un duplicat de mesaj. Verificam daca reluarea produce acelasi efect permis, nu doua efecte. Acesta este motivul pentru care idempotenta, checkpointurile si jurnalizarea sunt componente de fiabilitate, nu detalii decorative.

Pentru testarea securitatii introducem date de intrare care incearca sa depaseasca limitele: o pagina web care contine instructiuni de a ignora regula de aprobare sau un fisier care cere trimiterea unor date in afara sistemului. Agentul trebuie sa trateze acele texte ca date neautorizate, nu ca ordine superioare. OWASP descrie prompt injection si autonomia excesiva printre riscurile importante ale aplicatiilor LLM [S16].

## C.5. Niveluri de autonomie propuse

| Nivel | Ce poate face | Conditie suplimentara |
|---|---|---|
| 0 — Asistenta | Produce sugestii, fara instrumente care modifica date | Utilizatorul verifica toate livrabilele |
| 1 — Citire | Consulta surse si construieste rapoarte | Loguri si verificari ale surselor |
| 2 — Pregatire | Creeaza ciorne si propuneri reversibile | Validari automate ale formatului |
| 3 — Executie limitata | Modifica date numai in domenii cu risc redus | Teste, permisiuni si monitorizare |
| 4 — Executie extinsa | Gestioneaza mai multe cazuri autorizate | Aprobare pentru exceptii si actiuni sensibile |

Nivelurile sunt doar o schema didactica. Nu reprezinta un standard de certificare. Chiar si la nivelul superior raman limite de acces, oprire de urgenta, jurnalizare si responsabilitate umana asupra sistemului.

De asemenea, un agent poate avea nivel 3 pentru clasificarea tichetelor si nivel 0 pentru operatii financiare. Autonomia este specifica sarcinii si instrumentului, nu un titlu global acordat modelului.

## C.6. Cum tratam un Trust Score

Un scor util poate sintetiza rezultate obtinute in conditii bine precizate. De pilda, o organizatie poate combina corectitudinea, respectarea permisiunilor si recuperarea dupa intreruperi. Ponderile sunt decizii de politica interna, nu adevaruri stiintifice. Trebuie explicat de ce un anumit tip de eroare are greutate mai mare.

Mai sigur decat un singur numar este un mic profil: `corectitudine=...`, `actiuni_neautorizate=...`, `escalare_corecta=...`, `recuperare=...`, `test_cases=...`, `config_version=...`. Pentru un agent de suport, rata de identificare a cazurilor care necesita un om poate cantari mai mult decat stilul raspunsului. Pentru un agent de dezvoltare, testele trecute pe versiunea integrata si absenta defectelor critice pot avea prioritate.

Daca totusi folosim un scor compozit, il prezentam ca instrument de comparatie interna, cu limite si interval de validitate. Nu spunem „agentul este de incredere 94%” fara sa precizam pentru ce tip de activitate, pe ce date si care au fost esecurile.

## C.7. Cine verifica verificatorul?

Un model folosit ca evaluator poate descoperi probleme pe care alt model le-a omis. Insa poate face propriile erori si poate repeta presupunerile celui evaluat. Din acest motiv, incepem cu verificari mecanice acolo unde exista un raspuns exact: scheme, tipuri de date, teste unitare, comparatii cu surse si reguli de permisiune. Evaluarea semantica prin LLM este utila pentru criterii care nu pot fi exprimate usor in cod, dar trebuie calibrata pe exemple evaluate de oameni.

Separarea de rol reduce contaminarea contextului. Agentul QA primeste cerinta si rezultatul, nu doar afirmatia „am terminat, totul e corect”. Daca folosim acelasi model pentru dezvoltare si QA, trebuie sa recunoastem riscul de erori corelate. Pentru sarcini critice putem folosi metode sau evaluatori diferiti, nu numai alte prompturi.

## C.8. Cand repetam evaluarea?

Nu o singura data, la lansare. Reevaluam dupa schimbari relevante de model, prompt, instrument, schema a datelor, sursa RAG sau politica de acces. In plus, periodic introducem cazuri noi din incidentele reale, dar pastram distinctia dintre datele folosite pentru ajustare si cele folosite pentru verificare independenta.

Putem folosi si *shadow mode*: agentul executa procesul in paralel, fara a aplica modificari reale, iar propunerile sunt comparate cu deciziile luate de procedura existenta. Aceasta etapa poate arata erori si costuri neprevazute. Apoi un *pilot cu limite* permite actiuni numai pe un volum restrans si reversibil. Cresterea autonomiei urmeaza rezultatele, nu calendarul comercial al proiectului.

## C.9. Raportul final de evaluare

Un raport scurt, dar util, raspunde la sapte intrebari: ce am testat, pe ce versiune, in ce mediu, cu ce date, ce rezultate am obtinut, ce defecte au ramas si ce actiuni sunt autorizate in continuare. Daca nu exista raspuns verificabil la una dintre ele, marcajul corect este „necunoscut”, nu „probabil bine”.

### Exemplu de raport, complet fictiv

```text
Sistem: clasificare si pregatire raspuns suport
Clasa: Support-Assistant 1.2
Test: 200 cereri, dintre care 40 cazuri limita
Corecte: 184/200
Escalari obligatorii: 35/40 executate corect
Actiuni externe neautorizate: 0 observate in setul testat
Erori importante: 5 escalari ratate, 11 clasificari gresite
Timp median: masurat separat in mediul de test
Decizie: doar ciorne si clasificare, fara trimitere automata
Reevaluare: dupa remedierea esecurilor si pe un set nou
```

Acest raport nu demonstreaza ca rata de eroare din productie va fi identica. Il putem insa folosi pentru o decizie informata: agentul ramane asistiv pana cand sunt remediate erorile considerate inacceptabile.
