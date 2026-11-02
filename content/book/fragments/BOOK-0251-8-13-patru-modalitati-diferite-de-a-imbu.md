### 8.13. Patru modalitati diferite de a imbunatati un raspuns

Cand rezultatul este slab, nu avem automat nevoie de antrenarea unui model. Intai stabilim ce lipseste:

| Problema observata | Prima directie de investigat |
|---|---|
| Cerinta este neclara ori formatul variaza | Prompt, exemple si contract de iesire |
| Informatiile lipsesc sau sunt vechi | Recuperare si actualizare a surselor prin RAG |
| Sunt necesare date curente ori actiuni externe | Unealta sau API cu verificarea rezultatului |
| Modelul trebuie adaptat repetat la un comportament specializat | Evaluare a oportunitatii de fine-tuning, dupa o comparatie cu solutiile mai simple |

Finetuning-ul schimba parametri ai modelului. RAG schimba informatia adusa la momentul raspunsului. Uneltele aduc observatii sau executa actiuni. Promptul clarifica sarcina. Aceste mecanisme se pot combina, dar nu sunt interschimbabile.

