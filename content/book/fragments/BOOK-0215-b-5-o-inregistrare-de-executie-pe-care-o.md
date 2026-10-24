## B.5. O inregistrare de executie pe care o putem audita

```text
run_id: 2026-10-13-00042
agent_class: QA
agent_config_version: 1.3
model_identifier: model/version, daca este disponibil
request_id: ticket-122
input_reference: cerere-122-rev2
context_sources: [spec-122, policy-returns-rev5]
tool_calls: [nume, argumente validate, moment]
tool_results: [status, identificator, verificari]
output_artifact: review-122.md
independent_checks: [check-schema PASS, check-total PASS]
final_status: ACCEPTED / REJECTED / ESCALATED
owner_approval: required / not_required / approved
```

Nu orice jurnal trebuie sa pastreze integral continutul sensibil al documentelor. Poti pastra referinte, hash-uri, metadate si rezultate de verificare, iar continutul brut doar daca politica de securitate si nevoia de audit il justifica. Cu cat sistemul vorbeste cu mai multe aplicatii, cu atat conteaza mai mult corelarea prin `run_id`.

