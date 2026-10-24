### 14.10. Ce se intampla cand un agent esueaza?

Orchestratorul trebuie sa deosebeasca un esec temporar de unul logic. Un timeout poate justifica reluarea limitata a unei cereri de citire. O schema gresita poate cere corectarea datelor. O operatie financiara cu stare necunoscuta cere intai verificarea efectului, nu retrimiterea pe orbeste. Daca QA respinge implementarea, sarcina se intoarce la Development cu defectele si dovezile, nu cu un mesaj generic de tipul "mai incearca".

Un mecanism de **failsafe** poate bloca accesul, poate pune o sarcina in asteptare sau poate opri intregul workflow. Pentru operatii reversibile poate exista rollback. Pentru cele ireversibile, uneori singura masura realista e prevenirea prin permisiuni, validare si aprobare.

