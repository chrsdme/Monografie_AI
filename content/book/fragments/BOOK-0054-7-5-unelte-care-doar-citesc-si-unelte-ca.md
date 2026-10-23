### 7.5. Unelte care doar citesc si unelte care schimba lumea

Cautarea documentelor nu e acelasi lucru cu stergerea lor. Citirea unei facturi e altceva decat emiterea unei plati. Intr-un sistem controlat, fiecare unealta are un nume clar, o schema pentru argumente, permisiuni minime si rezultate usor de inspectat. Pentru actiunile cu efecte ireversibile sau financiare ai nevoie de aprobari si verificari in plus.

Exemplu: `draft_email(recipient, body)` poate salva o ciorna fara sa o trimita. `send_email(recipient, body)` produce un efect in lumea reala. Chiar daca ambele apeleaza acelasi model pentru text, riscul operational nu e acelasi.

