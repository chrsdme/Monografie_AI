# 16. Observabilitatea: vedem ce a facut efectiv sistemul

## 16.1. De ce raspunsul final nu este suficient

Un agent poate spune „am verificat datele si totul este in regula”. Fraza nu ne permite sa stabilim daca a citit documentul corect, daca a folosit instrumentul necesar sau daca a inventat o concluzie. Pentru o intrebare banala putem accepta acest nivel de incertitudine. Pentru un proces care modifica documente, cod sau plati, nu este suficient.

**Observabilitate** inseamna capacitatea de a intelege comportamentul unui sistem din dovezile pe care le produce: jurnale, evenimente, metrici si trace-uri. Un **log** inregistreaza un eveniment. Un **trace** leaga operatiile care apartin aceleiasi cereri si arata relatiile dintre ele. O **metrica** agrega valori precum durata, rata erorilor sau costul. Nu sunt sinonime si niciuna nu demonstreaza singura corectitudinea rezultatului.

## 16.2. Patru elemente minime pentru un agent care foloseste unelte

Pentru o investigatie tehnica avem nevoie, cel putin, de: **(1) cererea si instructiunile relevante**, **(2) apelurile de instrumente cu argumentele lor**, **(3) rezultatele efective ale instrumentelor** si **(4) raspunsul sau artefactul final**. La acestea adaugam identitatea rularii, versiunea modelului sau serviciului, identificatorii documentelor, momentele executiei si deciziile de aprobare. Datele sensibile trebuie protejate, nu inregistrate fara limite.

Exemplul meteo ramane potrivit: daca utilizatorul cere Paris, Franta, dar agentul interogheaza Paris, Texas, raspunsul final poate fi plauzibil. Abia un log al geocodarii explica eroarea. Daca instrumentul a returnat 18 grade, iar agentul a raspuns 28, avem alta categorie de defect. Remedierea depinde de identificarea cauzei.

## 16.3. Un exemplu de trace, de la intrare la verdict

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

Aici observam ca procesarea a avut loc si ca exista o neconcordanta. Nu putem concluziona insa ca toate documentele care au trecut verificarile automate au fost clasificate perfect. Pentru aceasta avem nevoie de teste si comparatii independente. Observabilitatea raspunde mai intai la intrebarea **ce s-a intamplat?**, evaluarea raspunde la **cat de corect a fost?**.

## 16.4. Cum evitam logurile imposibil de folosit

Logarea integrala a fiecarei intrari poate produce volume mari si riscuri de confidentialitate. Un sistem matur poate pastra evenimentele operationale pe termen mai lung si continutul detaliat doar cat este necesar. Putem esantiona cereri obisnuite, dar pastra urme complete pentru incidente, erori si teste controlate, respectand regulile de protectie a datelor. Politica trebuie definita inainte de productie, nu improvizata dupa un incident.

In plus, logurile trebuie sa poata fi corelate. Daca o cerere trece prin trei servicii si cinci agenti, fiecare eveniment trebuie sa poarte identificatori care permit reconstructia traseului. Standardizarea semnificatiei evenimentelor ajuta cand schimbam framework-ul, motiv pentru care conventiile OpenTelemetry sunt relevante [S12].

## 16.5. Efectiv versus declarat

Una dintre regulile cele mai folositoare este separarea dintre **actiuni observate** si **actiuni declarate**. Daca agentul afirma ca a rulat un test, cautam dovada in jurnalul executiei. Daca spune ca a verificat o sursa, cautam referinta sau rezultatul apelului. Daca spune ca a livrat un fisier, verificam existenta si continutul fisierului. Aceasta disciplina elimina o categorie surprinzator de mare de neintelegeri.
