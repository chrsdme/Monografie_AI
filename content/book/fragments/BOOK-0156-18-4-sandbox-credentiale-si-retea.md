### 18.4. Sandbox, credentiale si retea

Un **sandbox** este un mediu izolat care limiteaza efectele unei executii. Un agent de dezvoltare poate lucra intr-un container sau spatiu dedicat, cu fisiere selectate si acces restrans la retea. Mediul poate reduce daunele, dar izolarea trebuie testata. Eticheta "sandboxed" nu dovedeste singura ca datele sau credentialele sunt protejate.

Credentialele se stocheaza si se ofera prin mecanisme dedicate, cu durata si permisiuni limitate. Nu le pui in prompt, ca text simplu. Pentru o unealta care trimite email, foloseste o identitate autorizata si, unde e nevoie, un traseu de aprobare. In productie, foloseste de preferat alte identitati si chei decat in mediul de test.

