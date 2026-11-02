### 8.11. Cautarea hibrida: de ce merita sa combinam cuvintele si sensul

Intr-o colectie de documente, unele intrebari depind de sens, iar altele de o potrivire exacta. Sa presupunem ca un client intreaba „Care este scadenta facturii FCT-2026-017?”. O cautare semantica poate gasi documente despre scadente, dar poate omite factura cu identificatorul exact. O cautare lexicala poate gasi acel cod, dar poate rata o intrebare formulata prin sinonime.

**Cautarea lexicala** foloseste cuvintele din interogare si din documente. O metoda des intalnita este **BM25**, care estimeaza relevanta textuala in functie de potrivirile termenilor si de caracteristicile documentelor. **Cautarea vectoriala** compara reprezentari numerice pentru a aproxima apropierea semantica. Niciuna nu castiga in toate situatiile.

**Cautarea hibrida** combina rezultatele celor doua metode. O tehnica pentru reunirea listelor se numeste **Reciprocal Rank Fusion (RRF)**: in loc sa adune scoruri foarte diferite, metoda foloseste pozitiile documentelor in clasamentele separate [S51]. Un document poate urca in lista daca este relevant atat lexical, cat si semantic.

Dupa recuperare, un **reranker** poate reordona un grup mic de candidati folosind o evaluare mai detaliata a relatiei dintre intrebare si pasaj. Un reranker nu repara faptul ca documentul corect lipseste complet din lista de candidati. Din acest motiv, cautarea si reordonarea trebuie masurate separat.

Un traseu simplificat, complet ilustrativ:

```text
Intrebare: "Cand trebuie achitata FCT-2026-017?"
      |
      v
verificare identitate + autorizare; stabilire domeniu permis
      |
      +--> cautare lexicala DOAR in documentele autorizate
      +--> cautare vectoriala DOAR in documentele autorizate
      |
      v
combinare rezultate autorizate (de exemplu RRF)
      |
      v
optional: reranking doar pe candidatii autorizati
      |
      v
raspuns + identificatorul documentului + verificarea valorii
```

**Atentie:** controlul accesului se aplica inaintea cautarii, pe domeniul de documente permis utilizatorului, si ramane obligatoriu la recuperare, reranking si afisare. Nu trimitem pasaje neautorizate nici catre motorul de reordonare, nici catre model. Filtrarea afisajului abia la final nu inlocuieste izolarea surselor.

