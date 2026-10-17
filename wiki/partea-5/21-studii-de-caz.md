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

## 21.7. Studiul de caz E: acelasi retur prin trei arhitecturi

**Statut:** simulare didactica, nu implementare comerciala. Un client solicita la ora 23:00 rambursarea unui produs deteriorat. Magazinul fictiv permite procesarea automata numai pentru sume de cel mult **100 RON**, cu identitate, comanda, dovezi si eligibilitate verificate. Pragul este inventat pentru exercitiu, nu reprezinta o obligatie legala.

### E1. Automatizare clasica: codul decide

```text
LA primirea unei cereri:
    verifica_identitatea()
    comanda = obtine_comanda()
    DACA eligibila(comanda) SI dovada_suficienta
         SI nu_exista_rambursare SI suma <= 100 RON:
         initiaza_cu_cheie_de_idempotenta()
         reconciliaza_rezultatul()
         confirma_doar_dupa_succes()
    ALTFEL: escaladeaza()
```

Nu exista un LLM. Ramificatiile sunt programate, iar operatiile cu efect extern sunt controlate in cod. Daca datele sunt standardizate si regulile suficiente, aceasta poate fi alegerea potrivita.

### E2. Workflow AI: modelul ajuta in etape delimitate

```text
LA primirea unui email:
    intentie, order_id = AI.extrage_date(email)
    DACA order_id_lipseste: solicita_completare(); OPRESTE
    comanda = cauta_comanda(order_id)
    eligibil = valideaza_in_cod(comanda, client)
    DACA eligibil SI suma <= 100 RON:
        rezultat = proceseaza_controlat()
        DACA rezultat.confirmat:
            text = AI.redacteaza_confirmare(rezultat)
            trimite_email(text)
    ALTFEL: escaladeaza()
```

AI interpreteaza emailul si redacteaza un mesaj, dar nu alege liber traseul complet. Workflow-ul poate avea ramificatii, etape paralele si rutare cu AI fara a deveni automat un agent.

### E3. Agent AI: modelul propune urmatoarea actiune

Agentul primeste obiectivul, instructiunile, contextul, instrumentele disponibile si o bucla de actiune-feedback. El poate decide sa caute comanda, sa verifice istoricul, sa ceara o fotografie sau sa escaladeze cazul. **Autorizarea nu vine din prompt.**

```text
OBIECTIV = "Rezolva cererea de rambursare"
INSTRUMENTE = [cauta_comanda, verifica_politica,
               verifica_duplicat, cere_dovezi, pregateste_rambursare,
               verifica_rezultat, trimite_confirmare, escaladeaza]
CONTEXT = [cerere, rezultate_verificate, actiuni_anterioare]

REPETA maximum 12 pasi:
    actiune = MODEL.alege_urmatorul_pas(OBIECTIV, CONTEXT, INSTRUMENTE)
    DACA actiunea este interzisa: escaladeaza(); OPRESTE
    DACA actiunea produce rambursare:
        verifica_identitate_eligibilitate_moneda_suma()
        verifica_duplicat_si_aprobare()
        DACA verificarea_esueaza: escaladeaza(); OPRESTE
    rezultat = DISPATCHER.executa_doar_actiunea_autorizata(actiune)
    CONTEXT.adauga(rezultat)
    DACA asteptam_clientul: salveaza_starea(); OPRESTE_TEMPORAR
    DACA rezultatul_final_este_verificat: OPRESTE
ALTFEL: escaladeaza_pentru_limita_de_pasi()
```

O bucla `REPETA` nu defineste singura un agent: conteaza daca modelul poate alege dinamic actiunile. Dispatcher-ul din aplicatie trebuie sa valideze argumentele, permisiunile, limitele si rezultatele.

**Trei cazuri:** 62 RON cu dovezi complete -> pregatire si verificare a operatiunii; 350 RON -> escalare fara plata; lipsa dovezii -> solicitare de clarificari si stare `WAITING_CUSTOMER`. Reincercarea unui API dupa timeout cere mai intai reconcilierea tranzactiei, ca sa nu rambursam de doua ori.

### E4. Configuratie de demonstratie

```yaml
name: refund_assistant_demo
model:
  provider: mock
  name: qwen2.5:14b
policy:
  currency: RON
  auto_refund_max: 100.00
  max_steps: 12
  require_verified_customer: true
  require_proof_for_damage: true
  allow_production_refunds: false
safety:
  backend: sandbox
  idempotency: request_id
```

**Citirea configuratiei:** `mock` inseamna model simulat, `sandbox` inseamna fara operatii financiare reale, iar `request_id` este cheia folosita pentru a recunoaste aceeasi cerere. YAML este un format de configurare, nu un standard Shopify. Un test cu mock verifica regulile simulatoare, nu demonstreaza integrarea reala. Pentru Shopify, mutatia `refundCreate` necesita o cheie de idempotenta in versiunile API incepand cu 2026-04. [Documentatie Shopify](https://shopify.dev/docs/api/admin-graphql/2026-10/mutations/refundCreate).

**Evaluare:** verificam separat 62 RON, 350 RON, lipsa dovezii, client neverificat, solicitare duplicata, API indisponibil, unealta interzisa si limita de pasi. Pentru tranzactii, o singura plata neautorizata este un defect critic, indiferent de rata globala de succes.

## 21.8. Studiul de caz F: cercetare YouTube si productie editoriala cu doi agenti

**Scop:** un creator urmareste canalele X, Y si Z, vrea sa detecteze materiale noi, sa obtina idei originale si sa aprobe personal orice publicare. Materialul analizat apartine creatorilor sai; ideile trebuie dezvoltate independent si conditiile platformei respectate.

### F1. Inaintea agentilor: automatizare si workflow

O automatizare clasica salveaza titlul, descrierea si URL-ul videoclipurilor noi. Un workflow AI poate adauga un rezumat al datelor accesibile si o schita de scenariu, prin etape prestabilite. Nu este obligatoriu sa introducem agenti daca asta rezolva problema.

### F2. Agentul Research: documentare si propuneri

Agentul primeste obiectivul editorial, canalele, publicul tinta, istoria propriilor materiale si reguli de cercetare. Poate alege ce metadate sa compare si unde sa caute documentatie suplimentara. Foloseste numai surse si unelte autorizate.

```text
PERIODIC: preia_metadate_noi(); elimina_duplicate()
PENTRU cel_mult_N_iteratii:
    actiune = RESEARCH.alege_urmatoarea_actiune()
    DACA cere o sursa permisa: consulta_sursa()
    DACA informatia este insuficienta: marcheaza_incertitudine()
    DACA propunerea este documentata: finalizeaza_brief(); OPRESTE
```

Titlurile, descrierile si data publicarii sunt **metadate**, nu transcrieri. Nu putem afirma ca agentul a analizat integral un videoclip pentru care nu are acces la continut. Nici trei videoclipuri asemanatoare nu confirma singure un trend.

Exemplu de propunere: „De ce nu orice workflow AI este automat agent AI?”, cu trei titluri candidate, o schita de clip de 60–90 secunde si sursele documentate.

### F3. Contractul de predare catre Production

```yaml
handoff_id: VID-041
from: research_agent
to: production_agent
status: READY_FOR_DRAFT
proposed_topic: "De ce nu orice AI workflow este agent?"
analysis_scope: metadata_only
source_urls:
  - "https://www.youtube.com/watch?v=EXEMPLU_1"
  - "https://www.youtube.com/watch?v=EXEMPLU_2"
limitations:
  - "Transcrierile altor autori nu au fost accesate"
  - "Trendul nu este demonstrat"
requested_variants: 3
requires_human_approval: true
```

Identificatorii de mai sus sunt fictivi. Contractul este un artefact de predare, nu o dovada ca sursele au fost vizionate ori verificate. `READY_FOR_DRAFT` permite redactarea, nu publicarea.

### F4. Agentul Production: trei variante si aprobare

Production poate folosi **acelasi model** ca Research, dar primeste alte instructiuni, contexte si instrumente. El propune variantele A (scurt si dinamic), B (explicativ cu diagrame) si C (demonstratie practica). Video-ul efectiv necesita un motor de randare, continut vizual autorizat si integrare tehnica.

```text
DACA handoff_invalid: OPRESTE
PENTRU stil IN [A, B, C]:
    genereaza_scenariu_original()
    genereaza_storyboard()
    verifica_durata_si_afirmatiile_factuale()
    DACA exista_renderer_autorizat: genereaza_preview()
    ALTFEL: livreaza_documente_de_productie()
STATUS = WAITING_HUMAN_APPROVAL
```

Utilizatorul poate aproba, combina sau respinge variante. Aprobarea trebuie asociata **hash-ului artefactului concret**; orice modificare ulterioara necesita o noua aprobare. Incarcarea unui clip pe canal necesita OAuth si drepturi efective de publicare, iar schimbarea vizibilitatii din privat in public poate cere o aprobare distincta. In configuratia didactica publicarea este dezactivata.

```yaml
name: editorial_research_demo
research:
  source_mode: fixture
  max_videos: 12
  allowed_content: metadata_only
  allow_third_party_caption_download: false
production:
  variant_names: [scurt_dinamic, explicativ, demonstratie]
  video_renderer: not_configured
  publisher: disabled
  approval_required: true
  publish_default_privacy: private
```

`fixture` inseamna date de test cunoscute. YouTube Data API permite citirea anumitor metadate publice, dar `captions.download` necesita drept de editare a videoclipului, deci nu ofera transcrierile oricarui creator: [PlaylistItems.list](https://developers.google.com/youtube/v3/docs/playlistItems/list), [Captions.download](https://developers.google.com/youtube/v3/docs/captions/download), [Videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert).

**Evaluare:** urmarim identificarea clipurilor noi, duplicatele, provenienta surselor, afirmatiile neverificate, originalitatea scenariilor, versiunile aprobate si absenta oricarei publicari neautorizate. Un sistem care produce trei scenarii JSON nu a generat trei videoclipuri MP4.

## 21.9. Comparatie: cine decide pasul urmator?

| Sistem | Traseu | Decizia AI | Control necesar |
| --- | --- | --- | --- |
| Automatizare clasica | Ramificatii programate | Nu este necesara | Validari si drepturi in cod |
| Workflow AI | Trasee definite in avans | Interpretare si decizii delimitate | Scheme, conditii, aprobari |
| Agent AI | Obiectiv si limite fixe; pasi dinamici | Modelul propune urmatoarea actiune | Dispatcher, verificari, buget si oprire |
| Doi agenti | Contract de predare si responsabilitati distincte | Alegeri in aria fiecarui agent | Validarea handoff-ului si a livrabilelor |
| „AI Employee” | Responsabilitate recurenta | Optional, daca include agenti | Monitorizare, escalare si responsabil uman |

„AI Employee” este o **eticheta operationala sau comerciala**, nu o categorie tehnica standard si nici o garantie de memorie persistenta ori autonomie nelimitata. Un scheduler, o baza de date si un agent pot colabora fara sa transforme fiecare componenta intr-un agent.

**Regula practica:** alegem cel mai simplu sistem care rezolva verificabil problema. Daca deciziile sunt previzibile, folosim reguli; daca doar anumite etape cer interpretare, folosim workflow AI; daca ordinea actiunilor trebuie adaptata dinamic, evaluam un agent; daca apar responsabilitati distincte, evaluam orchestrarea. Alegerea trebuie sustinuta de rezultate, nu de numarul agentilor.

Studiile E si F sunt **fictive**. Pseudocodul ilustreaza arhitectura, configurarile YAML sunt demonstrative, iar teste cu mock nu reprezinta probe de plata Shopify, transcriere YouTube ori incarcare video reala. Recomandarea de a incepe cu cea mai simpla arhitectura este sustinuta de [Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents).

