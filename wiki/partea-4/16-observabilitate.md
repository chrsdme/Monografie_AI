# 16. Observabilitatea: vedem ce a facut efectiv sistemul

## 16.1. De ce raspunsul final nu ajunge

Un agent poate spune "am verificat datele si totul e in regula". Fraza asta nu te lasa sa afli daca a citit documentul corect, daca a folosit unealta necesara sau daca a inventat o concluzie. La o intrebare banala poti accepta incertitudinea. La un proces care modifica documente, cod sau plati, nu.

**Observabilitate** inseamna sa poti intelege comportamentul unui sistem din dovezile pe care le produce: jurnale, evenimente, metrici si trace-uri. Un **log** inregistreaza un eveniment. Un **trace** leaga operatiile care apartin aceleiasi cereri si arata relatiile dintre ele. O **metrica** agrega valori precum durata, rata erorilor sau costul. Nu sunt sinonime, iar niciuna nu demonstreaza singura ca rezultatul e corect.

## 16.2. Patru elemente minime pentru un agent care foloseste unelte

Pentru o investigatie tehnica ai nevoie, cel putin, de: **(1) cererea si instructiunile relevante**, **(2) apelurile de unelte, cu argumentele lor**, **(3) rezultatele reale ale uneltelor** si **(4) raspunsul sau artefactul final**. Ca sa le completezi, adaugi identitatea rularii, versiunea modelului sau a serviciului, identificatorii documentelor, momentele executiei si deciziile de aprobare. Datele sensibile se protejeaza, nu se inregistreaza fara limite.

Exemplul meteo ramane potrivit. Daca utilizatorul cere Paris, Franta, iar agentul interogheaza Paris, Texas, raspunsul final poate parea plauzibil. Abia logul geocodarii explica eroarea. Daca unealta a returnat 18 grade si agentul a raspuns 28, avem alt tip de defect. Remedierea depinde de cauza.

## 16.3. Un trace de la intrare la verdict

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

## 16.4. Cum evitam logurile care nu mai pot fi folosite

Daca logezi integral fiecare intrare, ajungi la volume mari si la riscuri de confidentialitate. Un sistem matur poate pastra evenimentele operationale mai mult timp si continutul detaliat doar cat e necesar. Poti esantiona cererile obisnuite si pastra urme complete pentru incidente, erori si teste controlate, cu respectarea regulilor de protectie a datelor. Politica se defineste inainte de productie, nu se improvizeaza dupa un incident.

Logurile trebuie sa si poata fi corelate. Daca o cerere trece prin trei servicii si cinci agenti, fiecare eveniment poarta identificatori care permit reconstituirea traseului. Standardizarea sensului evenimentelor ajuta cand schimbi framework-ul, de aceea conventiile OpenTelemetry sunt relevante, cu rezerva ca au statutul "Development" si pot evolua [S12](../anexe/bibliografie.md#s12). Printre atributele definite se numara si cele pentru consumul de tokeni de intrare si de iesire, utile pentru analiza costurilor.

## 16.5. Efectiv versus declarat

Una dintre cele mai folositoare reguli este sa separi **actiunile observate** de **actiunile declarate**. Daca agentul spune ca a rulat un test, cauti dovada in jurnalul executiei. Daca spune ca a verificat o sursa, cauti referinta sau rezultatul apelului. Daca spune ca a livrat un fisier, verifici ca fisierul exista si ce contine. Disciplina asta elimina o categorie surprinzator de mare de neintelegeri.
