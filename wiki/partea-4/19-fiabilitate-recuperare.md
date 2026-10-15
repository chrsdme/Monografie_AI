# 19. Fiabilitate si recuperare: un sistem bun trebuie sa stie si sa esueze

## 19.1. Succesul nu este singura stare posibila

Un workflow real intalneste servicii indisponibile, documente corupte, permisiuni expirate si cereri incomplete. Arhitectura trebuie sa stabileasca ce face in aceste situatii. Un agent care inventeaza ca operatia a reusit pentru a putea continua este mai problematic decat unul care raporteaza clar o eroare.

**Timeout** inseamna ca o operatie a depasit intervalul asteptat. **Retry** inseamna reluarea ei. **Backoff** introduce pauze crescatoare intre incercari. Aceste mecanisme sunt utile, dar trebuie aplicate in functie de efectele operatiei. Nu orice esec se repara prin repetare.

## 19.2. Idempotenta: de ce conteaza enorm

Daca un instrument de citire a vremii este apelat de doua ori, costul poate creste, dar efectul extern este redus. Daca o functie de transfer financiar este apelata de doua ori, putem avea doua plati. **Idempotenta** este proprietatea prin care repetarea aceleiasi cereri nu produce efecte suplimentare nedorite. O tehnica este utilizarea unui identificator unic de operatie, verificat de serviciul care aplica modificarea. Acelasi identificator trebuie reutilizat la reincercarea aceleiasi operatii; generarea unui identificator nou la fiecare retry nu previne dublarea. Garantia depinde si de modul in care serviciul pastreaza si verifica aceste chei.

Daca starea unei operatii sensibile este necunoscuta dupa un timeout, procesul trebuie sa interogheze mai intai sistemul pentru a vedea daca efectul exista deja. Reincercarea oarba este periculoasa.

## 19.3. Checkpoint si reluare

Un **checkpoint** este un punct in care starea necesara continuarii este salvata. De exemplu, dupa procesarea primelor 200 de documente din 1.000, sistemul poate salva identificatorii celor procesate si rezultatele validate. La o intrerupere, reia de la pasul urmator, fara sa repete operatiile deja confirmate. Checkpoint-ul trebuie asociat cu versiunea datelor si a procesului; altfel, o schimbare intre doua rulari poate invalida reluarea.

## 19.4. Rollback si actiuni compensatorii

**Rollback** inseamna revenirea la o stare anterioara. Pentru codul software putem utiliza controlul versiunilor si un mecanism de deploy care repune ultima versiune stabila. Pentru o factura trimisa sau un email expediat, revenirea completa poate fi imposibila. Uneori se poate efectua o operatie compensatorie, precum anularea unei rezervari, dar nu toate efectele pot fi sterse. Din acest motiv, prevenirea este mai importanta decat promisiunea de rollback.

## 19.5. Detectarea buclelor fara progres

Un agent poate apela acelasi instrument de mai multe ori, fara sa obtina informatie noua. Un harness bine proiectat poate identifica repetarea argumentelor, lipsa schimbarii de stare si depasirea unui buget. Sistemul trebuie sa se opreasca si sa raporteze blocajul. O bucla mai lunga nu inseamna automat o bucla mai inteligenta.

## 19.6. Schimbari de model, prompt si instrument

O actualizare aparent minora poate schimba felul in care agentul apeleaza o functie sau interpreteaza un mesaj de eroare. Pentru fluxurile importante, configuratiile trebuie versionate si testele de regresie reluate. Nu este suficient sa verificam numai daca noul model raspunde mai frumos. Trebuie sa verificam daca respecta acelasi contract operational.
