### 10.4. Ce este bucla agentului

Un harness poate controla un ciclu ca acesta:

```text
Primeste obiectivul
  -> construieste contextul relevant
  -> cere modelului urmatorul pas
  -> valideaza actiunea propusa
  -> cere aprobare, daca este necesar
  -> executa unealta permisa
  -> inregistreaza rezultatul real
  -> verifica daca obiectivul a fost atins
  -> continua, corecteaza, escaladeaza sau se opreste
```

Bucla nu are voie sa mearga la nesfarsit. Ai nevoie de un numar maxim de pasi, de un buget de timp sau de cost, de conditii de oprire la eroare si de reguli pentru actiunile care nu se pot repeta fara efecte secundare. Un mecanism care poate retrimite de zece ori o cerere de rambursare este un exemplu limpede de design prost.

Anthropic subliniaza si un alt detaliu: agentii trebuie sa primeasca "ground truth" din mediu la fiecare pas, de exemplu rezultatele uneltelor sau ale executiei de cod [S10]. Cu alte cuvinte, bucla se sprijina pe ce s-a intamplat cu adevarat, nu pe ce spune modelul ca s-a intamplat.

