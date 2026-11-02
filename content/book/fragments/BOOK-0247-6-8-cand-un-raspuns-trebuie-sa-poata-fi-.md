### 6.8. Cand un raspuns trebuie sa poata fi citit de un program

Pana acum am vorbit despre prompturi care cer explicatii. Dar ce se intampla cand rezultatul trebuie folosit de un alt program? Sa presupunem ca vrem sa transformam mesajele clientilor in tichete. Un raspuns precum "Pare o problema urgenta cu plata" este usor de citit de om, dar dificil de prelucrat automat fara reguli fragile.

Putem cere o **iesire structurata**, de exemplu un obiect JSON cu `category`, `urgency` si `summary`. Formatul stabileste cum arata datele. Nu stabileste singur daca ele sunt corecte. O valoare `urgency: 99` este un numar valid, dar poate incalca regula procesului care admite doar nivelurile 1, 2 si 3.

O validare completa are trei intrebari: **exista campurile obligatorii?**, **au tipurile si intervalele permise?**, **corespund datelor din mesaj si regulilor procesului?** Primele doua pot fi verificate mecanic. A treia poate cere consultarea sursei, reguli suplimentare sau revizuire umana. O biblioteca de validare precum Pydantic permite constrangeri explicite pentru campuri [S55].

Exemplu Python, ilustrativ, pentru verificarea structurii:

```python
from typing import Literal
from pydantic import BaseModel, Field, ValidationError

class Ticket(BaseModel):
    category: Literal["billing", "bug", "feature", "other"]
    urgency: int = Field(ge=1, le=3)
    summary: str = Field(min_length=1, max_length=500)

try:
    ticket = Ticket.model_validate_json(raw_model_output)
except ValidationError:
    ticket = None  # cazul ajunge la corectare sau revizuire
```

`raw_model_output` reprezinta textul JSON primit de la model; obtinerea lui nu este implementata in acest fragment. Nici o iesire care trece validarea de schema nu trebuie considerata automat adevarata. De exemplu, programul poate accepta perfect `category="billing"` pentru un mesaj care descrie un defect tehnic. Validarea structurii si validarea **sensului** sunt teste diferite.

**De retinut:** un format corect permite integrarea dintre sisteme; un rezultat corect necesita in plus dovezi si verificarea regulilor de afaceri.

