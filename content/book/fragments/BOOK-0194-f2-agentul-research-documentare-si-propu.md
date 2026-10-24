#### F2. Agentul Research: documentare si propuneri

Agentul primeste obiectivul editorial, canalele, publicul tinta, istoria propriilor materiale si reguli de cercetare. Poate alege ce metadate sa compare si unde sa caute documentatie suplimentara. Foloseste numai surse si unelte autorizate.

```text
PERIODIC: preia_metadate_noi(); elimina_duplicate()
PENTRU cel_mult_N_iteratii:
    actiune = RESEARCH.alege_urmatoarea_actiune()
    DACA cere o sursa permisa: consulta_sursa()
    DACA informatia este insuficienta: marcheaza_incertitudine()
    DACA propunerea este documentata: finalizeaza_brief(); OPRESTE
```

Titlurile, descrierile si data publicarii sunt **metadate**, nu transcrieri. Nu putem afirma ca agentul a analizat integral un videoclip pentru care nu are acces la continut. Nici trei videoclipuri asemanatoare nu confirma singure un trend.

Exemplu de propunere: "De ce nu orice workflow AI este automat agent AI?", cu trei titluri candidate, o schita de clip de 60-90 secunde si sursele documentate.

