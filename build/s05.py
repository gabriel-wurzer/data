"""Session 5: putting it together, a digital twin of the classroom."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from nbbau import Notebook, DATA_BOX, homework_header, TERMS_FOOTER, box

nb = Notebook()

nb.md(r'''
# Session 5: Putting it together, a digital twin of the classroom

**259.021 Fundamentals of Utilizing Data Sources** · Session 5 of 5

A building scientist is more and more the keeper of a building's **digital twin**: a copy of the
building in data that knows what is going on inside it right now. Sensors report, a database
remembers, a picture shows it. Today you build a small one for a classroom door, with everything
from the last four sessions: a file, a web request, JSON, a database.

One thing first. Many sensors send their data to some company's cloud. Will that company still
exist in 40 years, which is about how long a building's systems run? The little street sensor
19330 that earlier years of this course read on Sensoto has sent nothing since August 2026. Data you
care about, you keep yourself.
''')

nb.md(r'''
## Step 1: count a door with your phone

Open the **occupancy sensor** app on your phone ([gabriel-wurzer.github.io/data/webapps/occupancy-sensor](https://gabriel-wurzer.github.io/data/webapps/occupancy-sensor/)). Lean the phone against something at
the side of a door or your laptop screen, press Start and step out of the picture. Walk your hand
through the picture from left to right, then right to left. The number goes up, then down.

Keep it running during the class, at the classroom door or just with your hand, and press **Download
CSV** after the break, so the break is in it. You will load that file in step 9. Until then we work with a recording of a
whole lecture morning.
''')

nb.md(DATA_BOX.format(text='''`door_events_sample.csv` is a recording of one classroom door on a Friday morning, 09:00 to
11:00, in exactly the format the app writes: one line per person passing, with the time, `in` or
`out`, and the number of people inside after that event. The file is made up, and the sensor in it
makes mistakes, as real ones do. Finding them is part of today.'''))

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 2: the plan, extract, transform, load

A worked example with four door events, by hand:

| time | event | count after it |
|---|---|---|
| 09:01 | in | 1 |
| 09:02 | in | 2 |
| 09:04 | out | 1 |
| 09:07 | in | 2 |

To turn this into a twin, we first read the four lines. Then we turn them into "at the end of 09:00 to
09:05 there was 1 person inside, at the end of 09:05 to 09:10 there were 2". Then we write those two
numbers into a table we keep. Those three moves have a name, **ETL**:

| | what it means | today |
|---|---|---|
| **E**xtract | get the raw data from where it is | the door CSV, the outdoor temperature from Sensoto |
| **T**ransform | clean and reshape it | readable times, repair mistakes, one number per 5 minutes |
| **L**oad | store it where you keep it | a small SQLite database file |

At the end, we show it in one picture.
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 3: extract the door events

Run the two cells. The first, collapsed, holds helpers for reading and fetching; you do not need to read
it. The second reads the CSV into a table, as in session 1, and checks that it has the three columns
the app writes.
''')

nb.code(r'''
# Helpers for reading the door file and fetching the weather; you do not need to read them.
import json                                           # to read and write JSON (session 3)
import os                                             # to check whether a file exists
import sqlite3                                        # the database (session 4)
import pandas as pd                                   # tables
import requests                                       # web requests (session 2)
import plotly.graph_objects as go                     # plots built piece by piece
from plotly.subplots import make_subplots             # several plots stacked


def read_door_events(path):
    """Extract: read a CSV from the occupancy sensor app and check it."""
    if not os.path.exists(path):                      # a typo in the path, or not uploaded yet
        raise FileNotFoundError(f"There is no file {path}. Upload it into the data folder and check the name.")
    events = pd.read_csv(path)                        # read the file into a table
    missing = {"time", "event", "occupancy"} - set(events.columns)   # columns the app always writes
    assert not missing, f"The file has no column(s) {missing}. Is it a CSV from the occupancy sensor app?"
    assert len(events) > 0, "The file has a header but no door events. Record a bit longer and download again."
    events["event"] = events["event"].astype(str).str.strip().str.lower()   # " In" counts as "in"
    odd = set(events["event"]) - {"in", "out"}        # anything that is neither in nor out
    assert not odd, f"The column 'event' should only contain in and out, but also has {odd}."
    return events                                     # hand back the table


def to_clock_time(texts):
    """Text like 2026-10-16T08:43:43+02:00 to a time, keeping the clock time and leaving the +02:00 aside."""
    try:
        return pd.to_datetime(texts.astype(str).str[:19])   # the first 19 characters are date and clock time
    except (ValueError, TypeError):
        raise ValueError("Some times in the file cannot be read. They must look like 2026-10-16T08:43:43+02:00 "
                         "(the +02:00 may be left out).") from None


STATION = ("https://api.sensoto.io/v1/organizations/open/networks/ghcn-hourly"     # Sensoto, weather stations
           "/devices/aum00011035/sensors/temperature/measurements")                # Wien Hohe Warte, temperature


def station_url(first_time):
    """The Sensoto address for 24 hourly means on the day of first_time, in its clock offset."""
    day, offset = first_time[:10], first_time[19:] or "+00:00"   # "2026-10-16" and "+02:00"
    return (f"{STATION}?interval=R24/{day}T00:00:00{offset.replace('+', '%2B')}/PT1H"   # 24 times one hour
            "&timeFormat=interval&agg=MEAN")          # the mean of each hour


def hours_with_values(answer):
    """How many hours of a Sensoto answer have a value; 0 if the answer is not what we expect."""
    if not isinstance(answer, list) or not all(isinstance(r, dict) and "begin" in r and "v" in r for r in answer):
        return 0                                      # an error message or something else
    return sum(r["v"] is not None for r in answer)    # hours with a number


def get_outdoor_temperature(first_time):
    """Extract: hourly outdoor temperature for the day of first_time, from Sensoto or from our own copy."""
    day = first_time[:10]                             # "2026-10-16"
    copy_path = f"../data/outdoor_temperature_{day}.json"   # where our own copy of that day lives
    copy = None
    if os.path.exists(copy_path):                     # a copy saved earlier
        with open(copy_path, encoding="utf-8") as f:
            copy = json.load(f)
    answer = None
    try:
        answer = requests.get(station_url(first_time), timeout=15).json()   # ask Sensoto, wait at most 15 s
    except Exception as problem:                      # no internet, Sensoto down, not JSON
        print(f"Could not get data from Sensoto ({type(problem).__name__}).")
    if hours_with_values(answer) == 0:                # nothing usable came back
        if answer is not None:
            print(f"Sensoto has no values for {day} yet; the station publishes a few days late.")
        answer = None
    elif hours_with_values(answer) >= hours_with_values(copy):   # at least as complete as our copy
        with open(copy_path, "w", encoding="utf-8") as f:
            json.dump(answer, f, indent=2)            # keep our own copy
        print(f"✓ Sensoto answered for {day}: {hours_with_values(answer)} hours; saved a copy in {copy_path}")
    else:                                             # Sensoto has fewer hours than our copy
        answer = None
    if answer is None:                                # use our own copy
        if hours_with_values(copy) == 0:              # no copy for that day either
            print("There is no copy for that day either; the twin goes on without outdoor temperature.")
            return pd.DataFrame({"time": pd.to_datetime([]), "temperature": []})   # an empty table
        answer = copy
        print(f"✓ Using our own copy {copy_path}")
    weather = pd.DataFrame(answer)[["begin", "v"]]    # keep the start of each hour and its value
    weather.columns = ["time", "temperature"]         # English names that say what they are
    weather["time"] = pd.to_datetime(weather["time"]).dt.tz_localize(None)   # text to time, keep the clock time
    return weather.dropna().reset_index(drop=True)    # drop hours without a value


print("✓ helpers ready")
''', hidden=True)

nb.code(r'''
events = read_door_events("../data/door_events_sample.csv")   # the sample morning
print(f"✓ {len(events)} door events, from {events['time'].iloc[0]} to {events['time'].iloc[-1]}")
events.head()                                         # show the first five lines
''')

nb.code(r'''
print(events["event"].value_counts())                 # how many in, how many out
print()
print(events.tail(3))                                 # the last three lines
''')

nb.md(r'''
Everyone who came in also left at the end. So how many `in` and how many `out` should there be? What
do the counts and the last line say instead?

<details>
<summary>Answer</summary>

There should be exactly as many `out` as `in`, and the count after the last event should be 0. Here
there are 34 `out` but only 33 `in`, and the last line says **−1**: one person more left than came
in. A room cannot hold minus one person. Somewhere the sensor missed someone, and we have to repair
that in step 5.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 4: extract the outdoor temperature

A twin of a room also wants to know the weather outside. Sensoto, from session 3, has the official
weather station Wien Hohe Warte. We ask it for one value per hour, for the day of the recording; the
day and the clock offset (`+02:00`, Vienna summer time) come from the first line of the door file.

The station publishes a few days late. When the answer has values, the helper saves a **copy** of it as
a JSON file in `data/`; when it has none, or Sensoto cannot be reached, it reads the copy instead. Run
the cell. You can paste the printed address into a browser tab to see the raw answer.
''')

nb.code(r'''
first_time = events["time"].iloc[0]                   # the first door event, as text
print(station_url(first_time))                        # the address we ask: a URL with parameters (session 2)
weather = get_outdoor_temperature(first_time)         # ask Sensoto, or use our own copy
print(f"✓ {len(weather)} hourly values, from {weather['temperature'].min()} to {weather['temperature'].max()} °C")
weather.head()                                        # the first five hours
''')

nb.md(r'''
Open `data/` in the file browser on the left and double-click the JSON file of that day. It is the
raw answer of Sensoto, a list of objects with `begin`, `end` and `v`, as in session 3. Why is it worth
keeping that file, when you could ask Sensoto again any time?

<details>
<summary>Answer</summary>

Because "any time" is not guaranteed. The station runs a few days late, the internet can be down in
class, and a service can change or vanish, like sensor 19330. With the copy, the notebook still runs
and gives the same result. It is your data now.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 5: transform, part 1, check and repair

First the times. In the file they are text, `"2026-10-16T08:43:43+02:00"`. The helper `to_clock_time`
turns them into real times that pandas can sort and group, keeping the clock time as you would read it
on the wall.
''')

nb.code(r'''
events["time"] = to_clock_time(events["time"])        # text to time, keep the clock time
events = events.sort_values("time", ignore_index=True)   # in the order they happened, to be safe
print(f"✓ times read: first {events['time'].iloc[0]:%H:%M:%S}, last {events['time'].iloc[-1]:%H:%M:%S}")
''')

nb.md(r'''
Then the check. A count can never be below 0, and never above what the room holds. When it gets there,
the sensor has made a mistake: a **miscount**.

The repair is simple. Count again from the events, starting from an empty room. Whenever the count would
drop below 0, keep it at 0; whenever it would go above the room's capacity, keep it at the capacity. Each
time counts as one repaired miscount. By hand, for four events:

| event | in | out | out | in |
|---|---|---|---|---|
| count, as the sensor had it | 1 | 0 | −1 | 0 |
| count, repaired | 1 | 0 | **0** | 1 |

One miscount repaired, and from there on the count is one higher than before.
''')

nb.code(r'''
room_capacity = 30                                    # seats in our classroom; more than this is implausible


def repair(events, capacity):
    """Transform: count again from the events, never below 0 or above capacity."""
    assert isinstance(capacity, int) and capacity > 0, "The capacity must be a whole number above 0, e.g. 4."
    count, fixed, miscounts = 0, [], 0                # start with an empty room
    for event in events["event"]:                     # go through the events in order
        count = count + 1 if event == "in" else count - 1   # one more or one less
        if count < 0:                                 # fewer than nobody: a miscount
            count, miscounts = 0, miscounts + 1       # keep it at 0, and note it
        elif count > capacity:                        # more than fit into the room: a miscount
            count, miscounts = capacity, miscounts + 1    # keep it at capacity, and note it
        fixed.append(count)                           # remember the count after this event
    events["occupancy_fixed"] = fixed                 # a new column next to the sensor's own
    return events, miscounts                          # the table, and how many repairs


events, miscounts = repair(events, room_capacity)     # check and repair the sample morning
print(f"sensor's own count: lowest {events['occupancy'].min()}, highest {events['occupancy'].max()}")
print(f"repaired count:     lowest {events['occupancy_fixed'].min()}, highest {events['occupancy_fixed'].max()}")
print(f"✓ {miscounts} miscount(s) repaired.")
''')

nb.md(r'''
The repair found one miscount, at the very end, where the last person left an "empty" room. Does the
repaired count now tell the truth about the whole morning?

<details>
<summary>Answer</summary>

Not necessarily. The repair only sees the moment where the count became impossible. The sample was made
with three mistakes planted on purpose: two students walking in side by side were counted as one, a
person standing in the doorway in the break was counted as an extra `out`, and one student was counted
`in` twice. Two of them cancel out; the one missing person makes the count end at −1. All morning, the
count was probably one too low, but the twin cannot know since when. The repair makes the numbers
possible, not true.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 6: transform, part 2, one number per five minutes

The door events come at odd times: 08:43:43, 08:50:09, ... For a picture and for comparing days we want
one number per fixed step of time, here five minutes: **how many people are in the room at the end of
each five minutes**. Turning irregular events into regular steps is called **resampling**. In the worked
example from step 2: at the end of 09:00 to 09:05 the count was 1 (after the `out` at 09:04), at the end
of 09:05 to 09:10 it was 2.

pandas does it in two short lines. For hourly temperatures, they would read:

    timeline = weather.set_index("time")
    hourly = timeline["temperature"].resample("1h").mean()

The first line makes the time the row labels (the "index"), so pandas knows where each hour begins. The
second, in words: *hourly becomes the column "temperature" of timeline, resampled to "1h", taking the
`.mean()` of each hour*. In the cell below, the first line is written for you; the second is yours.
''')

nb.code(r'''
def per_5_minutes(events):
    """Transform: the repaired count at the end of each five minutes."""
    timeline = events.set_index("time")               # time becomes the index, so pandas can step through it

    # YOUR TURN: replace the line "raise ..." with one line:
    #   occupancy becomes the column "occupancy_fixed" of timeline, resampled to "5min", taking the .last() of each
    raise NotImplementedError("replace this line with the line described above")

    return occupancy.ffill().astype(int)              # five quiet minutes keep the count from before; whole people


occupancy = per_5_minutes(events)                     # the sample morning in five-minute steps
print(f"✓ {len(occupancy)} five-minute steps, from {occupancy.index[0]:%H:%M} to {occupancy.index[-1]:%H:%M}")
print(occupancy.head(6))                              # the first half hour
''', solution=r'''
def per_5_minutes(events):
    """Transform: the repaired count at the end of each five minutes."""
    timeline = events.set_index("time")               # time becomes the index, so pandas can step through it

    occupancy = timeline["occupancy_fixed"].resample("5min").last()   # the last count in each five minutes

    return occupancy.ffill().astype(int)              # five quiet minutes keep the count from before; whole people


occupancy = per_5_minutes(events)                     # the sample morning in five-minute steps
print(f"✓ {len(occupancy)} five-minute steps, from {occupancy.index[0]:%H:%M} to {occupancy.index[-1]:%H:%M}")
print(occupancy.head(6))                              # the first half hour
''')

nb.md(r'''
<details>
<summary>Answer</summary>

    occupancy = timeline["occupancy_fixed"].resample("5min").last()

</details>

Each step is labelled with its start: the line `08:50  7` means "at the end of 08:50 to 08:55, seven
people were in the room". In the `return` line, `.ffill()` ("fill forward"), handles five minutes
in which nobody passed the door: no event, so the count from before still holds. `.astype(int)` makes
the counts whole numbers again.
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 7: load into a database

Now we keep everything in one SQLite file, as in session 4: the repaired door events, the five-minute
counts and the outdoor temperature, one table each. `to_sql` writes a pandas table into the database;
`if_exists="replace"` overwrites the table if you run the cell again.
''')

nb.code(r'''
def load(db_path, events, occupancy, weather):
    """Load: write the three tables into one SQLite file."""
    db = sqlite3.connect(db_path)                     # open the file, or create it
    events.to_sql("door_events", db, if_exists="replace", index=False)           # table 1: every door event
    occupancy.rename("occupancy").reset_index().to_sql("occupancy_5min", db,      # table 2: five-minute counts
                                                       if_exists="replace", index=False)
    weather.to_sql("outdoor_temperature", db, if_exists="replace", index=False)   # table 3: hourly temperature
    db.commit()                                       # make sure it is written to the file
    return db                                         # hand back the open database


db = load("../data/classroom_twin.db", events, occupancy, weather)   # our twin's memory
for table in ["door_events", "occupancy_5min", "outdoor_temperature"]:   # check before you trust:
    rows = db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]       # count the rows in the file
    print(f"✓ {table}: {rows} rows")
''')

nb.md(r'''
Compare the row counts with the tables above: 67 door events, 29 five-minute steps, and one row per
hour of temperature. Same numbers, so nothing got lost on the way into the file.

Now ask the database, in SQL. First: when was the room fullest?
''')

nb.code(r'''
peak = pd.read_sql("""
    SELECT time, occupancy FROM occupancy_5min
    ORDER BY occupancy DESC, time                     -- fullest first, the earliest of equals first
    LIMIT 1                                           -- only the top row
""", db)                                              # run the query, get a pandas table back
print(peak)
''')

nb.md(r'''
And the two sources side by side, by hour: a `JOIN` (session 4) that matches each five-minute count with
the temperature of its hour. `strftime('%H', time)` picks the hour out of a time.
''')

nb.code(r'''
by_hour = pd.read_sql("""
    SELECT strftime('%H:00', o.time) AS hour,         -- the hour, e.g. 09:00
           ROUND(AVG(o.occupancy), 1) AS people,      -- average count in that hour
           t.temperature AS outdoor_temperature       -- the outdoor temperature of that hour
    FROM occupancy_5min AS o
    JOIN outdoor_temperature AS t                     -- match the two tables ...
      ON strftime('%Y-%m-%d %H', o.time) = strftime('%Y-%m-%d %H', t.time)   -- ... on day and hour
    GROUP BY hour                                     -- one row per hour
""", db)
print(by_hour)
''')

nb.md(r'''
Keep this little table in mind; after the picture in step 8 you will see what is behind its numbers.
''')

nb.md(box("Earlier years did this in node-red", '''Students in earlier years built the same pipeline in
**node-red**, a tool where you draw it instead of writing it: boxes ("nodes") for "receive a door event",
"change the count", "write to a file", joined by lines, with messages flowing along them as JSON. It runs
on a small computer such as a Raspberry Pi next to the door, all day. You do not need it for this course;
it is worth a look if you want your twin to run on its own.'''))

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 8: show it

A twin needs a face. Run the cell: one picture, dashboard style. On top, the people in the room, every
door event as a thin grey line and the five-minute counts in blue; below, the outdoor temperature over
the same hours. Each blue dot sits at the end of its five minutes. Hover for values.
''')

nb.code(r'''
# the dashboard: occupancy on top, outdoor temperature below, peak and dip marked
def show(events, occupancy, weather, miscounts, title):
    peak_value = events["occupancy_fixed"].max()                      # most people at any moment
    peak_time = events.loc[events["occupancy_fixed"].idxmax(), "time"]  # the first time it got there
    half = occupancy >= peak_value / 2                                # steps with at least half the peak
    inside = occupancy[half.idxmax(): half[::-1].idxmax()]             # from first to last such step
    low = inside < peak_value / 2                                     # dips below half in between
    dip = None
    if low.any():                                                     # find the longest run of low steps
        runs = (low != low.shift()).cumsum()[low]
        longest = runs.value_counts().idxmax()
        steps = runs[runs == longest].index
        dip = (steps[0], steps[-1] + pd.Timedelta("5min"))
    start = events["time"].min().floor("15min") - pd.Timedelta("15min")   # a quarter hour of margin
    end = events["time"].max().ceil("15min") + pd.Timedelta("15min")
    near = weather[(weather["time"] >= start - pd.Timedelta("1h")) & (weather["time"] <= end)]
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.72, 0.28], vertical_spacing=0.08,
                        subplot_titles=("", "outdoor temperature, Wien Hohe Warte [°C]"))
    fig.add_trace(go.Scatter(x=events["time"], y=events["occupancy_fixed"], mode="lines", line_shape="hv",
                             line=dict(color="#b8b8b8", width=1), name="after every door event"), row=1, col=1)
    fig.add_trace(go.Scatter(x=occupancy.index + pd.Timedelta("5min"), y=occupancy.values, mode="lines+markers",
                             line_shape="hv", line=dict(color="#4c78a8", width=2), marker=dict(size=6),
                             name="at the end of each 5 minutes"), row=1, col=1)
    fig.add_trace(go.Scatter(x=[peak_time], y=[peak_value], mode="markers+text",
                             marker=dict(size=12, color="#4c78a8", line=dict(color="white", width=2)),
                             text=[f"peak {peak_value:.0f}"], textposition="top center", showlegend=False),
                  row=1, col=1)
    if dip:                                                           # shade the dip, probably a break
        fig.add_vrect(x0=dip[0], x1=dip[1] + pd.Timedelta("5min"),   # grey drop to the end of the blue dip
                      fillcolor="#d8a24a", opacity=0.18, line_width=0, row=1, col=1,
                      annotation_text="dip (a break?)", annotation_position="top left")
    if len(near):
        fig.add_trace(go.Scatter(x=near["time"], y=near["temperature"], mode="lines+markers",
                                 line=dict(color="#d8a24a", width=2), marker=dict(size=7),
                                 showlegend=False, name="outdoor °C"), row=2, col=1)
    fig.update_xaxes(range=[start, end], tickformat="%H:%M")
    fig.update_yaxes(rangemode="tozero", title_text="people in the room", row=1, col=1)
    fig.update_layout(height=560, hovermode="x unified", legend=dict(orientation="h", y=1.1, x=0),
                      margin=dict(t=110), title=f"{title}: peak {peak_value:.0f} people, first at "
                      f"{peak_time:%H:%M}, {miscounts} miscount(s) repaired")
    fig.show()
    return peak_value, peak_time, dip


peak_value, peak_time, dip = show(events, occupancy, weather, miscounts, "Classroom door, sample morning")
''', hidden=True)

nb.md(r'''
Find the peak, the break and the end of the lecture in the picture. When did the break start, and what
does the count say after it?

<details>
<summary>Answer</summary>

The peak is 20 people, first reached at 09:21 when the last latecomer came in. The break is the shaded
dip: from 09:45 the count falls, the five-minute readings at 09:50 and 09:55 are 7 and 6, and from 10:05
it is back at 18. The count rose by 12, but that does not prove 12 people came back: in the story of
this file, 11 returned and one was counted twice. At 11:00 everyone leaves and the count drops to 0. The
temperature below rises through the morning; it says nothing about the room itself.

</details>

Now back to the table by hour from step 7. The room was fullest in the 09:00 hour, yet its average is
lower than that of 10:00. Why? And can you tell from that table whether the people made the room warmer?

<details>
<summary>Answer</summary>

The break lies inside the 09:00 hour: the readings at 09:50 and 09:55, 7 and 6, pull its average down
to 16.7. In the 10:00 hour every five-minute reading is 18, so its average is 18.0. An average hides what
happened inside the hour. Whether the people warmed the room, no: we only have the temperature
**outside**. There is no sensor inside the room, so the twin does not know.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 9: your own door

The whole pipeline, extract, transform, load, show, now fits in one function: it just calls the steps
above one after the other. The repair starts counting from an empty room, so a recording only makes
sense if it started with nobody inside (press Reset in the app before you start) and everyone used that
one door. Upload the CSV from your phone into the `data` folder (upload arrow at the
top of the file browser; from the phone, open the hub in its browser, or send the file to yourself).
Then put its name below, instead of `None`, and run.
''')

nb.code(r'''
def run_twin(csv_path, capacity, db_path, title):
    """The whole pipeline for one recording."""
    events = read_door_events(csv_path)                                    # extract the door
    weather = get_outdoor_temperature(events["time"].iloc[0])              # extract the weather
    events["time"] = to_clock_time(events["time"])                         # transform: real times
    events = events.sort_values("time", ignore_index=True)                 # in the order they happened
    events, miscounts = repair(events, capacity)                           # transform: check and repair
    occupancy = per_5_minutes(events)                                      # transform: five-minute steps
    load(db_path, events, occupancy, weather).close()                      # load, then close the file
    peak_value, peak_time, dip = show(events, occupancy, weather, miscounts, title)   # show
    return {"events": len(events), "miscounts": miscounts, "peak": peak_value, "peak_time": peak_time}


# YOUR CHOICE: the name of your own CSV in the data folder, e.g. "../data/door_events_AE_U1-5_2026-10-16.csv"
my_csv = None

if my_csv is None:                                    # nothing chosen yet
    print("No file chosen yet. Upload your CSV into the data folder, put its name above, and run again.")
else:
    mine = run_twin(my_csv, room_capacity, "../data/my_twin.db", "My door")   # the pipeline on your file
    print(f"✓ {mine['events']} events, peak {mine['peak']:.0f}, {mine['miscounts']} miscount(s) repaired.")
''')

nb.md(r'''
If you only waved your hand, your twin shows a few spikes. Did it count every pass? If your count
went below 0 at some point, the repair caught it.
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Tests

Run this cell before you submit. It recomputes the worked examples of steps 2 and 5 with your functions,
tries five quiet minutes, and reads the five-minute counts back from the database.
''')

nb.code(r'''
by_hand = pd.DataFrame({"time": pd.to_datetime(["2026-01-01 09:01", "2026-01-01 09:02",      # step 2, by hand
                                                "2026-01-01 09:04", "2026-01-01 09:07"]),
                        "event": ["in", "in", "out", "in"]})
by_hand, n = repair(by_hand, 30)                      # nothing to repair here
assert n == 0 and list(by_hand["occupancy_fixed"]) == [1, 2, 1, 2], "repair should count 1, 2, 1, 2"
steps = per_5_minutes(by_hand)                        # your resampling line
assert list(steps) == [1, 2], f"expected 1 at 09:00 and 2 at 09:05, got {list(steps)}"
assert list(steps.index.strftime("%H:%M")) == ["09:00", "09:05"], "the steps should start at 09:00 and 09:05"

table5 = pd.DataFrame({"event": ["in", "out", "out", "in"]})   # step 5, by hand
table5, n = repair(table5, 30)
assert n == 1 and list(table5["occupancy_fixed"]) == [1, 0, 0, 1], "repair should give 1, 0, 0, 1 with one miscount"
full = repair(pd.DataFrame({"event": ["in"] * 3}), 2)  # three in, but the room holds two
assert full[1] == 1 and list(full[0]["occupancy_fixed"]) == [1, 2, 2], "capacity should cap the count"

quiet = pd.DataFrame({"time": pd.to_datetime(["2026-01-01 09:01", "2026-01-01 09:12"]), "event": ["in", "in"]})
quiet, n = repair(quiet, 30)                          # nobody passes from 09:05 to 09:10
assert list(per_5_minutes(quiet)) == [1, 1, 2], "five quiet minutes should keep the count from before: 1, 1, 2"

stored = pd.read_sql("SELECT occupancy FROM occupancy_5min ORDER BY time", db)["occupancy"]   # back from the file
assert list(stored) == list(occupancy), "the database does not hold the same five-minute counts"
assert db.execute("SELECT COUNT(*) FROM door_events").fetchone()[0] == len(events), "door events lost"
print("✓ All green. Your pipeline extracts, repairs, resamples and loads correctly.")
''')

nb.md(r'''
## Where you stand now

You have built a small digital twin from scratch: a door recorded with your phone, the weather from a
web API, both cleaned, checked, stored in your own database and shown in one picture. That is all five
sessions in one pipeline.

| session | what you used of it today |
|---|---|
| 1 Files, where data lives | the door CSV in `data/`, your own JSON copy next to it |
| 2 The web, asking a machine for data | a URL with parameters, a GET request with a timeout |
| 3 Sensors, data as JSON | Sensoto's answer as a list of objects with `begin` and `v` |
| 4 Databases, keeping data in order | `to_sql`, `SELECT ... ORDER BY`, a `JOIN` |
| 5 Putting it together | extract, transform, load, show |

Three habits to take with you, whatever the data:

1. **Know where your data comes from, and in which format.** A phone, a station, a file; CSV or JSON;
   which clock.
2. **Keep your own copy.** Services stop, sensors go silent. A CSV, a JSON and an SQLite file will
   still open in 40 years.
3. **Check before you trust.** Count the rows, look for impossible values, and remember that a repaired
   number is possible, not necessarily true.

---

### Terms to learn

''' + TERMS_FOOTER + r'''

| term | in one sentence |
|---|---|
| digital twin | a copy of a building in data that follows what goes on in the real one |
| data pipeline | a chain of steps that takes raw data to a stored, usable result, the same way every time |
| ETL | extract, transform, load: get the raw data, clean and reshape it, store it |
| resampling | turning events at irregular times into one value per regular step, such as five minutes |
| plausibility check | a test for values that cannot be true, such as fewer than zero people in a room |
''')

# ---------------------------------------------------------------------------------------------
nb.md(homework_header(
    "a twin of a door at home",
    """In class you ran the pipeline on a classroom morning. Now run it on a door of your own life:
record any door at home, the kitchen, the bathroom, the front door of your flat, for about 20 minutes at
a busy time (dinner, morning rush, a party). Start when nobody is inside, press Reset in the app, and
pick a door that everyone has to use. Then run the twin on it and tell us what it saw, what it
repaired, and what it cannot know.

No phone that works with the app? Write down the door by hand for 20 minutes, one line per person
passing, and save it in JupyterLab as a CSV with the same three columns as the sample (File, New, Text
File, then rename it to `.csv`). That is your own data too. It starts like this:

    time,event,occupancy
    2026-10-20T18:02:00+02:00,in,1
    2026-10-20T18:05:30+02:00,out,0

If you recorded in the last few days, the station has no temperature for your day yet, and the lower
panel stays empty. That is fine; the twin goes on without it.""",
    """The cells below come with the worked example filled in: the sample classroom morning, with its
miscount, and example answers under the questions. Run it once first, then put in your own file,
door name and capacity."""))

nb.code(r'''
# YOUR CHOICE: your own recording (upload it into the data folder first), what door it is,
# and how many people can plausibly be behind it at the same time
homework_csv = "../data/door_events_sample.csv"
door_name = "Classroom door, sample morning"
door_capacity = 30

home = run_twin(homework_csv, door_capacity, "../data/home_twin.db", door_name)   # the whole pipeline
print(f"✓ {home['events']} door events, peak {home['peak']:.0f} at {home['peak_time']:%H:%M}, "
      f"{home['miscounts']} miscount(s) repaired.")
''')

nb.md(r'''
### Your answers

One to three sentences per question, about your own door.

1. **Peak.** When was it fullest behind your door, and how many? Does that match what you saw?
2. **Miscounts.** How many miscounts did the twin repair? Can you guess what caused them (two people at
   once, someone turning back, the cat)? Were there mistakes the repair could not see?
3. **What the twin cannot know.** Name one thing about your room that matters to a building scientist
   and that your twin cannot know from a door and an outdoor temperature.
4. **Your own copy.** Which files in `data/` did your run use or create, and in which formats? Would you
   be able to open them in 40 years, and why?

<details>
<summary>Example answers for the sample morning. Click to see what a good answer looks like.</summary>

1. The peak was 20 people, first at 09:21, and again from 09:31 to 09:45. In the story of the file,
   20 students and the lecturer were there, so 21; the twin is one short.
2. One miscount, at 11:04, where the last person left a room that the count said was empty. The cause is
   earlier: two people side by side counted as one. The extra `out` and the double `in` in the break
   cancel out, so the repair cannot see them at all.
3. How warm and stale the air in the room got. We have only the outdoor temperature; without a
   thermometer or CO₂ sensor inside, the twin does not know what 20 people did to the room.
4. In `data/`: the door events as CSV, the station's answer as JSON, and everything in `home_twin.db`,
   an SQLite file. All three are open, plain formats that many programs read, so yes, as long as I keep
   the files.

These fit the example only. Your answers are about your own door.

</details>

*Your text here.*
''')

nb.write("05_twin")
