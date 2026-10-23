### 20.1. Costul real depaseste factura de tokeni

Intr-un sistem cu agenti consumi resurse pentru inferenta, cautare, stocare, unelte, rularea testelor si monitorizare. Unele servicii factureaza separat intrarile, iesirile, stocarea sau apelurile de unelte. Un model local nu elimina costurile: hardware-ul, energia, mentenanta si timpul operatorului raman relevante. Nu exista un pret universal si nu construim decizii pe tarife care se pot schimba oricand.

Un detaliu mai putin cunoscut: acelasi text poate cere un numar diferit de tokeni in limbi diferite. Un studiu din 2023 a constatat ca acelasi continut poate necesita pana la circa 15 ori mai multi tokeni in unele limbi fata de altele, ceea ce afecteaza si costul, si cat context incape [S38]. Nu avem aici o cifra verificata pentru romana, deci masoara pe textele tale reale cu tokenizatorul modelului pe care il folosesti.

