## C.3. Ce masuram si cum evitam cifrele inselatoare

Rata de succes e utila, dar insuficienta. Prezinta-o impreuna cu numarul de executii si cu tipurile de eroare. La zece teste, noua reusite inseamna 90%; la o mie de teste, 900 de reusite inseamna tot 90%. Precizia estimarii si varietatea cazurilor sunt insa foarte diferite. Pentru rapoarte serioase adauga intervale de incredere statistice (de exemplu intervalul Wilson, vezi sectiunea 17.5) si rezultate separate pe categorii.

Indicatori recomandati:

- **Corectitudine:** rezultatul respecta datele si cerintele initiale.
- **Conformitatea actiunilor:** s-au folosit doar unelte si operatii autorizate.
- **Trasabilitate:** exista dovezi suficiente pentru a reconstitui executia.
- **Recuperare:** intreruperile se trateaza fara dublarea operatiilor si fara pierderea necontrolata a starii.
- **Escalare:** sistemul se opreste sau cere ajutor atunci cand este necesar.
- **Cost si timp:** numarul de apeluri, durata si resursele consumate.
- **Severitatea defectelor:** tratata separat de numarul simplu de erori.

Un agent care a dat 990 de raspunsuri corecte din 1.000, dar a executat o singura plata neautorizata, nu este "99% sigur" pentru tranzactii financiare. Evaluarea riscului cere reguli de acceptare distincte de media performantelor.

