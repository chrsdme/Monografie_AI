### 10.6. Cum lucreaza un harness cu mai multe modele

Un harness poate avea o interfata generica pentru servicii de inferenta. Pentru un raport simplu alege un model economic, pentru programare unul mai capabil, iar pentru imagini unul multimodal. Rutarea poate fi o regula fixa sau o decizie luata de alta componenta. E o optiune de arhitectura, nu o garantie de economie: o rutare gresita si transferurile repetate pot scumpi sistemul.

Important: **schimbarea modelului nu trebuie sa schimbe automat permisiunile agentului**. Daca agentul are drept de citire, faptul ca foloseste un model mai bun nu ii da drept de stergere. Si invers, un model slab nu trebuie lasat sa execute actiuni periculoase doar pentru ca a formulat o cerere convingatoare.

