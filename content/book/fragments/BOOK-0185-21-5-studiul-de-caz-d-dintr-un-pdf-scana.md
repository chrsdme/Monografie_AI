### 21.5. Studiul de caz D: dintr-un PDF scanat intr-o inregistrare verificata

Procesarea inteligenta a documentelor, numita adesea **IDP** (*Intelligent Document Processing*), combina recunoasterea textului, clasificarea documentelor, extragerea campurilor si verificarea lor. Este mai mult decat OCR. OCR transforma imaginea literelor in text. IDP urmareste un rezultat operational, de pilda date de factura pregatite pentru sistemul contabil [S20].

O factura scanata poate fi procesata asa: sistemul identifica paginile, recunoaste textul, gaseste furnizorul, moneda, totalul, data si numarul facturii, verifica aritmetic subtotalul si taxele, compara furnizorul cu registrul si marcheaza neconcordantele. Un model multimodal poate ajuta la documente cu layout neobisnuit, dar calculele aritmetice si identificarea duplicatelor se fac prin reguli verificabile.

Din perspectiva increderii, sunt trei intrebari diferite: **a citit corect textul?**, **a extras campurile corecte?**, **avem dreptul sa facem operatia urmatoare?** Un rezultat bun la primele doua nu este o autorizatie de plata. Aprobarea, jurnalul si controalele de duplicat raman in sistemul operational. Cazul arata de ce un workflow poate integra AI fara ca toate etapele sa fie delegate unui agent autonom.

