### 1.1. AI nu este un singur obiect

"Inteligenta artificiala" aduna la un loc metode prin care programele fac lucruri pe care le asociem de obicei cu perceptia, clasificarea, predictia, generarea de continut sau luarea deciziilor. Un filtru de spam, un sistem care recunoaste imagini si un chatbot modern sunt toate AI, dar nu seamana intre ele. Unele merg pe reguli scrise de oameni. Altele folosesc modele invatate din exemple. Multe le combina pe amandoua.

De exemplu, o regula poate muta toate mesajele primite de la o anumita adresa intr-un dosar. Pentru a grupa emailuri dupa ceea ce solicita oamenii, chiar cand folosesc formulari diferite, un model antrenat poate fi util. In primul caz aplicam o conditie fixa; in al doilea interpretam continutul, dar putem si gresi. O regula simpla nu reprezinta automat inteligenta artificiala.

Un **model** este o reprezentare matematica antrenata sau configurata sa transforme o intrare intr-o iesire. La clasificarea imaginilor, intrarea e o fotografie, iar iesirea o categorie. La un model de limbaj generativ autoregresiv, intrarea e o secventa de tokeni (de exemplu cuvinte, parti de cuvinte sau semne de punctuatie), iar iesirea e o estimare a tokenului care ar putea urma. Repetat de multe ori, mecanismul acesta produce fraze, cod, rezumate si discutii intregi. Dar el ramane un mecanism de predictie. Nu e intelegere omeneasca si nu e un verificator automat de adevar.

Nu trebuie sa stii cum se ajusteaza intern fiecare parametru ca sa folosesti un model, la fel cum poti conduce o masina fara sa fi proiectat motorul. Trebuie totusi sa stii diferenta dintre ce poate motorul si ce reguli are masina din jurul lui. De aceea vom separa mereu modelul de aplicatia care il gazduieste.

