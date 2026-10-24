#### E1. Automatizare clasica: codul decide

```text
LA primirea unei cereri:
    verifica_identitatea()
    comanda = obtine_comanda()
    DACA eligibila(comanda) SI dovada_suficienta
         SI nu_exista_rambursare SI suma <= 100 RON:
         initiaza_cu_cheie_de_idempotenta()
         reconciliaza_rezultatul()
         confirma_doar_dupa_succes()
    ALTFEL: escaladeaza()
```

Nu exista un LLM. Ramificatiile sunt programate, iar operatiile cu efect extern sunt controlate in cod. Daca datele sunt standardizate si regulile suficiente, aceasta poate fi alegerea potrivita.

