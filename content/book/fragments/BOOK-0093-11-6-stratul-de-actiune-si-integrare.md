### 11.6. Stratul de actiune si integrare

Aici se executa efectiv operatiile: interogari SQL, citirea sau scrierea fisierelor, cautare web, apeluri catre sisteme de gestiune, build-uri sau notificari. Uneltele trebuie sa valideze argumentele, sa impuna drepturile de acces si sa returneze coduri de rezultat precise. Daca o actiune a esuat, modelul nu trebuie sa poata transforma esecul in succes prin felul in care formuleaza raspunsul final.

Pentru operatiile cu efecte secundare, stratul de integrare trebuie sa sustina, unde se poate, **idempotenta**: repetarea aceleiasi cereri sa nu dubleze efectul. Un identificator unic al unei plati, de exemplu, poate preveni trimiterea tranzactiei de doua ori dupa o eroare de retea.

