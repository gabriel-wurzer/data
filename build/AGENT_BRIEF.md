# Brief for building one session of v3

You build one session of a revamped TU Wien course: **259.021 Fundamentals of Utilizing Data Sources**
(working title; the v2 notebooks carry it). Same students as the sibling course in `C:/temp/data2`:
third-semester master's students in Building Sciences and Environment, mostly architects. No maths,
statistics or programming in their bachelor; they read a little Python but switch off when they must write
code. Gen Z: if nothing rewarding happens within a minute, they are gone.

**This course must be easy.** Easier than `C:/temp/data2`. No machine learning, no formulas. The skill is
handling data sources: files, the web, JSON from sensors, databases, putting them together. Students should
mostly run cells, change a value, see something happen, and fill one small, literal gap per session.

## The format (binding)

Read `C:/temp/data/v3/sessions/format.md` (German). It
was written for the sibling course; apply it here with these adjustments:

- Numbered steps ("Step 1: ..."), each with something to do. At most three or four sentences of prose at a
  time. A worked example with concrete values before every concept.
- Every question in the class part gets a `<details><summary>Answer</summary>...</details>` below it,
  answerable from what was shown up to that point.
- A personal thread: something of the student's own appears early and comes back (their room, their
  flat, their street, a sensor near their home).
- Interactive or visual reward where it helps (Plotly; sliders only where they explain something).
- English only, also all identifiers. Every code line has a short plain-English comment. Pure plotting or
  plumbing code is collapsed (`hidden=True` in the builder). Friendly `✓` messages after cells; student
  inputs validated with helpful messages.
- Exactly one gap ("YOUR TURN") per session, a literal translation: the comment says exactly what to write,
  and a Python example of the same form stands right before it in the markdown. The solution notebook
  differs from the student notebook only in that gap.
- End with "Tests" (they recompute, not just check existence), then "Where you stand now" with a terms table
  (4 to 6 terms), then the homework.
- Homework: consolidation and transfer to the student's own life, fun, no new material, no traps. A
  complete, realistically messy worked example is pre-filled, with example answers in a `<details>`.
  Four questions, one to three sentences each. Use `homework_header(...)` from the builder (4 points for
  running, 6 for answers). About one hour of work at home.
- Look at `C:/temp/data2/notebooks/02_two_inputs_solution.ipynb` and `03_kinks_solution.ipynb` (or the builder
  script `C:/temp/data/v3/build/example_session_from_other_course.py`) for the tone, density and structure.
  Do not copy their topics.

## Material to reuse (the lecturer's own earlier versions)

- `C:/temp/data/v2/data_lecture.ipynb`: basic types, writing/reading an own text file, a versioned file
  format (header, version 2), downloading the teddy OBJ and plotting it in 3D, HTTP overview.
- `C:/temp/data/v2/data_lecture2.ipynb`: databases, SQL with SQLite (CREATE, INSERT, SELECT, JOIN,
  UPDATE, DELETE), the same with pandas, writing back; plus exercises.
- `C:/temp/data/v2/data_lecture3.ipynb`: real sensors via the Sensoto API (JSON), pandas, mean temperature,
  XML (SensorML) glance. The API works (checked 12.10.2026), e.g.
  `https://api.sensoto.io/v1/organizations/open/networks/luftdaten-info/devices/19330-u2edkcj6uj4/sensors/temperature/measurements?interval=R30/2025-10-17T00:00:00.000%2B01:00/P1D&timeFormat=interval&agg=MEAN&interpolator=LINEAR&includeLatest=true`
- `C:/temp/data/v1/data.pptx` (text extract below): Unix in a shell (ls, mkdir, cd, pwd, cat, rm, chmod, the
  file system tree), web server directory and index.html, URLs (IP, DNS via nslookup, ports, protocols), HTTP
  GET/POST seen raw via telnet, virtualisation and docker, node-red (msg objects, JSON, inject/function/debug,
  HTTP in/out, HTTP request to fetch a website), occupancy sensor as a digital classroom twin.
- `C:/temp/data/v1/without-contacting-server/occupancy-sensor/index.html`: a browser page that uses the phone
  camera to count people walking through a door (the "gimmick"). A v3 version lives in
  `C:/temp/data/v3/webapps/occupancy-sensor/` (being built in parallel): it runs on GitHub Pages over HTTPS,
  counts in/out events and can download them as CSV with columns `time,event,occupancy`
  (ISO time, `in` or `out`, occupancy after the event). A sample file will be at
  `C:/temp/data/v3/data/door_events_sample.csv`.

## Running environment

Students use the TU Wien JupyterHub (JupyterLab 4, Python, pandas, plotly, requests; a terminal is
available). Notebooks live in `notebooks/`, data in `../data/`. Internet access from the hub is available.
For the sibling course a helper downloads nothing at import; do the same, and make every network call fail
with a friendly message (and a fallback file in `../data/` if the call is essential).

## How to build

- Builder: `C:/temp/data/v3/build/nbbau.py` (`Notebook().md()`, `.code(text, hidden=False, solution=None)`,
  `.write(stem)` writes `notebooks/{stem}.ipynb` and `notebooks/{stem}_solution.ipynb`; `DATA_BOX`,
  `homework_header`, `TERMS_FOOTER`, `box(title, text)`). Write your builder as
  `C:/temp/data/v3/build/sNN.py` with `sys.path.insert(0, <build dir>)`.
- Python: `C:/Users/Gabriel Wurzer/.pyenv/pyenv-win/versions/3.12.9/python.exe`. Run the solution notebook
  with `build/run_notebooks.py <outdir> <notebook>` from inside `notebooks/` (set `PYTHONIOENCODING=utf-8`;
  set `PLOTLY_RENDERER=notebook_connected` if you export HTML). If the session has a `YOUR CHOICE` that is
  `None` by default, make a temporary probe copy with a value filled in for the test run; never leave probe
  files in `notebooks/`.
- `build/dump.py <executed notebook> <out.txt>` dumps cells with outputs for reading and review.
- Check every number in your text and answers against the executed output.
- Write scripts with the Write tool, not with long shell heredocs (they break on Windows).

## Review, once

When the session runs green: one adversarial review with Codex, read-only:
`codex exec --skip-git-repo-check -s read-only - < prompt.txt` (run from `C:/temp/data`). Ask it to check, for
this audience and this easy course, what the student knows at each point, every number, comprehensibility,
whether the gap is a literal translation, whether the homework consolidates and fits an hour; first line
"NOTHING BLOCKING" or "BLOCKING", at most 10 items. Fix what is right, then stop (one more round only if
it found real errors in facts or numbers).

## Deliverables

1. `notebooks/NN_name.ipynb` and `notebooks/NN_name_solution.ipynb` (built, not hand-edited).
2. `build/sNN.py` (the builder).
3. `sessions/session-NN-plan.md` in German: timetable for 120 minutes (Friday 09:00 to 11:00 style: about 75
   minutes of work, a 10-minute break, a 10-minute short test at minute 95 to 105, homework intro at the
   end) and the numbers that come up in class.
4. `sessions/privat/session-NN-extras.md`: the short test (3 questions, English) with the answer key
   (German, what earns the point), and German grading notes for the homework with the reference run's numbers.
5. `webapps/flashcards/cards_sNN.json`: one card per term of the terms table, format
   `{"id","session","image","question","answers":[4 strings],"correct":[indices, usually two],"explanation"}`,
   image path `images/<id>.png` (images come later; the app shows a placeholder), plus one line per card in
   `webapps/flashcards/image_prompts_sNN.md` describing a photographic image without text.

Do not touch files of other sessions. Report at the end in under 200 words: what you built, the review
result, anything left open.

## Text of v1/data.pptx, condensed

Motivation: the building scientist as keeper of the digital twin (sensor, network, simulation, actuator,
real building and BIM). Sensors and actuators are connected to the net, but putting data in the cloud is not
a good idea: will these services exist in 40 years? So you manage it yourself. Work plan: infrastructure for
rapid development in isolation (Unix, the network, docker), sensor/actuator workflows with an ETL server
(javascript, JSON, node-red), deployment to self-contained platforms (raspberry). Then a long hands-on Unix
walk over ssh: ls -la, mkdir with the student number, cd, touch, cat, rm, cp, mv, permissions (d/rwx for
owner, group, others), rmdir, pwd, the root directory, a tour of /bin /etc /home /usr /var, the web server's
htdocs, editing index.html with nano and seeing it at http://IP:8000, URLs (IPv4/IPv6, DNS lookups with
nslookup, ports 21/22/25/80/443, protocols http/smtp/ftp/ssh), HTTP GET and POST, telnet to port 80 and a
raw GET. chmod, which, PATH, writing and executing a small script, symbolic links, pipes and redirects.
Virtualisation: server, VMs, docker containers, why that helps you (no reinstall pain), docker hub,
`docker run -p 1880:1880 nodered/node-red`. Node-red: flows of nodes, the msg object (payload, topic), JSON
values (boolean, number, string, null, list, object), inject, function (`msg.payload = Math.round(Math.random()*100)`),
debug, change, range, switch, exec, template, HTTP in/out with URL parameters, HTTP request to fetch a website
(OpenSensorWeb). Finally the occupancy sensor flows (set-occupancy writes a number to a file, get-occupancy reads it).
