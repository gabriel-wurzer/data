# Session 4: Databases, Ordnung in den Daten

Notebook `notebooks/04_databases.ipynb`, Lösung `04_databases_solution.ipynb`, Builder `build/s04.py`.
Eine Idee: Daten, die aufeinander verweisen, gehören in Tabellen mit Schlüsseln, und SQL fragt sie ab.
Gebäudebeispiel statt Schule aus v2: `rooms`, `sensors`, `readings`. Das eigene Zimmer kommt in Step 4
als Raum 6 dazu und taucht im JOIN wieder auf.

## Zeitraster (Freitag 09:00 bis 11:00)

| Zeit | Minute | Was |
|---|---|---|
| 09:00 | 0–5 | Hub-Login, Notebook öffnen, Ziel zeigen: am Ende das eigene Zimmer in der Temperaturrangliste |
| 09:05 | 5–15 | Step 1: geteilte Logdatei, sechs Schreibweisen für zwei Räume; kurz Codd 1970, SQL, NoSQL |
| 09:15 | 15–22 | Step 2: Tabelle, Zeile, Spalte, Schlüssel; `building.db` öffnen, `CREATE TABLE rooms` |
| 09:22 | 22–35 | Step 3: `INSERT`, `commit`, Fremdschlüssel, Sensoren und Messwerte, Sensor in Raum 99 wird abgelehnt |
| 09:35 | 35–42 | Step 4: eigenes Zimmer eintragen. Zweimal ausführen lassen: der Schlüssel lehnt ab |
| 09:42 | 42–52 | Step 5: `WHERE`, `ORDER BY ... DESC`, Text in einfachen Hochkommas |
| 09:52 | 52–55 | Step 6: die Lücke, `WHERE floor = 2` |
| 09:55 | 55–65 | Pause |
| 10:05 | 65–75 | Step 7: JOIN Sensor zu Raum, dann drei Tabellen, `AND`, `AS`; eigenes Zimmer im Balken suchen |
| 10:15 | 75–83 | Step 8: `UPDATE` (Library heißt jetzt Reading room, JOIN unverändert neu laufen lassen), `DELETE` des Ausreißers |
| 10:23 | 83–90 | Step 9: `read_sql`, Filter in pandas, `to_sql`, Datei schließen und wieder öffnen |
| 10:30 | 90–95 | Tests laufen lassen |
| 10:35 | 95–105 | Kurztest (TUWEL), siehe `privat/session-04-extras.md` |
| 10:45 | 105–115 | Hausübung vorstellen: zwei Tabellen aus dem eigenen Leben, WG-Beispiel einmal laufen lassen |
| 10:55 | 115–120 | Puffer, Fragen |

Rund 80 Minuten Arbeit. Zeitnot: Step 9 nur bis `to_sql` zeigen, das Wiederöffnen ansagen.

## Zahlen, die im Unterricht vorkommen

- Logdatei Step 1: 6 Zeilen, 2 Räume, 6 Schreibweisen.
- Räume: Lecture hall (EG, 180 m²), Seminar room (1, 48), Library (1, 120), Studio (2, 95),
  Server room (2, 12). Eigenes Zimmer im Beispiel: "my room", Stock 1, 14 m², 21,0 °C.
- 7 Sensoren, davon 2 CO2 (Lecture hall, Studio). 15 Messwerte, einer davon −40 °C (Sensor 3, 10:30).
- Sensor 6: Studio, CO2, 900 ppm um 10:00.
- `WHERE area_m2 > 50`: 3 Räume. Sortiert landet das Beispielzimmer an fünfter von sechs Stellen.
- Lücke: Studio und Server room (plus eigenes Zimmer, falls Stock 2).
- Temperaturen 10:00: Server room 27,5, Studio 23,5, Lecture hall 22,0, Seminar room 21,5,
  my room 21,0, Library 20,0.
- Nach UPDATE und DELETE: 6 Räume, 8 Sensoren, 15 Messwerte. Tabellen in der Datei: rooms, sensors,
  readings, big_rooms.

## Stolpersteine

- Step 4 zweimal ausführen: absichtlich abgelehnt. Wer Werte ändern will, Run All.
- Hochkommas: SQL-Text in einfachen, der Python-String in doppelten. Wer `"co2"` in SQL schreibt, bekommt
  einen Spaltenfehler.
- Wer die Lücke ohne Anführungszeichen schreibt, bekommt einen Python-Syntaxfehler, kein SQL-Problem.
- `building.db` und `my_life.db` entstehen im Notebook-Ordner und werden bei jedem Lauf neu angelegt.
