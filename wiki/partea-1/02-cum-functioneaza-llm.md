# 2. Cum produce un LLM un raspuns

## 2.1. De la text la tokeni

Un model de limbaj nu citeste textul in acelasi mod in care citim noi o pagina. Intrarea este impartita in unitati numite **tokeni**. Un token poate reprezenta un cuvant, o bucata de cuvant, un semn de punctuatie sau un element dintr-o reprezentare mai complexa. De aceea, 1.000 de cuvinte nu sunt neaparat 1.000 de tokeni. Numarul depinde si de limba, de vocabularul utilizat de model si de tipul continutului.

La generare, modelul estimeaza o distributie de probabilitate pentru urmatorul token. Sistemul alege un token conform regulilor de decodare, il adauga secventei si repeta. O temperatura mai scazuta poate reduce variatia unor raspunsuri, dar nu garanteaza exactitate sau identitate perfecta intre executii. In plus, aplicatia poate introduce instrumente, rutare sau postprocesare care schimba rezultatul final.

## 2.2. Antrenare, inferenta si ajustare

**Antrenarea** este procesul costisitor prin care parametrii modelului sunt ajustati pe date. **Inferenta** este folosirea modelului deja antrenat pentru o cerere. Cand vorbim zilnic cu un chatbot, de regula facem inferenta; nu rescriem greutatile modelului la fiecare mesaj. **Fine-tuning** inseamna o forma de antrenare suplimentara pe date si obiective specifice. Nu trebuie confundat cu adaugarea unui document in conversatie sau cu memorarea unei preferinte de catre aplicatie.

Un exemplu: daca ii furnizam manualul unei centrale termice, modelul poate raspunde pe baza paginilor primite. Nu inseamna ca modelul a fost reantrenat. Daca sistemul salveaza manualul intr-o baza de documente si il recupereaza la intrebarea urmatoare, am construit un mecanism de recuperare a informatiei, nu un model nou.

## 2.3. De unde vine impresia de rationament?

Modelele moderne pot produce comportamente care seamana cu rationamentul si pot rezolva probleme complexe. Uneori genereaza planuri coerente, cod functional si explicatii foarte bune. Natura exacta a acestor procese este in continuare cercetata; pentru utilizarea practica este suficient sa retinem ca un raspuns bine argumentat nu inseamna automat ca fiecare afirmatie a fost verificata impotriva unei surse externe. Modelul poate formula un raspuns foarte convingator care contine o data inventata sau o referinta inexistenta.

**Halucinatie** este termenul folosit curent pentru un continut generat care nu este sustinut de fapte ori de datele disponibile. Dar nu toate esecurile sunt halucinatii. Modelul poate calcula gresit, poate intelege ambiguu o cerinta, poate folosi un document invechit sau poate executa instrumentul potrivit cu parametrii nepotriviti. Diferentierea conteaza pentru remediere.

## 2.4. Ce inseamna comportament probabilistic

Un program clasic pentru suma `2 + 2` trebuie sa returneze `4`, daca a fost implementat corect si intrarile sunt valide. Un model poate explica suma in mai multe moduri. In sarcini deschise, nu exista intotdeauna un singur raspuns acceptabil. De aici apare distinctia dintre verificarea unei valori exacte si evaluarea unui raspuns deschis.

Totusi, lipsa unui singur raspuns nu anuleaza ideea de greseala. O analiza de piata poate admite concluzii diferite, dar nu poate inventa volumele de vanzari si apoi pretinde ca rezultatul este valid. Vom reveni la aceasta diferenta cand vom construi evaluarile.

## 2.5. O mica perspectiva istorica

Cercetarea in AI este mult mai veche decat chatboturile actuale. Pentru arhitecturile de limbaj moderne, lucrarea *Attention Is All You Need* din 2017 reprezinta un reper important: a introdus arhitectura Transformer care a influentat profund evolutia modelelor de limbaj [S01]. Nu inseamna ca AI a inceput atunci; inseamna ca acest moment explica o parte din accelerarea ulterioara.

**De retinut:** probabilistic nu inseamna aleatoriu fara reguli. Inseamna ca modelul estimeaza si selecteaza iesiri, iar calitatea trebuie analizata prin sarcina, context si verificari externe.
