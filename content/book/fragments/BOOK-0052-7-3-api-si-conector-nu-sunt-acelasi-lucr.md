### 7.3. API si conector nu sunt acelasi lucru

API-ul defineste cum ceri functii de la un serviciu. Un **conector** este o integrare care adapteaza serviciul pentru o anumita aplicatie: autentificare, lista de operatii, conversia datelor, tratarea erorilor. Un conector pentru email poate oferi operatiile "cauta mesaje", "citeste mesaj" si "pregateste raspuns". Utilizatorul nu trebuie sa cunoasca endpointurile HTTP pe care conectorul le foloseste in fundal.

Un conector nu inseamna automat acces complet. Permisiunile pot fi doar de citire sau pot include scriere, stergere si trimitere. Aceste diferente fac parte din arhitectura, nu sunt un detaliu de decor.

