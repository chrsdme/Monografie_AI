### 10.1. Ce problema rezolva

Sa zicem ca un model poate scrie un program Python. Utilizatorul ii cere sa modifice o aplicatie, iar modelul propune un fragment de cod. Bun. Dar cine deschide proiectul? Cine citeste fisierul corect, aplica modificarea, ruleaza testele, prinde erorile, compara rezultatul cu cerinta si il aduce pe model inapoi in discutie? Fara toate astea, modelul ramane mai ales un consultant care genereaza text.

**Harness** este numele tot mai folosit pentru infrastructura operationala din jurul modelului, cea care il lasa sa execute sarcini intr-un mod repetabil. Nu exista o definitie oficiala acceptata de toti furnizorii. Aici folosim termenul pentru ansamblul care gestioneaza sesiuni, instructiuni, contexte, unelte, permisiuni, bucle de executie, jurnale si puncte de verificare. Unele produse includ si orchestrarea; alte arhitecturi o tin separat.

Gandeste-te la un meserias foarte priceput care ajunge intr-un atelier gol. Stie sa lucreze, dar nu are scule, planuri, materiale sau cineva care sa verifice lucrarea. Harness-ul este atelierul pregatit: uneltele potrivite, regulile de acces, registrul operatiilor si procesul prin care vedem daca produsul final se potriveste cu planul. Analogia are limite, dar arata de ce modelul si mediul lui trebuie evaluate separat.

