## B.3. Contract pentru transferul dintre doua etape

Sa presupunem ca Research trebuie sa predea rezultatul catre Development. Evita transferul unui istoric lung de conversatii si foloseste un document scurt, verificabil:

```text
run_id: proiect-041
predare: Research -> Development
specificatie_aprobata: SPEC-12, revizia 3
cerinte_obligatorii: [C1, C2, C3]
decizii_confirmate: [D1, D2]
probleme_deschise: [P4]
linkuri_surse: [URL sau identificatori de fisiere]
artefacte: [calea / identificatorul documentelor]
criterii_de_acceptare: [T1, T2, T3]
stare: READY sau BLOCKED
```

Contractul trebuie sa fie suficient ca noul agent sa poata incepe, dar nu sa contina toate ipotezele si toate mesajele celui dinainte. Cand lipseste un element esential, etapa este `BLOCKED`. Nu inventezi detaliul ca sa pastrezi aparenta de progres.

