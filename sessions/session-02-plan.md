# Session 2: The web, asking a machine for data

Notebook `notebooks/02_web.ipynb`, Lösung `02_web_solution.ipynb`, Builder `build/s02.py`.
Eine Idee: Eine URL ist eine Frage an eine Maschine; Teile, Name zu Nummer, GET, Statuscode, und ein
Query-Parameter ändert die Frage.

## Zeitraster (Freitag 09:00 bis 11:00)

| Zeit | Minute | Was |
|---|---|---|
| 09:00 | 0–5 | Hub-Login, Notebook öffnen. Anknüpfen: der Teddy kam letzte Woche "aus dem Web", heute wie |
| 09:05 | 5–13 | Step 1: TISS-URL zerlegen, Tabelle vorne an der Tafel, dann `urlsplit` |
| 09:13 | 13–22 | Step 2: eigene URL vom Handy kopieren (Wiener Linien, willhaben, YouTube). Herumgehen: fehlendes `https://`, Leerzeichen, Anführungszeichen |
| 09:22 | 22–30 | Step 3: DNS mit `gethostbyname`, Ports-Tabelle. Optional im Terminal `nslookup tiss.tuwien.ac.at` |
| 09:30 | 30–45 | Step 4: GET auf die eigene URL, die Anfrage als Text, 404 auf TISS |
| 09:45 | 45–55 | Step 5: die Lücke (`params`-Dictionary), Wetterkurve, dann 7 Tage, eigene Koordinaten, 30 Tage → 400 |
| 09:55 | 55–65 | Pause. Vorher den Link zum Occupancy Sensor (QR-Code) zeigen; zwei Freiwillige zählen die Rückkehr an der Tür |
| 10:05 | 65–75 | Step 6: index.html (Lernkarten-App dreimal), Kasten Occupancy Sensor, Ergebnis der Türzähler ansehen, CSV aufheben für Einheit 5 |
| 10:15 | 75–82 | Step 7: POST, zwei Sätze, Passwortfrage |
| 10:22 | 82–88 | Tests laufen lassen (forecast_days zurück auf 1 bis 16!) |
| 10:28 | 88–95 | Puffer für Nachzügler aus Step 2/5 |
| 10:35 | 95–105 | Kurztest (TUWEL), siehe `privat/session-02-extras.md` |
| 10:45 | 105–115 | Hausübung vorstellen: drei eigene URLs, eine holen, einen Parameter ändern; Beispiel einmal laufen lassen |
| 10:55 | 115–120 | Fragen |

Rund 75 Minuten Arbeit. Wenn das Netz am Hub ausfällt: Step 1, 2, 7 und die Tests laufen offline,
Step 5 zeigt die gespeicherte Wetterkopie (`data/weather_vienna_sample.json`, 12.10.2026, 72 Stunden).

## Zahlen, die im Unterricht vorkommen (Referenzlauf 12.10.2026)

- TISS-URL: Host `tiss.tuwien.ac.at`, Port 443 (Default), Pfad `/course/courseDetails.xhtml`, Query
  `courseNr=259021`, `semester=2026W`, Fragment `groups`.
- DNS: `tiss.tuwien.ac.at` → 128.130.32.110, `www.wienerlinien.at` → 167.86.50.133,
  `gabriel-wurzer.github.io` → 185.199.108.153 (eine von mehreren GitHub-Adressen, kann wechseln).
- GET TISS-Kursseite: 200, `text/html;charset=UTF-8`, 7 967 Bytes, Server `Apache`.
  Wiener-Linien-Startseite mit Query: 200, rund 118 kB.
- TISS `/this-page-does-not-exist`: 404, trotzdem 11 997 Bytes Fehlerseite.
- Open-Meteo, 3 Tage: 200, `application/json`, rund 2 000 Bytes, 72 Stundenwerte; 7 Tage: 168;
  30 Tage: 400 (erlaubt bis 16). Die URL enthält `timezone=Europe%2FVienna`.
- Lernkarten-App: `/index.html`, `/` und ohne Schrägstrich je 12 034 Bytes, die letzte nach einem 301.
- Größen von Live-Seiten ändern sich; Zahlen nur als Größenordnung nennen.

## Stolpersteine

- URL ohne `https://` aus der Handy-Adresszeile: Prüfzelle sagt es; bis dahin läuft alles mit TISS weiter.
- Manche Seiten antworten Programmen mit 403 oder einer Cookie-Seite. Das ist ein Ergebnis, kein Fehler.
- Wer in Step 5 bei 30 Tagen stehen bleibt, bekommt keine Kurve und einen roten Test. Vor den Tests ansagen.
- Occupancy-Sensor-Link steht bei Redaktionsschluss noch nicht fest (App wird parallel gebaut); vor der
  Einheit in TUWEL eintragen und QR-Code bereithalten.
