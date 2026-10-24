### 21.9. Comparatie: cine decide pasul urmator?

| Sistem | Traseu | Decizia AI | Control necesar |
| --- | --- | --- | --- |
| Automatizare clasica | Ramificatii programate | Nu este necesara | Validari si drepturi in cod |
| Workflow AI | Trasee definite in avans | Interpretare si decizii delimitate | Scheme, conditii, aprobari |
| Agent AI | Obiectiv si limite fixe; pasi dinamici | Modelul propune urmatoarea actiune | Dispatcher, verificari, buget si oprire |
| Doi agenti | Contract de predare si responsabilitati distincte | Alegeri in aria fiecarui agent | Validarea handoff-ului si a livrabilelor |
| "AI Employee" | Responsabilitate recurenta | Optional, daca include agenti | Monitorizare, escalare si responsabil uman |

"AI Employee" este o **eticheta operationala sau comerciala**, nu o categorie tehnica standard si nici o garantie de memorie persistenta ori autonomie nelimitata. Un scheduler, o baza de date si un agent pot colabora fara sa transforme fiecare componenta intr-un agent.

**Regula practica:** alegem cel mai simplu sistem care rezolva verificabil problema. Daca deciziile sunt previzibile, folosim reguli; daca doar anumite etape cer interpretare, folosim workflow AI; daca ordinea actiunilor trebuie adaptata dinamic, evaluam un agent; daca apar responsabilitati distincte, evaluam orchestrarea. Alegerea trebuie sustinuta de rezultate, nu de numarul agentilor.

**Simulator si configuratii:** [exemplele Python, YAML si testele pentru studiile E/F](https://github.com/chrsdme/Monografie_AI/tree/main/examples/agent_studies). Sunt exercitii sandbox; codul nu executa plati si nu publica videoclipuri.

Studiile E si F sunt **fictive**. Pseudocodul ilustreaza arhitectura, configurarile YAML sunt demonstrative, iar teste cu mock nu reprezinta probe de plata Shopify, transcriere YouTube ori incarcare video reala. Recomandarea de a incepe cu cea mai simpla arhitectura este sustinuta de [Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents).


