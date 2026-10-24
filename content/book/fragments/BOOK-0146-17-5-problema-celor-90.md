### 17.5. Problema celor 90%

Sa zicem ca 90 din 100 de cereri sunt rezolvate corect. Ai o rata observata de 90% pentru setul respectiv de teste. Nu poti concluziona, fara alte informatii, ca agentul va rezolva 90% din toate cererile viitoare. Testele pot fi prea usoare, datele pot semana cu cele folosite la dezvoltare, iar cele zece esecuri pot include un incident grav.

Un rezultat din 100 de observatii are si incertitudine statistica. Un interval Wilson de 95% pentru 90 din 100 merge, aproximativ, de la 82,6% pana la 94,5%. Cu 900 din 1.000, intervalul se strange la 88,0%-91,7%. Mai multe teste dau un interval mai ingust, dar nu rezolva problema testelor nereprezentative. Daca vrei sa compari doua versiuni apropiate ca performanta, ai nevoie de esantioane mai mari si de teste comparabile.

Pentru sarcinile cu risc mare, o rata medie de succes nu ajunge. Analizeaza separat numarul de incalcari ale limitelor critice, de preferat cu toleranta foarte mica sau zero in testele de acceptare. Si aici statistica avertizeaza: zero esecuri in 200 de teste nu inseamna risc zero. Dupa "regula celor trei", limita superioara a ratei de esec este de circa 3/200, adica 1,5%, la un nivel de incredere de 95%.

O nuanta in plus vine din felul in care un agent se comporta la repetare. Ghidul Anthropic distinge `pass@k` (cel putin una din k incercari reuseste) de `pass^k` (toate cele k incercari reusesc) si arata ca cele doua spun lucruri foarte diferite pe masura ce k creste [S33]. Pentru un agent care trebuie sa fie de incredere de fiecare data, a doua masura e mai apropiata de realitate.

