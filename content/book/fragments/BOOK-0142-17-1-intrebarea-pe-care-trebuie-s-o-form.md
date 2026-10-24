### 17.1. Intrebarea pe care trebuie s-o formulam corect

"Pot avea incredere in agent?" e prea larg. Incredere pentru ce? Sa explice vremea, sa editeze o ciorna, sa ruleze teste, sa schimbe o configuratie in productie? Un agent poate fi excelent la rezumate si nepotrivit pentru operatii financiare. Increderea se leaga de o **categorie de sarcini**, o **configuratie concreta**, un **nivel de autonomie** si un **set de conditii de evaluare**.

Folosim expresia **Trust Score** pentru o evaluare operationala propusa in aceasta lucrare. Nu este un standard consacrat si nu exista un scor universal care sa transforme automat 90% succes in permisiunea de a opera in productie. Scorul are sens doar impreuna cu tipul testelor, severitatea erorilor si intervalul de incertitudine.

Pentru vocabular, merita sa stii cum defineste Anthropic o evaluare: un test pentru un sistem AI in care dai o intrare si aplici o logica de notare asupra iesirii, ca sa masori succesul [S33]. Ghidul lor (9 ianuarie 2026) deosebeste notarea prin cod, prin model si prin oameni, precum si evaluarile de capabilitate de cele de regresie. Primele intreaba "ce stie sa faca agentul?", celelalte "mai stie sa faca ce stia ieri?".

