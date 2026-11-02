### 20.6. Cum calculam valoarea unui pilot, nu doar costul API-ului

O automatizare poate avea un pret mic pe apel si un cost mare pe rezultat acceptat, daca necesita multe corectii. Pentru un pilot, stabilim mai intai **baseline-ul**: timpul efectiv consumat azi, numarul de cazuri, erorile si costurile asociate interventiilor umane. Apoi masuram aceleasi lucruri dupa introducerea workflow-ului.

Un exemplu exclusiv ilustrativ: daca un proces economiseste 12 ore pe saptamana, costul intern al unei ore este 20 de unitati monetare, iar procesul ruleaza 48 de saptamani, valoarea aritmetica a timpului eliberat este `12 x 20 x 48 = 11.520` de unitati monetare pe an. Aceasta **nu este economisire financiara demonstrata**: timpul eliberat poate fi redistribuit, iar mentenanta si verificarea pot adauga costuri.

In raportul pilotului trebuie separate: costurile de infrastructura, costul modelului si al uneltelor, timpul de corectare, timpul de supraveghere si consecintele erorilor. Indicatorul util este adesea **costul pe sarcina acceptata si verificata**, nu doar numarul de tokeni consumati. Un beneficiu economic se afirma numai dupa compararea cu situatia initiala si dupa explicarea ipotezelor.

