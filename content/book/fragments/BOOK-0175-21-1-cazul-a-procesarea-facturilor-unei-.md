### 21.1. Cazul A: procesarea facturilor unei firme mici

**Situatia initiala.** O firma primeste lunar intre 50 si 150 de facturi, prin email si intr-un portal. Unele sunt PDF-uri cu text, altele scanari. O persoana trebuie sa identifice furnizorul, numarul, suma, moneda si scadenta, sa compare cu registrul si sa semnaleze dublurile. Volumul nu e urias, dar operatiile repetitive consuma timp.

**Nivelul 1: chat.** Utilizatorul intreaba un model ce campuri conteaza intr-o factura si cere o lista de verificare. Modelul explica si, eventual, redacteaza un sablon de tabel. Nu citeste automat niciun document. Beneficiul e cognitiv: omul intelege mai repede procesul.

**Nivelul 2: lucrul cu documente.** Utilizatorul incarca cinci facturi si cere extragerea campurilor. Modelul returneaza un tabel. Omul compara valorile cu documentele, mai ales sumele, numerele si datele. Daca un scan e ilizibil, o reactie buna este sa marcheze campul "necunoscut", nu sa il inventeze. Criteriul de acceptare e corespondenta dintre sursa si tabel.

**Nivelul 3: unelte.** Aplicatia poate citi atasamente printr-un conector autorizat, poate apela un serviciu de extragere a textului si poate cauta furnizorul intr-un registru. Modelul ajuta la interpretarea formatelor variabile. Validarea campurilor obligatorii si calculul totalurilor se fac in cod. Un jurnal inregistreaza documentul, rezultatul extragerii si orice diferenta. Nu e nevoie de autonomie completa.

**Nivelul 4: workflow fix.** La sosirea unui email de la un expeditor permis, sistemul salveaza atasamentul, identifica tipul documentului, extrage campurile, compara cu registrul si pregateste o inregistrare. Cand gaseste o diferenta, o trimite intr-o coada de verificare. Procesul e determinist la exterior, cu AI doar in componenta care interpreteaza documentul. Daca arata bine la teste reprezentative, poate fi deja sistemul final.

**Nivelul 5: agent pentru exceptii.** Sa presupunem ca furnizorii trimit formate foarte diferite, iar unele facturi fac referire la comenzi care trebuie cautate in alt sistem. Agentul poate cerceta neconcordanta cu unelte de citire, poate propune o explicatie si poate pregati un dosar pentru operator. Nu primeste dreptul de plata. Plata cere un flux separat, cu autentificare si aprobare.

**Nivelul 6: orchestrare justificata.** Daca procesul creste la sute de documente pe zi si include verificari fiscale, contracte si comenzi de achizitie, un orchestrator poate distribui extragerea, reconcilierea si verificarea. Operatiile au contexte si drepturi separate. Tot nu creezi un agent pentru fiecare camp din factura.

