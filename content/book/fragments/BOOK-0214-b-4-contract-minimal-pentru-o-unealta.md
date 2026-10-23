## B.4. Contract minimal pentru o unealta

O unealta care modifica date are nevoie de un comportament mai precis decat "actualizeaza comanda". Un exemplu generic:

```text
Operatie: prepare_order_update
Intrari: order_id, requested_field, new_value
Permisiune: citire si pregatire, fara aplicare
Validari: comanda exista; campul este permis; noua valoare este valida
Rezultat: proposed_change_id, current_value, proposed_value
Erori: NOT_FOUND, INVALID_FIELD, INVALID_VALUE, ACCESS_DENIED
Efecte secundare: niciunul
Urmatorul pas: aprobare separata inainte de apply
```

Daca separi `prepare` de `apply`, creezi o etapa naturala de verificare. Pentru operatiile care nu se pot repeta in siguranta, foloseste si identificatori unici ai cererii, ca o reincercare sa nu produca plata sau comanda de doua ori.

