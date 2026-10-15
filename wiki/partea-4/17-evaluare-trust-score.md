# 17. Evaluarea si Trust Score: incredere acordata treptat



## 17.1. Intrebarea pe care trebuie s-o formulam corect

„Pot avea incredere in agent?” este prea larg. Incredere pentru ce? Sa explice vremea, sa editeze o ciorna, sa ruleze teste, sa schimbe o configuratie in productie? Un agent poate fi excelent la rezumate si nepotrivit pentru operatii financiare. Increderea trebuie atasata unei **categorii de sarcini**, unei **configuratii concrete**, unui **nivel de autonomie** si unui **set de conditii de evaluare**.

Vom folosi expresia **Trust Score** pentru o evaluare operationala propusa in aceasta lucrare. Nu este un standard consacrat si nu exista un scor universal care transforma automat 90% succes in permisiunea de a opera in productie. Scorul are sens numai impreuna cu tipul testelor, severitatea erorilor si intervalul de incertitudine.

## 17.2. Construirea unui mediu controlat

Pornim de la agentul meteo. Ii dam o cerere fara ambiguitate, un instrument disponibil si valori de test cunoscute. De exemplu, un serviciu simulat returneaza pentru un anumit oras o temperatura fixa si o ora a observatiei. Verificam daca agentul apeleaza unealta, foloseste argumentele corecte, preia valoarea si explica eventualele limite. Nu intrebam doar „a sunat bine raspunsul?”.

Urmeaza cazuri diferite: localitati cu nume identice, temperaturi negative, date lipsa, raspunsuri vechi, erori HTTP, timeout, rate limit sau informatii contradictorii. Unele teste sunt alese aleatoriu dintr-o distributie controlata. Altele sunt **teste adversariale**, construite special pentru punctele unde agentul este probabil sa esueze.

## 17.3. Evaluarea progresiva

O strategie coerenta are mai multe trepte:

**Treapta A — comportament strict definit.** Agentul primeste cereri precise, un singur instrument si criterii exacte. Trebuie sa dovedeasca executia corecta.

**Treapta B — variatie controlata.** Schimbam orase, formate si valori, dar pastram un rezultat de referinta.

**Treapta C — perturbari si intreruperi.** Introducem erori, date incomplete si opriri in mijlocul procesului. Verificam daca agentul raporteaza limitele si evita actiunile gresite.

**Treapta D — sarcini mai largi.** Oferim mai multe instrumente si situatii neprevazute; testam daca agentul alege corect traseul.

**Treapta E — autonomie in mediu izolat.** Relaxam constrangerile specifice scenariilor de test, dar pastram izolarea, jurnalele si regulile reale de siguranta.

**Treapta F — utilizare supravegheata.** Permitem sarcini reale cu impact limitat si aprobari. Observam stabilitatea pe o perioada suficienta si re-evaluam dupa modificari.

Ordinea este importanta. Nu putem demonstra robustetea unui agent numai prin repetarea aceleiasi intrebari de o mie de ori. Variatia intrarilor si testarea erorilor sunt cel putin la fel de importante.

## 17.4. Ce verificam, concret

Pentru o sarcina operationala, evaluarea ar trebui sa separe: **corectitudinea rezultatului**, **corectitudinea apelurilor de instrumente**, **respectarea regulilor**, **gestionarea erorilor**, **calitatea raportarii incertitudinii** si **consumul de resurse**. Un raspuns corect obtinut printr-un acces neautorizat nu este succes. Un raspuns partial care recunoaste lipsa datelor poate fi preferabil unei afirmatii complete, dar inventate.

Putem combina mai multe tipuri de verificatori. **Validatoarele deterministe** compara valori, scheme si reguli fixe. **Evaluatorii bazati pe modele** ajuta la aprecierea calitatii textelor sau a coerentei, dar pot avea propriile erori si prejudecati. **Oamenii** revizuiesc cazurile cu mize, ambiguitati sau efecte care nu pot fi masurate automat.

## 17.5. Problema celor 90%

Sa presupunem ca 90 dintre 100 de cereri sunt rezolvate corect. Avem o rata observata de 90% pentru acel set de teste. Nu putem concluziona fara alte informatii ca agentul va rezolva 90% din toate cererile viitoare. Testele ar putea fi prea usoare, datele ar putea fi similare cu cele folosite la dezvoltare, iar cele zece esecuri ar putea include un incident grav.

Un rezultat din 100 de observatii are si incertitudine statistica. Daca vrem sa comparam doua versiuni apropiate ca performanta, avem nevoie de esantioane mai mari si de teste comparabile. Pentru sarcinile cu risc ridicat, o rata medie de succes este insuficienta: trebuie analizat separat numarul de incalcari ale limitelor critice, preferabil cu toleranta foarte scazuta sau zero in testele de acceptare.

## 17.6. Un scor compozit, numai ca instrument intern

Putem defini un tablou de evaluare cu mai multe componente, de exemplu: corectitudinea finala 40%, apeluri corecte 20%, gestionarea erorilor 15%, respectarea regulilor 20% si raportarea limitelor 5%. Aceste ponderi sunt **exclusiv un exemplu pedagogic**, nu o formula recomandata universal. In productie, le stabilim prin analiza riscului, iar unele defecte trebuie sa fie conditii eliminatorii, nu simple penalizari.

O greseala de formatare poate scadea scorul usor. O plata neautorizata trebuie sa blocheze promovarea, chiar daca alte 999 de teste au trecut. Un scor unic fara istoricul defectelor ar ascunde tocmai informatia de care avem nevoie.

## 17.7. Trei niveluri de evaluare

**La nivel de run**, intrebam daca executia concreta a indeplinit criteriile. **La nivel de clasa**, masuram cum performeaza o configuratie de agenti pe o colectie de sarcini. **La nivel de sistem**, verificam daca orchestratorul a transmis corect informatii, a gestionat dependente, a impus permisiuni si a integrat rezultatele. Un model bun poate face parte dintr-un sistem prost orchestrat. Invers, o arhitectura buna nu poate garanta succesul unui agent nepotrivit.

## 17.8. Teste ascunse, perturbari aleatorii si reevaluare

Pe langa testele folosite in timpul dezvoltarii, avem nevoie de un set de evaluare pastrat separat. Altfel, putem adapta promptul exact la cazurile cunoscute si supraestima performanta. Testele aleatorii trebuie generate din clase realiste de situatii, nu doar prin schimbarea unor cuvinte. Intreruperile, raspunsurile invalide si datele incomplete sunt foarte utile pentru evaluarea mecanismelor failsafe.

Dupa modificarea modelului, promptului, instrumentelor, bazei de documente sau regulilor de orchestrare, evaluarea relevanta trebuie repetata. Increderea nu este o diploma permanenta. Este o concluzie conditionata de versiunea si conditiile sistemului.

## 17.9. Ce inseamna „human-in-the-loop” in practica

Un operator poate aproba o plata, poate revizui o concluzie ambigua sau poate confirma o modificare in productie. Dar simpla existenta a unui buton de aprobare nu este o garantie daca omul nu primeste contextul necesar. Aprobarea buna arata ce se va schimba, de ce, pe baza caror date, ce verificari au trecut si cum se poate reveni. Pentru sarcinile repetitive si de risc mic, verificarile automate sunt mai scalabile; pentru exceptii si consecinte importante, interventia umana ramane esentiala.

## 17.10. Legatura cu gestionarea riscului

NIST trateaza gestionarea riscului AI ca pe un proces care include guvernare, intelegerea contextului, masurare si gestionare continua [S15]. Nu extragem din aceasta abordare un „scor NIST” inventat. O folosim ca principiu: masurarea are valoare numai daca este conectata la decizii operationale si la responsabilitati clare.

## 17.11. Competenta demonstrata nu este acelasi lucru cu autoritatea acordata

Un agent poate executa corect mii de sarcini si totusi sa nu primeasca automat dreptul de a produce consecinte mai mari. **Competenta** descrie ce a demonstrat ca poate face in conditiile testate. **Autoritatea** descrie ce ii permite organizatia sa faca prin politici si permisiuni tehnice.

Rezultatele bune pot justifica reevaluarea mandatului, nu extinderea automata a acestuia. Autonomia poate creste in interiorul unei zone deja autorizate, in timp ce operatiile cu risc ridicat raman conditionate de aprobare. Invers, regresiile sau incidentele pot reduce autonomia chiar daca modelul nu s-a schimbat. Aceasta separare este compatibila cu principiile de gestionare a riscului si cu evitarea autonomiei excesive [S15, S16].

## 17.12. Evaluarea unui RAG: retrieval-ul si raspunsul se masoara separat

Un raspuns RAG poate esua in cel putin doua locuri: sistemul poate recupera fragmente nepotrivite sau modelul poate folosi prost fragmentele corecte. De aceea, evaluarea nu ar trebui redusa la impresia ca „raspunsul suna bine”.

Framework-uri precum **RAGAS** separa dimensiuni precum *Context Precision*, *Context Recall*, *Response Relevancy* si *Faithfulness*. Context Precision urmareste daca fragmentele relevante sunt clasate inaintea celor irelevante; Faithfulness verifica daca afirmatiile raspunsului sunt sustinute de contextul recuperat. Unele metrici folosesc un LLM evaluator, ceea ce inseamna ca si evaluatorul trebuie calibrat si verificat, nu tratat ca oracol [S27].

## 17.13. Consensul nu inseamna independenta dovezilor

Zece agenti care repeta aceeasi informatie nu ofera zece confirmari independente daca toti au pornit de la aceeasi sursa. Un sistem multi-agent poate crea impresia de consens in timp ce propaga o singura eroare initiala.

Pentru concluziile importante, jurnalul ar trebui sa pastreze provenienta afirmatiilor si sa permita identificarea surselor comune. Cand cerem verificare independenta, diversitatea agentilor conteaza mai putin decat independenta dovezilor, a testelor si a mecanismelor de validare. Aceasta este una dintre limitele evaluarii prin „mai multi agenti care se verifica intre ei”.
