### 2.1. De la text la tokeni

Un model de limbaj nu citeste o pagina asa cum o citim noi. Textul e taiat in bucati numite **tokeni**: un cuvant, o parte de cuvant, un semn de punctuatie sau un element dintr-o reprezentare mai complexa. De aceea 1.000 de cuvinte nu inseamna neaparat 1.000 de tokeni. Numarul depinde de limba, de vocabularul modelului si de tipul continutului.

La generare, modelul estimeaza cat de probabil este fiecare token posibil ca urmator. Sistemul alege unul dupa regulile de decodare, il adauga la secventa si o ia de la capat. O temperatura mai mica poate reduce variatia intre raspunsuri, dar nu garanteaza exactitate si nici raspunsuri identice la fiecare rulare. In plus, aplicatia poate adauga unelte, rutare sau postprocesare care schimba rezultatul final.

