### 16.4. Cum evitam logurile care nu mai pot fi folosite

Daca logezi integral fiecare intrare, ajungi la volume mari si la riscuri de confidentialitate. Un sistem matur poate pastra evenimentele operationale mai mult timp si continutul detaliat doar cat e necesar. Poti esantiona cererile obisnuite si pastra urme complete pentru incidente, erori si teste controlate, cu respectarea regulilor de protectie a datelor. Politica se defineste inainte de productie, nu se improvizeaza dupa un incident.

Logurile trebuie sa si poata fi corelate. Daca o cerere trece prin trei servicii si cinci agenti, fiecare eveniment poarta identificatori care permit reconstituirea traseului. Standardizarea sensului evenimentelor ajuta cand schimbi framework-ul, de aceea conventiile OpenTelemetry sunt relevante, cu rezerva ca au statutul "Development" si pot evolua [S12]. Printre atributele definite se numara si cele pentru consumul de tokeni de intrare si de iesire, utile pentru analiza costurilor.

