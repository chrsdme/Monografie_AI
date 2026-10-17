# Publicare automata si arhiva editiilor

`main` este protejat de regula GitHub `Wiki_Rules`: fiecare modificare necesita Pull Request. Workflow-ul nu incearca sa ocoleasca aceasta regula.

## Editii, date si changelog

La un merge editorial in `main`, `tools/release.py` verifica versiunea din sursa. Pastreaza editia declarata in PR (de exemplu 1.2), cu data efectiva de publicare Europe/London, ori creste incremental: `1.2 -> 1.2.1 -> 1.2.2`.

Actualizeaza coperta, front matter, citarea, Anexa E si changelog-ul. Generatorul reconstruieste cuprinsul, wiki-ul, PDF-ul si blocul automat de pe pagina Acasa. Acesta include versiunea, data, linkul catre changelog, PDF-ul curent si arhiva.

## PDF-ul si arhiva

PDF-ul validat este publicat automat la https://chrsdme.github.io/Monografie_AI/downloads/Monografie_AI_De_la_Chat_la_Sisteme_Agentice.pdf . Copiile istorice au numele `docs/Monografie_AI_De_la_Chat_la_Sisteme_Agentice_X.Y[.Z].pdf`, iar `docs/Monografie_AI_De_la_Chat_la_Sisteme_Agentice.pdf` este copia curenta.

Pentru ca botul **nu are voie sa faca push direct in main**, jobul `archive_pr` pregateste automat o ramura `auto/archive-...` si deschide un PR cu PDF-ul numerotat, copia curenta, manifestul `docs/.publication.json`, sursa, changelog-ul si paginile wiki. **Proprietarul trebuie sa faca merge la acel PR pentru persistenta arhivei in main.** PDF-ul de pe Pages este disponibil imediat, independent de acel merge.

Cand PR-ul de arhivare este integrat, workflow-ul detecteaza modificarea manifestului, **nu incrementeaza editia din nou**, iar fisierul PDF istoric este reutilizat fara suprascriere.

## Permisiuni necesare

Jobul `build` are numai `contents: read`; jobul `archive_pr` are drepturi `contents: write` si `pull-requests: write`, doar pentru ramura de arhivare si crearea PR-ului. In `Settings > Actions > General > Workflow permissions` poate fi necesara activarea optiunii **Allow GitHub Actions to create and approve pull requests**. Botul nu face merge. Daca optiunea este blocata, jobul raporteaza eroare si lasa ramura `auto/archive-...` disponibila pentru PR manual.

Changelog-ul automat enumera provenienta commitului si domeniile afectate. Pentru o editie importanta, rezumatul editorial detaliat trebuie verificat in PR, pentru ca lista de fisiere nu demonstreaza singura semnificatia modificarilor.

## Linkuri

- Wiki: https://chrsdme.github.io/Monografie_AI/
- PDF curent: https://chrsdme.github.io/Monografie_AI/downloads/Monografie_AI_De_la_Chat_la_Sisteme_Agentice.pdf
- Arhiva GitHub: https://github.com/chrsdme/Monografie_AI/tree/main/docs

`workflow_dispatch` regenereaza aceeasi editie fara incrementare.
