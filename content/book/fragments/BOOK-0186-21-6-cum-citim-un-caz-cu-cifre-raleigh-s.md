### 21.6. Cum citim un caz cu cifre: Raleigh si Cordoba

Pana aici am lucrat cu simulari. In realitate, o sa intalnesti comunicate de presa si pagini de proiect care spun lucruri ca "costuri reduse cu 66%". Nu le tratam nici ca minciuni, nici ca dovezi. Le citim cu un set de intrebari. Doua cazuri publice recente ne servesc drept exercitiu. Nu le validam independent: aratam doar ce spun sursele si ce lipseste din ele.

**Exemplul 1: Raleigh (Carolina de Nord).** Pe 8 octombrie 2026, ServiceNow a publicat un comunicat cu titlul "Raleigh, North Carolina, reduces IT service desk costs by 66% with ServiceNow AI agents" [S34]. Comunicatul spune ca biroul de asistenta IT al orasului are patru oameni si deserveste 4.400 de angajati ai primariei. Cifra de 66% este atribuita redirectionarii timpului personalului. Alte cifre din text: o rata de deviere de 98% pentru agentul de autoservire Ral-E, 98% dintre rezumatele de incidente generate de AI acceptate fara modificari si aproape jumatate dintre cererile de suport IT rezolvate autonom, cu o tinta de 85%. Directorul de informatica al orasului, Mark Wittenburg, spune: "We're introducing AI deliberately, building trust step by step and keeping our people in the loop."

Ce lipseste: comunicatul nu indica perioada de masurare, nu spune fata de ce s-a calculat scaderea de 66% si nu explica ce intra la "costuri". Nu apar sume in bani. Iar "aproape jumatate" este un rezultat, pe cand 85% este o tinta. Fraza despre incredere si oameni in bucla e, in schimb, o buna descriere a abordarii graduale din aceasta carte.

**Exemplul 2: Cordoba (Argentina).** Pe 21 septembrie 2026, baza de date OECD.AI a adaugat o initiativa a provinciei Cordoba, "AI for resilient digital government services", despre un sistem de operare asistat de AI pentru infrastructura cloud a administratiei [S30]. Pagina vorbeste despre peste 3,8 milioane de locuitori deserviti si despre un MVP care a tratat "more than 25 incidents with over 90% success", cu timpul de diagnostic redus de la aproximativ o ora la sub trei minute. Rezultatele par raportate de proiect insusi, iar pagina nu spune ca au fost verificate independent.

Observatii de cititor atent: pagina da in prezentare cifra de 66 de conturi AWS, dar in alta sectiune vorbeste despre extinderea la 26 de conturi de productie, fara sa explice relatia dintre ele. Spune ca faza curenta "operates strictly in read-only mode", dar descrie si un flux in sapte etape cu o etapa de executie si un sistem care a tratat incidente "autonomously". Poate exista o explicatie simpla, de exemplu faze diferite. Pagina nu o da. Nu avem nici date de baza, nici marimea esantionului, nici definitia unui "incident".

**Lista de intrebari pentru orice astfel de cifra:**

1. **Cine o raporteaza?** Furnizorul, clientul sau un tert independent?
2. **Ce perioada acopera?** O luna, un an, un pilot?
3. **Fata de ce se compara?** Care este situatia de dinainte, masurata cum?
4. **Ce inseamna exact metrica?** "Cost" inseamna bani cheltuiti mai putin sau timp reorientat catre alte sarcini? "Succes" inseamna rezolvat sau inchis?
5. **Cat de mare e esantionul?** 25 de incidente sau 25.000?
6. **Rezultat sau tinta?** Cifrele aspirationale se amesteca usor cu cele obtinute.
7. **E coerent textul cu el insusi?** Numere sau faze care se bat cap in cap sunt un semnal sa ceri clarificari.
8. **Exista o a doua sursa?** Fara ea, retii cifra ca "afirmata de", nu ca "dovedita".

Aplicata asupra propriilor tale proiecte, aceeasi lista te protejeaza de entuziasmul de dupa o demonstratie reusita. Cazurile de mai sus sunt, ca exemple de comunicare publica, utile tocmai pentru ce lasa nespus, nu pentru ca ar fi false.

