# 3. Unde folosim un model: browser, aplicatie, CLI, API si infrastructura locala

## 3.1. Browserul: poarta de intrare obisnuita

Pentru un incepator, cel mai simplu e un chatbot in browser. Scrii intrebarea, adaugi eventual un fisier si primesti un raspuns. Interfata se ocupa de autentificare, de afisarea conversatiei si, unde exista, de accesul la unelte. Merge bine pentru explicatii, redactare, idei, rezumate si experimente fara operatii sensibile.

Limita: ce vezi pe ecran nu arata toata arhitectura din spate. Aplicatia poate alege un model, poate comprima istoricul, poate tine fisierele in spatii separate si poate impune reguli de utilizare. Sa nu presupui ca istoricul afisat este exact ce primeste modelul la fiecare cerere.

## 3.2. Aplicatia instalata si CLI-ul

O aplicatie desktop poate oferi acces comod la fisiere, notificari sau alte functii ale sistemului, in limitele permisiunilor. **CLI** vine de la *command-line interface*, adica o interfata controlata prin comenzi text. Un CLI pentru lucrul cu AI poate citi proiecte, rula teste si modifica fisiere. Dar CLI nu inseamna "model local". Multe CLI-uri folosesc modele gazduite in cloud.

Diferenta care conteaza nu e culoarea terminalului, ci ce poate face aplicatia. Doar genereaza text, sau poate folosi unelte? Poate scrie fisiere? Poate rula comenzi? Cere confirmare? Pastreaza un jurnal? Putem reveni la versiunea de dinainte?

## 3.3. API-ul: modelul devine o piesa dintr-un alt program

**API** este o interfata prin care un program cere functii de la un alt serviciu. In loc sa scrii tu intr-un browser, propria ta aplicatie trimite o cerere catre un model si primeste un raspuns. Asa se construiesc asistenti pentru clienti, procesatoare de documente sau servicii de analiza. Modelul nu capata acces la calculatorul tau. Programul decide ce trimite, ce primeste si ce are voie sa se execute.

Un exemplu: un site trimite modelului mesajul unui utilizator si trei articole de suport. Modelul propune un raspuns, iar programul il poate verifica, afisa sau trimite spre aprobare. La fiecare pas, programul ramane raspunzator de controlul accesului si de actiunile finale.

## 3.4. Rularea locala, pe scurt

Unele modele pot rula pe echipamente proprii cu ajutorul unui **motor de inferenta**. llama.cpp, Ollama si vLLM sunt exemple din aceasta categorie, cu roluri si moduri de lucru diferite. Motorul incarca modelul, face calculul si poate expune un API. Hardware-ul, formatul greutatilor, memoria si configuratia limiteaza ce poti rula. Uneori merge pe CPU, alteori pe GPU sau pe hardware specializat.

Aplicatia sau harness-ul nu trebuie sa fie pe aceeasi masina cu motorul. Un program local poate apela un model din cloud. Invers, un agent pornit de pe alt calculator poate folosi un model servit de masina ta. Fiecare varianta schimba costurile, confidentialitatea, latenta si munca de administrare.

## 3.5. Trei intrebari practice

Cand alegi cum folosesti AI-ul, intreaba-te: **ce date trimit**, **ce operatii vreau sa se execute** si **cine raspunde cand ceva merge prost**. Pentru o intrebare de istorie ajunge un chatbot. Pentru un script care muta fisiere ai nevoie de acces controlat si de jurnal. Pentru o aplicatie care lucreaza cu date sensibile, conteaza termenii serviciului, cat timp se pastreaza datele si restrictiile legale.

Nu atribuim performante absolute unor produse. Capacitatile, planurile si modelele se schimba des. Produsele pe care le dam ca exemplu sunt repere, nu recomandari pe termen lung.
