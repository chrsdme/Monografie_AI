### 19.2. Idempotenta: de ce conteaza enorm

Daca o unealta care citeste vremea e apelata de doua ori, costul poate creste, dar efectul extern e mic. Daca o functie de transfer financiar e apelata de doua ori, poti avea doua plati. **Idempotenta** este proprietatea prin care repetarea aceleiasi cereri nu produce efecte suplimentare nedorite. O tehnica este un identificator unic al operatiei, verificat de serviciul care aplica modificarea.

Daca starea unei operatii sensibile e necunoscuta dupa un timeout, procesul interogheaza intai sistemul, ca sa vada daca efectul exista deja. Reincercarea oarba e periculoasa.

