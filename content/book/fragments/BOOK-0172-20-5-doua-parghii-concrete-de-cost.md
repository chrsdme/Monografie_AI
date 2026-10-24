### 20.5. Doua parghii concrete de cost

Cand promptul tau are o parte lunga si stabila (instructiuni, documentatie, exemple), poti folosi *prompt caching*, un mecanism prin care furnizorul reutilizeaza partea deja procesata. Documentatia Anthropic spune ca asta "significantly reduces processing time and costs for repetitive tasks or prompts with consistent elements" si indica, pentru cache-ul de 5 minute, o scriere la 1,25 ori pretul de baza al tokenilor de intrare si o citire la 0,1 ori acel pret [S39]. Sunt cifre ale unui furnizor, valabile la data consultarii, cu exceptii pe model. Verifica tarifele curente si masoara pe traficul tau.

A doua parghie este rutarea: sarcinile simple merg pe un model mai ieftin, cele grele pe unul mai capabil, cu masurarea erorilor de rutare (sectiunea 14.3). Ambele functioneaza doar daca ai o evaluare care iti spune ca se pastreaza calitatea.

