# Session 3: Sensors, data as JSON

Notebook `notebooks/03_sensors.ipynb`, Lösung `03_sensors_solution.ipynb`, Builder `build/s03.py`.
Daten `data/vienna_sensors.json` und `data/sensor_fallback.json`, erzeugt von `data/sensor_fallback_fetch.py`.
Eine Idee: JSON lesen, aus einem echten Sensor über die API, in eine Tabelle, drei Zahlen und ein Bild.

## Zeitraster (Freitag 09:00 bis 11:00)

| Zeit | Minute | Was |
|---|---|---|
| 09:00 | 0–5 | Hub-Login, Notebook öffnen, Ziel zeigen: ein Monat Temperatur aus dem eigenen Bezirk |
| 09:05 | 5–15 | Step 1: eine Messung als JSON, `json.loads`, `reading["temperature"]`, KeyError mit großem T (Zelle danach löschen!) |
| 09:15 | 15–27 | Step 2: Liste und Objekt im Objekt, `vienna_sensors.json` im Dateibrowser öffnen, Karte, eigenen Bezirk wählen |
| 09:27 | 27–37 | Step 3: API, ISO-8601-Intervall `R30/2025-10-17T00:00/P1D`, URL im Browser anklicken, Schlüssel `v hi lo c` |
| 09:37 | 37–45 | Step 4: `pd.DataFrame`, Umbenennen, `pd.to_datetime` |
| 09:45 | 45–55 | Step 5: die Lücke (`table["temperature"].mean()`), kältester und wärmster Tag |
| 09:55 | 55–65 | Pause |
| 10:05 | 65–75 | Step 6: Plot, dann alle fünf Bezirke: wer war am wärmsten, warum (Stadtrand, Sensorort) |
| 10:15 | 75–83 | Step 7: `PT12H`, Zickzack, Höchstwert bleibt gleich |
| 10:23 | 83–91 | Step 8: XML, `xml.etree`, Text statt Zahl, warum JSON fürs Web |
| 10:31 | 91–95 | Tests laufen lassen |
| 10:35 | 95–105 | Kurztest (TUWEL), siehe `privat/session-03-extras.md` |
| 10:45 | 105–115 | Hausübung vorstellen: eigener Zeitraum, vorher aufschreiben, woran man sich erinnert; Beispiel einmal laufen lassen |
| 10:55 | 115–120 | Puffer, Fragen |

Rund 80 Minuten Arbeit. Wenn es knapp wird, Step 8 auf Vorzeigen kürzen; die Tests brauchen nur die
Zelle aus Step 8 ausgeführt.

## Zahlen, die im Unterricht vorkommen

Alle für Leopoldstadt (Vorgabe), 17.10. bis 15.11.2025, abgefragt am 12.10.2026.

- Step 1: 11.6 °C, plus eins 12.6. Step 2: dritter Sensor Penzing, Länge 16.26.
- Step 3: erster Tag `v` 13.3, `hi` 14.8, `lo` 11.6, Spanne 3.2 Grad; 30 Einträge.
- Step 4: 17.10.2025 war ein Freitag, Zeitraum 30 Tage.
- Step 5: Mittel 11.2 °C, tiefster Wert 4.8 °C (Mi 12.11.), höchster 19.3 °C (Do 23.10.), Mitte zwischen beiden 12.1 °C.
- Step 6, Mittel der fünf: Penzing 11.9, Leopoldstadt 11.2, Favoriten 11.2, Floridsdorf 9.7, Donaustadt 9.3 °C.
- Step 7: 60 Halbtage, zweite Hälfte an 27 von 30 Tagen wärmer, Höchstwert 19.3 in beiden, Mittel 11.18 und 11.19 °C.
- Step 8: dieselbe Messung 139 Zeichen XML, 101 Zeichen JSON.

Wer einen anderen Bezirk wählt (Step 5, gleicher Zeitraum):

| Bezirk | Mittel | tiefster Wert | höchster Wert | erster Tag `v` |
|---|---|---|---|---|
| Leopoldstadt | 11.2 | 4.8 (12.11.) | 19.3 (23.10.) | 13.3 |
| Favoriten | 11.2 | 3.9 (19.10.) | 21.5 (23.10.) | 12.8 |
| Penzing | 11.9 | 2.5 (19.10.) | **39.0 (04.11.)** | 12.1 |
| Floridsdorf | 9.7 | −1.0 (19.10.) | 21.6 (23.10.) | 11.6 |
| Donaustadt | 9.3 | −3.1 (19.10.) | 27.0 (04.11.) | 10.7 |

Penzing mit 39 °C im November: Sonne auf dem Sensor. Steht im Notebook als Antwort, gut für ein Gespräch.

## Was die API kann (geprüft 12.10.2026)

- `interval` ist Pflicht, ohne kommt 400. Form `R<Anzahl>/<Start>/<Periode>`, Start als `2025-10-17T00:00`
  (ein reines Datum geht mit `P1D`, aber nicht mit `PT12H`).
- Perioden: `PT1H`, `PT6H`, `PT12H`, `P1D`, `P1M`, `P1Y` gehen; `P1W` gibt 400.
- `agg` kennt nur `MEAN`; `MAX`, `MIN`, `MEDIAN` geben 400. `hi` und `lo` kommen ohnehin mit.
- `timeFormat=interval` fügt nur `end` hinzu, `interpolator=LINEAR` ändert nichts; beide weggelassen.
- Zeiten immer mit festem `+01:00`, auch im Sommer.
- Lücken: alle fünf Sensoren ohne Daten vom 25.07. bis 08.10.2026 (Leopoldstadt auch danach nicht);
  bei allen geprüften Sensoren Lücke 11.03. bis 27.04.2023; einzelne Tage, z. B. 16. und 17.03.2025.
- Gerätecodes enden auf einen Geohash (`u2ed…` = Wien); die Liste aller 101 081 Geräte lässt sich nur
  seitenweise holen, Filter nach Ort gibt es nicht.

## Stolpersteine

- Die KeyError-Zelle aus Step 1 muss wieder weg, sonst bricht Run All.
- Ohne Netz springt `../data/sensor_fallback.json` ein, aber nur für die Abfragen des Unterrichts und das
  Hausübungsbeispiel. Eigene Zeiträume brauchen Netz.
- Server-Fehler 5xx nimmt ebenfalls die gespeicherte Kopie; 400 (z. B. `P1W`) wird gemeldet.
- pandas-Version: `begin` heißt je nach Version `object` oder `str`; der Text sagt beides.
- Plotly 6 verbindet Linien über `NaN` hinweg; `plot_period` gibt deshalb `None` weiter.
