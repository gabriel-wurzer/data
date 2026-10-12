"""Session 4: databases, keeping data in order."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from nbbau import Notebook, DATA_BOX, homework_header, TERMS_FOOTER, box

nb = Notebook()

nb.md(r'''
# Session 4: Databases, keeping data in order

**259.021 Fundamentals of Utilizing Data Sources** · Session 4 of 5

So far you have pulled data out of files, the web and sensors. Each time you got one loose table.
A building has rooms, rooms have sensors, sensors send readings, and if all of that sits in loose
files it gets out of order within a week. Today you put it into a **database**: a few tables that
point at each other, and one short language, SQL, to ask them questions. Your own room moves in
early on, and at the end you will find it again among the warmest rooms of the building.
''')

nb.md(DATA_BOX.format(text='''Today's data is small and made up on purpose: five rooms of a university building, seven sensors
and the readings of one morning, 16 October 2026. Small enough that you can check every answer by
eye. The SQL you learn works the same on a table with a million rows.'''))

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 1: why not just a file?

Two people log the temperature of two rooms into one shared file. Here is what the file looks like
after one morning. Run the cell and count: how many rooms does the file think there are?
''')

nb.code(r'''
import io                                             # to read text as if it were a file
import sqlite3                                        # the database that comes with Python
from pathlib import Path                              # to handle the database file
import pandas as pd                                   # tables, as in the last session
import plotly.express as px                           # quick interactive plots
from IPython.display import HTML, display             # to show tables below a cell

shared_log = """time,room,kind,value
2026-10-16 09:00,Seminar room,temperature,21.0
2026-10-16 09:00,Lecture hall,temperature,20.5
2026-10-16 10:00,Seminar Room,temperature,21.5
2026-10-16 10:00,lecture hall,temperature,22.0
2026-10-16 10:00,Seminar rm,temperature,21.5
2026-10-16 11:00,Lecture Hall ,temperature,22.5"""

log = pd.read_csv(io.StringIO(shared_log))            # read the text as a table
print(log.to_string(index=False))                     # show it
print()
print("different room names in the file:", log["room"].nunique())   # count the spellings
for name in log["room"].unique():                     # list them, in quotes so spaces show
    print(f"  '{name}'")
''')

nb.md(r'''
<details>
<summary>Answer</summary>

Six, for two real rooms: capitals, an abbreviation, a space at the end. Nobody did anything wrong
on purpose, and still the file cannot tell you the average temperature of the seminar room.

</details>

Now imagine the seminar room is renamed to "Room 1.04". You would have to edit every line that
mentions it, in every file, on every laptop.

Databases were invented for exactly this. In the 1960s data lived in files, each program with its
own format. In 1970 Edgar F. Codd proposed keeping data in **tables** that refer to each other by
number, and asking them questions in one common language, which became **SQL** (Structured Query
Language). PostgreSQL, MySQL and SQLite all work this way. Since the 2000s there are other kinds
too, for example document databases that store JSON like the sensor data of last session, but
tables and SQL are still where everybody starts.

How would you store the room names so that a rename touches only one place?

<details>
<summary>Answer</summary>

Write each room name once, in a list of rooms, and give each room a number. Every reading then
says "room 2" instead of typing the name. Renaming means changing one line in the list of rooms;
all readings still point at number 2. That is the whole idea of today.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 2: a table, and its key

Here is the list of rooms as a table:

| id | name | floor | area_m2 |
|---|---|---|---|
| 1 | Lecture hall | 0 | 180.0 |
| 2 | Seminar room | 1 | 48.0 |
| 3 | Library | 1 | 120.0 |

Each **row** is one room. Each **column** is one property, with one kind of value: `name` is
text, `floor` a whole number, `area_m2` a decimal number. The column `id` is the **key**: a number
that each room has exactly once, so "room 2" always means the seminar room, whatever it is called.

The database we use is **SQLite**. It comes with Python and keeps a whole database in a single
file, here `building.db`. Run the next two cells: the first opens the file, the second creates the
empty table.
''')

nb.code(r'''
if "conn" in globals():                               # if this cell ran before:
    conn.close()                                      # close the old connection first
Path("building.db").unlink(missing_ok=True)           # delete an old file, so every run starts fresh
conn = sqlite3.connect("building.db")                 # open (and create) the database file
conn.execute("PRAGMA foreign_keys = ON")              # make SQLite check links between tables (step 3)


def show(sql, db=None):
    """Run a SELECT and show the result as a small table."""
    result = pd.read_sql(sql, db or conn)             # ask the database, get a pandas table back
    display(HTML(result.to_html(index=False)))        # show it without pandas' row numbers
    print(f"({len(result)} row{'' if len(result) == 1 else 's'})")   # and how many rows came back


print(f"✓ database open: {Path('building.db').resolve()}")   # where the file is
''')

nb.md(r'''
A small helper, `show(...)`, is now defined: you hand it a question in SQL and it shows the answer
as a table. SQL reads almost like English. Inside SQL, `--` starts a comment, like `#` in Python.
''')

nb.code(r'''
conn.execute("""
CREATE TABLE rooms (
    id      INTEGER PRIMARY KEY,   -- the key: one number per room, never twice
    name    TEXT,                  -- text
    floor   INTEGER,               -- a whole number
    area_m2 REAL                   -- a decimal number, square metres
)
""")                                                  # create the table, still empty
show("SELECT * FROM rooms")                           # look at it: columns, no rows yet
''')

nb.md(r'''
`SELECT * FROM rooms` means "give me all columns (`*`) of the table `rooms`". You will type it a
lot today.
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 3: putting rows in

`INSERT INTO rooms VALUES (...)` adds one row, with the values in the order of the columns. The
cell below adds five rooms. `conn.commit()` then saves them into the file; until then they are only
pencilled in.

**Before:** the empty table you just saw.
''')

nb.code(r'''
conn.execute("INSERT INTO rooms VALUES (1, 'Lecture hall', 0, 180.0)")   # one row per room
conn.execute("INSERT INTO rooms VALUES (2, 'Seminar room', 1, 48.0)")
conn.execute("INSERT INTO rooms VALUES (3, 'Library',      1, 120.0)")
conn.execute("INSERT INTO rooms VALUES (4, 'Studio',       2, 95.0)")
conn.execute("INSERT INTO rooms VALUES (5, 'Server room',  2, 12.0)")
conn.commit()                                         # save into the file
show("SELECT * FROM rooms")                           # after: five rows
''')

nb.md(r'''
Now the sensors and their readings, each in their own table. A sensor does not repeat the room's
name; it only says `room_id`, the key of its room. For example:

| id | room_id | kind |
|---|---|---|
| 3 | 2 | temperature |

This is sensor 3, a temperature sensor, and its `room_id` 2 says it hangs in room 2, the seminar
room. Such a column, pointing at the key of another table, is called a **foreign key**. A reading
in turn only says which sensor it came from.

    rooms  ←  sensors  ←  readings
     id       room_id     sensor_id

Run the cell; it creates both tables and fills them.
''')

nb.code(r'''
conn.execute("""
CREATE TABLE sensors (
    id      INTEGER PRIMARY KEY,               -- the key of the sensor
    room_id INTEGER REFERENCES rooms(id),      -- foreign key: which room it hangs in
    kind    TEXT                               -- 'temperature' or 'co2'
)
""")                                                  # the sensor table
conn.execute("""
CREATE TABLE readings (
    sensor_id INTEGER REFERENCES sensors(id),  -- foreign key: which sensor measured
    time      TEXT,                            -- when, as text: year-month-day hour:minute
    value     REAL                             -- °C for temperature, ppm for CO2
)
""")                                                  # the reading table

sensors = [(1, 1, "temperature"), (2, 1, "co2"),      # lecture hall: two sensors
           (3, 2, "temperature"),                     # seminar room
           (4, 3, "temperature"),                     # library
           (5, 4, "temperature"), (6, 4, "co2"),      # studio: two sensors
           (7, 5, "temperature")]                     # server room
conn.executemany("INSERT INTO sensors VALUES (?, ?, ?)", sensors)   # insert all of them at once

readings = [(1, "2026-10-16 09:00", 20.5), (1, "2026-10-16 10:00", 22.0),
            (2, "2026-10-16 09:00", 650),  (2, "2026-10-16 10:00", 1150),
            (3, "2026-10-16 09:00", 21.0), (3, "2026-10-16 10:00", 21.5),
            (3, "2026-10-16 10:30", -40.0),           # a glitch: the sensor lost power for a moment
            (4, "2026-10-16 09:00", 19.5), (4, "2026-10-16 10:00", 20.0),
            (5, "2026-10-16 09:00", 22.5), (5, "2026-10-16 10:00", 23.5),
            (6, "2026-10-16 09:00", 800),  (6, "2026-10-16 10:00", 900),
            (7, "2026-10-16 09:00", 27.0), (7, "2026-10-16 10:00", 27.5)]
conn.executemany("INSERT INTO readings VALUES (?, ?, ?)", readings)  # insert all of them at once
conn.commit()                                         # save into the file
print(f"✓ {len(sensors)} sensors and {len(readings)} readings saved.")
''')

nb.md(r'''
The `?` are placeholders: Python fills them in from the list, row by row. Look at both tables.
''')

nb.code(r'''
show("SELECT * FROM sensors")                         # seven sensors, each with the key of its room
''')

nb.code(r'''
show("SELECT * FROM readings")                        # fifteen readings, each with the key of its sensor
''')

nb.md(r'''
The database now also guards the links. Run the cell: it tries to hang a sensor into room 99,
which does not exist.
''')

nb.code(r'''
try:                                                  # try something that should fail
    conn.execute("INSERT INTO sensors VALUES (8, 99, 'temperature')")   # room 99 does not exist
except sqlite3.IntegrityError as error:               # the database says no
    print(f"✓ refused, as it should be: {error}")     # show its reason
''')

nb.md(r'''
In which room is sensor 6, and what did it measure at 10:00? Use the tables above.

<details>
<summary>Answer</summary>

Sensor 6 has `room_id` 4, and room 4 is the studio. It is a CO2 sensor, and its reading at 10:00
is 900 ppm. You had to look in three tables and match the numbers by eye; in step 7 the database does
that for you.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 4: your room moves in

Add a room of your own: your room at home, your favourite café corner, the studio desk you work
at. Change the four values under `# YOUR CHOICE`, then run the cell. The temperature is your guess
for 10:00 this morning. The cell adds your room as room 6, gives it a temperature sensor (number 8)
and stores your reading.
''')

nb.code(r'''
# YOUR CHOICE: your own room
my_room_name = "my room"                              # what you call it
my_floor = 1                                          # which floor it is on (0 = ground floor)
my_area = 14.0                                        # its area in m², a guess is fine
my_temperature = 21.0                                 # its temperature at 10:00 in °C, a guess is fine

assert isinstance(my_room_name, str) and my_room_name.strip(), "my_room_name must be some text in quotes"
assert isinstance(my_floor, int), "my_floor must be a whole number, like 1"
assert 1 <= my_area <= 1000, "my_area should be in square metres, between 1 and 1000"
assert 5 <= my_temperature <= 40, "my_temperature should be in °C, between 5 and 40"
if my_room_name == "my room":                         # the example is still there
    print("Tip: give your room a name of your own, then run this cell again.")

try:                                                  # add the room, its sensor and the reading
    conn.execute("INSERT INTO rooms VALUES (6, ?, ?, ?)", (my_room_name, my_floor, my_area))
    conn.execute("INSERT INTO sensors VALUES (8, 6, 'temperature')")              # sensor 8 in room 6
    conn.execute("INSERT INTO readings VALUES (8, '2026-10-16 10:00', ?)", (my_temperature,))
    conn.commit()                                     # save into the file
    print(f"✓ '{my_room_name}' is room 6 now.")
except sqlite3.IntegrityError:                        # room 6 exists already
    conn.rollback()                                   # undo the half-done insert
    print("Room 6 is already in the database; the key allows it only once. "
          "To change your room, choose Run, Run All Cells.")
show("SELECT * FROM rooms")                           # after: six rows, the last one is yours
''')

nb.md(r'''
What would happen if you ran the cell a second time, and why?

<details>
<summary>Answer</summary>

Nothing would be added. Room 6 exists, and `id` is the key, so the database refuses a second row
with the same number. The cell catches that and tells you. A plain text file has no key, so it
would take the same line twice without complaint.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 5: asking questions, with WHERE and ORDER BY

`WHERE` keeps only the rows for which a condition is true. Rooms bigger than 50 m²:
''')

nb.code(r'''
show("SELECT * FROM rooms WHERE area_m2 > 50")        # only rows with more than 50 m²
''')

nb.md(r'''
Instead of `*` you can list the columns you want. `ORDER BY` sorts, and `DESC` (descending) puts
the biggest first:
''')

nb.code(r'''
show("SELECT name, area_m2 FROM rooms ORDER BY area_m2 DESC")   # two columns, biggest room first
''')

nb.md(r'''
Text goes in single quotes inside SQL. All CO2 sensors:
''')

nb.code(r'''
show("SELECT * FROM sensors WHERE kind = 'co2'")      # only the CO2 sensors
''')

nb.md(r'''
Where does your room land in the sorted list of areas? And which query would list only the rooms
on the ground floor?

<details>
<summary>Answer</summary>

That depends on your area: with 14 m² it lands second to last, between the seminar room (48) and
the server room (12). The ground floor is floor 0, so
`SELECT * FROM rooms WHERE floor = 0`; that gives the lecture hall, plus your room if you put it on
floor 0.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 6: your part, one query

In Python, a query is just text in quotes. Here are the names of all rooms on the first floor:

    floor_1_query = "SELECT name FROM rooms WHERE floor = 1"

Run it:
''')

nb.code(r'''
floor_1_query = "SELECT name FROM rooms WHERE floor = 1"   # the question, as text
show(floor_1_query)                                   # ask it
''')

nb.md(r'''
Now you: the names of all rooms on the **second** floor. One line is yours.
''')

nb.code(r'''
# YOUR TURN: replace None with the text in quotes
#   "SELECT name FROM rooms WHERE floor = 2"
floor_2_query = None

if floor_2_query is None:                             # nothing written yet
    print("Not yet: replace None with the query described in the comment, then run the cell again.")
else:                                                 # run the query
    show(floor_2_query)                               # the answer, as a table
    print("✓ the rooms on the second floor.")
''', solution=r'''
# YOUR TURN: replace None with the text in quotes
#   "SELECT name FROM rooms WHERE floor = 2"
floor_2_query = "SELECT name FROM rooms WHERE floor = 2"

if floor_2_query is None:                             # nothing written yet
    print("Not yet: replace None with the query described in the comment, then run the cell again.")
else:                                                 # run the query
    show(floor_2_query)                               # the answer, as a table
    print("✓ the rooms on the second floor.")
''')

nb.md(r'''
<details>
<summary>Answer</summary>

    floor_2_query = "SELECT name FROM rooms WHERE floor = 2"

The studio and the server room, and your room too if you put it on floor 2.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 7: JOIN, putting the tables back together

In step 3 you matched sensor 6 to the studio by eye. `JOIN` does that matching: it glues each row
of one table to the row of another table whose key fits. Here every sensor gets the name of its
room, because `sensors.room_id` equals `rooms.id`. With two tables in play, a column is written
`table.column`.
''')

nb.code(r'''
show("""
SELECT sensors.id, sensors.kind, rooms.name
FROM sensors
JOIN rooms ON sensors.room_id = rooms.id
""")                                                  # each sensor with the name of its room
''')

nb.md(r'''
Now the question we wanted from the start: **the temperature of every room at 10:00, by room
name.** That needs all three tables: readings to sensors, sensors to rooms. The `WHERE` keeps only
rows where both conditions hold, joined by `AND`: a temperature sensor, and a reading from 10:00; `ORDER BY` puts the warmest room first. Look for your
room.
''')

nb.code(r'''
temperature_query = """
SELECT rooms.id, rooms.name, readings.value AS temperature
FROM readings
JOIN sensors ON readings.sensor_id = sensors.id
JOIN rooms   ON sensors.room_id = rooms.id
WHERE sensors.kind = 'temperature' AND readings.time = '2026-10-16 10:00'
ORDER BY readings.value DESC
"""
show(temperature_query)                               # one row per room, warmest first
''')

nb.code(r'''
# the same answer as a bar chart, your room in orange
temps = pd.read_sql(temperature_query, conn)          # the result as a pandas table
temps["whose"] = ["yours" if i == 6 else "building" for i in temps["id"]]   # mark your room, number 6
fig = px.bar(temps, x="name", y="temperature", color="whose", text="temperature",          # one bar per room
             color_discrete_map={"building": "#4c78a8", "yours": "#f58518"})
fig.update_layout(height=380, showlegend=False, xaxis_title="", yaxis_title="temperature at 10:00 [°C]")
fig.show()                                            # draw it
''', hidden=True)

nb.md(r'''
The word `AS` renames a column in the answer: `readings.value AS temperature`. Where is your room,
and why does the lecture hall appear only once although it has two sensors?

<details>
<summary>Answer</summary>

With the example 21.0 °C, your room comes fifth of six, just below the seminar room (21.5) and
above the library (20.0); the server room is the warmest at 27.5. The lecture hall's second
sensor measures CO2, and the `WHERE` keeps only temperature sensors.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 8: changing and removing rows, UPDATE and DELETE

The library gets renamed to "Reading room". `UPDATE ... SET ... WHERE ...` changes the rows that
match the condition. **Before:**
''')

nb.code(r'''
show("SELECT * FROM rooms WHERE id = 3")              # before: the library
''')

nb.code(r'''
conn.execute("UPDATE rooms SET name = 'Reading room' WHERE id = 3")   # change the name of room 3
conn.commit()                                         # save
show("SELECT * FROM rooms WHERE id = 3")              # after: same row, new name
''')

nb.md(r'''
One row changed. Now run the temperature question from step 7 again, without touching it:
''')

nb.code(r'''
show(temperature_query)                               # the same query as in step 7
''')

nb.md(r'''
The new name is there, because the readings never contained the name, only the key. That is the
rename from step 1, done in one line.

Next, the glitch: sensor 3 reported −40 °C at 10:30. `DELETE FROM ... WHERE ...` removes the rows
that match. Always write the `WHERE`: without it, `DELETE` empties the whole table. **Before:**
''')

nb.code(r'''
show("SELECT * FROM readings WHERE sensor_id = 3")    # before: three readings, one of them -40
''')

nb.code(r'''
conn.execute("DELETE FROM readings WHERE value < -30")   # remove impossible readings
conn.commit()                                         # save
show("SELECT * FROM readings WHERE sensor_id = 3")    # after: two readings left
''')

nb.md(r'''
Why is `WHERE value < -30` a better condition here than `WHERE sensor_id = 3`?

<details>
<summary>Answer</summary>

`WHERE sensor_id = 3` would delete all readings of sensor 3, including the two good ones. The
condition should describe exactly the rows you want gone, here the impossible temperature.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 9: the same with pandas, and back

pandas can read the answer of any query into a table (`pd.read_sql`), and you can carry on there
with what you already know. Filtering in pandas does what `WHERE` does in SQL.
''')

nb.code(r'''
rooms_df = pd.read_sql("SELECT * FROM rooms", conn)   # the whole rooms table, as a pandas table
big_df = rooms_df[rooms_df["area_m2"] > 50]           # keep rooms over 50 m², like WHERE area_m2 > 50
display(HTML(big_df.to_html(index=False)))            # show it
print(f"✓ {len(big_df)} rooms over 50 m², the same as with SQL in step 5.")
''')

nb.md(r'''
And back into the database: `to_sql` writes a pandas table as a new database table.
`if_exists="replace"` overwrites it if it is there already, so the cell can run twice.
''')

nb.code(r'''
big_df.to_sql("big_rooms", conn, if_exists="replace", index=False)   # write it as table big_rooms
conn.commit()                                         # save
show("SELECT * FROM big_rooms")                       # read it back with SQL
show("SELECT name FROM sqlite_master WHERE type = 'table'")   # all tables now in the file
''')

nb.md(r'''
Last, the point of a file. Close the database, as if you shut down the notebook, and open it again.
''')

nb.code(r'''
conn.close()                                          # close the database
conn = sqlite3.connect("building.db")                 # open the file again
conn.execute("PRAGMA foreign_keys = ON")              # and switch the link check on again
show("SELECT * FROM rooms WHERE id = 6")              # your room is still there
''')

nb.md(r'''
<details>
<summary>Where is your room now, really?</summary>

In the file `building.db` next to this notebook, in the file browser on the left. Any program
that speaks SQL can open it: another notebook, a colleague's script, a viewer like "DB Browser for
SQLite".

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Tests

Run this cell before you submit. It recounts the tables, checks your query against a pandas
filter, and finds your room through the JOIN.
''')

nb.code(r'''
count = lambda table: conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]   # rows in a table
# recount: 5 rooms + yours, 7 sensors + yours, 15 readings + yours - the glitch
assert count("rooms") == 6 and count("sensors") == 8, "expected 6 rooms and 8 sensors; choose Run All Cells"
assert count("readings") == 15, "expected 15 readings: 15 + yours - the glitch; choose Run All Cells"
assert conn.execute("SELECT name FROM rooms WHERE id = 3").fetchone()[0] == "Reading room", "rename missing"   # step 8
assert conn.execute("SELECT COUNT(*) FROM readings WHERE value < -30").fetchone()[0] == 0, "glitch still there"   # step 8

assert floor_2_query is not None, "fill in the YOUR TURN query in step 6"   # the gap is filled
by_sql = set(pd.read_sql(floor_2_query, conn)["name"])                   # your query
rooms_df = pd.read_sql("SELECT * FROM rooms", conn)                     # the table again
by_pandas = set(rooms_df[rooms_df["floor"] == 2]["name"])               # the same question, in pandas
assert by_sql == by_pandas, f"your query gives {by_sql}, the second floor has {by_pandas}"

temps = pd.read_sql(temperature_query, conn)                             # the JOIN from step 7
mine = temps[temps["id"] == 6]                                          # your room in it
assert len(mine) == 1 and mine["temperature"].iloc[0] == my_temperature, "your room is not in the JOIN"
assert temps["temperature"].is_monotonic_decreasing, "the JOIN should be sorted warmest first"   # ORDER BY ... DESC
print(f"✓ All green. Six rooms, your query finds {sorted(by_sql)}, "
      f"and '{my_room_name}' is in the JOIN at {my_temperature} °C.")
''')

nb.md(r'''
## Where you stand now

You know why a pile of files gets out of order and what a database does about it. You can create a
table, put rows in, ask it questions with `WHERE` and `ORDER BY`, join three tables by their keys,
change and delete rows, and move a table between SQL and pandas. Your room is in a database file and
stays there.

Next session: putting sources together, files, web, sensors and databases, into one picture.

---

### Terms to learn

''' + TERMS_FOOTER + r'''

| term | in one sentence |
|---|---|
| database | an organised set of tables in one place, which programs can query, change and share |
| table, row, column | a table holds one kind of thing; each row is one of them, each column one property |
| key (primary, foreign) | a number each row has once; a foreign key in another table points at it |
| SQL query | a question to the database, like `SELECT name FROM rooms WHERE floor = 2` |
| JOIN | glues rows of two tables together where a foreign key matches a key |
''')

# ---------------------------------------------------------------------------------------------
nb.md(homework_header(
    "a small database of your own life",
    """In class you built a building database: rooms, sensors and readings linked by keys. Now build one
about something from your own life, with two tables and one join. The first table lists who or what
(people, team members, plants, bikes), each with one number. The second lists things that happen, each
belonging to one entry of the first table, also with a number.

Ideas: a flatshare with people and their chores; a sports club with members and training sessions; your
plants and when you watered them; your friends and the money you lent each other. Five to ten lines in
the first table and ten to twenty in the second are plenty.""",
    """The cells come with a complete worked example: an invented flatshare of four people and their
chores for one week, typed the way people really type, with example answers under the questions. Run it
once first, then replace it with your own data."""))

nb.code(r'''
# YOUR CHOICE: what your two tables are called, in lower case, no spaces (use _ instead)
first_table = "people"                                # who or what, one row each
first_number = "room_m2"                              # the one number each of them has
second_table = "chores"                               # what happens; each line belongs to one of the first table
second_number = "minutes"                             # the one number each line has

# YOUR CHOICE: the first table, one line each: name; number. Decimal commas work.
# Anything after a # is a note for you. The example is invented.
first_lines = """
Lena; 18
tobi; 11,5        # smallest room, pays least
Mira ; 14
Jonas; 16         # moved in in September
"""

# YOUR CHOICE: the second table, one line each: what; name from the first table; number
second_lines = """
dishes; Lena; 20
dishes; Tobi; 20
bins; mira; 5
bathroom;Jonas; 45
hoovering; Lena; 30

shopping; Tobi; 40    # the big shop, Saturday
bathroom; Mira; 45
plants; lena; 15
"""

# YOUR CHOICE: the name of one entry of the first table you care about, for example yourself
my_name = "Tobi"
''')

nb.code(r'''
# reads your two text blocks into two database tables; you do not need to change anything here
import re                                             # to check the table names


def parse(text, parts):
    """Split a text block into lines of `parts` fields, dropping notes and empty lines."""
    rows = []                                         # the cleaned lines
    for line in text.strip().splitlines():            # go through the text line by line
        line = line.split("#")[0].strip()             # drop the note after a #
        if not line:                                  # an empty line:
            continue                                  # skip it
        fields = [f.strip() for f in line.split(";")] # split at the semicolons, trim spaces
        assert len(fields) == parts, f"this line needs exactly {parts - 1} semicolon(s): {line!r}"
        rows.append(fields)                           # keep it
    return rows


def number(text, line):
    """Turn '11,5' or '11.5' into 11.5, with a helpful message if it is not a number."""
    try:
        return float(text.replace(",", "."))          # decimal comma or point
    except ValueError:
        raise ValueError(f"'{text}' is not a number, in this line: {line}") from None


for word in (first_table, first_number, second_table, second_number):   # names must work in SQL
    assert re.fullmatch(r"[a-z][a-z0-9_]*", word), f"'{word}': use lower-case letters, digits and _ only"
assert first_table != second_table, "the two tables need different names"
sql_words = {"group", "order", "select", "from", "where", "join", "table", "index", "values", "key", "by"}
for word in (first_table, second_table, first_number, second_number):   # words SQL keeps for itself
    assert word not in sql_words, f"'{word}' is a word of SQL itself; pick another name, e.g. '{word}s'"
for word in (first_number, second_number):            # columns the tables have already
    assert word not in {"id", "name", "what", f"{first_table}_id"}, f"'{word}' is taken; pick another name"
first_rows, second_rows = parse(first_lines, 2), parse(second_lines, 3)   # read both text blocks
assert first_rows and second_rows, "both text blocks need at least one line"
my_name = my_name.strip()                             # drop spaces around my_name

if "home" in globals():                               # if this cell ran before:
    home.close()                                      # close the old connection first
Path("my_life.db").unlink(missing_ok=True)            # start fresh on every run
home = sqlite3.connect("my_life.db")                  # your own database file
home.execute("PRAGMA foreign_keys = ON")              # check the links, as in class
link = f"{first_table}_id"                            # the foreign key column, e.g. people_id
home.execute(f"CREATE TABLE {first_table} (id INTEGER PRIMARY KEY, name TEXT, {first_number} REAL)")
home.execute(f"CREATE TABLE {second_table} (id INTEGER PRIMARY KEY, what TEXT, "
             f"{link} INTEGER REFERENCES {first_table}(id), {second_number} REAL)")

key_of = {}                                           # lower-case name -> key, to match "lena" with "Lena"
for i, (name, value) in enumerate(first_rows, start=1):   # numbers the rows 1, 2, 3, ...
    assert name.lower() not in key_of, f"'{name}' appears twice in the first table"
    key_of[name.lower()] = i                          # remember its key
    home.execute(f"INSERT INTO {first_table} VALUES (?, ?, ?)", (i, name, number(value, name)))

for i, (what, name, value) in enumerate(second_rows, start=1):
    assert name.lower() in key_of, f"'{name}' is not in your first table; check the spelling or add it there"
    home.execute(f"INSERT INTO {second_table} VALUES (?, ?, ?, ?)",
                 (i, what, key_of[name.lower()], number(value, what)))   # the name becomes a key here
home.commit()                                         # save into the file
assert my_name.lower() in key_of, f"my_name '{my_name}' is not in your first table"
print(f"✓ {len(first_rows)} rows in {first_table}, {len(second_rows)} rows in {second_table}, saved in my_life.db.")
''', hidden=True)

nb.code(r'''
show(f"SELECT * FROM {first_table}", home)            # your first table
show(f"SELECT * FROM {second_table}", home)           # your second table: names have become keys
''')

nb.code(r'''
join_query = f"""
SELECT {second_table}.what, {first_table}.name, {second_table}.{second_number}
FROM {second_table}
JOIN {first_table} ON {second_table}.{link} = {first_table}.id
ORDER BY {first_table}.name
"""                                                   # the JOIN, with your table names filled in
print(join_query)                                     # see the SQL that runs
show(join_query, home)                                # every line of the second table, with a name
''')

nb.code(r'''
mine_query = f"""
SELECT {second_table}.what, {second_table}.{second_number}
FROM {second_table}
JOIN {first_table} ON {second_table}.{link} = {first_table}.id
WHERE {first_table}.name = ?
"""                                                   # the same JOIN, only the lines of my_name
my_real_name = home.execute(f"SELECT name FROM {first_table} WHERE id = ?",
                            (key_of[my_name.lower()],)).fetchone()[0]   # the name as written in table 1
mine = pd.read_sql(mine_query, home, params=(my_real_name,))            # ask the database
display(HTML(mine.to_html(index=False)))             # show it
print(f"✓ {my_real_name}: {len(mine)} lines, {mine[second_number].sum():g} {second_number} in total.")
''')

nb.code(r'''
# the totals per name as a bar chart, my_name in orange
joined = pd.read_sql(join_query, home)                # the JOIN as a pandas table
totals = joined.groupby("name", as_index=False)[second_number].sum()   # add up per name
totals["whose"] = ["yours" if n == my_real_name else "others" for n in totals["name"]]   # mark my_name
fig = px.bar(totals, x="name", y=second_number, color="whose", text=second_number,       # one bar per name
             color_discrete_map={"others": "#4c78a8", "yours": "#f58518"})
fig.update_layout(height=380, showlegend=False, xaxis_title="",
                  title=f"{second_number} per entry of {first_table}, from the JOIN")
fig.show()                                            # draw it
''', hidden=True)

nb.md(r'''
### Your answers

One to three sentences per question, about your own database.

1. **What is a row?** In each of your two tables, what does one row stand for? Give one real row as an
   example.
2. **Why a key?** Your second table stores a number instead of a name. What does that number protect you
   from? Think of how you typed the names.
3. **What does the join answer?** Name one question your JOIN or the bar chart answers that neither table
   answers alone, and give the answer for `my_name`.
4. **What would break without the database?** Imagine you kept all of this in one text file or chat
   message for a year. What would go wrong first?

<details>
<summary>Example answers for the flatshare. Click to see what a good answer looks like.</summary>

1. In `people` a row is one flatmate, for example "tobi" with his 11.5 m² room, spelled the way I first typed him. In `chores` a row is one
   chore done once, for example "shopping, Tobi, 40 minutes".
2. I typed Lena as "Lena" and "lena". The reading cell matched the two spellings once, when it
   turned names into keys; from then on every chore of hers just says 1, and 1 is always the same
   Lena. If she wanted to be called "Helena", one `UPDATE` on her row would do, and all her chores
   would follow.
3. The chores table has only numbers for people, and the people table has no chores. Only joined do
   I see who does how much: Tobi 60 minutes, Lena 65, Mira 50, Jonas 45. Tobi has the smallest
   room and does almost the most.
4. After a few weeks there would be five spellings of every name and nobody could add up a month.
   And if Jonas changed his name, I would have to find and fix every line he appears in, instead of one row.

These fit the example only. Your answers are about your own database.

</details>

*Your text here.*
''')

nb.write("04_databases")
