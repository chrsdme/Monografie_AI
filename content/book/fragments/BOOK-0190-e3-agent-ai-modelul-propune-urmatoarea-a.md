#### E3. Agent AI: modelul propune urmatoarea actiune

Agentul primeste obiectivul, instructiunile, contextul, instrumentele disponibile si o bucla de actiune-feedback. El poate decide sa caute comanda, sa verifice istoricul, sa ceara o fotografie sau sa escaladeze cazul. **Autorizarea nu vine din prompt.**

```text
OBIECTIV = "Rezolva cererea de rambursare"
INSTRUMENTE = [cauta_comanda, verifica_politica,
               verifica_duplicat, cere_dovezi, pregateste_rambursare,
               verifica_rezultat, trimite_confirmare, escaladeaza]
CONTEXT = [cerere, rezultate_verificate, actiuni_anterioare]

REPETA maximum 12 pasi:
    actiune = MODEL.alege_urmatorul_pas(OBIECTIV, CONTEXT, INSTRUMENTE)
    DACA actiunea este interzisa: escaladeaza(); OPRESTE
    DACA actiunea produce rambursare:
        verifica_identitate_eligibilitate_moneda_suma()
        verifica_duplicat_si_aprobare()
        DACA verificarea_esueaza: escaladeaza(); OPRESTE
    rezultat = DISPATCHER.executa_doar_actiunea_autorizata(actiune)
    CONTEXT.adauga(rezultat)
    DACA asteptam_clientul: salveaza_starea(); OPRESTE_TEMPORAR
    DACA rezultatul_final_este_verificat: OPRESTE
ALTFEL: escaladeaza_pentru_limita_de_pasi()
```

O bucla `REPETA` nu defineste singura un agent: conteaza daca modelul poate alege dinamic actiunile. Dispatcher-ul din aplicatie trebuie sa valideze argumentele, permisiunile, limitele si rezultatele.

**Trei cazuri:** 62 RON cu dovezi complete -> pregatire si verificare a operatiunii; 350 RON -> escalare fara plata; lipsa dovezii -> solicitare de clarificari si stare `WAITING_CUSTOMER`. Reincercarea unui API dupa timeout cere mai intai reconcilierea tranzactiei, ca sa nu rambursam de doua ori.

