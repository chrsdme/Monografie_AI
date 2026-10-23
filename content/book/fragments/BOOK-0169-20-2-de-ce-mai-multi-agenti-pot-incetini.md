### 20.2. De ce mai multi agenti pot incetini sistemul

Sa zicem ca o sarcina simpla se rezolva cu un apel de model si un test. Daca o imparti intre patru agenti, adaugi pregatirea contextului, transferuri, verificarea contractelor si sintetizarea rezultatelor. Poate iesi mai lent si mai scump. Paralelizarea ajuta doar cand munca se poate separa, exista resurse suficiente si costul coordonarii nu anuleaza castigul.

Un sistem cu sase instante care folosesc acelasi model pe un singur accelerator nu e automat de sase ori mai rapid. Serviciul poate pune cererile la coada, poate imparti capacitatea sau poate atinge limitele de memorie. De aceea masori **durata completa a workflow-ului**, nu doar viteza unui apel individual.

