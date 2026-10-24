#### Un exemplu de defect introdus fara intentie

Cerinta spune ca doua rezervari nu pot folosi acelasi interval. Un dezvoltator verifica disponibilitatea, apoi salveaza rezervarea. In timpul dintre verificare si salvare, o alta cerere poate ocupa acelasi interval. Ambele teste individuale trec, dar doua cereri concurente pot produce o rezervare dubla. QA trebuie sa testeze concurenta, iar sistemul are nevoie de o constrangere in baza de date sau de o tranzactie potrivita. Un prompt de tipul "nu permite rezervari duble" nu rezolva problema la nivelul integritatii datelor.

