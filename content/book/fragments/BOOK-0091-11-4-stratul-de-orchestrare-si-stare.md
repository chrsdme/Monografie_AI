### 11.4. Stratul de orchestrare si stare

Orchestratorul primeste sarcina pregatita si hotaraste cum se proceseaza. Poate alege un singur agent, poate porni un workflow fix, poate imparti problema intre specialisti si poate astepta terminarea dependentelor. Mai important, **tine adevarul operational**: ce s-a cerut, ce e in lucru, cine raspunde, ce versiune a unui rezultat e aprobata si ce conditii au blocat executia.

Un orchestrator care spune doar "delegat cu succes", fara identificatori de sarcini, rezultate si stari verificabile, nu ofera nicio garantie. Starea trebuie sa traiasca intr-o sursa controlata de aplicatie, nu doar intr-un rezumat din conversatie.

