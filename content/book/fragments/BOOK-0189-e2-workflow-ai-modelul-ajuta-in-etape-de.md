#### E2. Workflow AI: modelul ajuta in etape delimitate

```text
LA primirea unui email:
    intentie, order_id = AI.extrage_date(email)
    DACA order_id_lipseste: solicita_completare(); OPRESTE
    comanda = cauta_comanda(order_id)
    eligibil = valideaza_in_cod(comanda, client)
    DACA eligibil SI suma <= 100 RON:
        rezultat = proceseaza_controlat()
        DACA rezultat.confirmat:
            text = AI.redacteaza_confirmare(rezultat)
            trimite_email(text)
    ALTFEL: escaladeaza()
```

AI interpreteaza emailul si redacteaza un mesaj, dar nu alege liber traseul complet. Workflow-ul poate avea ramificatii, etape paralele si rutare cu AI fara a deveni automat un agent.

