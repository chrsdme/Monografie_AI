### 8.4. Ce inseamna memoria unui agent

**Memoria de lucru** e informatia din contextul curent: obiective, rezultate recente, pasi in curs. **Memoria persistenta** e informatia salvata intre rulari: preferinte, decizii confirmate, rezumate de proiect, fapte cu surse. **Memoria episodica** poate descrie rularile anterioare, iar **memoria semantica** poate aduna cunostinte despre domeniu. Termenii sunt utili, dar implementarea poate fi mult mai simpla: fisiere, baze SQL, un registru de decizii sau un motor de cautare.

O nota scrisa automat nu e un fapt verificat. Daca agentul retine din greseala ca un proiect foloseste versiunea 3 a unei biblioteci, cand de fapt foloseste versiunea 2, eroarea se poate propaga la fiecare sarcina urmatoare. De aceea informatiile persistente trebuie sa pastreze sursa, data, domeniul de valabilitate si, unde e cazul, statutul de confirmare.

