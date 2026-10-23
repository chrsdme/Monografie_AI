#### E4. Configuratie de demonstratie

```yaml
name: refund_assistant_demo
model:
  provider: mock
  name: qwen2.5:14b
policy:
  currency: RON
  auto_refund_max: 100.00
  max_steps: 12
  require_verified_customer: true
  require_proof_for_damage: true
  allow_production_refunds: false
safety:
  backend: sandbox
  idempotency: request_id
```

**Citirea configuratiei:** `mock` inseamna model simulat, `sandbox` inseamna fara operatii financiare reale, iar `request_id` este cheia folosita pentru a recunoaste aceeasi cerere. YAML este un format de configurare, nu un standard Shopify. Un test cu mock verifica regulile simulatoare, nu demonstreaza integrarea reala. Pentru Shopify, mutatia `refundCreate` necesita o cheie de idempotenta in versiunile API incepand cu 2026-04. [Documentatie Shopify](https://shopify.dev/docs/api/admin-graphql/2026-10/mutations/refundCreate).

**Evaluare:** verificam separat 62 RON, 350 RON, lipsa dovezii, client neverificat, solicitare duplicata, API indisponibil, unealta interzisa si limita de pasi. Pentru tranzactii, o singura plata neautorizata este un defect critic, indiferent de rata globala de succes.

