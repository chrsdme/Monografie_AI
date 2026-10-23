### 19.3. Checkpoint si reluare

Un **checkpoint** este un punct in care se salveaza starea necesara continuarii. De exemplu, dupa procesarea primelor 200 de documente din 1.000, sistemul poate salva identificatorii celor procesate si rezultatele validate. La o intrerupere reia de la pasul urmator, fara sa repete operatiile deja confirmate. Checkpoint-ul se leaga de versiunea datelor si a procesului; altfel, o schimbare intre doua rulari poate invalida reluarea.

Un detaliu de implementare care loveste din senin: in LangGraph, cand un nod se intrerupe pentru aprobare si apoi este reluat, nodul reporneste de la inceputul lui, nu din punctul exact al intreruperii. Efectele secundare dinaintea intreruperii trebuie sa fie idempotente, altfel se pot repeta [S29]. Regula e valabila mai larg: cand reiei un pas, presupune ca partea dinainte se va executa din nou.

