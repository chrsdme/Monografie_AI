### 11.2. Stratul de intrare

Primeste cererea. Poate fi un mesaj intr-un chat, o actiune intr-o aplicatie, un email, un eveniment de monitorizare sau un apel API. Aici afli cine e utilizatorul, ce a cerut, in ce limba vrea raspunsul si daca cererea include fisiere. Inainte de orice inferenta e rezonabil sa faci verificari elementare: dimensiunea fisierelor, tipul continutului, autentificarea, autorizarea si datele lipsa.

Nu orice intrare trebuie trimisa unui LLM. Daca soseste un eveniment "backup finalizat", o regula clasica poate actualiza starea fara model. AI-ul intervine cand natura informatiei sau a deciziei o justifica.

