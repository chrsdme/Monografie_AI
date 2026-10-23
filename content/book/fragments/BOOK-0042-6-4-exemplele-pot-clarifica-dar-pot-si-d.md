### 6.4. Exemplele pot clarifica, dar pot si deforma

Metoda numita **few-shot prompting** ofera cateva perechi intrare-iesire. Ajuta la extragerea uniforma de date sau la clasificarea mesajelor. Exemplele alese prost pot insa induce o regula falsa. Daca toate facturile din exemple au TVA, modelul poate presupune ca si o factura scutita trebuie sa aiba TVA. Testele de acceptare trebuie sa includa si cazuri care nu seamana cu exemplele comode.

Nu exista o reteta unica pentru toate modelele. Unele merg mai bine cu instructiuni scurte, altele tolereaza structuri complexe. O schimbare de versiune poate modifica rezultatele, deci pentru fluxurile importante promptul se versioneaza si se evalueaza din nou [S05].

