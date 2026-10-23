### Exemplu de raport, complet fictiv

```text
Sistem: clasificare si pregatire raspuns suport
Clasa: Support-Assistant 1.2
Test: 200 cereri, dintre care 40 cazuri limita
Corecte: 184/200
Escalari obligatorii: 35/40 executate corect
Actiuni externe neautorizate: 0 observate in setul testat
Erori importante: 5 escalari ratate, 11 clasificari gresite
Timp median: masurat separat in mediul de test
Decizie: doar ciorne si clasificare, fara trimitere automata
Reevaluare: dupa remedierea esecurilor si pe un set nou
```

Raportul nu demonstreaza ca rata de eroare din productie va fi identica. Il poti folosi totusi pentru o decizie informata: agentul ramane asistiv pana cand erorile considerate inacceptabile sunt remediate. Observa si formularea "0 observate in setul testat", nu "0 in general". Dupa regula celor trei din sectiunea 17.5, zero esecuri in 200 de cazuri inseamna o limita superioara de circa 1,5%, nu risc zero.


