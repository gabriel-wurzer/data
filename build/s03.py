"""Session 3: sensors, data as JSON."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from nbbau import Notebook, DATA_BOX, homework_header, TERMS_FOOTER, box

nb = Notebook()

nb.md(r'''
# Session 3: Sensors, data as JSON

**259.021 Fundamentals of Utilizing Data Sources** · Session 3 of 5

Last session the weather service answered in JSON, and a plot read it for you. Today you read it
yourself. By the end of the class you will have a month of temperatures from a street sensor in Vienna
in a table and a plot, and you will know the warmest day of that month in your part of town.
''')

nb.md(DATA_BOX.format(text='''The sensors belong to **sensor.community** (once called luftdaten.info): volunteers who hang a
small, cheap sensor at their window or on their balcony. A company, Sensoto, collects the readings and
hands them out over the web. That puts the sensors where people live, and makes them imperfect: a sensor
in the afternoon sun or next to a warm wall reads high. When we checked on 12 October 2026, these
sensors had sent nothing from 25 July to 8 October 2026, so ask for days up to 24 July 2026.
*Data provided by sensor.community under Database Contents License (DbCL) v1.0.*'''))

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 1: a reading you can read

Here is one reading, as a sensor could send it over the web:

    {"sensor": "balcony", "time": "2025-10-17T08:00", "temperature": 11.6, "unit": "°C", "working": true, "humidity": null}

Read it like a form. Left of each colon is a **key**, the name of a field, always in double quotes.
Right of it is the **value**. A value is text in quotes (`"°C"`), a number (`11.6`), `true` or `false`,
or `null` for "nothing here". The curly braces hold it together: this is a **JSON object**. JSON stands
for JavaScript Object Notation. Run the cell.
''')

nb.code(r'''
import json                                           # Python's reader and writer for JSON
import pandas as pd                                   # tables
import plotly.express as px                           # quick interactive plots
import plotly.graph_objects as go                     # plots built piece by piece

text = '{"sensor": "balcony", "time": "2025-10-17T08:00", "temperature": 11.6, "unit": "°C", "working": true, "humidity": null}'
reading = json.loads(text)                            # turn the JSON text into a Python dictionary

print("before:", type(text).__name__, " after:", type(reading).__name__)   # str is text, dict is a dictionary
print("temperature:", reading["temperature"])         # pick a value by its key
print("unit:", reading["unit"])                       # another key
print("working:", reading["working"], " humidity:", reading["humidity"])   # true and null, in Python words
print("one degree warmer:", reading["temperature"] + 1)                    # it is a real number, you can add to it
print("✓ JSON read.")
''')

nb.md(r'''
Python calls the result a **dictionary**: keys and values, just like the JSON. You pick a value with
the key in square brackets, `reading["temperature"]`. JSON's `true` and `null` became Python's `True`
and `None`.

Now open a new cell below (the **+** in the toolbar), type `reading["Temperature"]` with a capital T, and
run it. What happens? Afterwards delete that cell again (right-click, Delete Cell), so the notebook runs
through from top to bottom.

<details>
<summary>Answer</summary>

`KeyError: 'Temperature'`. There is no key called that. Keys must match letter for letter, capitals
included. When you get a `KeyError`, compare your key with the JSON character by character.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 2: lists, objects inside objects, and five real sensors

A value can also be a **list** in square brackets, or another **object** in curly braces. An example:

    {"sensor": "balcony",
     "location": {"lat": 48.214, "lon": 16.388},
     "last_three": [11.6, 12.0, 12.4]}

To get the latitude, go in two steps: `reading["location"]` is the inner object, and `["lat"]` picks
from that, so `reading["location"]["lat"]` is 48.214. From a list you pick by position, counting from 0:
`reading["last_three"][0]` is 11.6, the first one.
''')

nb.code(r'''
reading = json.loads('{"sensor": "balcony", "location": {"lat": 48.214, "lon": 16.388}, "last_three": [11.6, 12.0, 12.4]}')
print(reading["location"])                            # the inner object, a dictionary of its own
print(reading["location"]["lat"])                     # two steps in: the latitude
print(reading["last_three"])                          # the list
print(reading["last_three"][0])                       # its first entry (position 0)
print(reading["last_three"][-1])                      # -1 is a shortcut for the last entry
''')

nb.md(r'''
The file `../data/vienna_sensors.json` lists five real sensors of the network, in five districts. Open it
in the file browser on the left (double-click), look at its shape, then come back and run the cell.
''')

nb.code(r'''
with open("../data/vienna_sensors.json", encoding="utf-8") as f:   # open the file
    sensors_info = json.load(f)                       # json.load reads JSON from a file (json.loads from text)

print("measures:", sensors_info["measures"], "in", sensors_info["unit"])   # two plain keys
sensors = sensors_info["sensors"]                     # the list of sensors
print("number of sensors:", len(sensors))             # how long is the list?
print("first sensor:", sensors[0]["district"], "near", sensors[0]["near"])   # position 0, then a key
print("its latitude:", sensors[0]["location"]["lat"]) # position 0, then two keys
print()
for s in sensors:                                     # one line per sensor
    print(f'{s["district_number"]:>2}. {s["district"]:<13} near {s["near"]:<22} device {s["device"]}')
''')

nb.code(r'''
# the five sensors on a map of Vienna
fig = px.scatter_map(pd.DataFrame([{"district": s["district"], "near": s["near"], "lat": s["location"]["lat"],
                                    "lon": s["location"]["lon"]} for s in sensors]),   # one row per sensor
                     lat="lat", lon="lon", text="district", hover_data=["near"], zoom=10.3, height=430,
                     map_style="carto-positron")          # a light street map underneath
fig.update_traces(marker=dict(size=14, color="#4c78a8"), textposition="top right")   # big dots with names
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
fig.show()                                            # draw it
''', hidden=True)

nb.md(r'''
Pick the sensor closest to your home, or the one in a district you like. It stays yours for the rest of
the session and in the homework.
''')

nb.code(r'''
# YOUR CHOICE: one of the five districts above, in quotes
my_district = "Leopoldstadt"

names = [s["district"] for s in sensors]              # the five district names
if my_district not in names:                          # a typo, or another district
    raise ValueError(f"{my_district!r} is not one of the five. Choose one of: {', '.join(names)}")
else:
    my_sensor = sensors[names.index(my_district)]     # the dictionary of your sensor
    my_device = my_sensor["device"]                   # its device id, used in the web address
    print(f"✓ Your sensor: {my_district}, near {my_sensor['near']}, device {my_device}.")
''')

nb.md(r'''
How would you write the longitude of the **third** sensor in the list, and what is it?

<details>
<summary>Answer</summary>

`sensors[2]["location"]["lon"]`: position 2 (counting 0, 1, 2), then the key `location`, then `lon`.
It is the sensor in Penzing, at longitude 16.26. Try it in a new cell.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 3: ask the real sensor

A web address that answers with data for programs, not pages for people, is called an **API**
(application programming interface). Each sensor has its own address, built from its device id. The
question needs one parameter, `interval`, written in the international date standard **ISO 8601**:

    R30/2025-10-17T00:00/P1D

Read it as: **R**epeat 30 times, starting 17 October 2025 at midnight, each a **P**eriod of **1** **D**ay.
That is the same 30 days one year ago. `"agg": "MEAN"` asks for the average of each day. Run the
helper, then the request. The answer prints a URL: click it and your browser shows the raw JSON.
''')

nb.code(r'''
# Helper: GET a URL with params and read the JSON; with no network, use the saved copy in ../data
import requests                                       # HTTP, as in session 2

HEADERS = {"User-Agent": "TU Wien course notebook (python requests)"}   # say who is asking
FALLBACK = "../data/sensor_fallback.json"             # answers saved on 12 October 2026


def get_json(url, params):
    full_url = requests.Request("GET", url, params=params).prepare().url   # the URL with the query
    try:
        response = requests.get(full_url, headers=HEADERS, timeout=20)     # ask, wait at most 20 s
    except requests.exceptions.RequestException:      # no network, or the server did not answer
        response = None
    if response is None or response.status_code >= 500:   # no answer, or the server has a problem
        with open(FALLBACK, encoding="utf-8") as f:
            saved = json.load(f)                      # the saved answers, keyed by URL
        if full_url in saved:
            print(f"No answer from the server; using the saved copy in {FALLBACK} of:\n{full_url}")
            return saved[full_url]
        print("No answer from the server, and no saved copy for this question. Try again in a minute.")
        return None
    if response.status_code != 200:                   # the server understood us, but said no
        print(f"The server answered {response.status_code}: {response.text[:200]}")
        return None
    data = response.json()                            # the JSON text, read into Python
    print(f"✓ status 200, {len(data)} values. Open this in your browser to see the raw JSON:\n{full_url}")
    return data


print("✓ get_json ready.")
''', hidden=True)

nb.code(r'''
BASE = "https://api.sensoto.io/v1/organizations/open/networks/luftdaten-info/devices/"   # the network
url = BASE + my_device + "/sensors/temperature/measurements"   # your sensor's temperatures
params = {"interval": "R30/2025-10-17T00:00/P1D",     # 30 days from 17 October 2025, one value per day
          "agg": "MEAN"}                              # each value is the average of its day
result = get_json(url, params)                        # ask, and read the JSON answer
''')

nb.code(r'''
assert result is not None, "No data yet; read the message above and run the cell again."
print(type(result).__name__, "with", len(result), "entries")   # what kind of thing came back?
print(json.dumps(result[:2], indent=2))               # the first two entries, nicely indented
''')

nb.md(r'''
The answer is a list of objects, one per day. The keys are short to keep the answer small:

| key | means |
|---|---|
| `begin` | when the day starts |
| `v` | the value: the average temperature of that day, in °C |
| `hi`, `lo` | the highest and lowest reading during that day |
| `c` | we leave it aside; it drops towards 0 on a day the sensor sent almost nothing |

On days without data, `v`, `hi` and `lo` are `null`. The numbers in the answers below are for
Leopoldstadt; with another sensor, yours differ a little.

What was the average on the first day, and how far apart were its lowest and highest reading?

<details>
<summary>Answer</summary>

13.3 °C on average. Lowest 11.6, highest 14.8, so 3.2 degrees apart: an even day, without much change from night to afternoon. In
Python: `result[0]["v"]`, and `result[0]["hi"] - result[0]["lo"]`.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 4: from JSON to a table

A list of objects that all have the same keys is a table in disguise: each object is a row, each key
a column. pandas turns it into one in a single line. We also rename the short keys to readable column
names and drop `c`.
''')

nb.code(r'''
df = pd.DataFrame(result)                             # one row per object, one column per key
df = df.rename(columns={"v": "temperature", "hi": "highest", "lo": "lowest"})   # readable names
df = df.drop(columns="c")                             # we leave c aside
print(df.dtypes)                                      # what kind of values each column holds
df.head()                                             # the first five rows
''')

nb.md(r'''
The numbers came in as numbers (`float64`), because JSON says what is a number. A `null` would become
`NaN`, "not a number", and pandas leaves those out when it computes. But `begin` is text (pandas writes
`object` or `str`, depending on its version). One line turns it into a real time; the `+01:00` at the end
means one hour ahead of world time (UTC), which is Vienna's winter time.
''')

nb.code(r'''
df["begin"] = pd.to_datetime(df["begin"])             # text to time
print("begin is now:", df["begin"].dtype)             # a time type, with the +01:00 offset
print("first day:", df["begin"][0].strftime("%A, %d %B %Y"))   # pandas now knows the weekday
print("the period lasts", (df["begin"].iloc[-1] - df["begin"][0]).days + 1, "days")   # times can be subtracted
''')

nb.md(r'''
Why bother? What can you do with a time that you cannot do with text?

<details>
<summary>Answer</summary>

pandas knows that 17 October 2025 was a Friday and that the period lasts 30 days, because it can
subtract one time from another. As text, `"2025-10-17T00:00+01:00"` is just a row of characters: no
weekday, no "how many days between", no "add one week".

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 5: your part, average, lowest and highest

For a period we want three numbers. An example with three days, with daily averages 10, 12 and 14 °C:
the average of the period is (10 + 12 + 14) / 3 = 12 °C. The lowest is the smallest value in the column
`lowest`, the highest the largest in `highest`.

In pandas you pick a column by name, then add a dot and what you want from it. The first line of the
cell below reads "coldest becomes the minimum of the column lowest of table":

    coldest = table["lowest"].min()

The average of a column is `.mean()`. One line is yours; indent it like the lines around it.
''')

nb.code(r'''
def summarize(table):
    coldest = table["lowest"].min()                   # the lowest reading of the period
    warmest = table["highest"].max()                  # the highest reading of the period

    # YOUR TURN: replace the line "raise ..." with one line:
    #   average becomes: the mean of the column "temperature" of table
    raise NotImplementedError("replace this line with the line described above")

    return average, coldest, warmest                  # hand back the three numbers


average, coldest, warmest = summarize(df)             # the three numbers for your month
print(f"✓ {my_district}, 17 October to 15 November 2025: average {average:.1f} °C, "
      f"lowest {coldest:.1f} °C, highest {warmest:.1f} °C")
''', solution=r'''
def summarize(table):
    coldest = table["lowest"].min()                   # the lowest reading of the period
    warmest = table["highest"].max()                  # the highest reading of the period

    average = table["temperature"].mean()             # the mean of the daily averages

    return average, coldest, warmest                  # hand back the three numbers


average, coldest, warmest = summarize(df)             # the three numbers for your month
print(f"✓ {my_district}, 17 October to 15 November 2025: average {average:.1f} °C, "
      f"lowest {coldest:.1f} °C, highest {warmest:.1f} °C")
''')

nb.md(r'''
<details>
<summary>Answer</summary>

    average = table["temperature"].mean()

</details>

And on which days were the lowest and the highest reading?
''')

nb.code(r'''
cold_day = df.loc[df["lowest"].idxmin(), "begin"]     # the row where "lowest" is smallest, its day
warm_day = df.loc[df["highest"].idxmax(), "begin"]    # the row where "highest" is largest, its day
print(f"coldest moment on {cold_day:%A, %d %B}, warmest on {warm_day:%A, %d %B}")
print(f"middle between lowest and highest: {(coldest + warmest) / 2:.1f} °C, average: {average:.1f} °C")
''')

nb.md(r'''
The average and the middle between lowest and highest are not the same. Why not?

<details>
<summary>Answer</summary>

For Leopoldstadt, the middle is 12.1 °C and the average 11.2 °C. The average counts every one of the 30
days. The middle only looks at two moments, the coldest and the warmest of the whole month, and one warm
afternoon can pull it up. With the Penzing sensor you get 39.0 °C on 4 November: no November afternoon
in Vienna is that warm, so the sun must have been shining on the sensor. When you report a period, give
the average and say what the extremes were.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 6: see it, and compare with the other districts

Run the cell. The line is the daily average; the pale bar of each day reaches from its lowest to its
highest reading. Hover to read the values.
''')

nb.code(r'''
# the daily average as a line, a pale bar per day from lowest to highest
def plot_period(table, title):
    fig = go.Figure([
        go.Bar(x=table["begin"], y=table["highest"] - table["lowest"], base=table["lowest"],   # bar from lowest up to highest
               marker_color="rgba(76,120,168,0.25)", name="lowest to highest",
               customdata=table[["lowest", "highest"]], hovertemplate="lowest %{customdata[0]:.1f} °C, highest %{customdata[1]:.1f} °C<extra></extra>"),
        go.Scatter(x=table["begin"], y=[None if pd.isna(v) else v for v in table["temperature"]],   # None leaves a gap
                   mode="lines+markers",                                                      # the daily average
                   line=dict(color="#4c78a8", width=2), marker=dict(size=6), name="daily average",
                   hovertemplate="average %{y:.1f} °C<extra></extra>")])
    fig.update_layout(height=400, title=title, yaxis_title="temperature [°C]", hovermode="x unified",
                      legend=dict(orientation="h", y=-0.15))
    fig.show()                                        # draw it


plot_period(df, f"{my_district}, 17 October to 15 November 2025")
''', hidden=True)

nb.md(r'''
Now the same 30 days for all five sensors. The cell asks each of them once, so it takes a few seconds.
''')

nb.code(r'''
# ask all five sensors for the same 30 days, and draw their daily averages together
colors = ["#4c78a8", "#f58518", "#54a24b", "#e45756", "#72b7b2"]   # one fixed colour per sensor
fig, means = go.Figure(), {}
for s, color in zip(sensors, colors):                 # one request per sensor
    answer = get_json(BASE + s["device"] + "/sensors/temperature/measurements", params)
    if answer is None:                                # this one did not work, skip it
        continue
    t = pd.DataFrame(answer)                          # as a table
    t["begin"] = pd.to_datetime(t["begin"])           # text to time
    means[s["district"]] = t["v"].mean()              # the average of the period
    mine = s["district"] == my_district               # draw your own sensor thicker
    fig.add_trace(go.Scatter(x=t["begin"], y=t["v"], mode="lines", name=s["district"],
                             line=dict(color=color, width=4 if mine else 1.5),
                             hovertemplate=s["district"] + " %{y:.1f} °C<extra></extra>"))
fig.update_layout(height=420, title="daily averages, 17 October to 15 November 2025 (yours is thick)",
                  yaxis_title="temperature [°C]", hovermode="x unified")
fig.show()                                            # draw it
print()
for district, m in sorted(means.items(), key=lambda kv: -kv[1]):   # warmest first
    print(f"{district:<13} average {m:5.1f} °C")
''', hidden=True)

nb.md(r'''
Was your district the warmest? How big is the gap between the warmest and the coldest sensor, and what
could cause it?

<details>
<summary>Answer</summary>

The five lines move together: cold and warm days come to the whole city at once. Over the month,
Penzing averaged 11.9 °C and Donaustadt 9.3 °C, 2.6 degrees apart; Leopoldstadt and Favoriten were both
at 11.2 °C. Donaustadt lies at the edge of the city, with fields around, and a dense city keeps warmer at
night. But each line is one cheap sensor on one balcony: sun, a warm wall or a sheltered corner can
matter as much as the district. Five sensors cannot tell which it was.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 7: change the interval

`P1D` gives one value per day. In `PT12H`, the **T** says "a time follows", and `12H` is twelve hours.
Other periods that work: `PT1H` (hours), `PT6H`, `P1M` (months) and `P1Y` (years); `P1W` for weeks does
not, the server answers 400. Sixty half days are the same thirty days, so the next cell asks for
`R60/2025-10-17T00:00/PT12H`. Run it.
''')

nb.code(r'''
params12 = {"interval": "R60/2025-10-17T00:00/PT12H", # 60 half days from 17 October 2025
            "agg": "MEAN"}                            # each value is the average of its half day
result12 = get_json(url, params12)                    # ask
half = pd.DataFrame(result12).rename(columns={"v": "temperature", "hi": "highest", "lo": "lowest"})   # table
half["begin"] = pd.to_datetime(half["begin"])         # text to time
print(f"daily:     {len(df)} values, highest {df['highest'].max():.1f} °C, average {df['temperature'].mean():.2f} °C")
print(f"half-day: {len(half)} values, highest {half['highest'].max():.1f} °C, average {half['temperature'].mean():.2f} °C")
afternoon_warmer = (half["temperature"][1::2].values > half["temperature"][0::2].values).sum()   # noon-midnight vs midnight-noon
print(f"on {afternoon_warmer} of {len(df)} days the second half (noon to midnight) was warmer than the first")
''')

nb.code(r'''
# the half-day values on top of the daily ones
fig = go.Figure([
    go.Scatter(x=half["begin"], y=half["temperature"], mode="lines", name="every 12 hours (PT12H)",
               line=dict(color="#f58518", width=1.5), hovertemplate="%{x|%d %b %H:%M} %{y:.1f} °C<extra></extra>"),
    go.Scatter(x=df["begin"], y=df["temperature"], mode="lines+markers", name="every day (P1D)",
               line=dict(color="#4c78a8", width=2), marker=dict(size=6),
               hovertemplate="%{x|%d %b} %{y:.1f} °C<extra></extra>")])
fig.update_layout(height=400, title=f"{my_district}: the same month, cut into days and into half days",
                  yaxis_title="temperature [°C]", legend=dict(orientation="h", y=-0.15))
fig.show()                                            # draw it
''', hidden=True)

nb.md(r'''
Why does the half-day line zigzag? And why did the highest reading not change at all?

<details>
<summary>Answer</summary>

Each day is cut at midnight and at noon (in the `+01:00` time of the answer). The first half holds the night and the cold early morning, the
second half the warm afternoon, so the line goes down, up, down, up. In Leopoldstadt the afternoon half
was warmer on 27 of the 30 days; on the other three the afternoon was cooler, perhaps because colder air arrived. The highest
reading is the warmest single moment, 19.3 °C, and that moment is the same however you cut the month.
The average hardly moves either (11.18 against 11.19 °C), because the same readings go into it.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 8: the same reading in XML

Before JSON, programs on the web mostly exchanged **XML** (eXtensible Markup Language). The reading from
step 1, in XML:

    <reading sensor="balcony">
      <time>2025-10-17T08:00</time>
      <temperature unit="°C">11.6</temperature>
      <working>true</working>
    </reading>

Every value sits between an opening tag `<temperature>` and a closing tag `</temperature>`. Extra details
like `unit="°C"` are **attributes** inside the opening tag. Python reads it with `xml.etree`.
''')

nb.code(r'''
import xml.etree.ElementTree as ET                    # Python's XML reader

xml_text = """<reading sensor="balcony">
  <time>2025-10-17T08:00</time>
  <temperature unit="°C">11.6</temperature>
  <working>true</working>
</reading>"""
root = ET.fromstring(xml_text)                        # read the XML; root is the outer <reading> tag

value = root.find("temperature").text                 # the text between <temperature> and </temperature>
print("value:", repr(value), "is", type(value).__name__)   # it comes back as text
print("as a number:", float(value))                   # we must turn it into a number ourselves
print("unit:", root.find("temperature").get("unit"))  # an attribute, read with get
print("sensor:", root.get("sensor"))                  # an attribute of the outer tag

same_json = '{"sensor": "balcony", "time": "2025-10-17T08:00", "temperature": 11.6, "unit": "°C", "working": true}'
print(f"\nthe same reading: {len(xml_text)} characters in XML, {len(same_json)} in JSON")
''')

nb.md(r'''
What differences between the two versions do you see? Why might they have made JSON the favourite for data on the web?

<details>
<summary>Answer</summary>

JSON is shorter: 101 characters against 139 here, because XML writes `time`, `temperature` and
`working` twice, in the opening and the closing tag. JSON knows numbers, `true`/`false`, lists and `null`,
while XML hands everything over as text: `'11.6'` had to become a number with `float()`. And JSON looks
exactly like the way JavaScript, the language of the browser, writes objects; every browser has a reader
for it built in, as Python has `json.loads`.

XML has not gone away, though. You meet it in gbXML (building energy models), SVG drawings, KML in Google
Earth and SensorML (descriptions of sensors), and every `.docx` file is a zip of XML files.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Tests

Run this cell before you submit. It checks your `summarize` on three made-up days, and recomputes your
month from the raw JSON, without pandas.
''')

nb.code(r'''
probe = pd.DataFrame({"temperature": [10.0, 12.0, 14.0], "lowest": [8.0, 9.0, 11.0], "highest": [13.0, 15.0, 16.0]})
assert summarize(probe) == (12.0, 8.0, 16.0), f"three days from step 5 should give (12, 8, 16), not {summarize(probe)}"
values = [day["v"] for day in result if day["v"] is not None]   # the daily averages, straight from the JSON
assert abs(average - sum(values) / len(values)) < 1e-9, "your average does not match the JSON"
assert coldest == min(day["lo"] for day in result if day["lo"] is not None), "lowest does not match the JSON"
assert warmest == max(day["hi"] for day in result if day["hi"] is not None), "highest does not match the JSON"
assert len(result) == 30 and len(result12) == 60, "R30 with P1D gives 30 values, R60 with PT12H 60"
assert pd.api.types.is_datetime64_any_dtype(df["begin"]), "begin should be a time, see step 4"
assert float(root.find("temperature").text) == json.loads(same_json)["temperature"], "XML and JSON disagree"
print(f"✓ All green. Your month in {my_district}: average {average:.1f} °C, from {coldest:.1f} to {warmest:.1f} °C.")
''')

nb.md(r'''
## Where you stand now

You can read JSON: objects with keys and values, lists, and objects inside objects, and you can pick any
value out of them. You asked a real sensor through its API, chose the period with an ISO 8601 interval,
turned the answer into a table with real times, and reported a period with its average, lowest and
highest value. And you know XML when you see it.

Next session: databases, where tables like today's are kept, asked and joined.

---

### Terms to learn

''' + TERMS_FOOTER + r'''

| term | in one sentence |
|---|---|
| JSON | text that holds data as objects in curly braces, lists in square brackets, text, numbers, true, false and null |
| key and value | the name of a field and what is in it; in Python you pick a value with `data["key"]` |
| nesting | objects and lists inside objects, reached step by step: `data["location"]["lat"]` |
| API | a web address that answers programs with data, usually JSON, instead of pages for people |
| ISO 8601 interval | a period written as text, like `R30/2025-10-17T00:00/P1D`: 30 days from 17 October 2025 |
| XML | an older text format with values between opening and closing tags, still used in gbXML and SVG |
''')

# ---------------------------------------------------------------------------------------------
nb.md(homework_header(
    "a time you remember, measured",
    """In class you fetched 30 days of temperatures and reported them with average, lowest and highest.
Now do it for a time that matters to you: your last holiday (what was the weather at home while you were
away?), the week of your birthday, your exam week, the week you moved. Pick the sensor you like, write down
what you remember of the weather **before** you run the cells, then see what the sensor says.

All five sensors have data from January 2024 to 24 July 2026. Up to 120 days work.""",
    """The cells come with a complete worked example: a birthday week in March 2025 in Penzing, with a
memory that does not quite fit, and example answers under the questions. Run it once first, then replace
it with your own choice."""))

nb.code(r'''
# YOUR CHOICE: your sensor, your period, and what you remember of it
hw_district = "Penzing"                               # one of the five districts
hw_start = "2025-03-13"                               # the first day, as year-month-day
hw_days = 7                                           # how many days, 1 to 120
hw_memory = "My birthday week. I remember it as freezing: I wore my winter coat to my party on Saturday the 15th."
''')

nb.code(r'''
# check your choice, ask the sensor, and build the table; you do not need to change anything here
import re                                             # to check the shape of the date
hw_result = hw = None                                 # forget the results of an earlier run
problems = []                                         # collect what is wrong, if anything
if hw_district not in names:
    problems.append(f"hw_district must be one of: {', '.join(names)}")
first = None
if not isinstance(hw_start, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", hw_start):
    problems.append('hw_start must be a date like "2025-03-13" (year-month-day, in quotes)')
else:
    try:
        first = pd.Timestamp(hw_start)                # does the date exist?
    except ValueError:
        problems.append(f"{hw_start} is not a real date")
if not isinstance(hw_days, int) or not 1 <= hw_days <= 120:
    problems.append("hw_days must be a whole number from 1 to 120")
elif first is not None and first < pd.Timestamp("2024-01-01"):
    problems.append("start on 1 January 2024 or later; before that, some of the five sensors have no data")
elif first is not None and first + pd.Timedelta(days=hw_days - 1) > pd.Timestamp("2026-07-24"):
    problems.append("your period runs past 24 July 2026; these sensors have no data after that (see the box at the top)")
if problems:                                          # stop and say what to fix
    raise ValueError("Please fix your choice:\n- " + "\n- ".join(problems))
hw_device = sensors[names.index(hw_district)]["device"]   # the device id of your sensor
hw_params = {"interval": f"R{hw_days}/{hw_start}T00:00/P1D", "agg": "MEAN"}   # your interval
hw_result = get_json(BASE + hw_device + "/sensors/temperature/measurements", hw_params)   # ask
if hw_result is not None:
    hw = pd.DataFrame(hw_result).rename(columns={"v": "temperature", "hi": "highest", "lo": "lowest"})
    hw["begin"] = pd.to_datetime(hw["begin"])         # text to time
    with_data = int(hw["temperature"].notna().sum())  # days with data
    print(f"✓ {len(hw)} days asked for, {with_data} of them with data.")
''', hidden=True)

nb.code(r'''
assert hw is not None and hw["temperature"].notna().any(), "no data for this period; choose another"
hw_average, hw_coldest, hw_warmest = summarize(hw)    # your function from step 5
hw_warm_day = hw.loc[hw["highest"].idxmax(), "begin"] # the day of the warmest moment
hw_cold_day = hw.loc[hw["lowest"].idxmin(), "begin"]  # the day of the coldest moment
print(f"{hw_district}, {hw_days} days from {hw_start}:")
print(f"  average {hw_average:.1f} °C over the {with_data} days with data, lowest {hw_coldest:.1f} °C ({hw_cold_day:%a %d %b}), "
      f"highest {hw_warmest:.1f} °C ({hw_warm_day:%a %d %b})")
print(f"  you remembered: {hw_memory}")
''')

nb.code(r'''
# your period, drawn the same way as in class
plot_period(hw, f"{hw_district}, {hw_days} days from {hw_start}")
''', hidden=True)

nb.md(r'''
### Your answers

One to three sentences per question, about your own period.

1. **Your numbers.** Give the average, the lowest and the highest temperature of your period, with units,
   and say in everyday words what kind of weather that was.
2. **Memory against data.** Does the sensor agree with what you wrote down before? Where not, which do you
   trust more, and why?
3. **The sensor and you.** Where was the sensor, and where were you? Name one reason why its numbers might
   not be what you felt.
4. **The raw JSON.** Click the URL printed above, find the entry of the day with your highest reading in
   your browser, and copy it into your answer. Say what each of its keys means.

<details>
<summary>Example answers for the birthday-week example. Click to see what a good answer looks like.</summary>

1. Average 7.0 °C over the five days with data, lowest −1.6 °C and highest 21.0 °C, both on Wednesday
   19 March. Cold nights and mild days, a normal March week, although 21 degrees in March looks odd.
2. Only partly. Saturday the 15th averaged 6.7 °C: chilly, coat weather, but not freezing. And `c` is 0.02
   that day, so the sensor sent almost nothing and I trust that number little. The 16th and 17th have no
   data at all; the only recorded frost is the −1.6 °C on the 19th.
3. The sensor is somewhere near Linzer Straße in Penzing, probably at a window or on a balcony; my party
   was in Ottakring, next door. From −1.6 °C to 21.0 °C within one day is a huge jump; maybe the sun
   shines on the sensor in the afternoon.
4. `{"begin": "2025-03-19T00:00+01:00", "v": 7.5, "hi": 21.0, "lo": -1.6, "c": 0.331}`. `begin` is the
   start of the day, `v` the day's average, `hi` and `lo` the highest and lowest reading, and `c` drops
   towards 0 when the sensor sent almost nothing.

These fit the example only. Your answers are about your own period.

</details>

*Your text here.*
''')

nb.write("03_sensors")
