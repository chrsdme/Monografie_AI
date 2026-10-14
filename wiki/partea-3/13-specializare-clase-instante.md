# 13. Specializare, clase si instante: impartim munca fara sa o fragmentam

## 13.1. Mai intai definim ce inseamna „clasa”

In aceasta carte, **clasa de agenti** inseamna o categorie de responsabilitati: cercetare, dezvoltare, verificare, operare, suport sau analiza. Este o clasificare arhitecturala pe care o alegem noi; nu inseamna obligatoriu o clasa dintr-un limbaj de programare. O clasa poate contine mai multe configuratii. De exemplu, clasa Development poate cuprinde un specialist Python si unul pentru interfete web.

O **instanta** este o activare concreta a unei configuratii pentru o sarcina: `Developer-D4` modifica schema bazei de date, iar `Developer-D5` lucreaza la notificari. Ambele pot avea acelasi set de reguli de baza, dar fiecare trebuie sa aiba context, identificator, stare si eventual un spatiu de lucru propriu.

## 13.2. De ce nu facem un singur agent pentru orice

Un agent generalist poate fi foarte util pentru sarcini variate. Dar cand are simultan acces la toate instrumentele, la toate fisierele si la istoricul complet al organizatiei, creste suprafata de risc si devine mai greu de inteles ce era autorizat sa faca. O specializare bine aleasa reduce informatia irelevanta si permite evaluarea intr-un domeniu precis.

Totusi, specializarea nu garanteaza performanta. Un agent etichetat „expert in securitate” poate gresi exact ca unul generalist. Beneficiul apare cand rolul este sustinut de instrumente potrivite, permisiuni restranse, date relevante si criterii de verificare distincte.

## 13.3. Studiul unei functii simple

Cerinta: „Transportul este gratuit doar cand valoarea comenzii este **mai mare de** 50 de lire”. Agentul de dezvoltare implementeaza `total >= 50`, apoi isi ruleaza testele pe valori de 30 si 70. Ambele trec. Dar pentru 50, rezultatul este gresit. Acesta este un esec al cazurilor de test, nu neaparat al executiei testelor.

Am putea crea sase agenti: unul scrie functia, unul ruleaza `pytest`, unul citeste logul, altul corecteaza, unul face commit si ultimul redacteaza raportul. Dar ar fi o fragmentare excesiva. Toate aceste operatii pot face parte din responsabilitatea fireasca a agentului de Development. Transferurile intre sase entitati ar creste complexitatea si ar adauga riscul ca o informatie sa se piarda intre ele.

Un **agent QA separat** are sens fiindca indeplineste o alta responsabilitate: verifica implementarea fata de cerinta initiala. Poate construi teste la pragul exact de 50, poate inspecta modificarile si poate refuza acceptarea. Ideal, evaluarea sa porneste din specificatia originala si din dovezile reale, nu numai din afirmatia dezvoltatorului ca totul este gata.

## 13.4. Ce inseamna independenta verificarii

Separarea in doua sesiuni nu produce independenta perfecta. Daca folosim acelasi model si aceleasi presupuneri, evaluatorul poate rata acelasi defect. O evaluare mai puternica adauga **oracole independente**: comparatii numerice implementate in cod, validarea schemelor, testele proiectului, date de referinta si inspectie umana pentru lucrurile greu de masurat automat.

De exemplu, un validator Python poate confirma fara ambiguitate ca pentru `total=50` functia returneaza cost de transport pozitiv. Modelul de QA poate descoperi cazul relevant, dar verdictul numeric il dam prin programul de test.

## 13.5. Specializare utila sau fragmentare excesiva?

Un nou rol se justifica daca schimba **responsabilitatea**, **setul de instrumente**, **nivelul de permisiune** ori **criteriile independente de verificare**. Separarea dintre Development si QA indeplineste de obicei aceste conditii. Separarea dintre „scrie functie” si „ruleaza testele aceleiasi functii” nu le indeplineste automat.

Pentru o aplicatie mare putem avea separat arhitectura, securitatea, infrastructura si conformitatea. Pentru un proiect mic, doua roluri bine definite pot fi suficiente. Numarul optim nu se afla intr-un articol comercial; rezulta din problemele si constrangerile reale ale proiectului.

## 13.6. Clasificarile populare de agenti

Articolul Valorem Reply enumera agenti bazati pe reguli, conversationali, predictivi, colaborativi, adaptivi, RPA si cognitivi [S13]. Este o lista utila pentru discutia despre **moduri de utilizare**, dar nu reprezinta o taxonomie exclusiva. Un agent conversational poate fi si predictiv, iar un proces RPA poate apela un LLM. Un sistem cu reguli fixe poate fi automatizare determinista, chiar daca este numit comercial „agent AI”.

Pentru proiectare, sugeram trei axe separate. **Rolul functional:** cercetare, implementare, suport. **Capabilitatea:** conversatie, predictie, cautare, actiune, colaborare. **Autonomia:** recomanda, pregateste, executa in sandbox, executa cu aprobare, executa in limite prestabilite. Aceasta descriere evita sa confundam o categorie de marketing cu o proprietate tehnica.

## 13.7. Exemplu cu trei clase si douazeci de instante

Putem defini clasele Research, Development si QA. Intr-un workflow, orchestratorul poate porni 2 instante Research, 14 Development si 4 QA. Rezulta **3 clase** si **20 de instante**, nu 20 de modele diferite. Instantele pot utiliza unul sau mai multe modele partajate. Pot fi executate in paralel numai in masura in care sarcinile si resursele o permit.

Aceasta distinctie are valoare economica si operationala: actualizarile unei configuratii comune pot influenta executarile viitoare ale acelei clase, iar rezultatele se pot analiza per responsabilitate. In acelasi timp, fiecare instanta are propria identitate in jurnal, pentru ca un esec concret sa poata fi reconstituit.
