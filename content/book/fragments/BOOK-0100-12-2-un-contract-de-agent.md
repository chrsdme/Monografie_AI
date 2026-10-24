### 12.2. Un contract de agent

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

