### 4.3. Context mare nu inseamna context bun

O fereastra mare te lasa sa pui mai multa informatie, dar nu garanteaza ca modelul va folosi bine fiecare detaliu. Cercetarea despre fenomenul *lost in the middle* a aratat ca unele modele se descurca mai prost cand informatia relevanta e in mijlocul unei intrari lungi [S02]. Concluzia practica nu e sa elimini documentele, ci sa alegi si sa prezinti ce e util in asa fel incat sa poata fi verificat.

Anthropic formuleaza ideea direct, in ghidul lor despre ingineria contextului: "Context, therefore, must be treated as a finite resource with diminishing marginal returns" [S03]. Pe romaneste: contextul e o resursa limitata, iar fiecare token in plus aduce tot mai putin.

Un exemplu: ai 500 de pagini de loguri, dar intrebarea priveste eroarea de la ultima instalare. Daca trimiti tot, adaugi zgomot. Mai util este un extras cu eroarea, perioada, versiunea aplicatiei si pasii de reproducere. Originalele pot ramane la indemana, pentru consultare ulterioara.

