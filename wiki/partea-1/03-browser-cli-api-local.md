# 3. Unde folosim un model: browser, aplicatie, CLI, API si infrastructura locala

## 3.1. Browserul: punctul obisnuit de intrare

Pentru un incepator, cel mai simplu mod este un chatbot in browser. Scrii intrebarea, adaugi eventual un fisier si primesti un raspuns. Interfata se ocupa de autentificare, prezentarea conversatiei si, unde exista, accesul la instrumente. Este potrivit pentru explicatii, redactare, idei, rezumate si experimente fara operatii sensibile.

Limita este ca functiile vizibile nu dezvaluie intreaga arhitectura din spate. Aplicatia poate alege un model, poate comprima istoricul, poate gestiona fisiere in spatii separate si poate impune reguli de utilizare. Nu trebuie sa presupunem ca istoricul afisat pe ecran coincide integral cu ceea ce este trimis modelului la fiecare cerere.

## 3.2. Aplicatia instalata si CLI-ul

O aplicatie desktop poate oferi acces convenabil la fisiere, notificari sau alte functii ale sistemului, in limitele permisiunilor. **CLI** inseamna *command-line interface*, adica o interfata controlata prin comenzi text. Un CLI pentru lucrul cu AI poate citi proiecte, poate executa teste si poate modifica fisiere. Dar CLI nu este sinonim cu „model local”. Foarte multe CLI-uri folosesc modele gazduite in cloud.

Diferenta importanta nu este culoarea terminalului, ci ce poate face aplicatia: numai genereaza text, sau poate utiliza instrumente? Poate scrie fisiere? Poate executa comenzi? Are nevoie de confirmare? Pastreaza jurnalul? Se poate reveni la versiunea anterioara?

## 3.3. API-ul: modelul devine o componenta a altui program

**API** inseamna o interfata prin care un program solicita functii altui serviciu. In loc sa scriem manual intr-un browser, propria aplicatie trimite o cerere catre un model si primeste un raspuns. Prin API putem construi un sistem de asistenta pentru clienti, un procesor de documente sau un serviciu de analiza. Modelul nu capata automat acces la calculatorul nostru. Programul decide ce transmite, ce primeste si ce permite sa se execute.

Exemplu: un site trimite modelului mesajul utilizatorului si trei articole de suport. Modelul propune un raspuns. Programul il poate verifica, afisa sau trimite spre aprobare. In toate etapele, programul ramane responsabil de controlul accesului si de actiunile finale.

## 3.4. Rularea locala, pe scurt

Unele modele pot fi rulate pe echipamente proprii cu ajutorul unui **motor de inferenta**. Exemple de tehnologii din aceasta categorie sunt llama.cpp, Ollama si vLLM, cu roluri si moduri de operare diferite. Motorul incarca modelul, gestioneaza calculul si expune, eventual, un API. Hardware-ul, formatul greutatilor, memoria si configuratia limiteaza ce putem rula. Uneori modelul ruleaza pe CPU, alteori pe GPU sau pe hardware specializat.

Nu este obligatoriu ca aplicatia sau harness-ul sa fie pe aceeasi masina cu motorul de inferenta. Un program poate fi rulat local si poate consulta un model in cloud. Invers, un agent accesat din alta masina poate folosi un model servit de propriul nostru calculator. Aceste optiuni au consecinte asupra costurilor, confidentialitatii, latentei si administrarii.

## 3.5. Trei intrebari practice

Cand alegem un mod de utilizare, intrebarile bune sunt: **ce date trimitem**, **ce operatii vrem sa executam** si **cine raspunde cand ceva merge gresit**. Pentru o intrebare despre istorie, un chatbot este suficient. Pentru un script care muta fisiere, avem nevoie de acces controlat si jurnal. Pentru o aplicatie care prelucreaza date sensibile, conteaza termenii serviciului, pastrarea datelor si eventualele restrictii legale.

Nu vom atribui performante absolute unor produse. Capacitatile, planurile si modelele disponibile se schimba frecvent. Exemplele de produse sunt puncte de orientare, nu recomandari permanente.
