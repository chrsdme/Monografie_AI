# Auditul termenilor - 17 octombrie 2026

## Sursele verificate

- Sursa Markdown si cele 22 de capitole din Monografie_AI 1.1.3; sursa coincide ca blob Git cu cea din main la inceputul auditului.
- PDF-ul original atasat 1.1.3: 78 pagini. PDF-ul auto-generat ulterior: 79 pagini conform CI; nu a fost accesibil vizual pentru acest audit.
- [Lexiconul agentilor AI, Ovidiu Boticiu](https://ovidiuboticiu.github.io/lexiconul-agentilor-ai/index.html): 361 intrari, cu licenta editoriala CC BY-NC 4.0; am verificat structura si un esantion, nu 361 definitii individual.

## Rezultate

Glosarul avea **68 de intrari**, multe concepte de baza fiind explicate deja in Capitolele 9, 12, 14 si Anexa A. Nu duplicam agent, workflow, bucla agentica, orchestrator, handoff, MCP sau Human-in-the-loop. Idempotenta exista deja in glosar si in sectiunea 19.2; adaugam separat cheia de idempotenta.

Termenii mentionati fara intrare distincta includ metadate, artefact, hash, JSON, YAML, reconciliere. Noile studii de caz aduc mock, fixture, OAuth, scheduler, sursa de adevar si AI Employee (eticheta operationala, nu standard). Adaugam 16 intrari proprii si recomandam lexiconul doar ca resursa externa, pentru a pastra licenta MIT a cartii fara preluare nepermisa.

**Limita metodologica:** prezenta unui cuvant in PDF nu dovedeste o definitie corecta. Am inspectat sectiunile importante si am distins definitiile existente de cele lipsa; nu am validat factual integral cele 361 de definitii externe. Noile exemple practice raman fictive si vor fi publicate intr-un PR separat.

## Schimbari ulterioare in PR-uri separate

1. Sugestia acceptata pentru Capitolul 1, cu clarificari despre reguli versus AI, tokeni, categorii si model/aplicatie/sistem.
2. Studii de caz cu rambursari si cercetare/producere YouTube, pseudocod, configuratii si limite verificabile.
