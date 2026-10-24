### 4.2. Patru lucruri care se confunda des

**Istoricul vizibil** este ce vezi in interfata. **Contextul transmis** este pachetul concret primit de model la o cerere. **Memoria aplicatiei** este informatia salvata pentru sesiuni viitoare. **Cunostintele antrenate** sunt tiparele codificate in parametrii modelului. Sunt patru lucruri diferite. O aplicatie poate afisa o conversatie foarte lunga si totusi sa trimita modelului doar mesajele recente si un rezumat al celor vechi.

Si invers: un chat nou poate primi preferinte salvate sau informatii recuperate din fisiere, chiar daca ele nu apar in istoricul recent. Comportamentul nu e universal, deci merita verificat pentru aplicatia pe care o folosesti.

