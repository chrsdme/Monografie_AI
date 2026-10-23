### 8.3. Ce poate merge prost intr-un RAG

Recuperarea gresita e una dintre cele mai greu de observat probleme. Daca intrebi despre politica de retur din 2026 si sistemul aduce politica din 2023, modelul poate scrie un raspuns elegant, dar depasit. Daca fragmentele sunt prea mici, se pierde contextul. Daca sunt prea mari, cautarea devine mai putin precisa. Daca informatia nu exista, modelul trebuie sa poata spune ca sursele nu ajung.

RAG nu elimina halucinatiile si nu face credibila o sursa care nu e. O pagina web poate contine informatii false, iar documentele recuperate pot contine chiar instructiuni rauvoitoare. De aceea calitatea recuperarii, calitatea raspunsului si securitatea surselor sunt trei evaluari separate [S09].

