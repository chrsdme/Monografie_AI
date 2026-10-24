### 11.9. Stratul de observabilitate si imbunatatire

Jurnalele si trace-urile descriu ce s-a intamplat, cand si cu ce rezultat. Metricile aduna durata, costul, rata de succes, frecventa erorilor si numarul de interventii umane. Datele astea ajuta la investigarea incidentelor si la compararea versiunilor. Conventiile semantice OpenTelemetry pentru AI generativ acopera operatii de inferenta, recuperare si apeluri de unelte, dar au statutul "Development", deci se pot schimba, iar sistemele concrete pot avea implementari diferite [S12].

Aici trebuie sa deosebesti **pastrarea datelor pentru diagnostic** de **folosirea datelor pentru a imbunatati un model**. A doua poate presupune evaluari, modificari de prompt, unelte noi sau antrenare separata. Nu se intampla automat doar pentru ca ai conectat un registru de loguri.

