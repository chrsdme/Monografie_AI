### 10.3. Harness si motor de inferenta

Confuzia apare des cand cineva instaleaza un motor pentru modele locale si vede ca acesta raspunde printr-un API. **Motorul de inferenta** incarca modelul si face calculul necesar generarii. **Harness-ul** gestioneaza sarcina, contextul, uneltele si procesul de executie. Un motor poate include functii de servire, de gestionare a cererilor sau de apeluri structurate, dar asta nu inseamna ca ruleaza un workflow complet de dezvoltare software. Figura 3 separa cele doua roluri.

![Figura 3. Motorul genereaza; harness-ul gestioneaza executia si controlul.](Monografie_AI_figuri/fig03_harness.svg)

*Figura 3. Responsabilitatile motorului de inferenta si ale harness-ului.*

Exemplu local: un serviciu de inferenta primeste intrebarea si returneaza text. Un harness separat ii trimite cerintele, ii ofera fisierele relevante, interpreteaza cererea de rulare a testelor si inapoiaza rezultatul. Exemplu cloud: acelasi harness poate folosi un API administrat de un furnizor. Din perspectiva proiectului, responsabilitatile de context si executie raman asemanatoare. Furnizorul poate oferi insa propriul harness administrat, caz in care o parte din responsabilitati se muta in serviciul extern.

