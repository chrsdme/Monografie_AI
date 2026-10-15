# 8. Cunostinte externe, memorie si RAG

## 8.1. De ce avem nevoie de informatii din afara modelului

Un model poate explica principiile contabilitatii, dar nu cunoaste automat facturile unei firme. Poate descrie un limbaj de programare, dar nu stie fara acces cum arata ultima versiune a codului nostru. Sa-i repetam manual toate documentele la fiecare cerere este incomod, iar introducerea integrala a unei arhive mari poate depasi contextul ori poate inrautati relevanta.

Solutia este sa pastram documentele intr-un sistem separat si sa recuperam numai fragmentele necesare. Aceasta familie de metode este cunoscuta sub numele de **RAG**: *Retrieval-Augmented Generation*. Lucrarea de referinta a lui Lewis si colaboratorii din 2020 a descris combinarea generarii cu recuperarea informatiei dintr-o memorie externa [S08]. De atunci, termenul este folosit pentru multe implementari practice, nu doar pentru arhitectura exacta din articolul original.

## 8.2. RAG in cinci pasi

1. Avem o colectie de documente sau inregistrari, de exemplu regulile unei firme.
2. Sistemul pregateste documentele pentru cautare: extrage text, separa fragmente, retine metadate si eventual calculeaza reprezentari numerice.
3. Utilizatorul pune o intrebare, de exemplu „Care este termenul de retur pentru produsul X?”.
4. Sistemul cauta fragmente relevante si le trimite modelului impreuna cu intrebarea.
5. Modelul redacteaza raspunsul folosind materialul recuperat, eventual cu indicarea sursei.

Un **embedding** este o reprezentare numerica a continutului, utila in unele sisteme de cautare semantica. O **baza vectoriala** poate stoca asemenea reprezentari si cauta vecini similari. Dar RAG nu necesita in mod obligatoriu o baza vectoriala: cautarea dupa cuvinte-cheie, SQL sau o combinatie intre metode pot fi suficiente, uneori chiar mai potrivite.

## 8.3. Ce poate sa mearga prost intr-un RAG

Recuperarea gresita este una dintre cele mai subtile probleme. Daca intrebam de politica de retur din 2026 si sistemul aduce politica din 2023, modelul poate produce un raspuns elegant, dar depasit. Daca documentele sunt impartite in fragmente prea mici, se pierde contextul. Daca sunt prea mari, cautarea devine mai putin precisa. Daca informatia nu exista, modelul trebuie sa poata spune ca sursele nu sunt suficiente.

RAG nu elimina halucinatiile si nu transforma automat o sursa intr-una credibila. O pagina web poate contine informatii false. Mai mult, documentele recuperate pot contine instructiuni malitioase. De aceea, calitatea recuperarii, calitatea raspunsului si securitatea surselor sunt trei evaluari distincte [S09].

## 8.4. Ce inseamna memoria unui agent

**Memoria de lucru** este informatia din contextul curent: obiective, rezultate recente, pasi in curs. **Memoria persistenta** este informatia salvata intre executii: preferinte, decizii confirmate, rezumate de proiect, fapte cu surse. **Memoria episodica** poate descrie executarile anterioare, iar **memoria semantica** poate reuni cunostinte despre domeniu. Sunt termeni utili, dar implementarea concreta poate fi mult mai simpla: fisiere, baze SQL, un registru de decizii sau un motor de cautare.

Nu trebuie sa confundam o nota scrisa automat cu un fapt verificat. Daca un agent memoreaza din greseala ca un proiect foloseste versiunea 3 a unei biblioteci, iar proiectul foloseste de fapt versiunea 2, memoria poate propaga eroarea la fiecare sarcina urmatoare. De aceea, informatiile persistente ar trebui sa pastreze sursa, data, domeniul de valabilitate si, unde este cazul, statutul de confirmare.

## 8.5. Cine actualizeaza memoria si cand?

Un mecanism simplu poate salva la finalul unei sarcini doar deciziile aprobate si faptele verificate. Informatiile temporare, presupunerile si incercarile esuate raman in jurnal, dar nu devin automat reguli permanente. Pentru proiecte lungi, memoria poate avea niveluri: reguli generale, decizii ale proiectului, starea unei executii si documente recuperabile.

**Stergerea si expirarea** fac parte din design. Unele informatii sunt valabile numai pana la urmatoarea factura, pana la schimbarea versiunii software sau pana la o anumita data. O memorie buna stie nu numai ce sa pastreze, ci si cand sa nu se mai bazeze pe un lucru vechi.

## 8.6. RAG si memoria nu sunt acelasi lucru

RAG este o **metoda de a recupera informatie pentru generare**. Memoria desemneaza **ce informatie este pastrata si cum supravietuieste intre sarcini**. Putem folosi RAG peste o biblioteca de manuale fara sa avem memorie personala. Putem avea memorie persistenta intr-o baza SQL fara sa folosim RAG. Deseori cele doua se combina, dar au responsabilitati diferite.


## 8.7. Provenienta, versiunea si expirarea cunostintelor

O baza de cunostinte nu este doar o colectie de raspunsuri reutilizabile. Fiecare afirmatie importanta ar trebui sa poata indica sursa originala, data consultarii, versiunea relevanta si statutul verificarii. Acest principiu apare si in ghidurile practice despre construirea unei baze personale de cunostinte tehnice: separam sursa, interpretarea si experimentul [S21].

Sa presupunem ca pastram regula „clientii pot returna produsele in 30 de zile”. Intre timp, firma schimba politica la 14 zile pentru o anumita categorie. Daca agentul recupereaza nota veche fara data, poate produce un raspuns perfect formulat, dar incorect. Solutia nu este un prompt mai autoritar. Avem nevoie de o sursa oficiala, actualizare, identificarea versiunii si eliminarea ori marcarea drept expirate a fragmentelor vechi.

Acelasi principiu se aplica documentatiei software, preturilor, procedurilor interne si notelor de cercetare. Un rezultat de test trebuie pastrat impreuna cu mediul in care a fost obtinut. „A functionat” este insuficient daca nu mai stim ce versiune, ce fisiere sau ce configuratie au fost folosite.

## 8.8. Un flux de cunoastere cu aprobare

Intr-un sistem robust, agentul poate propune o noua nota de memorie, dar o regula sau un responsabil verifica daca nota reprezinta un fapt, o preferinta, o ipoteza sau doar un rezultat temporar. O concluzie neverificata nu trebuie transformata in regula generala pentru toate executarile viitoare. De asemenea, nu pastram inutil date sensibile doar pentru ca pot deveni folositoare candva.

Un ciclu simplu ar fi: *sursa identificata → extras verificabil → interpretare marcata → validare → stocare cu versiune → reevaluare la expirare*. Este acelasi reflex pe care il folosim la un jurnal tehnic bine intretinut, aplicat memoriei unui sistem AI.
