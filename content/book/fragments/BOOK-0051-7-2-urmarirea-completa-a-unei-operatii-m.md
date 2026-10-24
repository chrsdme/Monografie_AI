### 7.2. Urmarirea completa a unei operatii meteo

Sa zicem ca utilizatorul intreaba: "Cat e de cald la Paris, Franta?". Sistemul poate produce un jurnal simplificat:

```text
run_id: meteo-104
cerere: "Paris, Franta, acum"
tool_call: geocode(city="Paris", country="FR")
tool_result: latitude=48.86, longitude=2.35
tool_call: weather(latitude=48.86, longitude=2.35)
tool_result: temperature=18.2, observed_at=...
raspuns_final: "La Paris sunt 18,2 grade..."
validare: orasul corespunde; valoarea se potriveste; sursa este recenta
```

Valorile sunt ilustrative, nu o observatie meteo reala. Ideea e ca fiecare veriga se poate inspecta. Daca raspunsul iese gresit, poti vedea daca s-a ales Paris din Texas, daca serviciul a returnat date vechi sau daca modelul a copiat prost temperatura.

