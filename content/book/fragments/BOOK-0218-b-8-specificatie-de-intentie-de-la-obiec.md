## B.8. Specificatie de intentie: de la obiectiv la verificare

Un *Intent Spec* este un artefact de documentare, nu o functie standard a unui model. Exemplul de mai jos completeaza [studiul 21.7 despre rambursari](https://chrsdme.github.io/Monografie_AI/partea-5/21-studii-de-caz/#217-studiul-de-caz-e-acelasi-retur-prin-trei-arhitecturi); aceleasi intrebari sunt utile pentru [cei doi agenti YouTube din 21.8](https://chrsdme.github.io/Monografie_AI/partea-5/21-studii-de-caz/#218-studiul-de-caz-f-cercetare-youtube-si-productie-editoriala-cu-doi-agenti). Explicatia conceptului este in [sectiunea 6.7](https://chrsdme.github.io/Monografie_AI/partea-2/06-prompturi-instructiuni-briefuri/#67-intent-engineering-de-la-cerere-la-obiectiv-verificabil).

```yaml
intent_id: refund_resolution_v1
status: exemplu_didactic
problem: "Solicitarile trebuie solutionate corect si consecvent."
evidence: "Comanda, politica magazinului si verificari in sistem."
objective: "Rezolva cererile eligibile, fara plati duplicate sau neautorizate."
success_criteria:
  - final_state_verified_or_escalated
  - no_duplicate_refund
  - customer_notified_only_after_confirmation
constraints:
  currency: RON
  auto_refund_limit: 100
  require_verified_customer: true
priorities: [authorisation, correctness, speed]
human_approval_when: [amount_above_limit, unclear_eligibility]
stop_when: [verified_outcome, waiting_for_customer, human_escalation, budget_limit]
verification: [test_62_ron, test_350_ron, test_duplicate_refund]
owner: support_operations
```

**Interpretare:** pentru 62 RON verificam eligibilitatea si confirmarea operatiei; pentru 350 RON verificam escalarea fara plata. Pentru YouTube am inlocui limita financiara cu sursele permise, verificarea originalitatii si aprobarea versiunii exacte a videoclipului.

**Limita:** YAML-ul este ilustrativ, nu este format oficial si nu este citit automat de simulatorul din Capitolul 21. Campurile nu impun singure permisiuni, nu efectueaza tranzactii si nu verifica rezultate; aplicatia trebuie sa implementeze controalele si testele.

