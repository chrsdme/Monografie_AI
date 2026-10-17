# 12. Anatomia unui agent: rol, model, instrumente, stare si limite

## 12.1. Agentul nu este doar un system prompt

Un prompt care spune "Esti un expert contabil" exprima o intentie, nu un sistem contabil. Pentru un agent operational ai nevoie de un executant cu acces la model, un set de unelte, un obiectiv, un context, o stare a sarcinii si reguli de terminare. Poti adauga memorie, verificari si interactiune umana. Nu toate se vad utilizatorului, dar fara ele autonomia ramane mai mult o eticheta.

**Rolul** spune ce responsabilitate are agentul. **Modelul** e motorul de generare. **Uneltele** delimiteaza capacitatile concrete. **Contextul** ii da datele relevante. **Starea** ii permite sa continue un proces in mai multi pasi. **Politicile** controleaza ce operatii sunt admise. **Criteriile de acceptare** definesc succesul. **Jurnalul** arata ce s-a executat.

## 12.2. Un contract de agent

Pentru un agent care analizeaza documente, un contract simplificat ar putea arata asa:

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

E un exemplu conceptual, nu un format obligatoriu pentru vreun framework. Rolurile si permisiunile se aplica in aplicatie, iar campurile de acceptare trebuie transformate in verificari reale. O lista YAML nu poate bloca singura nicio operatie. Pentru a lega contractul de problema reala si de criteriile succesului, vezi [Intent Engineering (6.7)](https://chrsdme.github.io/Monografie_AI/partea-2/06-prompturi-instructiuni-briefuri/#67-intent-engineering-de-la-cerere-la-obiectiv-verificabil).

## 12.3. Starea si sesiunile

O **sesiune** poate pastra conversatia si rezultatele relevante. Un **run** este o executie concreta a unei sarcini. Un **task** este o unitate de lucru cu obiectiv si criterii de finalizare. Un run poate contine mai multe apeluri de model si de unelte. O sesiune poate avea mai multe run-uri, iar un workflow poate cuprinde sarcini si sesiuni diferite. Terminologia exacta variaza intre produse; aici o folosim consecvent, pentru claritate.

De exemplu, "revizuieste documentele de azi" poate produce un run care citeste 30 de documente si returneaza 30 de rezultate. Daca agentul se intrerupe dupa al cincisprezecelea, o reluare corecta cere sa stii ce documente au fost deja procesate si care operatii au efecte secundare. Starea asta trebuie pastrata in afara povestii pe care modelul o spune despre ce a facut.

## 12.4. Cand se opreste agentul?

Un agent nu trebuie sa mearga pana "se simte gata". Conditiile de oprire pot fi: obiectivul indeplinit cu dovezi, lipsa unei informatii esentiale, depasirea bugetului, repetarea aceleiasi actiuni fara progres, esecul unei verificari critice sau nevoia de aprobare umana. Orice bucla are nevoie de un capat.

## 12.5. Autoevaluarea si limitele ei

Un agent poate compara raspunsul cu o schema, isi poate verifica rezumatul si poate cere teste. Sunt operatii utile. Dar **autoevaluarea narativa**, de tipul "cred ca rezultatul e corect", nu este o verificare independenta. Preferam dovezi observabile: comenzi rulate, rezultate de test, comparatii cu surse si controale programatice.

## 12.6. Cand nu avem nevoie de un agent

Daca ai de convertit un CSV in JSON dupa o schema fixa, o biblioteca existenta e de obicei mai previzibila. Daca trebuie programat un raport zilnic fara interpretarea unor date nestructurate, un scheduler si un script pot fi suficiente. Modelul se adauga acolo unde judecata flexibila aduce valoare, nu in fiecare pas, ca sa poti spune ca sistemul e "agentic".
