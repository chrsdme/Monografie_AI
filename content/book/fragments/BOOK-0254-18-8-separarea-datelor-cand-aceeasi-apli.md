### 18.8. Separarea datelor cand aceeasi aplicatie deserveste mai multi clienti

Un produs poate avea mai multi utilizatori din aceeasi firma sau mai multe firme care folosesc aceeasi infrastructura. In arhitecturile **multi-tenant**, fiecare client sau organizatie reprezinta un domeniu logic de izolare a datelor si permisiunilor. Faptul ca doua firme folosesc acelasi model nu le da dreptul sa consulte documentele una alteia.

Sa presupunem ca o unealta poate cauta facturi dupa identificator. Verificarea nu se limiteaza la `document_id`. Sistemul determina identitatea si organizatia autorizata din sesiunea autentificata, impune filtrarea si verifica permisiunea pentru obiectul cerut. Nu accepta pur si simplu un `tenant_id` furnizat de model sau de utilizator ca dovada a dreptului de acces. Riscul de acces la obiectele altui client este documentat de OWASP sub denumirea *Broken Object Level Authorization* [S52].

In unele baze de date, o protectie suplimentara poate fi **Row-Level Security (RLS)**, care restrictioneaza randurile vizibile sau modificabile pentru un rol. O asemenea politica trebuie configurata si testata: anumite roluri privilegiate si proprietarii tabelelor pot ocoli implicit regulile, conform documentatiei PostgreSQL [S58].

Regula se aplica atat cautarii RAG, cat si logurilor, fisierelor exportate, memoriei persistente si cache-urilor. Un test minim foloseste doua organizatii distincte: o identitate din prima trebuie sa nu poata vedea datele celei de-a doua, inclusiv prin rezultate de cautare, titluri sau rezumate.

