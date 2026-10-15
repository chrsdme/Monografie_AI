# 11. Arhitectura de referinta: straturile unui workflow AI



## 11.1. De ce vorbim despre straturi

Cand o aplicatie creste, nu mai putem trata totul ca pe un singur prompt. Apar surse diferite, utilizatori cu permisiuni distincte, sarcini care dureaza, intreruperi, documente, instrumente, alerte si aprobari. Pentru a intelege sistemul, il descompunem in responsabilitati. **Straturile** sunt o metoda de analiza, nu opt sau zece servere obligatorii. Intr-un prototip pot functiona in acelasi program; intr-o organizatie mare pot fi servicii diferite.


## 11.2. Stratul de intrare

Acesta primeste cererea. Intrarea poate fi un mesaj in chat, o actiune intr-o aplicatie, un email, un eveniment de monitorizare sau un apel API. Aici aflam cine este utilizatorul, ce a solicitat, in ce limba doreste raspunsul si daca cererea contine fisiere. Inainte de orice inferenta, este rezonabil sa aplicam verificari elementare: dimensiunea fisierelor, tipul continutului, autentificarea, autorizarea si eventualele date lipsa.

Nu orice intrare trebuie trimisa direct unui LLM. Daca primim un eveniment „backup finalizat”, o regula clasica poate actualiza starea fara model. AI intervine atunci cand natura informatiei sau a deciziei o justifica.

## 11.3. Stratul de interpretare si pregatire

Acest strat transforma cererea intr-o descriere operationala: obiectiv, intrari, iesiri, reguli si nivel de risc. De exemplu, „verifica platile restante” poate necesita stabilirea perioadei si identificarea bazei de date. Daca informatia esentiala lipseste, sistemul poate intreba utilizatorul in loc sa inventeze. In alte cazuri, poate aplica valori implicite aprobate.

Aici pot functiona validatoare clasice, un clasificator sau un model de limbaj. Rezultatul ar trebui sa fie o structura clara, nu un paragraf vag care urmeaza sa fie ghicit de alte componente.

## 11.4. Stratul de orchestrare si stare

Orchestratorul primeste sarcina pregatita si stabileste cum trebuie procesata. Poate alege un singur agent, poate porni un workflow fix, poate imparti problema intre specialisti si poate astepta finalizarea dependentelor. Mai important, **pastreaza adevarul operational**: ce s-a cerut, ce este in lucru, cine raspunde, ce versiune a unui artefact este aprobata si ce conditii au blocat executia.

Un orchestrator care doar spune „delegat cu succes” fara sa aiba identificatori de sarcini, rezultate si stari verificabile nu ofera o garantie utila. Starea trebuie sa existe intr-o sursa controlata de aplicatie, nu doar intr-un rezumat conversational.

## 11.5. Stratul modelelor si agentilor

Aici sunt executate cererile de generare si deciziile asistate de model. Agentii pot avea roluri diferite, dar toti trebuie sa respecte contractele stabilite de arhitectura. Un specialist in cercetare poate avea acces la cautare si documentatie; un specialist in dezvoltare poate utiliza fisiere si teste; un evaluator poate inspecta rezultate fara sa modifice implementarea.

Separarea rolurilor se justifica prin responsabilitati, instrumente, criterii de acceptare sau niveluri de risc diferite. Nu trebuie sa existe un agent nou pentru fiecare comanda de terminal.

## 11.6. Stratul de actiune si integrare

Aici sunt executate efectiv operatiile: interogari SQL, citire sau scriere de fisiere, cautare web, apeluri catre sisteme de gestiune, build-uri software ori trimiterea unor notificari. Instrumentele trebuie sa valideze argumentele, sa impuna drepturile de acces si sa returneze coduri de rezultat precise. Daca o actiune este esuata, modelul nu trebuie sa poata transforma esecul in succes prin formularea raspunsului final.

Pentru operatiile cu efecte secundare, stratul de integrare trebuie sa suporte, unde este posibil, **idempotenta**: repetarea aceleiasi cereri sa nu dubleze efectul. De exemplu, un identificator unic al unei plati poate preveni trimiterea aceleiasi tranzactii de doua ori dupa o eroare de retea.

## 11.7. Stratul de cunostinte si memorie

Documentele, registrele, bazele de date si deciziile confirmate trebuie pastrate intr-o forma administrabila. Unele date se recupereaza prin RAG; altele prin interogari structurate. Memoria de proiect are alta durata de viata decat contextul unei sarcini. Nu orice conversatie trebuie arhivata pentru totdeauna si nu orice rezumat merita sa devina regula.

Aici conteaza sursele, versiunile, accesul si politicile de pastrare a datelor. Un sistem care recupereaza dintr-o arhiva invechita poate genera erori consistente, chiar daca modelul si orchestratorul functioneaza impecabil.

## 11.8. Stratul de verificare si control

Acesta compara actiunile si rezultatele cu criterii independente. Poate verifica schema unui JSON, suma unei facturi, rezultatul unei suite de teste ori conformitatea unei operatii cu permisiunile aprobate. Pentru decizii complexe, poate folosi un evaluator AI si poate solicita verificare umana. Dar un evaluator AI nu este o instanta magica a adevarului; verdictul lui trebuie calibrat si verificat.

Limitele cu efect juridic, financiar sau de securitate trebuie aplicate de cod si infrastructura. O cerere de confirmare intr-un prompt nu este echivalenta cu blocarea efectiva a functiei `send_payment` pana la aprobarea unui operator autorizat.

## 11.9. Stratul de observabilitate si imbunatatire

Jurnalele si trace-urile descriu ce s-a intamplat, cand si cu ce rezultat. Metricile agrega durata, costul, rata de succes, frecventa erorilor si numarul de interventii umane. Aceste date ajuta la investigarea incidentelor si la compararea versiunilor. Standardele OpenTelemetry includ conventii pentru operatii de inferenta, recuperare si apeluri de instrumente, dar sistemele concrete pot avea implementari diferite [S12].

Aici trebuie facuta distinctia dintre **a pastra date pentru diagnostic** si **a utiliza datele pentru imbunatatirea unui model**. Ultima poate implica evaluari, modificari de prompt, noi instrumente sau antrenare separata. Nu se intampla automat numai pentru ca am conectat un registru de loguri.

## 11.10. Responsabilitati transversale

Securitatea, confidentialitatea, administrarea identitatilor, auditul, costurile si disponibilitatea nu apartin unui singur strat. Ele traverseaza intreaga arhitectura. Sistemul trebuie sa stie ce utilizator a initiat o cerere, ce agent a executat-o, ce permisiuni erau active si cum poate fi izolata o componenta compromisa. Aceasta preocupare devine cu atat mai importanta cand agentii au acces la sisteme reale.
