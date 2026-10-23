### 16.3. Un trace de la intrare la verdict

```text
TRACE report-0082
  10:00:00 input accepted       user_id=...  task=invoice_report
  10:00:01 permissions checked  allow=read-only
  10:00:02 document search      period=2026-09  found=24
  10:00:04 extraction          processed=24  invalid=2
  10:00:06 validation          totals_mismatch=1
  10:00:07 result prepared     status=needs_review
  10:00:08 human approval      pending
```

Vedem ca procesarea a avut loc si ca exista o neconcordanta. Nu putem concluziona insa ca cele 22 de documente valide au fost clasificate perfect. Pentru asta ai nevoie de teste si comparatii independente. Observabilitatea raspunde intai la intrebarea **ce s-a intamplat?**, iar evaluarea la **cat de corect a fost?**.

