# 4. Contextul: ce vede modelul in momentul raspunsului

## 4.1. O conversatie nu e memorie omeneasca

Discuti trei ore cu un chatbot. Ai spus obiective, ai corectat presupuneri, ai incarcat documente si ai schimbat subiectul de cateva ori. Apoi ceri o sinteza si observi ca lipsesc detalii. De ce? Pentru ca modelul raspunde pe baza **contextului disponibil in momentul acelei cereri**, nu dintr-o amintire nelimitata a intregii relatii cu tine.

**Fereastra de context** este cantitatea maxima de informatie, de obicei masurata in tokeni, pe care modelul o poate procesa intr-o singura cerere. In acest buget intra instructiunile, mesajele relevante, fragmentele de documente, descrierile uneltelor, rezultatele apelurilor si, uneori, o parte din raspunsul aflat in curs de generare. Nu e sigur ca un produs foloseste toata fereastra anuntata pentru model.

## 4.2. Patru lucruri care se confunda des

**Istoricul vizibil** este ce vezi in interfata. **Contextul transmis** este pachetul concret primit de model la o cerere. **Memoria aplicatiei** este informatia salvata pentru sesiuni viitoare. **Cunostintele antrenate** sunt tiparele codificate in parametrii modelului. Sunt patru lucruri diferite. O aplicatie poate afisa o conversatie foarte lunga si totusi sa trimita modelului doar mesajele recente si un rezumat al celor vechi.

Si invers: un chat nou poate primi preferinte salvate sau informatii recuperate din fisiere, chiar daca ele nu apar in istoricul recent. Comportamentul nu e universal, deci merita verificat pentru aplicatia pe care o folosesti.

## 4.3. Context mare nu inseamna context bun

O fereastra mare te lasa sa pui mai multa informatie, dar nu garanteaza ca modelul va folosi bine fiecare detaliu. Cercetarea despre fenomenul *lost in the middle* a aratat ca unele modele se descurca mai prost cand informatia relevanta e in mijlocul unei intrari lungi [S02](../anexe/bibliografie.md#s02). Concluzia practica nu e sa elimini documentele, ci sa alegi si sa prezinti ce e util in asa fel incat sa poata fi verificat.

Anthropic formuleaza ideea direct, in ghidul lor despre ingineria contextului: "Context, therefore, must be treated as a finite resource with diminishing marginal returns" [S03](../anexe/bibliografie.md#s03). Pe romaneste: contextul e o resursa limitata, iar fiecare token in plus aduce tot mai putin.

Un exemplu: ai 500 de pagini de loguri, dar intrebarea priveste eroarea de la ultima instalare. Daca trimiti tot, adaugi zgomot. Mai util este un extras cu eroarea, perioada, versiunea aplicatiei si pasii de reproducere. Originalele pot ramane la indemana, pentru consultare ulterioara.

## 4.4. Cloud contra local: diferenta reala

La un model local, aplicatia ta hotaraste ce trimite motorului de inferenta si cum pastreaza istoricul. Ai control mai direct asupra fisierelor si a mecanismelor de compresie, dar esti limitat de software si hardware. La un serviciu cloud, fereastra modelului poate fi mare, dar furnizorul sau produsul intermediar poate impune limite, poate trata separat atasamentele sau poate gestiona memoria in felul lui.

Nu exista regula "local inseamna context mic" si "cloud inseamna context mare". O comparatie corecta spune ce model, ce varianta, ce fereastra efectiva, ce format de intrare, ce aplicatie, ce configuratie si ce moment al testului. Un CLI care apeleaza un API cloud nu mosteneste automat toate functiile chatbotului web de la acelasi furnizor. Iar un serviciu local cu aceleasi greutati poate avea alte setari si alte rezultate.

## 4.5. Cum reducem contextul fara sa pierdem deciziile importante

Trei strategii sunt des folosite: selectezi informatiile relevante, rezumi istoricul si recuperezi din surse externe doar cand e nevoie. Prima reduce zgomotul. A doua economiseste spatiu, dar poate sterge detalii importante sau poate introduce erori. A treia lasa documentele sa intre in joc atunci cand devin relevante. Niciuna nu merge bine fara verificare.

Un rezumat operational bun contine starea curenta, deciziile aprobate, sursele, lucrurile nerezolvate si urmatorii pasi. Nu transforma o presupunere in fapt doar pentru ca a fost repetata de mai multe ori. Ghidul Anthropic descrie aceeasi tinta: sa gasesti "the smallest set of high-signal tokens that maximize the likelihood of your desired outcome" [S03](../anexe/bibliografie.md#s03). De aici a ajuns **context engineering** o preocupare centrala in construirea agentilor.

## 4.6. Exemplu: un agent care prelucreaza facturi

Agentul primeste cererea "Identifica facturile neachitate". Nu are nevoie de toate emailurile persoanei din ultimii cinci ani. Are nevoie de perioada, sursa facturilor, registrul platilor, regulile pentru dubluri si permisiunea de a citi documentele. Daca trebuie sa pregateasca o plata, dar nu sa o execute, limita asta trebuie sa fie parte din configuratia uneltelor, nu o simpla promisiune scrisa in text.

**De retinut:** gestionarea contextului e munca de inginerie a sistemului. Nu se rezolva cerandu-i modelului sa "tina minte mai bine".
