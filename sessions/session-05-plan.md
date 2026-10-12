# Einheit 5: Putting it together, ein digitaler Zwilling des Hörsaals

Notebook `notebooks/05_twin.ipynb` (Lösung `05_twin_solution.ipynb`), Builder `build/s05.py`.
Rückblick auf die Einheiten 1 bis 4 als ETL-Pipeline: Türereignisse als CSV, Außentemperatur von
Sensoto als JSON, Prüfen und Reparieren, fünf Minuten-Schritte, SQLite, ein Plotly-Dashboard.

## Vorbereitung

- Link zur Occupancy-Sensor-App in TUWEL; vorher selbst am Handy testen (Kamera, HTTPS).
- Ein Handy an der Saaltür aufstellen und ab 09:00 laufen lassen, damit es eine echte Aufzeichnung des
  Vormittags gibt, die man nach der Pause zeigen kann.
- **Außentemperatur-Kopie:** `data/outdoor_temperature_2026-10-16.json` ist derzeit ein Platzhalter aus
  der Open-Meteo-Vorhersage (Stand 12.10.2026), weil die Station Wien Hohe Warte (GHCN hourly über
  Sensoto) einige Tage verzögert veröffentlicht. Ab etwa 20.10. das Lösungsnotebook einmal laufen
  lassen: Sobald Sensoto Werte liefert, überschreibt Schritt 4 die Kopie mit der echten Antwort.
  Danach die Temperaturzahlen unten nachtragen.
- Sensor 19330 (luftdaten, aus den Vorjahren) liefert seit August 2026 nichts mehr; im Notebook als
  Beispiel genannt. Vor der Einheit kurz prüfen, ob das noch stimmt.

## Zeitraster (Freitag 09:00 bis 11:00)

| Zeit | Min. | Was | Anmerkung |
|---|---|---|---|
| 09:00 | 5 | Einstieg: Zwilling, 40 Jahre, Sensor 19330 | keine Folien, Notebook-Kopf |
| 09:05 | 7 | Schritt 1: App am Handy, Hand durchs Bild | wer kein Handy hat, schaut beim Nachbarn; App läuft weiter bis nach der Pause |
| 09:12 | 5 | Schritt 2: ETL mit vier Ereignissen | an der Tafel nachrechnen: 1 Person um 09:05, 2 um 09:10 |
| 09:17 | 8 | Schritt 3: CSV einlesen | 33 in, 34 out, letzte Zeile −1 |
| 09:25 | 8 | Schritt 4: Sensoto, eigene Kopie | JSON-Datei im Dateibrowser öffnen |
| 09:33 | 10 | Schritt 5: Zeiten, Prüfen, Reparieren | Tabelle von Hand: 1, 0, −1, 0 wird 1, 0, 0, 1 |
| 09:43 | 7 | Schritt 6: Lücke (resample) | die eine Zeile; wer fertig ist, liest die Antwort zu `.ffill()` |
| 09:50 | 10 | **Pause** | App läuft weiter, die Pause soll in der eigenen Aufzeichnung sein |
| 10:00 | 12 | Schritt 7: SQLite, Zeilen zählen, SELECT, JOIN | 67 / 29 / 24 Zeilen |
| 10:12 | 8 | Schritt 8: Dashboard | Spitze, Pause, Ende suchen |
| 10:20 | 10 | Schritt 9: eigene CSV hochladen und laden | Hochladen vom Handy ist der Engpass, helfen |
| 10:30 | 5 | Tests | |
| 10:35 | 10 | **Kurztest** (Minute 95 bis 105) | `sessions/privat/session-05-extras.md` |
| 10:45 | 5 | Rückblick: fünf Einheiten, drei Gewohnheiten, node-red-Kasten | |
| 10:50 | 10 | Hausübung vorstellen | Tür zu Hause, 20 Minuten; ohne Handy von Hand mitschreiben |

## Zahlen, die in der Einheit vorkommen (Beispieldatei)

- 67 Türereignisse, 08:43:43 bis 11:04:40; 33 `in`, 34 `out`; letzte Zeile occupancy −1.
- Sensor-Zählung niedrigster Wert −1, höchster 20; nach der Reparatur 0 und 20; **1 Fehlzählung**
  repariert (das letzte `out` um 11:04:40).
- Eingebaut sind drei Fehler (`build/make_door_events.py`): zwei Studierende nebeneinander als einer
  gezählt, ein zusätzliches `out` in der Pause, ein doppeltes `in` beim Zurückkommen. Die letzten zwei
  heben sich auf. Laut Geschichte waren 21 Personen da (20 Studierende und Vortragender), der Zwilling
  sagt 20. Nach der Pause wirklich 19, der Zwilling sagt 18.
- 29 Fünf-Minuten-Schritte, 08:40 bis 11:00. Spitze 20 Personen, erstmals um 09:21; im Fünf-Minuten-Raster und im SQL-SELECT der Schritt 09:20.
- Pause: Senke ab 09:45, Fünf-Minuten-Werte 7 und 6 (Ende 09:50 und 09:55), ab 10:05 wieder 18. Die Zählung steigt um 12, laut Geschichte kamen 11 zurück (einer doppelt gezählt).
- Datenbank: 67, 29 und 24 Zeilen.
- Mittel je Stunde (JOIN): 08:00 5,5; 09:00 16,7; 10:00 18,0; 11:00 0,0. Die 09:00-Stunde ist trotz der
  Spitze niedriger, weil die Pause darin liegt.
- Außentemperatur (derzeit Platzhalter): 24 Stundenwerte, 4,9 bis 16,1 °C; 09:00 6,8, 10:00 9,4,
  11:00 11,7. Nach dem Austausch der Kopie neu eintragen.

## Was schiefgehen kann

- Hochladen der CSV vom Handy in den Hub: Upload-Pfeil im Dateibrowser, oder Datei an sich selbst
  schicken. Dateiname der App: `door_events_<Raum>_<Datum>.csv`.
- Kein Internet im Saal: Schritt 4 nimmt die Kopie; für eigene Aufzeichnungen vom selben Tag gibt es
  noch keine Stationswerte, der Zwilling läuft dann ohne Temperatur weiter (so gemeldet).
- Wer die Lücke nicht hat, bekommt ab Schritt 6 Fehler; die Antwort steht im `<details>` darunter.
