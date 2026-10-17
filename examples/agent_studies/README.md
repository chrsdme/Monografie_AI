# Capitolul 21 - Exemple executabile (simulator sandbox)

Aceste exemple folosesc configuratii YAML reale, citite de `demo.py`. In modul implicit folosesc **mock**, adica alegerea deterministica a actiunilor, pentru a arata mecanismul unei bucle de executie si controalele impuse de dispatcher. **Nu demonstram performanta unui LLM in modul mock.**

## Pornire

```bash
python -m pip install 'PyYAML>=6,<7'
python examples/agent_studies/demo.py refund --case ok
python examples/agent_studies/demo.py refund --case above_limit
python examples/agent_studies/demo.py refund --case missing_proof
python examples/agent_studies/demo.py refund --case duplicate
python examples/agent_studies/demo.py youtube
python -m unittest discover -s examples/agent_studies/tests -v
```

**Rambursari:** comenzile sunt fictive; datele provin din `fixtures/orders.json`. Registrul simulat este in memorie. Nu se fac plati, nu se contacteaza Shopify si nu se trimit emailuri.

**YouTube:** implicit se citesc metadate fictive din `fixtures/videos.json` si se genereaza 3 schite in JSON cu `WAITING_HUMAN_APPROVAL`. Nu se descarca transcrieri, nu se genereaza MP4, nu se publica nimic.

## Optiuni care necesita integrare suplimentara

Pentru metadate publice reale, in `config/youtube.yaml` se poate seta `source_mode: metadata_api`, lista `channel_ids` si cheia `YOUTUBE_API_KEY`. Calea de retea nu a fost testata in CI; respecta regulile si cotele platformei.

Pentru alegere dinamica printr-un model local, in `config/refund.yaml` se poate selecta `provider: ollama`, cu endpoint si model compatibil. Codul valideaza actiunile in dispatcher inclusiv atunci cand modelul cere direct un refund. Integrarea cu Ollama nu a fost testata in CI.

**Niciuna dintre aceste optiuni nu autorizeaza rambursari reale sau upload YouTube.** Un sistem de productie cere identitate verificata, drepturi minime, idempotenta server-side, jurnalizare, evaluari si aprobari impuse efectiv in aplicatie.
