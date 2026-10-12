"""Session 1: files, where data lives."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from nbbau import Notebook, DATA_BOX, homework_header, TERMS_FOOTER, box

nb = Notebook()

nb.md(r'''
# Session 1: Files, where data lives

**259.021 Fundamentals of Utilizing Data Sources** · Session 1 of 5

Sensors, websites, databases, the city's open data: sooner or later every data source ends up as a
**file** in a **folder** somewhere. Today you find out where your files live, write a small file about
your own room, read it back, and design a file format with a version number. At the end you download
a teddy bear and turn it in 3D. It is a text file too.
''')

nb.md(DATA_BOX.format(text='''Today's data is yours: four facts about the room you are sitting in at home. At the end comes
`teddy.obj`, a 3D model from an MIT computer graphics course (6.837, 2003), downloaded from the web. If
the download fails, a copy in `../data/teddy.obj` steps in.'''))

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 1: your room, in four values

Think of your own room at home, or the room you like best in your flat. Change the four values below
to yours and run the two cells; the second checks your values. The example is a 14.5 m² room with two windows, used by one person.
''')

nb.code(r'''
from pathlib import Path                  # file and folder paths
import pandas as pd                       # tables
import plotly.express as px               # quick interactive plots
import plotly.graph_objects as go         # plots built piece by piece

# YOUR CHOICE: your own room
room_name = "my room"                     # a name, in quotes
area_m2 = 14.5                            # floor area in m², a number without quotes, with a decimal point
windows = 2                               # how many windows
people = 1                                # how many people use the room
''')

nb.code(r'''
# checks your four values and stops with a hint if something is off
problems = []                             # collect what is wrong, if anything
if not isinstance(room_name, str) or not room_name.strip():          # the name must be text
    problems.append('room_name needs some text in quotes, like "kitchen"')
elif any(c in room_name for c in '=,"\n'):                           # these signs would confuse our files
    problems.append("room_name must not contain =, a comma or a quote sign")
if not isinstance(area_m2, (int, float)) or area_m2 <= 0:            # area: a positive number
    problems.append("area_m2 must be a number above 0, without quotes, with a point: 14.5, not 14,5")
if not isinstance(windows, int) or windows < 0:                      # windows: a whole number
    problems.append("windows must be a whole number, like 2")
if not isinstance(people, int) or people < 1:                        # people: at least one
    problems.append("people must be a whole number of at least 1")
if problems:                                                         # stop and tell what to fix
    raise ValueError("Please fix in the cell above, then run both cells again:\n- " + "\n- ".join(problems))
print(f"✓ {room_name}: {area_m2} m², windows: {windows}, people: {people}, "
      f"{area_m2 / people:.1f} m² per person.")
''', hidden=True)

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 2: where am I?

Every file sits in a folder, folders sit in folders, and the **path** is the address through them. An
example: `/home/jovyan/data/notebooks/01_files.ipynb` is the file `01_files.ipynb` in the folder
`notebooks`, which is in `data`, which is in `jovyan`, which is in `home`. The single `/` at the very
start is the top of it all. On Windows the same reads `C:\Users\...`, with backslashes.

The folder you are in right now is the **working directory**. Two dots, `..`, mean "one folder up".
A cell line that starts with `!` is sent to the terminal instead of Python. Run the cell.
''')

nb.code(r'''
!pwd
!ls
!ls ../data
''')

nb.md(r'''
`pwd` printed the working directory, `ls` what is in it, `ls ../data` what is in the folder `data` one
level up. Which path leads from this notebook to the file `teddy.obj`?

<details>
<summary>Answer</summary>

`../data/teddy.obj`: one folder up, into `data`, the file `teddy.obj`. A path like this, which starts
from where you are, is called a relative path. It still works if the whole course folder moves
somewhere else.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 3: the terminal

The terminal is a window where you type commands instead of clicking. Open one: **File, New, Terminal**.
It usually starts in your home folder, so first move to this notebook's folder. The next cell prints the
exact command; copy it into the terminal and press Enter.
''')

nb.code(r'''
print(f'cd "{Path.cwd()}"')               # "cd" means change directory; this is the folder of the notebook
''')

nb.md(r'''
Now type these, one per line, and press Enter after each. Look at what each one prints.

| you type | what it does |
|---|---|
| `pwd` | print the working directory: where am I? |
| `ls` | list what is in it |
| `mkdir -p my_files` | make a new folder called `my_files` (`-p`: no complaint if it is already there) |
| `cd my_files` | go into it |
| `pwd` | check: the path now ends in `/my_files` |
| `cd ..` | one folder up, back to `notebooks` |
| `ls` | `my_files` is now in the list |

Your new folder also appears in the file browser on the left. Run the next cell to check.
''')

nb.code(r'''
folder = Path("my_files")                 # the folder you made in the terminal
if folder.is_dir():                       # is it there?
    print("✓ my_files is there. Everything you write today goes into it.")
else:                                     # not there: make it, so the rest works
    folder.mkdir()
    print("my_files was not there, so I made it for you. Next time: mkdir -p my_files in the terminal, "
          "after the cd command above.")
''')

nb.md(r'''
Why did you need the `cd` command before `mkdir`?

<details>
<summary>Answer</summary>

`mkdir -p my_files` makes the folder inside the working directory. Without the `cd` it would have
landed in your home folder, not next to this notebook.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 4: write a file about your room

A **text file** is just characters, line after line. Each line of our file holds one fact, written as
`key=value`. For the example room the file reads:

    room=my room
    area_m2=14.5
    windows=2
    people=1

Run the cell. It writes your four values that way, then `cat` shows the file as it lies on disk.
''')

nb.code(r'''
room_text = (f"room={room_name}\n"             # one fact per line; \n means "new line"
             f"area_m2={area_m2}\n"
             f"windows={windows}\n"
             f"people={people}\n")
Path("my_files/my_room.txt").write_text(room_text, encoding="utf-8")    # utf-8: umlauts like ü work too
print("✓ written. This is the file:")      # what follows comes from the terminal
!cat my_files/my_room.txt
''')

nb.md(r'''
Open `my_files/my_room.txt` from the file browser on the left. Is there anything in it that says what
the file is about, or what unit the area is in?

<details>
<summary>Answer</summary>

Only what the keys say. `area_m2` hints at square metres because we put the unit into the name. There
is no line saying "this is a room". We fix that in step 6.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 5: your part, reading it back

Reading means taking each line apart at the `=` sign. Python's `split` does that. An example:

    name, number = "windows=2".split("=")

gives `name = "windows"` and `number = "2"`. In the cell below, one line is yours.
''')

nb.code(r'''
def split_line(line):
    # YOUR TURN: replace the line "raise ..." with one line:
    #   key, value become: line split at the "=" sign
    raise NotImplementedError("replace this line with the line described above")

    return key.strip(), value.strip()     # strip removes spaces around both


def read_room_plain(path):
    room = {}                             # an empty dictionary: key -> value
    for line in Path(path).read_text(encoding="utf-8").splitlines():   # the file, line by line
        key, value = split_line(line)     # your line at work
        room[key] = value                 # remember the pair
    return room


my_room = read_room_plain("my_files/my_room.txt")   # read your file back
print("✓ read back:", my_room)            # the whole dictionary
''', solution=r'''
def split_line(line):
    key, value = line.split("=")          # split the line at the "=" sign

    return key.strip(), value.strip()     # strip removes spaces around both


def read_room_plain(path):
    room = {}                             # an empty dictionary: key -> value
    for line in Path(path).read_text(encoding="utf-8").splitlines():   # the file, line by line
        key, value = split_line(line)     # your line at work
        room[key] = value                 # remember the pair
    return room


my_room = read_room_plain("my_files/my_room.txt")   # read your file back
print("✓ read back:", my_room)            # the whole dictionary
''')

nb.md(r'''
<details>
<summary>Answer</summary>

    key, value = line.split("=")

</details>

Look closely at the output: the numbers come back in quotes. The file only holds characters, so `'14.5'`
is text until you turn it into a number. `my_room["area_m2"]` looks up the value stored under the key
`area_m2`, and `float(...)` turns it into a number. Run the cell.
''')

nb.code(r'''
area = float(my_room["area_m2"])          # text -> decimal number
count = int(my_room["people"])            # text -> whole number
print(f"✓ {area / count:.1f} m² per person, computed from the file")   # now arithmetic works
''')

nb.md(r'''
What would `my_room["area_m2"] + 1` do?

<details>
<summary>Answer</summary>

It fails with a `TypeError`: Python will not add a number to text. Whoever reads a text file has to
know which values are numbers. The file itself does not say.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 6: a header and a version

In a year you will find this file and not remember what it is. So the first line says what kind of
file it is, the **header**, and the second line which **version** of the format it follows:

    ROOM FILE
    version 1
    room=my room
    area_m2=14.5
    ...

Run the cell: it writes that, then tries the reader from step 5 on it.
''')

nb.code(r'''
v1 = "ROOM FILE\nversion 1\n" + room_text    # header, version, then the same four lines
Path("my_files/my_room_v1.txt").write_text(v1, encoding="utf-8")    # save it
print("✓ written my_room_v1.txt")
try:                                      # try the old reader on the new file
    read_room_plain("my_files/my_room_v1.txt")
except ValueError as error:               # it breaks: say where
    print("The reader from step 5 fails:", error)
    print("It tried to split the line 'ROOM FILE' at an = sign, and there is none.")
''')

nb.md(r'''
Two extra lines, and the old reader breaks. Every change of a format can do that to old readers. So
from now on the version line is always there, and a reader looks at it first to know how to go on.

Now a **version 2** with one change: the four facts go on one line, separated by commas. That saves
lines when you have a whole flat of rooms.

    ROOM FILE
    version 2
    room=my room, area_m2=14.5, windows=2, people=1

Run the cell. It writes version 2 and defines one reader that understands both versions.
''')

nb.code(r'''
v2 = (f"ROOM FILE\nversion 2\n"           # same header, new version number
      f"room={room_name}, area_m2={area_m2}, windows={windows}, people={people}\n")   # all on one line
Path("my_files/my_room_v2.txt").write_text(v2, encoding="utf-8")    # save it


def read_room(path):
    lines = Path(path).read_text(encoding="utf-8").splitlines()     # the file, line by line
    if lines[0] != "ROOM FILE":                                     # first check the header
        raise ValueError(f"{path} is not a room file, it starts with {lines[0]!r}")
    if lines[1] == "version 1":                                     # version 1: one pair per line
        pairs = lines[2:]
    elif lines[1] == "version 2":                                   # version 2: pairs on one line
        pairs = lines[2].split(",")
    else:                                                           # a version we do not know
        raise ValueError(f"{path} has {lines[1]!r}, and this reader only knows versions 1 and 2")
    return dict(split_line(p) for p in pairs)                       # your split, on every pair


room_v1 = read_room("my_files/my_room_v1.txt")    # read version 1
room_v2 = read_room("my_files/my_room_v2.txt")    # read version 2
print("version 1:", room_v1)
print("version 2:", room_v2)
print("✓ same content" if room_v1 == room_v2 else "the two differ, check the files")
''')

nb.md(r'''
Somebody sends you a file that starts with `ROOM FILE` and `version 3`. What does `read_room` do, and
why is that better than guessing?

<details>
<summary>Answer</summary>

It stops with the message "this reader only knows versions 1 and 2". A clear stop is better than reading
the lines the old way and handing on wrong values that nobody notices.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 7: the same as a table, CSV

When there are many rooms, a table is handier. **CSV** (comma-separated values) is the most common
table file: the first line names the columns, every further line is one row, commas between the
values. Your room is the first row; the other three are an example flat, change them if you like.
''')

nb.code(r'''
csv_text = ("room,area_m2,windows\n"                 # first line: the column names
            f"{room_name},{area_m2},{windows}\n"     # your room
            "kitchen,9.5,1\n"                        # the rest of an example flat
            "bathroom,4.2,0\n"
            "hall,6.8,0\n")
Path("my_files/my_flat.csv").write_text(csv_text, encoding="utf-8")   # save it
!cat my_files/my_flat.csv
''')

nb.code(r'''
flat = pd.read_csv("my_files/my_flat.csv")           # pandas reads the whole table in one line
total = flat["area_m2"].sum()                        # add up the areas
print(f"✓ {len(flat)} rooms, {total:.1f} m² in total; yours is {area_m2 / total:.0%} of it.")
flat                                                 # show the table
''')

nb.code(r'''
# the rooms as bars
fig = px.bar(flat, x="room", y="area_m2", text="area_m2", height=350,
             labels={"area_m2": "area [m²]"}, title="the flat, read from my_flat.csv")
fig.show()
''', hidden=True)

nb.md(r'''
Our key=value reader gave back text, and you had to convert with `float`. Did you have to convert
anything for the sum here?

<details>
<summary>Answer</summary>

No. `pd.read_csv` looks at each column, and if every value in it looks like a number, it reads the
column as numbers. That is one reason CSV and pandas are the everyday pair for tables.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 8: a teddy bear from the web

3D models are files too. The **OBJ** format is plain text: a line starting with `v` is one point (a
vertex) with its x, y and z, and a line starting with `f` is one triangle (a face), naming three points
by their number. For example `v 1.0 2.0 0.5` is a point, and `f 1 2 3` connects the first three points.
Run the cell to download the teddy and look at a few of its lines.
''')

nb.code(r'''
import requests                                      # to fetch files from the web

url = "https://groups.csail.mit.edu/graphics/classes/6.837/F03/models/teddy.obj"   # where the teddy lives
try:
    response = requests.get(url, timeout=15)         # ask the server for the file, wait at most 15 s
    response.raise_for_status()                      # stop here if the server says no
    teddy_text = response.text                       # the file, as text
    print(f"✓ downloaded {len(teddy_text)} characters from the web")
except requests.RequestException:                    # no internet, or the server is down
    teddy_text = Path("../data/teddy.obj").read_text(encoding="utf-8")   # use the course copy
    print("The download did not work, so I am using the copy in ../data/teddy.obj. Same file.")
Path("my_files/teddy.obj").write_text(teddy_text, encoding="utf-8")      # keep your own copy

lines = teddy_text.splitlines()                      # the file, line by line
v_lines = [l for l in lines if l.startswith("v ")]   # the points
f_lines = [l for l in lines if l.startswith("f ")]   # the triangles
print(f"{len(lines)} lines: {len(v_lines)} start with v, {len(f_lines)} with f")
print("first two v lines:", v_lines[:2])
print("first two f lines:", f_lines[:2])
''')

nb.md(r'''
Reading the points is the same trick as in step 5, only the separator is a space instead of `=`.
Run the cell, then turn the teddy with the mouse.
''')

nb.code(r'''
xs, ys, zs = [], [], []                              # three lists for the coordinates
for line in v_lines:                                 # every point line
    _, x, y, z = line.split()                        # "v", then three numbers, split at spaces
    xs.append(float(x))                              # text -> number, as in step 5
    ys.append(float(y))
    zs.append(float(z))
print(f"✓ {len(xs)} points read")
''')

nb.code(r'''
# the points in 3D; OBJ has y pointing up, plotly has z up, so y and z swap places
fig = go.Figure(go.Scatter3d(x=xs, y=zs, z=ys, mode="markers", marker=dict(size=2, color="saddlebrown")))
fig.update_layout(height=550, margin=dict(l=0, r=0, b=0, t=30), title="the v lines of teddy.obj",
                  scene=dict(aspectmode="data", camera=dict(eye=dict(x=0.5, y=1.7, z=0.4))))
fig.show()
''', hidden=True)

nb.md(r'''
Only points so far. The `f` lines say which three points make a triangle. Run the cell to draw them.
''')

nb.code(r'''
# the triangles from the f lines; OBJ counts points from 1, Python from 0, hence the -1
faces = [[int(n) - 1 for n in l.split()[1:4]] for l in f_lines]
i, j, k = zip(*faces)                                # first, second and third corner of every triangle
fig = go.Figure(go.Mesh3d(x=xs, y=zs, z=ys, i=i, j=j, k=k, color="peru", flatshading=True,
                          lighting=dict(ambient=0.6, diffuse=0.8, specular=0.2)))
fig.update_layout(height=550, margin=dict(l=0, r=0, b=0, t=30), title="the v and f lines of teddy.obj",
                  scene=dict(aspectmode="data", camera=dict(eye=dict(x=0.5, y=1.7, z=0.4))))
fig.show()
''', hidden=True)

nb.md(r'''
Open `my_files/teddy.obj` from the file browser. Does a 3D program need anything other than these
text lines to draw the bear?

<details>
<summary>Answer</summary>

No. Everything is in the 1598 `v` lines and the 3192 `f` lines. A 3D model, a room file and a CSV table
are all text in an agreed format; the program only has to know the format.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Tests

Run this cell before you submit. It checks your `split_line`, reads your files again and compares them
with your four values, adds up the CSV by hand, and counts the teddy's points once more.
''')

nb.code(r'''
assert split_line("windows=2") == ("windows", "2"), "split_line('windows=2') should give ('windows', '2')"
assert split_line(" area_m2 = 14.5 ") == ("area_m2", "14.5"), "spaces around key and value should go"
expected = {"room": room_name.strip(), "area_m2": str(area_m2), "windows": str(windows), "people": str(people)}
assert read_room_plain("my_files/my_room.txt") == expected, "my_room.txt does not hold your four values"
assert read_room("my_files/my_room_v1.txt") == expected, "version 1 does not read back to your values"
assert read_room("my_files/my_room_v2.txt") == expected, "version 2 does not read back to your values"
by_hand = sum(float(row.split(",")[1]) for row in csv_text.splitlines()[1:])   # the areas, added without pandas
assert abs(pd.read_csv("my_files/my_flat.csv")["area_m2"].sum() - by_hand) < 1e-9, "CSV sum does not match"
saved = Path("my_files/teddy.obj").read_text(encoding="utf-8").splitlines()    # the teddy you saved
assert sum(l.startswith("v ") for l in saved) == len(xs) == 1598, "the teddy should have 1598 points"
corners = [int(n) for l in saved if l.startswith("f ") for n in l.split()[1:]]   # every corner number, again
assert len(corners) == 3 * 3192 == 3 * len(faces), "the teddy should have 3192 triangles of three corners"
assert min(corners) == 1 and max(corners) == len(xs), "every corner should name one of the points read"
print("✓ All green. Your files read back to what you wrote, and the teddy is complete.")
''')

nb.md(r'''
## Where you stand now

You know where your files live and how to get there with a path, from Python and from the terminal. You
wrote your own room into a text file, read it back, gave the format a header and a version, and changed
the format without losing the old files. You read a CSV table with pandas, and you have seen that a 3D
model is just text lines.

Next session: the web. Where the teddy came from, what a URL is, and what happens when you ask a server
for a file.

---

### Terms to learn

''' + TERMS_FOOTER + r'''

| term | in one sentence |
|---|---|
| path | the address of a file through its folders, like `../data/teddy.obj` |
| working directory | the folder you are in right now; relative paths start from there |
| text file | a file that holds only characters, line after line, readable with `cat` |
| header | the first line(s) of a file, saying what kind of file it is |
| format version | a number in the file that tells the reader which rules the rest follows |
| CSV | a table as text: column names in the first line, one row per line, commas between values |
''')

# ---------------------------------------------------------------------------------------------
nb.md(homework_header(
    "your flat as a data file",
    """In class you wrote your room in a format of ours. Now design your own: describe your flat, or any
place you know well (your grandparents' house, the studio, your favourite café), as a small text file.
Choose a header line, a version line, and the keys you want; then make a version 2 with **one** change
and read both back. Ideas for the change: rename a key so the unit shows, split one value into two
keys, add a line, merge two lines. Five to eight keys are plenty, at least one of them a number.""",
    """The cells come with a complete worked example: an invented, slightly untidy WG flat in Ottakring,
with a note line, an empty line and a decimal comma, and example answers under the questions. The reader
below skips empty lines and lines starting with `#` (notes for people), and reads a decimal comma as a
point. Run the example once first, then replace it with your own."""))

nb.code(r'''
# YOUR CHOICE: version 1 of your file. First line: your header. Second line: version 1.
# Then one key=value per line. Lines starting with # are notes and get skipped, empty lines too.
my_flat_v1 = """
WG FLAT, Ottakring
version 1
# measured with a folding rule, Oct 2026
street=Thaliastrasse
floor=3
size=68

rooms=4
kitchen=9,5
people=3
heating=gas, old boiler
"""

# YOUR CHOICE: version 2, the same place with ONE change. Here: "size" became "area_m2", to show the unit.
my_flat_v2 = """
WG FLAT, Ottakring
version 2
# measured with a folding rule, Oct 2026
street=Thaliastrasse
floor=3
area_m2=68

rooms=4
kitchen=9,5
people=3
heating=gas, old boiler
"""
''')

nb.code(r'''
# writes both versions to my_files and reads them back; you do not need to change anything here
def read_flat(flat_text, version):
    lines = [l.strip() for l in flat_text.strip().splitlines()]          # the lines, without spaces around
    assert len(lines) >= 3, "your file needs a header, a version line and at least one key=value line"
    assert lines[1] == f"version {version}", f"the second line should be 'version {version}', not {lines[1]!r}"
    flat = {}                                                       # key -> value
    for line in lines[2:]:                                          # everything after header and version
        if not line or line.startswith("#"):                        # empty lines and notes:
            continue                                                # skip them
        assert line.count("=") == 1, f"this line needs exactly one = sign: {line!r}"
        key, value = split_line(line)                               # your line from class
        assert key not in flat, f"the key {key!r} appears twice; give each line its own key"
        flat[key] = value
    return lines[0], flat                                           # the header and the pairs


for version, flat_text in ((1, my_flat_v1), (2, my_flat_v2)):            # save both versions as files
    Path(f"my_files/my_flat_v{version}.txt").write_text(flat_text.strip() + "\n", encoding="utf-8")
header1, flat1 = read_flat(Path("my_files/my_flat_v1.txt").read_text(encoding="utf-8"), 1)
header2, flat2 = read_flat(Path("my_files/my_flat_v2.txt").read_text(encoding="utf-8"), 2)
assert flat1 != flat2 or header1 != header2, "version 2 should differ from version 1 in one change"
print(f"✓ version 1: {len(flat1)} entries, header {header1!r}")
print(f"✓ version 2: {len(flat2)} entries, header {header2!r}")
''', hidden=True)

nb.code(r'''
# the two versions side by side; rows where they differ are marked
keys = list(dict.fromkeys(list(flat1) + list(flat2)))               # all keys, in order, no doubles
table = pd.DataFrame({"version 1": [flat1.get(k, "(missing)") for k in keys],
                      "version 2": [flat2.get(k, "(missing)") for k in keys]}, index=keys)
table["changed"] = ["◀" if a != b else "" for a, b in zip(table["version 1"], table["version 2"])]
changes = (table["changed"] != "").sum()                            # how many rows differ
print(f"{changes} rows differ between the versions (a renamed key counts twice: gone in one, new in the other)")
table
''', hidden=True)

nb.code(r'''
# the values of version 2 that are numbers, as bars (a decimal comma counts as a point)
numbers = {}
for k, v in flat2.items():                                          # try every value
    try:
        numbers[k] = float(v.replace(",", "."))                     # works for 68 and for 9,5
    except ValueError:                                              # text like "Thaliastrasse"
        pass
if numbers:                                                         # draw only if there is a number
    fig = px.bar(x=list(numbers), y=list(numbers.values()), text=list(numbers.values()), height=350,
                 labels={"x": "key", "y": "value"}, title=f"the numbers in version 2 of {header2!r}")
    fig.show()
else:
    print("No value in your file is a number, so there is nothing to draw. Add one, like area_m2=68.")
print(f"{len(numbers)} of {len(flat2)} values read as numbers; the rest stay text.")
''', hidden=True)

nb.md(r'''
### Your answers

One to three sentences per question, about your own file.

1. **Header.** What did you put in your header line, and what would someone who finds the file in five
   years still not know from it?
2. **Versions.** Why does the second line say the version? What would go wrong with your version 2 file
   if it had no version line?
3. **What breaks.** Your change from version 1 to 2: which program or person reading version 1 files
   would now get something wrong, and how would they notice (or not)?
4. **A colleague.** You send the file to a colleague. What do they need to know to read it correctly
   that is not in the file?

<details>
<summary>Example answers for the WG example. Click to see what a good answer looks like.</summary>

1. "WG FLAT, Ottakring": what it is and roughly where. In five years nobody knows which flat on
   Thaliastrasse, or whether size meant m² or rooms; the date sits in a comment, not in a key.
2. So a reader knows whether to look for `size` or `area_m2`. Without the line, the reader in this
   notebook stops at once, because it expects `version 2` there. A reader that skipped the check could
   not tell which name the area has.
3. Say a colleague wrote a script for my version 1 files that asks for `flat["size"]`. On version 2 it
   crashes with a KeyError, which at least they notice. Had I kept the name `size` and switched it to
   square feet, nobody would notice anything.
4. That `kitchen` is the kitchen's area in m², that the comma in 9,5 is a decimal comma while the comma
   in "gas, old boiler" is just text, and that the file is utf-8.

These fit the example only. Your answers are about your own file.

</details>

*Your text here.*
''')

nb.write("01_files")
