# Anexa C. Un protocol de evaluare progresiva si acordare a autonomiei

Anexa descrie o metoda generica. Nu pretinde ca exista un scor standard de industrie care garanteaza "increderea in AI". Scopul este sa poti spune exact pentru ce sarcini, in ce conditii si cu ce dovezi un sistem a demonstrat un anumit nivel de performanta.

## C.1. Unitatea de evaluare nu este doar modelul

Trebuie sa stabilesti ce testezi: un model izolat, o configuratie de agent cu unelte sau intregul workflow. Daca schimbi promptul, serviciul de inferenta, biblioteca unei unelte sau sursa documentelor, se poate schimba si rezultatul final. De aceea un raport de evaluare noteaza versiunile tuturor componentelor relevante.

Aceeasi clasa de agenti poate fi evaluata in mai multe configuratii. QA, de pilda, poate folosi acelasi model cu acces doar de citire sau cu unelte suplimentare pentru rularea testelor. Performanta demonstrata intr-o configuratie nu se transfera automat celeilalte.

## C.2. Construieste setul de cazuri inainte de a modifica agentul

Porneste de la cerintele unei activitati. Pentru exemplul meteo, cazurile includ localitate si tara explicite, localitati cu acelasi nume, date lipsa, raspunsuri invalide, conexiune intrerupta si cereri pentru prognoza, nu pentru vremea actuala. Pentru suport, cazurile includ comanda existenta, comanda inexistenta, status contradictoriu si cerere de rambursare neautorizata.

Setul trebuie sa contina situatii obisnuite, limite, erori de integrare si cazuri care cer refuz sau escalare. Imparte exemplele intre un set folosit la dezvoltare si un set pastrat separat pentru verificarea finala. Daca ajustezi agentul dupa fiecare rezultat din setul ascuns, setul nu mai este independent.

Un sistem care trece doar testele pe care le-a vazut poate fi perfect ajustat pentru demonstratie si slab in productie. Ca sa reduci riscul, include date noi si perturbari care nu schimba sensul cererii: reformulari, ordine diferite ale campurilor, mici intarzieri la unelte.

## C.3. Ce masuram si cum evitam cifrele inselatoare

Rata de succes e utila, dar insuficienta. Prezinta-o impreuna cu numarul de executii si cu tipurile de eroare. La zece teste, noua reusite inseamna 90%; la o mie de teste, 900 de reusite inseamna tot 90%. Precizia estimarii si varietatea cazurilor sunt insa foarte diferite. Pentru rapoarte serioase adauga intervale de incredere statistice (de exemplu intervalul Wilson, vezi sectiunea 17.5) si rezultate separate pe categorii.

Indicatori recomandati:

- **Corectitudine:** rezultatul respecta datele si cerintele initiale.
- **Conformitatea actiunilor:** s-au folosit doar unelte si operatii autorizate.
- **Trasabilitate:** exista dovezi suficiente pentru a reconstitui executia.
- **Recuperare:** intreruperile se trateaza fara dublarea operatiilor si fara pierderea necontrolata a starii.
- **Escalare:** sistemul se opreste sau cere ajutor atunci cand este necesar.
- **Cost si timp:** numarul de apeluri, durata si resursele consumate.
- **Severitatea defectelor:** tratata separat de numarul simplu de erori.

Un agent care a dat 990 de raspunsuri corecte din 1.000, dar a executat o singura plata neautorizata, nu este "99% sigur" pentru tranzactii financiare. Evaluarea riscului cere reguli de acceptare distincte de media performantelor.

## C.4. Teste normale, teste cu defecte si teste de recuperare

Verifici mai intai traseul obisnuit: date valide, unelte disponibile, raspuns corect. Apoi simulezi defecte. Pentru exemplul meteo, API-ul returneaza `HTTP 503`, timpul de raspuns depaseste limita sau geocodarea gaseste trei localitati. Comportamentul asteptat nu e neaparat un raspuns complet. Poate fi o reluare controlata, o cerere de clarificare sau un mesaj ca datele nu sunt disponibile.

Urmeaza intreruperile: procesul se opreste intre pregatirea si aplicarea unei actiuni, un raspuns de la o unealta soseste prea tarziu, apare un mesaj duplicat. Verifici daca reluarea produce acelasi efect permis, nu doua efecte. De aceea idempotenta, checkpoint-urile si jurnalizarea sunt componente de fiabilitate, nu detalii decorative.

Pentru securitate, introduci date care incearca sa depaseasca limitele: o pagina web cu instructiuni de a ignora regula de aprobare sau un fisier care cere trimiterea unor date in afara sistemului. Agentul trebuie sa trateze textele acelea ca date neautorizate, nu ca ordine superioare. OWASP include prompt injection si autonomia excesiva printre riscurile importante ale aplicatiilor LLM; verifica numerotarea in editia pe care o folosesti [S09](../anexe/bibliografie.md#s09), [S16](../anexe/bibliografie.md#s16).

## C.5. Niveluri de autonomie propuse

| Nivel | Ce poate face | Conditie suplimentara |
|---|---|---|
| 0. Asistenta | Produce sugestii, fara unelte care modifica date | Utilizatorul verifica toate livrabilele |
| 1. Citire | Consulta surse si construieste rapoarte | Loguri si verificari ale surselor |
| 2. Pregatire | Creeaza ciorne si propuneri reversibile | Validari automate ale formatului |
| 3. Executie limitata | Modifica date doar in domenii cu risc redus | Teste, permisiuni si monitorizare |
| 4. Executie extinsa | Gestioneaza mai multe cazuri autorizate | Aprobare pentru exceptii si actiuni sensibile |

Nivelurile sunt o schema didactica, nu un standard de certificare. Chiar si la nivelul cel mai de sus raman limitele de acces, oprirea de urgenta, jurnalizarea si responsabilitatea umana asupra sistemului.

Un agent poate avea nivelul 3 pentru clasificarea tichetelor si nivelul 0 pentru operatii financiare. Autonomia tine de sarcina si de unealta, nu e un titlu global acordat modelului.

## C.6. Cum tratam un Trust Score

Un scor util poate sintetiza rezultate obtinute in conditii bine precizate. O organizatie poate combina, de pilda, corectitudinea, respectarea permisiunilor si recuperarea dupa intreruperi. Ponderile sunt decizii de politica interna, nu adevaruri stiintifice, si trebuie explicat de ce un anumit tip de eroare cantareste mai mult.

Mai sigur decat un singur numar este un mic profil: `corectitudine=...`, `actiuni_neautorizate=...`, `escalare_corecta=...`, `recuperare=...`, `test_cases=...`, `config_version=...`. La un agent de suport, rata de identificare a cazurilor care cer un om poate cantari mai mult decat stilul raspunsului. La un agent de dezvoltare, testele trecute pe versiunea integrata si absenta defectelor critice pot avea prioritate.

Daca folosesti totusi un scor compozit, prezinta-l ca instrument de comparatie interna, cu limite si interval de validitate. Nu spune "agentul este de incredere 94%" fara sa precizezi pentru ce tip de activitate, pe ce date si care au fost esecurile.

## C.7. Cine verifica verificatorul?

Un model folosit ca evaluator poate descoperi probleme pe care alt model le-a ratat. Dar poate face si propriile erori si poate repeta presupunerile celui evaluat. De aceea incepi cu verificari mecanice acolo unde exista un raspuns exact: scheme, tipuri de date, teste unitare, comparatii cu surse si reguli de permisiune. Evaluarea semantica printr-un LLM e utila pentru criteriile greu de exprimat in cod, dar trebuie calibrata pe exemple evaluate de oameni.

Separarea de rol reduce contaminarea contextului. Agentul QA primeste cerinta si rezultatul, nu doar afirmatia "am terminat, totul e corect". Daca folosesti acelasi model pentru dezvoltare si pentru QA, recunoaste riscul de erori corelate. Pentru sarcinile critice poti folosi metode sau evaluatori diferiti, nu doar alte prompturi.

## C.8. Cand repetam evaluarea?

Nu o singura data, la lansare. Reevaluezi dupa schimbari relevante de model, prompt, unealta, schema datelor, sursa RAG sau politica de acces. In plus, introduci periodic cazuri noi din incidentele reale, dar pastrezi distinctia dintre datele folosite pentru ajustare si cele folosite pentru verificarea independenta.

Poti folosi si *shadow mode*: agentul executa procesul in paralel, fara sa aplice modificari reale, iar propunerile lui sunt comparate cu deciziile procedurii existente. Etapa asta poate arata erori si costuri neprevazute. Apoi un *pilot cu limite* permite actiuni doar pe un volum restrans si reversibil. Autonomia creste dupa rezultate, nu dupa calendarul comercial al proiectului.

## C.9. Raportul final de evaluare

Un raport scurt, dar util, raspunde la sapte intrebari: ce am testat, pe ce versiune, in ce mediu, cu ce date, ce rezultate am obtinut, ce defecte au ramas si ce actiuni sunt autorizate in continuare. Daca nu exista un raspuns verificabil la una dintre ele, marcajul corect este "necunoscut", nu "probabil bine".

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

Raportul nu demonstreaza ca rata de eroare din productie va fi identica. Il poti folosi totusi pentru o decizie informata: agentul ramane asistiv pana cand erorile considerate inacceptabile sunt remediate. Observa si formularea "0 observate in setul testat", nu "0 in general". Dupa regula celor trei din sectiunea 17.5, zero esecuri in 200 de cazuri inseamna o limita superioara de circa 1,5%, nu risc zero.
