# Session 1: Files, where data lives

Notebook `notebooks/01_files.ipynb`, Lösung `01_files_solution.ipynb`, Builder `build/s01.py`.
Eine Idee: Daten liegen als Dateien in Ordnern, und eine Datei ist Text in einem vereinbarten Format.

## Zeitraster (Freitag 09:00 bis 11:00)

| Zeit | Minute | Was |
|---|---|---|
| 09:00 | 0–5 | Hub-Login, Notebook öffnen, Ziel zeigen: am Ende der Teddy in 3D |
| 09:05 | 5–12 | Step 1: eigenes Zimmer in vier Werten |
| 09:12 | 12–20 | Step 2: Pfade, `!pwd`, `!ls`, `..` |
| 09:20 | 20–35 | Step 3: Terminal öffnen, `cd` aus der Zelle kopieren, `pwd ls mkdir -p cd`. Hier hängen die meisten, herumgehen |
| 09:35 | 35–42 | Step 4: `my_room.txt` schreiben, `cat`, im Dateibrowser öffnen |
| 09:42 | 42–55 | Step 5: die Lücke (`split`), dann Text vs. Zahl (`float`) |
| 09:55 | 55–65 | Pause |
| 10:05 | 65–78 | Step 6: Header und Version, alter Leser scheitert, Version 2, `read_room` |
| 10:18 | 78–85 | Step 7: CSV, `pd.read_csv`, Balken |
| 10:25 | 85–93 | Step 8: Teddy laden, v- und f-Zeilen, Punkte, dann Fläche |
| 10:33 | 93–95 | Tests laufen lassen |
| 10:35 | 95–105 | Kurztest (TUWEL), siehe `privat/session-01-extras.md` |
| 10:45 | 105–115 | Hausübung vorstellen: eigenes Format, Version 2 mit einer Änderung, Beispiel einmal laufen lassen |
| 10:55 | 115–120 | Puffer, Fragen |

Rund 80 Minuten Arbeit. Falls Step 3 ausufert: Wer `my_files` nicht anlegt, dem legt die Prüfzelle den
Ordner an, der Rest läuft weiter.

## Zahlen, die im Unterricht vorkommen

- Beispielzimmer: 14.5 m², 2 Fenster, 1 Person, 14.5 m² pro Person.
- Alter Leser auf Version-1-Datei: `not enough values to unpack (expected 2, got 1)` an der Zeile `ROOM FILE`.
- CSV mit Beispielwohnung: 4 Räume, 35.0 m² gesamt, Beispielzimmer 41 %.
- Teddy: 91538 Zeichen, 4790 Zeilen, 1598 v-Zeilen, 3192 f-Zeilen. Erste Zeile `v -4.75738 8.49991 8.28592`.
- Hausübungsbeispiel: je 7 Einträge, 2 Zeilen unterscheiden sich (umbenannter Schlüssel zählt doppelt),
  5 von 7 Werten sind Zahlen.

## Stolpersteine

- Terminal startet im Home-Ordner; ohne den kopierten `cd`-Befehl landet `my_files` dort.
- `!`-Zeilen laufen auf dem Hub (Linux). Lokal auf Windows gibt es `ls`, `cat`, `pwd` nur mit Git Bash im PATH.
- Raumname mit `=` oder Komma wird in Step 1 abgewiesen, sonst bricht `split`.
- Download des Teddys: bei Fehlschlag springt `../data/teddy.obj` ein, Meldung im Notebook.
- `my_files/` wird im Ordner `notebooks/` angelegt; nicht mit ins Repo nehmen.
