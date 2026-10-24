## C.2. Construieste setul de cazuri inainte de a modifica agentul

Porneste de la cerintele unei activitati. Pentru exemplul meteo, cazurile includ localitate si tara explicite, localitati cu acelasi nume, date lipsa, raspunsuri invalide, conexiune intrerupta si cereri pentru prognoza, nu pentru vremea actuala. Pentru suport, cazurile includ comanda existenta, comanda inexistenta, status contradictoriu si cerere de rambursare neautorizata.

Setul trebuie sa contina situatii obisnuite, limite, erori de integrare si cazuri care cer refuz sau escalare. Imparte exemplele intre un set folosit la dezvoltare si un set pastrat separat pentru verificarea finala. Daca ajustezi agentul dupa fiecare rezultat din setul ascuns, setul nu mai este independent.

Un sistem care trece doar testele pe care le-a vazut poate fi perfect ajustat pentru demonstratie si slab in productie. Ca sa reduci riscul, include date noi si perturbari care nu schimba sensul cererii: reformulari, ordine diferite ale campurilor, mici intarzieri la unelte.

