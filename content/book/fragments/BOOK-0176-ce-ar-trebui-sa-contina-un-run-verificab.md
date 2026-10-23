#### Ce ar trebui sa contina un run verificabil

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

