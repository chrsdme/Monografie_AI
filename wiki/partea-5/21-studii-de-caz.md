# 21. Studii de caz: factura si aplicatia web

Primele patru studii sunt **simulari didactice**, nu sisteme implementate si masurate in cadrul acestei lucrari. Ne intereseaza sa intelegem de ce alegem o anumita arhitectura, ce rezultate vrem sa verificam si ce se schimba atunci cand dam mai multa autonomie. Parcurgem aceleasi trepte: chat, documente, unelte, workflow si, numai daca exista motive, orchestrare intre agenti. Ultima sectiune a capitolului (21.6) este diferita: discuta cazuri publice reale.

## 21.1. Cazul A: procesarea facturilor unei firme mici

**Situatia initiala.** O firma primeste lunar intre 50 si 150 de facturi, prin email si intr-un portal. Unele sunt PDF-uri cu text, altele scanari. O persoana trebuie sa identifice furnizorul, numarul, suma, moneda si scadenta, sa compare cu registrul si sa semnaleze dublurile. Volumul nu e urias, dar operatiile repetitive consuma timp.

**Nivelul 1: chat.** Utilizatorul intreaba un model ce campuri conteaza intr-o factura si cere o lista de verificare. Modelul explica si, eventual, redacteaza un sablon de tabel. Nu citeste automat niciun document. Beneficiul e cognitiv: omul intelege mai repede procesul.

**Nivelul 2: lucrul cu documente.** Utilizatorul incarca cinci facturi si cere extragerea campurilor. Modelul returneaza un tabel. Omul compara valorile cu documentele, mai ales sumele, numerele si datele. Daca un scan e ilizibil, o reactie buna este sa marcheze campul "necunoscut", nu sa il inventeze. Criteriul de acceptare e corespondenta dintre sursa si tabel.

**Nivelul 3: unelte.** Aplicatia poate citi atasamente printr-un conector autorizat, poate apela un serviciu de extragere a textului si poate cauta furnizorul intr-un registru. Modelul ajuta la interpretarea formatelor variabile. Validarea campurilor obligatorii si calculul totalurilor se fac in cod. Un jurnal inregistreaza documentul, rezultatul extragerii si orice diferenta. Nu e nevoie de autonomie completa.

**Nivelul 4: workflow fix.** La sosirea unui email de la un expeditor permis, sistemul salveaza atasamentul, identifica tipul documentului, extrage campurile, compara cu registrul si pregateste o inregistrare. Cand gaseste o diferenta, o trimite intr-o coada de verificare. Procesul e determinist la exterior, cu AI doar in componenta care interpreteaza documentul. Daca arata bine la teste reprezentative, poate fi deja sistemul final.

**Nivelul 5: agent pentru exceptii.** Sa presupunem ca furnizorii trimit formate foarte diferite, iar unele facturi fac referire la comenzi care trebuie cautate in alt sistem. Agentul poate cerceta neconcordanta cu unelte de citire, poate propune o explicatie si poate pregati un dosar pentru operator. Nu primeste dreptul de plata. Plata cere un flux separat, cu autentificare si aprobare.

**Nivelul 6: orchestrare justificata.** Daca procesul creste la sute de documente pe zi si include verificari fiscale, contracte si comenzi de achizitie, un orchestrator poate distribui extragerea, reconcilierea si verificarea. Operatiile au contexte si drepturi separate. Tot nu creezi un agent pentru fiecare camp din factura.

### Ce ar trebui sa contina un run verificabil

```text
invoice_run_id
source_document_id + hash
source_received_at
extraction_model_or_method + version
fields_extracted + confidence_or_unknown
arithmetic_checks
supplier_registry_check
potential_duplicate_check
human_review_status
final_record_id (only after acceptance)
```

Nu toate campurile se logheaza ca text integral. Unele pot fi referinte la documente protejate. Important e sa poti reconstitui ce sursa a produs fiecare valoare.

### Un exemplu de eroare si cum o tratam

Factura spune total 1.260,00 si are doua linii de cate 500,00 plus TVA 260,00. Modelul extrage 1.620,00 dintr-o imagine neclara. Validatorul numeric constata ca suma extrasa nu corespunde totalului calculat din linii. Documentul nu e aprobat. Agentul poate incerca alta metoda de extragere, dar dupa un numar limitat de incercari il trimite unui operator. **Sistemul a functionat corect chiar daca modelul a gresit**, pentru ca eroarea a fost prinsa inainte sa produca un efect extern.

### De ce un al doilea agent nu e prima solutie

Daca verifici doar egalitatea dintre doua numere, un program clasic e mai simplu si mai sigur decat un al doilea LLM. Un evaluator AI devine util cand trebuie sa stabilesti daca o clauza contractuala permite o exceptie sau daca o descriere ambigua corespunde unei comenzi. Si atunci, justificarea trebuie legata de documentele consultate efectiv.

## 21.2. Cazul B: dezvoltarea unei aplicatii web

**Situatia initiala.** O echipa vrea o aplicatie de programari. Clientul isi poate crea cont, alege un interval si primeste o confirmare. Administratorul vede programarile. Datele trebuie protejate, iar o rezervare nu trebuie dublata daca utilizatorul apasa de doua ori butonul.

**Nivelul 1: chat pentru a intelege cerinta.** Utilizatorul cere modelului sa explice ce componente sunt necesare. Primeste o lista: interfata, autentificare, baza de date, API, notificari si teste. E un plan de discutat, nu un sistem construit. Modelul poate omite probleme: fusuri orare, suprapuneri sau stergerea datelor. Un cititor responsabil transforma planul intr-o specificatie verificabila.

**Nivelul 2: cerinte si contracte.** Definesti ce inseamna o programare valida: serviciu disponibil, data viitoare, interval liber, utilizator autorizat. Stabilesti comportamentul la anulare si la erori. Un contract de iesire pentru rezervare poate contine `booking_id`, `status`, `slot_start` si `slot_end`. Ai deja criterii care se pot testa fara AI.

**Nivelul 3: un agent de dezvoltare.** Agentul primeste proiectul, cerintele si unelte pentru editare, build si teste. Scrie cod, ruleaza testele si corecteaza erorile. Daca o cerinta spune ca intervalele sunt de 30 de minute, poate adauga un test pentru o rezervare de 45 de minute si poate observa respingerea. In faza asta nu ai nevoie de un agent separat pentru fiecare comanda `git`, functie sau test.

**Nivelul 4: verificare independenta.** Un agent QA primeste cerintele initiale, modificarile, rezultatele testelor si acces de citire la cod. Construieste cazuri noi: dubla rezervare, doua cereri simultane, schimbarea fusului orar, utilizator neautorizat, anulare dupa termen. Nu porneste de la afirmatia dezvoltatorului "am acoperit toate cazurile". Dovezile relevante sunt testele executabile si rezultatul din baza de date.

**Nivelul 5: orchestrare.** Cand proiectul creste, orchestratorul descompune sarcina: Research analizeaza documentatia si cerintele, Development lucreaza la componente independente, QA verifica integrarea. Daca o regula de securitate nu e stabilita, sarcina care depinde de ea ramane `BLOCKED`. Daca testele nu trec, rezultatul revine la implementare cu erorile exacte.

**Nivelul 6: instante paralele, nu clase noi.** Avem trei clase: Research, Development si QA. Putem porni o instanta Research, sase instante Development si doua QA. Instantele Development lucreaza la autentificare, calendar, baza de date, notificari, frontend si integrare, fiecare cu propria sarcina. Infrastructura de inferenta poate fi partajata, deci noua instante nu inseamna noua modele incarcate. La final, rezultatul integrat trebuie verificat din nou, pentru ca modificari corecte separat pot deveni incompatibile impreuna.

### De ce avem nevoie de spatii de lucru izolate

Daca doua instante modifica simultan acelasi fisier, pot suprascrie schimbarile sau pot produce conflicte. O strategie este sa folosesti ramuri Git sau copii de lucru separate. Orchestratorul urmareste ce ramura apartine fiecarei sarcini si impune o etapa de integrare. Un test trecut intr-o ramura nu echivaleaza cu o verificare pe versiunea finala integrata.

### Un exemplu de defect introdus fara intentie

Cerinta spune ca doua rezervari nu pot folosi acelasi interval. Un dezvoltator verifica disponibilitatea, apoi salveaza rezervarea. In timpul dintre verificare si salvare, o alta cerere poate ocupa acelasi interval. Ambele teste individuale trec, dar doua cereri concurente pot produce o rezervare dubla. QA trebuie sa testeze concurenta, iar sistemul are nevoie de o constrangere in baza de date sau de o tranzactie potrivita. Un prompt de tipul "nu permite rezervari duble" nu rezolva problema la nivelul integritatii datelor.

### Ce ar trebui sa blocheze publicarea

Publicarea nu trebuie sa depinda de un "QA spune PASS" scris liber. Un contract de acceptare poate cere: build reusit, teste obligatorii trecute, verificari de securitate fara defecte critice cunoscute, backup sau metoda de revenire, un artefact versionat si aprobare pentru productie. Unele verificari se executa automat, altele cer decizie umana. Orchestratorul poate strange dovezile, dar nu trebuie sa inlocuiasca politica de livrare.

## 21.3. Ce invatam din comparatie

La facturi, valoarea principala vine din extragerea datelor si din tratarea exceptiilor. La aplicatia web, valoarea apare din implementare si iteratie. Ambele profita de unelte si de verificari. Dar nu toate au nevoie de multi-agent si nu toate sarcinile se ruleaza autonom. Arhitectura corecta porneste de la procesul real, nu de la posibilitatea de a crea un numar mare de agenti.

## 21.4. Studiul de caz C: triajul solicitarilor de suport

Ca sa vezi ca aceleasi principii merg si in afara dezvoltarii software, luam un al treilea exemplu, mai scurt. O firma primeste emailuri despre livrari, retururi, facturi si probleme tehnice. Nu incepem prin a construi cinci agenti. Incepem prin a observa cum se rezolva acum cererile si unde se pierde timp.

**Versiunea asistata.** Un angajat copiaza mesajul intr-un chatbot si cere un rezumat si o propunere de raspuns. Verifica datele si trimite el raspunsul. Castigul posibil e la redactare, nu la executia completa.

**Versiunea conectata.** Aplicatia primeste un mesaj, identifica limba si categoria probabila, apoi consulta printr-un API starea comenzii. Politica actualizata de retur vine dintr-o baza documentara, cu sursa citata. Daca lipseste numarul comenzii, sistemul nu inventeaza unul, ci cere completari.

**Versiunea cu automatizare fixa.** Daca e doar o intrebare despre status si identitatea clientului e verificata, programul construieste un raspuns din datele comenzii. Daca mesajul contine o contestatie, informatii contradictorii sau o cerere financiara, trece la operator. Niciun LLM nu decide singur asupra unei rambursari.

**Versiunea agentica.** Pentru cererile complexe, un agent specializat poate planifica verificarea mai multor surse, dar executa doar actiunile permise. Un orchestrator urmareste dependentele si impune un numar maxim de incercari. Fiecare raspuns final include un rezumat al datelor consultate si tipul de verificare facuta. La cazurile sensibile, rezultatul ramane ciorna pana la aprobare.

**Cum evaluam.** Masuram separat clasificarea corecta a categoriei, folosirea datelor reale ale comenzii, rata de escaladare justificata, timpul pana la rezolvare si numarul de actiuni neautorizate. Nu confundam un raspuns politicos cu rezolvarea cererii. Exemplul combina tipurile de aplicatii din ghidul IBM despre AI workflow si recomandarile pentru suport asistat din surse practice romanesti, fara a prelua produse sau promisiuni comerciale [S17](../anexe/bibliografie.md#s17), [S22](../anexe/bibliografie.md#s22), [S36](../anexe/bibliografie.md#s36).

## 21.5. Studiul de caz D: dintr-un PDF scanat intr-o inregistrare verificata

Procesarea inteligenta a documentelor, numita adesea **IDP** (*Intelligent Document Processing*), combina recunoasterea textului, clasificarea documentelor, extragerea campurilor si verificarea lor. Este mai mult decat OCR. OCR transforma imaginea literelor in text. IDP urmareste un rezultat operational, de pilda date de factura pregatite pentru sistemul contabil [S20](../anexe/bibliografie.md#s20).

O factura scanata poate fi procesata asa: sistemul identifica paginile, recunoaste textul, gaseste furnizorul, moneda, totalul, data si numarul facturii, verifica aritmetic subtotalul si taxele, compara furnizorul cu registrul si marcheaza neconcordantele. Un model multimodal poate ajuta la documente cu layout neobisnuit, dar calculele aritmetice si identificarea duplicatelor se fac prin reguli verificabile.

Din perspectiva increderii, sunt trei intrebari diferite: **a citit corect textul?**, **a extras campurile corecte?**, **avem dreptul sa facem operatia urmatoare?** Un rezultat bun la primele doua nu este o autorizatie de plata. Aprobarea, jurnalul si controalele de duplicat raman in sistemul operational. Cazul arata de ce un workflow poate integra AI fara ca toate etapele sa fie delegate unui agent autonom.

## 21.6. Cum citim un caz cu cifre: Raleigh si Cordoba

Pana aici am lucrat cu simulari. In realitate, o sa intalnesti comunicate de presa si pagini de proiect care spun lucruri ca "costuri reduse cu 66%". Nu le tratam nici ca minciuni, nici ca dovezi. Le citim cu un set de intrebari. Doua cazuri publice recente ne servesc drept exercitiu. Nu le validam independent: aratam doar ce spun sursele si ce lipseste din ele.

**Exemplul 1: Raleigh (Carolina de Nord).** Pe 8 octombrie 2026, ServiceNow a publicat un comunicat cu titlul "Raleigh, North Carolina, reduces IT service desk costs by 66% with ServiceNow AI agents" [S34](../anexe/bibliografie.md#s34). Comunicatul spune ca biroul de asistenta IT al orasului are patru oameni si deserveste 4.400 de angajati ai primariei. Cifra de 66% este atribuita redirectionarii timpului personalului. Alte cifre din text: o rata de deviere de 98% pentru agentul de autoservire Ral-E, 98% dintre rezumatele de incidente generate de AI acceptate fara modificari si aproape jumatate dintre cererile de suport IT rezolvate autonom, cu o tinta de 85%. Directorul de informatica al orasului, Mark Wittenburg, spune: "We're introducing AI deliberately, building trust step by step and keeping our people in the loop."

Ce lipseste: comunicatul nu indica perioada de masurare, nu spune fata de ce s-a calculat scaderea de 66% si nu explica ce intra la "costuri". Nu apar sume in bani. Iar "aproape jumatate" este un rezultat, pe cand 85% este o tinta. Fraza despre incredere si oameni in bucla e, in schimb, o buna descriere a abordarii graduale din aceasta carte.

**Exemplul 2: Cordoba (Argentina).** Pe 21 septembrie 2026, baza de date OECD.AI a adaugat o initiativa a provinciei Cordoba, "AI for resilient digital government services", despre un sistem de operare asistat de AI pentru infrastructura cloud a administratiei [S30](../anexe/bibliografie.md#s30). Pagina vorbeste despre peste 3,8 milioane de locuitori deserviti si despre un MVP care a tratat "more than 25 incidents with over 90% success", cu timpul de diagnostic redus de la aproximativ o ora la sub trei minute. Rezultatele par raportate de proiect insusi, iar pagina nu spune ca au fost verificate independent.

Observatii de cititor atent: pagina da in prezentare cifra de 66 de conturi AWS, dar in alta sectiune vorbeste despre extinderea la 26 de conturi de productie, fara sa explice relatia dintre ele. Spune ca faza curenta "operates strictly in read-only mode", dar descrie si un flux in sapte etape cu o etapa de executie si un sistem care a tratat incidente "autonomously". Poate exista o explicatie simpla, de exemplu faze diferite. Pagina nu o da. Nu avem nici date de baza, nici marimea esantionului, nici definitia unui "incident".

**Lista de intrebari pentru orice astfel de cifra:**

1. **Cine o raporteaza?** Furnizorul, clientul sau un tert independent?
2. **Ce perioada acopera?** O luna, un an, un pilot?
3. **Fata de ce se compara?** Care este situatia de dinainte, masurata cum?
4. **Ce inseamna exact metrica?** "Cost" inseamna bani cheltuiti mai putin sau timp reorientat catre alte sarcini? "Succes" inseamna rezolvat sau inchis?
5. **Cat de mare e esantionul?** 25 de incidente sau 25.000?
6. **Rezultat sau tinta?** Cifrele aspirationale se amesteca usor cu cele obtinute.
7. **E coerent textul cu el insusi?** Numere sau faze care se bat cap in cap sunt un semnal sa ceri clarificari.
8. **Exista o a doua sursa?** Fara ea, retii cifra ca "afirmata de", nu ca "dovedita".

Aplicata asupra propriilor tale proiecte, aceeasi lista te protejeaza de entuziasmul de dupa o demonstratie reusita. Cazurile de mai sus sunt, ca exemple de comunicare publica, utile tocmai pentru ce lasa nespus, nu pentru ca ar fi false.
