### 17.2. Construirea unui mediu controlat

Pornim de la agentul meteo. Ii dam o cerere fara ambiguitate, o unealta disponibila si valori de test cunoscute. Un serviciu simulat returneaza, de exemplu, pentru un oras o temperatura fixa si o ora a observatiei. Verificam daca agentul apeleaza unealta, foloseste argumentele corecte, preia valoarea si explica eventualele limite. Nu intrebam doar "a sunat bine raspunsul?".

Urmeaza cazurile diferite: localitati cu nume identice, temperaturi negative, date lipsa, raspunsuri vechi, erori HTTP, timeout, rate limit sau informatii contradictorii. Unele teste se aleg la intamplare dintr-o distributie controlata. Altele sunt **teste adversariale**, construite special pentru punctele unde agentul probabil esueaza.

