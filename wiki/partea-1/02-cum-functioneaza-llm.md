# 2. Cum produce un LLM un raspuns

## 2.1. De la text la tokeni

Un model de limbaj nu citeste o pagina asa cum o citim noi. Textul e taiat in bucati numite **tokeni**: un cuvant, o parte de cuvant, un semn de punctuatie sau un element dintr-o reprezentare mai complexa. De aceea 1.000 de cuvinte nu inseamna neaparat 1.000 de tokeni. Numarul depinde de limba, de vocabularul modelului si de tipul continutului.

La generare, modelul estimeaza cat de probabil este fiecare token posibil ca urmator. Sistemul alege unul dupa regulile de decodare, il adauga la secventa si o ia de la capat. O temperatura mai mica poate reduce variatia intre raspunsuri, dar nu garanteaza exactitate si nici raspunsuri identice la fiecare rulare. In plus, aplicatia poate adauga unelte, rutare sau postprocesare care schimba rezultatul final.

## 2.2. Antrenare, inferenta si ajustare

**Antrenarea** e procesul scump in care parametrii modelului se ajusteaza pe date. **Inferenta** inseamna folosirea unui model deja antrenat pentru o cerere. Cand vorbesti cu un chatbot, in mod obisnuit faci inferenta: greutatile modelului nu se rescriu la fiecare mesaj. **Fine-tuning** inseamna o antrenare suplimentara, pe date si obiective specifice. Nu trebuie confundat cu adaugarea unui document in conversatie si nici cu faptul ca aplicatia isi aminteste o preferinta de-a ta.

Un exemplu: ii dai modelului manualul unei centrale termice si el raspunde pe baza paginilor primite. Asta nu inseamna ca a fost reantrenat. Daca sistemul salveaza manualul intr-o baza de documente si il aduce inapoi la intrebarea urmatoare, ai construit un mecanism de recuperare a informatiei, nu un model nou.

## 2.3. De unde vine impresia de rationament?

Modelele moderne pot face transformari logice si pot rezolva probleme complicate. Uneori scot planuri coerente, cod care merge si explicatii foarte bune. Capacitatea e reala. Dar asta nu inseamna ca fiecare afirmatie generata a fost verificata cu o sursa externa. Modelul poate formula un raspuns foarte convingator in care apare o data inventata sau o referinta care nu exista.

**Halucinatie** este termenul obisnuit pentru continutul generat care nu e sustinut de fapte sau de datele disponibile. Nu orice greseala e o halucinatie, insa. Modelul poate calcula prost, poate intelege ambiguu o cerinta, poate folosi un document invechit sau poate alege unealta potrivita cu parametri nepotriviti. Diferenta conteaza, pentru ca fiecare tip de greseala se repara altfel.

## 2.4. Ce inseamna comportament probabilistic

Un program clasic pentru `2 + 2` trebuie sa dea `4`, daca a fost implementat corect si intrarile sunt valide. Un model poate explica suma in mai multe feluri. La sarcinile deschise nu exista mereu un singur raspuns acceptabil, deci trebuie sa distingem intre verificarea unei valori exacte si evaluarea unui raspuns liber.

Faptul ca nu exista un singur raspuns nu face greseala imposibila. O analiza de piata poate ajunge la concluzii diferite, dar nu poate inventa volumele de vanzari si apoi sa pretinda ca rezultatul e valid. La aceasta diferenta ne intoarcem cand construim evaluarile.

## 2.5. O mica perspectiva istorica

Cercetarea in AI e mult mai veche decat chatboturile de azi. Pentru arhitecturile de limbaj moderne, un reper este lucrarea *Attention Is All You Need* din 2017, care a introdus arhitectura Transformer si a influentat profund modelele de limbaj de dupa [S01](../anexe/bibliografie.md#s01). Asta nu inseamna ca AI a inceput atunci. Inseamna ca momentul explica o parte din accelerarea de dupa.

**De retinut:** "probabilistic" nu inseamna "la intamplare". Inseamna ca modelul estimeaza si alege iesiri, iar calitatea trebuie judecata dupa sarcina, context si verificari externe.
