# 4. Contextul: ce vede modelul in momentul raspunsului

## 4.1. Conversatia nu este acelasi lucru cu memoria umana

Sa presupunem ca discutam trei ore cu un chatbot. Am mentionat obiective, am corectat presupuneri, am incarcat documente, am schimbat subiectul de cateva ori. Cand cerem o sinteza, unele detalii lipsesc. De ce? Pentru ca modelul raspunde pe baza **contextului efectiv disponibil la acea inferenta**, nu pe baza unei amintiri nelimitate a intregii relatii cu utilizatorul.

**Fereastra de context** este cantitatea maxima de informatie, masurata de regula in tokeni, pe care modelul o poate procesa intr-o cerere. In acest buget intra instructiuni, mesajele relevante, fragmente de documente, descrieri ale instrumentelor, rezultatele apelurilor si, uneori, o parte din generarea curenta. Nu este garantat ca orice produs foloseste intreaga fereastra anuntata de model.

## 4.2. Patru lucruri care se confunda frecvent

**Istoricul vizibil** este ceea ce vedem in interfata. **Contextul transmis** este pachetul concret primit de model la o cerere. **Memoria aplicatiei** este informatia salvata pentru sesiuni viitoare. **Cunostintele antrenate** sunt tipare codificate in parametrii modelului. Sunt patru lucruri diferite. O aplicatie poate afisa o conversatie foarte lunga, dar sa transmita doar mesajele recente si un rezumat al celor vechi.

Invers, un chat nou poate primi preferinte salvate sau informatii recuperate din fisiere, chiar daca acele informatii nu apar in istoricul recent. Nu este un comportament universal si trebuie verificat pentru aplicatia folosita.

## 4.3. Context mare nu inseamna automat context bun

O fereastra mare permite introducerea mai multor informatii, dar nu garanteaza ca modelul va folosi corect fiecare detaliu. Cercetarea despre fenomenul *lost in the middle* a aratat ca unele modele performeaza mai slab cand informatia relevanta se afla in mijlocul unor intrari lungi [S02]. Concluzia practica nu este sa eliminam toate documentele, ci sa selectam si sa prezentam informatia utila astfel incat sa poata fi verificata.

Exemplu: intr-un proiect software avem 500 de pagini de loguri, dar intrebarea priveste eroarea aparuta la ultima instalare. Trimiterea tuturor logurilor poate introduce zgomot. Mai util este un extras cu eroarea, perioada, versiunea aplicatiei si pasii de reproducere. Originalele pot ramane disponibile pentru consultare ulterioara.

## 4.4. Cloud versus local: diferenta reala

La un model local, aplicatia noastra stabileste ce trimite catre motorul de inferenta si cum pastreaza istoricul. Putem avea un control mai direct asupra fisierelor si a mecanismelor de compresie, dar suntem limitati de software si hardware. La un serviciu cloud, fereastra modelului poate fi mare, insa furnizorul sau produsul intermediar poate impune limite, trata separat atasamentele ori gestiona memoria in mod propriu.

Nu exista regula ca „local inseamna context mic” si „cloud inseamna context mare”. O comparatie corecta specifica modelul, varianta, fereastra efectiva, formatul intrarilor, aplicatia, configuratia si momentul testului. Un CLI care foloseste un API cloud nu mosteneste automat toate functiile chatbotului web de la acelasi furnizor. Un serviciu local cu aceleasi greutati poate folosi alte setari si poate avea rezultate diferite.

## 4.5. Reducerea contextului fara pierderea deciziilor importante

Trei strategii frecvente sunt selectia informatiilor relevante, rezumarea istoricului si recuperarea din surse externe la nevoie. Prima reduce zgomotul. A doua economiseste spatiu, dar poate elimina detalii importante sau poate introduce erori. A treia permite consultarea documentelor atunci cand devin relevante. Niciuna nu functioneaza perfect fara verificare.

Un rezumat operational bun contine starea curenta, deciziile aprobate, sursele, lucrurile nerezolvate si urmatorii pasi. Nu ar trebui sa transforme o presupunere intr-un fapt doar pentru ca a fost repetata de mai multe ori. Acesta este unul dintre motivele pentru care **context engineering** a devenit o preocupare centrala in construirea agentilor [S03].

## 4.6. Exemplu: un agent care prelucreaza facturi

Agentul primeste cererea „Identifica facturile neachitate”. Nu are nevoie de toate emailurile persoanei din ultimii cinci ani. Are nevoie de perioada, sursa facturilor, registrul platilor, regulile pentru identificarea dublurilor si permisiunea de a citi documentele. Daca trebuie sa pregateasca, dar nu sa execute, o plata, aceasta limita trebuie sa fie parte din configuratia instrumentelor, nu doar dintr-o promisiune textuala.

**De retinut:** gestionarea contextului este o sarcina de inginerie a sistemului, nu o simpla problema de a cere modelului sa „tina minte mai bine”.
