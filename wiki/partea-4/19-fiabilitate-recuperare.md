# 19. Fiabilitate si recuperare: un sistem bun trebuie sa stie si sa esueze

## 19.1. Succesul nu e singura stare posibila

Un workflow real intalneste servicii indisponibile, documente corupte, permisiuni expirate si cereri incomplete. Arhitectura trebuie sa stabileasca ce face in astfel de situatii. Un agent care pretinde ca operatia a reusit, ca sa poata continua, e mai problematic decat unul care raporteaza limpede o eroare.

**Timeout** inseamna ca o operatie a depasit intervalul asteptat. **Retry** inseamna reluarea ei. **Backoff** introduce pauze tot mai lungi intre incercari. Mecanismele sunt utile, dar se aplica in functie de efectele operatiei. Nu orice esec se repara prin repetare.

## 19.2. Idempotenta: de ce conteaza enorm

Daca o unealta care citeste vremea e apelata de doua ori, costul poate creste, dar efectul extern e mic. Daca o functie de transfer financiar e apelata de doua ori, poti avea doua plati. **Idempotenta** este proprietatea prin care repetarea aceleiasi cereri nu produce efecte suplimentare nedorite. O tehnica este un identificator unic al operatiei, verificat de serviciul care aplica modificarea.

Daca starea unei operatii sensibile e necunoscuta dupa un timeout, procesul interogheaza intai sistemul, ca sa vada daca efectul exista deja. Reincercarea oarba e periculoasa.

## 19.3. Checkpoint si reluare

Un **checkpoint** este un punct in care se salveaza starea necesara continuarii. De exemplu, dupa procesarea primelor 200 de documente din 1.000, sistemul poate salva identificatorii celor procesate si rezultatele validate. La o intrerupere reia de la pasul urmator, fara sa repete operatiile deja confirmate. Checkpoint-ul se leaga de versiunea datelor si a procesului; altfel, o schimbare intre doua rulari poate invalida reluarea.

Un detaliu de implementare care loveste din senin: in LangGraph, cand un nod se intrerupe pentru aprobare si apoi este reluat, nodul reporneste de la inceputul lui, nu din punctul exact al intreruperii. Efectele secundare dinaintea intreruperii trebuie sa fie idempotente, altfel se pot repeta [S29](../anexe/bibliografie.md#s29). Regula e valabila mai larg: cand reiei un pas, presupune ca partea dinainte se va executa din nou.

## 19.4. Rollback si actiuni compensatorii

**Rollback** inseamna revenirea la o stare anterioara. Pentru codul software poti folosi controlul versiunilor si un mecanism de deploy care repune ultima versiune stabila. Pentru o factura trimisa sau un email expediat, revenirea completa poate fi imposibila. Uneori poti face o operatie compensatorie, cum ar fi anularea unei rezervari, dar nu toate efectele se pot sterge. De aceea prevenirea conteaza mai mult decat promisiunea unui rollback.

## 19.5. Detectarea buclelor fara progres

Un agent poate apela aceeasi unealta de mai multe ori fara sa obtina informatie noua. Un harness bine proiectat poate observa repetarea argumentelor, lipsa unei schimbari de stare si depasirea unui buget. Sistemul trebuie sa se opreasca si sa raporteze blocajul. O bucla mai lunga nu este automat o bucla mai desteapta.

## 19.6. Schimbari de model, prompt si unealta

O actualizare aparent minora poate schimba felul in care agentul apeleaza o functie sau interpreteaza un mesaj de eroare. Pentru fluxurile importante, configuratiile se versioneaza si testele de regresie se reiau. Nu ajunge sa verifici ca noul model raspunde mai frumos. Trebuie sa verifici ca respecta acelasi contract operational.
