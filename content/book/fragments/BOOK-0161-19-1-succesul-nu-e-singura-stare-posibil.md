### 19.1. Succesul nu e singura stare posibila

Un workflow real intalneste servicii indisponibile, documente corupte, permisiuni expirate si cereri incomplete. Arhitectura trebuie sa stabileasca ce face in astfel de situatii. Un agent care pretinde ca operatia a reusit, ca sa poata continua, e mai problematic decat unul care raporteaza limpede o eroare.

**Timeout** inseamna ca o operatie a depasit intervalul asteptat. **Retry** inseamna reluarea ei. **Backoff** introduce pauze tot mai lungi intre incercari. Mecanismele sunt utile, dar se aplica in functie de efectele operatiei. Nu orice esec se repara prin repetare.

