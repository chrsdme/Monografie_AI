# 1. Ce este inteligenta artificiala si ce este un model?

**De ce incepem aici.** Cuvantul "AI" acopera lucruri foarte diferite: de la un filtru de spam cu reguli fixe pana la un chatbot care scrie eseuri. Aceeasi eticheta, mecanisme total diferite. Glosarul Stanford HAI este o referinta buna pentru distinctiile dintre inteligenta artificiala, algoritm, automatizare, modele fundamentale si sisteme agentice [S18](../anexe/bibliografie.md#s18). In cartea asta definim fiecare termen dupa ce face componenta, nu dupa numele comercial pe care il poarta.

## 1.1. AI nu este un singur obiect

"Inteligenta artificiala" aduna la un loc metode prin care programele fac lucruri pe care le asociem de obicei cu perceptia, clasificarea, predictia, generarea de continut sau luarea deciziilor. Un filtru de spam, un sistem care recunoaste imagini si un chatbot modern sunt toate AI, dar nu seamana intre ele. Unele merg pe reguli scrise de oameni. Altele folosesc modele invatate din exemple. Multe le combina pe amandoua.

De exemplu, o regula poate muta toate mesajele primite de la o anumita adresa intr-un dosar. Pentru a grupa emailuri dupa ceea ce solicita oamenii, chiar cand folosesc formulari diferite, un model antrenat poate fi util. In primul caz aplicam o conditie fixa; in al doilea interpretam continutul, dar putem si gresi. O regula simpla nu reprezinta automat inteligenta artificiala.

Un **model** este o reprezentare matematica antrenata sau configurata sa transforme o intrare intr-o iesire. La clasificarea imaginilor, intrarea e o fotografie, iar iesirea o categorie. La un model de limbaj generativ autoregresiv, intrarea e o secventa de tokeni (de exemplu cuvinte, parti de cuvinte sau semne de punctuatie), iar iesirea e o estimare a tokenului care ar putea urma. Repetat de multe ori, mecanismul acesta produce fraze, cod, rezumate si discutii intregi. Dar el ramane un mecanism de predictie. Nu e intelegere omeneasca si nu e un verificator automat de adevar.

Nu trebuie sa stii cum se ajusteaza intern fiecare parametru ca sa folosesti un model, la fel cum poti conduce o masina fara sa fi proiectat motorul. Trebuie totusi sa stii diferenta dintre ce poate motorul si ce reguli are masina din jurul lui. De aceea vom separa mereu modelul de aplicatia care il gazduieste.

## 1.2. AI, machine learning, deep learning, AI generativ

**Machine learning** inseamna ca programul invata regularitati din date, in loc sa primeasca toate regulile scrise de mana. **Deep learning** foloseste retele neuronale cu multe straturi. **AI generativ** este eticheta pentru sistemele care produc text, imagini, sunet, video sau alt continut nou. Un **LLM** (*large language model*) este un model de limbaj antrenat la scara mare. Marimea lui nu decide singura calitatea: conteaza datele, arhitectura, antrenarea, uneltele si sarcina.

Aceste categorii nu sunt complet separate: machine learning face parte din AI, iar deep learning este o ramura a machine learning. Termenii „generativ” si „multimodal” descriu alte caracteristici: ce produce modelul si ce tipuri de informatie poate procesa sau genera. Un model poate fi in acelasi timp generativ si multimodal.

Modelele **multimodale** lucreaza cu mai multe tipuri de informatie deodata. Poti incarca poza unei facturi si sa ceri suma totala. Sub interfata aceea simpla pot lucra, pe rand, detectia vizuala, citirea textului si generarea raspunsului. Ce poate face exact depinde de model si de produs, iar un nume comercial nu garanteaza ca ai acces la toate aceste capacitati.

## 1.3. Modelul, aplicatia si sistemul

Cand deschizi un chatbot in browser, folosesti un **produs**, nu direct un fisier cu modelul. Produsul poate adauga cautare web, fisiere, memorie, filtre, unelte, interfete grafice si reguli proprii. Doua produse construite pe aceeasi familie de modele se pot purta diferit tocmai din cauza acestor straturi.

De exemplu, doua aplicatii pot folosi aceeasi familie de modele, dar numai una sa permita incarcarea documentelor. Pentru a analiza un fisier, diferenta nu tine neaparat de model, ci de informatiile pe care aplicatia i le poate pune la dispozitie.

Prin **sistem AI** intelegem ansamblul care combina unul sau mai multe modele cu aplicatia si, dupa caz, surse de date, unelte, permisiuni, stare si verificari. Aceste functii pot fi reunite intr-un produs sau distribuite intre mai multe servicii.

GPT, Claude si Gemini sunt familii de modele oferite prin servicii cloud si aplicatii. Qwen, Llama si altele pot exista in variante accesibile printr-un serviciu administrat sau pe infrastructura proprie, in functie de licenta si de disponibilitate. Unele variante au parametrii antrenati disponibili pentru descarcare; cu software si resurse potrivite, ele pot rula pe echipamente proprii, daca licenta permite. Altele sunt disponibile doar prin servicii externe. Nu vom spune ca toate versiunile sunt echivalente si nu vom publica clasamente care se schimba de la o luna la alta.

## 1.4. Un exemplu concret

"Explica-mi ce este o factura proforma" se rezolva cu un raspuns informativ. Nu cere acces la conturi si nu are nevoie de autonomie. In schimb, "Cauta facturile primite luna asta, gaseste dublurile si pregateste un tabel cu scadente" inseamna citirea unor documente si mai multe operatii in lant. Modelul ramane o piesa; restul mecanismului trebuie sa vina de la aplicatie.

**De retinut:** modelul produce predictii si continut. Aplicatia ii da o interfata. Sistemul din jur decide ce date primeste modelul si ce actiuni sunt permise.
