# Format einer Einheit (Lehren aus Session 1, Oktober 2026)

Gilt für alle zehn Einheiten. Session 1 (`notebooks/01_neuron.ipynb`) ist das Muster.

## Publikum

Drittes Semester Building Sciences and Environment, fast alle Architekten. Kein Mathe, keine
Statistik, kein Programmieren im Bachelor; im Master ein Mathe-Kurs und Grasshopper. Sie lesen
Python, schreiben aber keine Formeln. Gen Z: ohne schnelle Belohnung schalten sie ab.

## Aufbau

- Eine Idee pro Einheit. Was nicht in etwa 75 Minuten Arbeitszeit passt, fliegt raus oder
  wandert in eine eigene Einheit.
- Nummerierte Schritte ("Step 1: ..."), jeder mit etwas zum Tun: Regler, eigene Eingabe, kurze
  Lücke. Höchstens drei, vier Sätze Text am Stück.
- Erst ein kleines Rechenbeispiel mit Zahlen zum Nachrechnen, dann der Begriff, dann der Code.
- Keine Ableitungen, keine Summen- oder Ableitungszeichen. Nur Grundrechnungsarten im Text.
- Jeder Begriff wird eingeführt, bevor er benutzt wird. Jede Frage ist an ihrer Stelle mit dem
  bis dahin Gezeigten beantwortbar.
- Jede Frage im Unterrichtsteil bekommt darunter ein `<details>`-Feld "Answer".
- Ein persönlicher Faden: etwas Eigenes (das eigene Haus, eigene Eingabe) taucht am Anfang auf
  und am Ende wieder.
- Interaktive Bilder dort, wo etwas verstanden werden soll: Regler (Plotly-Frames oder eigenes
  HTML mit `post_script`), Hover-Kasten mit Copy-Knopf statt Abtippen.
- Bilder müssen etwas zeigen: Farbskalen prüfen (logarithmisch bei großem Wertebereich), feste
  Achsen, Ausschnitt dort, wo es passiert, kein Text, der Bilder verdeckt. Jede Grafik im Browser
  ansehen, bevor sie rausgeht.

## Code

- Nur englische Namen: Variablen, Funktionen, Spalten, Dateien.
- Jede Anweisung mit einem Kommentar in einfachem Englisch.
- Reiner Zeichencode wird eingeklappt (`metadata.jupyter.source_hidden`), mit einem Satz Kommentar.
- Die Lücke ("YOUR TURN") ist eine Übersetzung: Der Kommentar sagt wörtlich, was hinkommt;
  direkt davor steht ein Beispiel in Python-Schreibweise. Formeln stecken in eingeklappten
  Hilfszellen, mit einer sichtbaren Kontrolle, dass sie stimmen.
- Freundliche Rückmeldung nach jeder Zelle ("✓ ..."); Fehler mit Hinweis, was zu tun ist.
- Eingaben der Studierenden prüfen und verständlich melden.

## Hausübung

- Festigen und auf den eigenen Alltag übertragen, mit Spaß. Kein neuer Stoff, keine Prüfung,
  keine Fallen, keine Live-Kontrolle.
- Eigene Daten oder ein eigenes Beispiel; ein ausgearbeitetes, realistisch unordentliches
  Beispiel ist vorausgefüllt, mit aufklappbaren Musterantworten.
- Vier kurze Fragen zum eigenen Fall, je ein bis drei Sätze. "I cannot tell from my data,
  because ..." ist eine gute Antwort.
- 4 Punkte für den Lauf (eigene Daten, Ergebnis, Abbildung, läuft durch), 6 für die Antworten
  zusammen. Unverändertes Beispiel kostet den Datenpunkt, abgeschriebene Musterantworten die
  Antwortpunkte.
- Hinweis im Kopf: vor dem Aktualisieren das Notebook umbenennen.

## Daneben

- Kurztest: drei Fragen aus dem Unterrichtsteil, in `sessions/privat/`.
- Lernkarten: die Begriffe der Einheit als Karten mit `session`-Nummer, Bild je Karte
  (Bildwunsch in `webapps/flashcards/image_prompts.md`).
- Prüfschleife: Codex adversarial (Wissensstand an jeder Stelle, Zahlen, Verständlichkeit),
  Haiku-Studierendenagent (Architektin, Gen Z), bis nichts mehr blockiert.
