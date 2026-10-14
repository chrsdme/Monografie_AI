# 12. Anatomia unui agent: rol, model, instrumente, stare si limite

## 12.1. Agentul nu este doar un system prompt

Un prompt care spune „Esti un expert contabil” defineste o intentie, nu un sistem contabil. Ca sa existe un agent operational, avem nevoie de un executant cu acces la model, un set de instrumente, un obiectiv, un context, o stare a sarcinii si reguli de terminare. Putem adauga memorie, verificari si interactiune umana. Nu toate sunt vizibile utilizatorului, dar fara ele autonomia ramane mai mult o eticheta.

**Rolul** spune ce responsabilitate are agentul. **Modelul** este motorul de generare. **Instrumentele** delimiteaza capacitatile concrete. **Contextul** ii ofera datele relevante. **Starea** ii permite sa continue un proces in mai multi pasi. **Politicile** controleaza ce operatii sunt admise. **Criteriile de acceptare** definesc succesul. **Jurnalul** arata ce s-a executat.

## 12.2. Un contract de agent

Pentru un agent care analizeaza documente, un contract simplificat ar putea fi:

```yaml
name: invoice_reviewer
responsibility: "Extrage si verifica date de pe facturi"
input: "Documente si reguli validate"
output: "Inregistrari structurate + neconcordante + surse"
tools:
  - read_document
  - lookup_supplier
  - query_invoice_registry
permissions:
  - read_only
forbidden:
  - create_payment
  - delete_invoice
acceptance:
  - required_fields_present
  - totals_reconciled
  - sources_recorded
on_failure: "Raporteaza eroarea si cere verificare"
```

Acesta este un exemplu conceptual, nu un format obligatoriu pentru un framework. Rolurile si permisiunile trebuie aplicate in aplicatie, iar campurile de acceptare trebuie transformate in verificari reale. O lista YAML nu poate bloca singura o operatie.

## 12.3. Starea si sesiunile

O **sesiune** poate pastra conversatia si rezultatele relevante. Un **run** este o executie concreta a unei sarcini. Un **task** este o unitate de lucru cu obiectiv si criterii de finalizare. Un run poate contine mai multe apeluri de model si instrumente. O sesiune poate include mai multe run-uri, iar un workflow poate cuprinde sarcini si sesiuni diferite. Terminologia exacta variaza intre produse; aici o folosim consistent pentru claritate.

De exemplu, „revizuieste documentele de azi” poate produce un run care citeste 30 de documente si returneaza 30 de rezultate. Daca agentul este intrerupt dupa al cincisprezecelea, reluarea corecta inseamna sa cunoastem ce documente au fost deja procesate si ce operatii au efecte secundare. Aceasta stare trebuie pastrata in afara simplei povesti pe care modelul o spune despre ce a facut.

## 12.4. Cand se opreste agentul?

Un agent nu trebuie sa functioneze pana „se simte gata”. Conditiile de oprire pot include finalizarea obiectivului cu dovezi, lipsa informatiei esentiale, depasirea bugetului, repetarea aceleiasi actiuni fara progres, esecul unei verificari critice sau necesitatea aprobarii umane. Orice bucla are nevoie de un capat.

## 12.5. Autoevaluarea si limitele ei

Un agent poate compara raspunsul cu o schema, isi poate verifica sumarul si poate solicita teste. Aceste operatii sunt utile. Dar **autoevaluarea narativa** de tipul „consider ca rezultatul este corect” nu constituie o verificare independenta. Preferam dovezi observabile: comenzi executate, rezultate de test, comparatii cu surse si controale programatice.

## 12.6. Cand nu avem nevoie de un agent

Daca avem doar de convertit un CSV in JSON folosind o schema fixa, o biblioteca existenta este in general mai predictibila. Daca trebuie sa programam un raport zilnic fara interpretarea unor date nestructurate, un scheduler si un script pot fi suficiente. Modelul trebuie adaugat acolo unde judecata flexibila aduce valoare, nu in fiecare pas pentru a putea spune ca sistemul este „agentic”.
