# 1. Ce este inteligenta artificiala si ce este un model?

**De ce incepem aici.** Termenul AI este folosit pentru aplicatii atat de diferite incat aceeasi eticheta poate ascunde sisteme cu reguli fixe, algoritmi statistici ori modele generative. Glosarul Stanford HAI este o referinta utila pentru distinctiile dintre inteligenta artificiala, algoritm, automatizare, modele fundamentale si sisteme agentice [S18]. In aceasta carte, fiecare termen este definit in functie de ce face componenta efectiv, nu de numele comercial pe care il poarta.

## 1.1. AI nu desemneaza un singur obiect

Expresia „inteligenta artificiala” reuneste metode prin care programele pot realiza sarcini asociate, de obicei, cu perceptia, clasificarea, predictia, generarea de continut sau decizia. Un filtru de spam, un sistem de recunoastere a imaginilor si un chatbot modern sunt toate aplicatii AI, dar nu au neaparat aceeasi arhitectura. Unele functioneaza cu reguli scrise explicit. Altele folosesc modele invatate din exemple. Multe combina cele doua abordari.

Un **model** este o reprezentare matematica antrenata ori configurata sa transforme o intrare intr-o iesire. La clasificarea imaginilor, intrarea poate fi o fotografie, iar iesirea o categorie. La un model de limbaj, intrarea este o secventa de tokeni, iar iesirea este o estimare despre ce token ar putea urma. Din repetarea acestui mecanism se formeaza fraze, programe, rezumate si discutii elaborate. Acest mecanism de baza nu trebuie confundat cu intelegerea umana, nici cu verificarea automata a adevarului.

Pentru a-l folosi, nu este obligatoriu sa stim cum se ajusteaza intern fiecare parametru. Exact cum putem folosi un motor fara sa proiectam un cilindru. Totusi, trebuie sa cunoastem diferenta dintre capacitatea motorului si regulile dupa care functioneaza masina. De aceea vom separa mereu modelul de aplicatia care il gazduieste.

## 1.2. AI, machine learning, deep learning, AI generativ

**Machine learning** inseamna invatarea unor regularitati din date, in locul programarii explicite a tuturor regulilor. **Deep learning** utilizeaza retele neuronale cu mai multe straturi. **AI generativ** desemneaza sisteme care pot produce texte, imagini, sunet, video sau alte tipuri de continut. Un **LLM**, prescurtare de la *large language model*, este un model de limbaj antrenat la scara mare. Dimensiunea lui nu stabileste singura calitatea: conteaza datele, arhitectura, antrenarea, instrumentele si sarcina.

Modelele multimodale proceseaza sau genereaza mai multe tipuri de informatie. De exemplu, un utilizator poate incarca o fotografie a unei facturi si poate cere extragerea sumei. In spatele unei interfete aparent simple pot participa detectia vizuala, interpretarea textului si generarea unui raspuns. Capacitatea exacta depinde de model si de produs; un nume comercial nu garanteaza acces la toate aceste operatii.

## 1.3. Exemple fara a transforma cartea intr-un catalog

Familiile GPT, Claude si Gemini sunt exemple de modele oferite prin servicii cloud si aplicatii pentru utilizatori. Qwen, Llama si alte familii pot exista in variante accesibile prin servicii administrate sau prin infrastructura proprie, in functie de licenta si disponibilitate. Unele sunt distribuite cu greutati descarcabile; altele pot fi accesate numai printr-un serviciu. Nu vom afirma ca toate versiunile sunt echivalente si nu vom compara performanta printr-un clasament care se poate schimba de la luna la luna.

Daca deschidem un chatbot intr-un browser, folosim un **produs**, nu direct un fisier care contine modelul. Produsul poate include cautare web, fisiere, memorie, filtrare, instrumente, interfete grafice si politici proprii. Doua produse care utilizeaza aceeasi familie de modele pot avea comportamente diferite tocmai din cauza acestor componente.

## 1.4. Un exemplu concret

Intrebarea „Explica-mi ce este o factura proforma” poate fi rezolvata printr-un raspuns informational. Nu cerem acces la conturi si nu avem nevoie de autonomie. In schimb, „Cauta facturile primite luna aceasta, identifica dublurile si pregateste un tabel cu scadente” presupune citirea unor documente si executarea mai multor operatii. Modelul ramane o componenta; aplicatia trebuie sa furnizeze restul mecanismului.

**De retinut:** modelul produce predictii si continut; aplicatia ii ofera o interfata; sistemul operational decide ce date primeste modelul si ce actiuni sunt permise.
