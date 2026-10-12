"""Session 2: the web, asking a machine for data."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from nbbau import Notebook, DATA_BOX, homework_header, TERMS_FOOTER, box

nb = Notebook()

nb.md(r'''
# Session 2: The web, asking a machine for data

**259.021 Fundamentals of Utilizing Data Sources** · Session 2 of 5

Every app on your phone asks machines for data all day: the next tram, tomorrow's weather, your
TISS timetable. Today you do it yourself. You take a web address apart, find the machine behind it,
ask it for something in plain Python, and then change the question and watch the answer change.
''')

nb.md(DATA_BOX.format(text='''Today the data comes live from the internet: TISS, a free weather service called
Open-Meteo that needs no account, and any page you choose. If the network is down, the cells say so
politely instead of crashing, and the weather step falls back to a saved copy in `../data/`.'''))

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 1: a web address, taken apart

A web address is called a **URL**. Here is one you know, the TISS page of this course:

    https://tiss.tuwien.ac.at/course/courseDetails.xhtml?courseNr=259021&semester=2026W#groups

It has parts, always in the same order:

| part | here | what it says |
|---|---|---|
| scheme | `https` | which language to speak with the machine (https is http, encrypted) |
| host | `tiss.tuwien.ac.at` | the name of the machine |
| port | not written, so 443 | which door of the machine to knock on (more in step 3) |
| path | `/course/courseDetails.xhtml` | which thing on that machine |
| query | `courseNr=259021` and `semester=2026W` | extra details of the question, as name=value pairs after the `?`, joined by `&` |
| fragment | `groups` | a place inside the page; your browser keeps this part to itself |

Run the cell: Python's `urllib.parse` finds the same parts.
''')

nb.code(r'''
from urllib.parse import urlsplit, parse_qsl          # Python's own tools for taking URLs apart

example_url = "https://tiss.tuwien.ac.at/course/courseDetails.xhtml?courseNr=259021&semester=2026W#groups"   # the example
parts = urlsplit(example_url)                         # split the URL into its parts
print("scheme  :", parts.scheme)                      # https
print("host    :", parts.hostname)                    # the machine's name
print("port    :", parts.port)                        # None: nobody wrote one
print("path    :", parts.path)                        # which thing on the machine
print("query   :", parse_qsl(parts.query))            # the name=value pairs, as a list
print("fragment:", parts.fragment)                    # the place inside the page
''')

nb.md(r'''
The port says `None` because nobody wrote one. Then the scheme decides: `https` means 443, `http`
means 80. The helper below does the same as the cell above, fills in that default port, and prints a
tidy table. You will use it on your own URL next.
''')

nb.code(r'''
# Helper: take a URL apart and print its parts as a small table
DEFAULT_PORTS = {"http": 80, "https": 443}            # the door used when no port is written


def port_of(parts):
    if parts.port is not None:                        # a port is written in the URL
        return parts.port, "written in the URL"
    return DEFAULT_PORTS.get(parts.scheme), f"not written, default for {parts.scheme}"


def take_apart(url):
    parts = urlsplit(url.strip())                     # split it
    port, how = port_of(parts)                        # which door, and why
    print(f"URL: {url.strip()}")
    print(f"  scheme   {parts.scheme}")
    print(f"  host     {parts.hostname}")
    print(f"  port     {port}  ({how})")
    print(f"  path     {parts.path or '/'}")
    pairs = parse_qsl(parts.query, keep_blank_values=True)   # the name=value pairs
    if pairs:
        for name, value in pairs:                     # one line per query parameter
            print(f"  query    {name} = {value}")
    else:
        print("  query    (none)")
    print(f"  fragment {parts.fragment or '(none)'}")
    return parts


def url_problem(u):
    if u is None:                                     # nothing pasted yet
        return "No URL yet. Paste one between quotes, like  my_url = \"https://...\" , and run again."
    if not isinstance(u, str):                        # a number or a list instead of text
        return "Put the URL between quotes."
    u = u.strip()                                     # ignore spaces around it
    if not u.startswith(("http://", "https://")):     # no scheme
        return "A URL starts with https:// or http://. If your address bar hid that part, add https:// in front."
    if " " in u:                                      # spaces break URLs
        return "There is a space in your URL. Copy it again straight from the address bar."
    try:
        parts = urlsplit(u)                           # split it
        parts.port                                    # a broken port like :abc fails here
    except ValueError:
        return "Python cannot read this URL (perhaps something odd after a colon). Copy it again."
    if not parts.hostname:                            # nothing after https://
        return "There is no machine name after https://. Copy the whole address."
    return None                                       # all fine


take_apart(example_url)                               # the TISS example once more
print("✓ helper ready.")
''', hidden=True)

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 2: your own URL

Open a page you use almost every day on your phone or laptop: the Wiener Linien route planner, a
weather page, a flat search, a YouTube video. Copy the whole address from the address bar (on the
phone: tap the address, then share or copy) and paste it below, between the quotes. Pick one with a `?`
in it if you can; that makes the next steps more fun.
''')

nb.code(r'''
# YOUR CHOICE: paste a URL you use often, between the quotes, instead of None
my_url = None

problem = url_problem(my_url)                         # None if your URL looks fine, else what to fix
url = example_url if problem else my_url.strip()      # the URL the next steps use
host = urlsplit(url).hostname                         # its machine name
if problem:                                           # something to fix first
    print(problem)
    print("Until then, the next steps use the TISS example.")
else:
    take_apart(url)                                   # your URL, taken apart
    print("✓ That is your URL in pieces. The next steps use it.")
''')

nb.md(r'''
Look at the query lines of your URL. Which part would you change to ask the same machine a different
question?

<details>
<summary>Answer</summary>

Usually a query parameter, the value after a `=`: a different date, a different search word, a
different station. Sometimes the path holds the question instead, like `/wiki/Karlskirche`. The host
stays: it is the same machine, you only ask it something else. If your URL has no query at all, the
path is all the machine gets.

</details>
''')


# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 3: from a name to a number

Machines on the internet do not find each other by name, but by number, the **IP address**. It is
like a phone number. The common kind (IPv4) is four numbers from 0 to 255 with dots, for example
`128.130.32.110`; the newer IPv6 numbers are longer. Turning a name into that number is the job of the
**DNS**, the phone book of the internet. Your phone asks it whenever it meets a name it has not
looked up recently. Run the cell and ask it yourself.
''')

nb.code(r'''
import socket                                         # Python's tools for network connections


def look_up(name):
    try:
        number = socket.gethostbyname(name)           # ask the DNS for the IP address
        print(f"✓ {name}  →  {number}")
        return number
    except socket.gaierror:                           # the DNS does not know the name, or no network
        print(f"Could not look up {name}. Either the name is misspelt or there is no network right now.")
    except (TypeError, UnicodeError):                 # not a usable name at all
        print(f"{name!r} is not a machine name.")


look_up("tiss.tuwien.ac.at")                          # the TISS machine
look_up(host)                                         # the machine behind your URL
look_up("gabriel-wurzer.github.io")                   # where the course's web apps live
''')

nb.md(r'''
One machine can offer several services, each behind its own door, the **port**. The number tells
which service you want:

| port | service |
|---|---|
| 21 | ftp, copying files (old) |
| 22 | ssh, a remote terminal |
| 25 | smtp, sending e-mail |
| 80 | http, web pages |
| 443 | https, web pages, encrypted |

You almost never see a port in a URL because the default does the job. Where you do see one is a
server that runs on an unusual door, like Jupyter on your own laptop: `http://localhost:8888/lab`.

Your URL from step 2 shows no port (most likely). Which door does your browser knock on, and how does
it know?

<details>
<summary>Answer</summary>

443, because the scheme is `https`. With `http` it would be 80. If a port is written, like `:8888`,
that one wins. The helper's port line says exactly this.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 4: asking, with HTTP GET

Now you know the machine and the door. What goes through the door is a language called **HTTP**; in
its version 1.1, the one shown here, it is plain text. The most common sentence is **GET**: "give me this thing". The teddy of session 1 came with
one GET. Years ago we typed such a request by hand into a program called telnet. Here is the TISS request, slightly shortened, the way it travels
inside the encryption of https:

    GET /course/courseDetails.xhtml?courseNr=259021&semester=2026W HTTP/1.1
    Host: tiss.tuwien.ac.at
    Accept: */*

Path and query go in the first line; the fragment `#groups` does not travel at all. The machine answers
with a **status code**, a few **headers** (lines of information about the answer) and then the content.
The status code is a three-digit number:

| code | meaning |
|---|---|
| 200 | OK, here it is |
| 301, 302 | moved, look over there (the program follows by itself) |
| 400 | I do not understand your question |
| 403 | I will not give this to you |
| 404 | not found |
| 500, 503 | the server has a problem |

Run the next two cells. The first prepares a helper, the second asks the machine behind your URL.
''')

nb.code(r'''
# Helper: fetch a URL politely, and say in plain words what went wrong if something does
import requests                                       # the usual Python package for HTTP

HEADERS = {"User-Agent": "TU Wien course notebook (python requests)"}   # say who is asking
MEANINGS = {200: "OK", 301: "moved permanently", 302: "moved for now", 304: "not modified",
            400: "bad request", 401: "login needed", 403: "forbidden", 404: "not found",
            429: "too many requests", 500: "server error", 503: "server unavailable"}


def fetch(url, params=None):
    try:
        return requests.get(url, params=params, headers=HEADERS, timeout=10)   # ask; give up after 10 s of silence
    except requests.exceptions.Timeout:
        print("The machine did not answer within 10 seconds. Try again, or another URL.")
    except requests.exceptions.ConnectionError:
        print("No connection: the name is unknown, the machine did not let us in, or there is no network. "
              "Try again in a moment.")
    except requests.exceptions.RequestException as error:
        print(f"That did not work: {type(error).__name__}. Check that the URL starts with https://.")


def report(response):
    size = len(response.content)                      # how many bytes came back
    print(f"status code : {response.status_code} ({MEANINGS.get(response.status_code, 'see the table')})")
    print(f"content type: {response.headers.get('Content-Type', 'not given')}")
    print(f"size        : {size:,} bytes, about {size / 1000:.0f} kB")
    if response.history:                              # there were redirects on the way
        print(f"redirected  : {' → '.join(str(r.status_code) for r in response.history)}, ended at {response.url}")


print("✓ fetch and report ready.")
''', hidden=True)

nb.code(r'''
response = fetch(url)                                 # GET the URL from step 2 (or the TISS example)
if response is not None:                              # only if something came back
    report(response)                                  # status code, content type, size
    request = response.request                        # the request that requests actually sent
    print("\n--- what was sent (the request, as text):")
    print(f"{request.method} {request.path_url} HTTP/1.1")   # first line: verb, path and query
    print(f"Host: {urlsplit(response.url).netloc}")          # which machine (and port, if written)
    for name in ("User-Agent", "Accept"):             # two of the headers we sent
        print(f"{name}: {request.headers.get(name)}")
    print("\n--- what came back (status line and three headers):")
    print(f"HTTP/1.1 {response.status_code} {response.reason}")
    for name in ("Content-Type", "Date", "Server"):   # three of the headers we got
        print(f"{name}: {response.headers.get(name, '(not sent)')}")
''')

nb.md(r'''
Is the content type `text/html`? Then the machine sent a page meant for people, which your browser
would draw. Now ask TISS for a page that does not exist.
''')

nb.code(r'''
missing = fetch("https://tiss.tuwien.ac.at/this-page-does-not-exist")   # a path nobody made
if missing is not None:
    report(missing)                                   # look at the status code
''')

nb.md(r'''
The machine answered, and it even sent a page, but the status code says something is wrong. Why is
the status code more useful to a program than the page that came with it?

<details>
<summary>Answer</summary>

The status code was 404, not found. The page that came with it is for people: a friendly error page,
made of HTML. A program cannot read "sorry, we could not find that" reliably, but it can check one
number. That is why we look at the status code first, before we touch the content.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 5: your part, changing the question

Query parameters are the knobs of a question. Open-Meteo is a free weather service that answers
with numbers instead of a page. You give it a place (latitude, longitude) and how many days you want,
as query parameters. In Python you write such name-value pairs as a **dictionary**, with curly braces:

    room = {"name": "Seminar room", "seats": 24, "floor": 3}

`requests` turns a dictionary into the `?name=value&...` part of the URL for you: `{"forecast_days": 3}`
becomes `?forecast_days=3`. In the cell below, one line is yours.
''')

nb.code(r'''
WEATHER = "https://api.open-meteo.com/v1/forecast"    # scheme, host and path of the weather service

# YOUR TURN: replace the line "raise ..." with one line:
#   params = {"latitude": 48.2082, "longitude": 16.3738, "forecast_days": 3}
raise NotImplementedError("replace this line with the line described above")

params["hourly"] = "temperature_2m"                   # also ask for the temperature of every hour
params["timezone"] = "Europe/Vienna"                  # and give the times in Vienna time
weather = fetch(WEATHER, params=params)               # GET, with the dictionary as query
if weather is not None:
    report(weather)                                   # status code, content type, size
    print("the URL requests built:", weather.url)     # the dictionary, turned into a query
''', solution=r'''
WEATHER = "https://api.open-meteo.com/v1/forecast"    # scheme, host and path of the weather service

params = {"latitude": 48.2082, "longitude": 16.3738, "forecast_days": 3}   # place and number of days

params["hourly"] = "temperature_2m"                   # also ask for the temperature of every hour
params["timezone"] = "Europe/Vienna"                  # and give the times in Vienna time
weather = fetch(WEATHER, params=params)               # GET, with the dictionary as query
if weather is not None:
    report(weather)                                   # status code, content type, size
    print("the URL requests built:", weather.url)     # the dictionary, turned into a query
''')

nb.md(r'''
<details>
<summary>Answer</summary>

    params = {"latitude": 48.2082, "longitude": 16.3738, "forecast_days": 3}

</details>

The content type is `application/json`: data for programs, not a page for people. You will read JSON
properly next session; here the plot reads it for you. If there is no network, it shows the saved copy.
''')

nb.code(r'''
# plot the hourly temperature; with no answer from the network, use the saved copy
import json                                           # to read the saved copy
import plotly.express as px                           # quick interactive plots

data, source = None, ""                               # nothing yet
if weather is not None and weather.status_code == 200:
    try:
        data, source = weather.json(), "live from Open-Meteo"        # the live answer
    except ValueError:                                # the answer was not JSON after all
        print("The weather service sent something odd. Using the saved copy instead.")
elif weather is not None and weather.status_code == 400:   # the server did not like the question
    print("The weather service said 400, bad request. Check your params: use 1 to 16 for forecast_days.")
elif weather is not None:                             # the service has a problem right now
    print(f"The weather service said {weather.status_code} ({MEANINGS.get(weather.status_code, '?')}). "
          "Using the saved copy instead.")
if data is None and (weather is None or weather.status_code != 400):   # no network or no usable answer
    with open("../data/weather_vienna_sample.json", encoding="utf-8") as f:   # the saved copy
        data, source = json.load(f), "saved copy from 12 October 2026, Vienna, 3 days"
if data is not None:
    hourly = data["hourly"]                           # the part with the hourly values
    fig = px.line(x=hourly["time"], y=hourly["temperature_2m"], height=380,
                  labels={"x": "time", "y": "temperature [°C]"},
                  title=f"{len(hourly['time'])} hours at latitude {data['latitude']:.2f}, "
                        f"longitude {data['longitude']:.2f} ({source})")
    fig.show()                                        # draw it
    print(f"✓ {len(hourly['time'])} hourly values.")
''', hidden=True)

nb.md(r'''
Now turn the knobs. In your line above, change `"forecast_days": 3` to `7`, and run the two cells
again. Then put in the latitude and longitude of your own home (in Google Maps, right-click your
house; the first line shows the two numbers). Then try `"forecast_days": 30`. When you are done, set
`forecast_days` back to a number from 1 to 16, so the notebook runs through for the Tests.

What did each change do to the URL, the number of hours and the status code?

<details>
<summary>Answer</summary>

With 7 days the URL says `forecast_days=7`, and 168 values come back instead of 72 (7 × 24 instead of
3 × 24). With your home, the latitude and longitude in the URL change and the title shows the grid
point the service picked near you. With 30 the server answers 400, bad request: it only forecasts up to
16 days. Same machine, same path, a different question each time. Did you notice `Europe%2FVienna` in
the URL? Characters with a special meaning in URLs get written as codes when `requests` builds a query:
`/` becomes `%2F`, a space becomes `+`.

</details>

Next session the same trick fetches days of temperatures from a real street sensor in Vienna.
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 6: what a web server does

A **web server** is a program that waits behind port 80 or 443 and answers GET requests. In the
simplest case it just hands out files from a folder: the teddy lived in the folder
`/graphics/classes/6.837/F03/models/` on MIT's web server. If the path ends in a folder, it sends the file
called `index.html` in that folder (that is how most servers are set up, GitHub's too). The flashcard app of your other course is exactly that. Run the
cell: three URLs, one file.
''')

nb.code(r'''
app = "https://gabriel-wurzer.github.io/data2/webapps/flashcards"   # a folder on GitHub's web server
for address in (app + "/index.html", app + "/", app):  # the file, the folder, the folder without /
    answer = fetch(address)                           # GET each
    if answer is not None:
        moved = " after " + ", ".join(str(r.status_code) for r in answer.history) if answer.history else ""
        print(f"{address:70s} → {answer.status_code}{moved}, {len(answer.content):,} bytes")
''')

nb.md(r'''
<details>
<summary>What do the three lines show?</summary>

The same number of bytes three times: almost certainly the same file (a size alone cannot prove it,
but here nothing else makes sense). Asked for the folder, the server sent its
`index.html`. Asked for the folder without the final `/`, it first answered 301, "moved, look at the
folder with a /", and `requests` followed that by itself.

</details>
''')

nb.md(box("📱 The occupancy sensor", r'''Open the occupancy sensor on your phone: [gabriel-wurzer.github.io/data/webapps/occupancy-sensor](https://gabriel-wurzer.github.io/data/webapps/occupancy-sensor/). It counts
people walking through a door, using the phone camera. Behind the link there is nothing but an
`index.html` on GitHub's web server, sent to you over HTTPS. Inside that file is a small program
(JavaScript) that your browser runs: it asks your permission for the camera, then watches the picture and
counts, right there on the phone. For a page from the internet, browsers only allow the camera
if it came over HTTPS, which is why the address starts with `https`.

Stand at the door of the lab and count us in after the break. The app can download its events as a
small table (time, in or out, how many are in the room). Keep that file: in session 5 its data comes back.'''))

nb.md(r'''
The app counts people. Where does the counting happen, on GitHub's server or on your phone?

<details>
<summary>Answer</summary>

On your phone. The web server did one thing: it answered a GET with a file. Everything after that,
camera, counting, the table, runs in your browser. This app sends no picture anywhere.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Step 7: sending instead of asking, HTTP POST

GET asks for something; what it asks fits into the URL, and the URL shows up in the address bar,
in the browser history and in the server's access records. **POST** sends something: the data
travels in the body of the request, below the headers, as with a login form, an upload, or a sensor that
reports its reading to a server. Here is what a sensor's POST looks like as text (the 32 is the
number of characters in the body):

    POST /readings HTTP/1.1
    Host: sensors.example.org
    Content-Type: application/json
    Content-Length: 32

    {"room": "PC5", "occupancy": 17}

Nothing to run here. Why would you not put a password into the query of a GET?

<details>
<summary>Answer</summary>

Because the query is part of the URL, and URLs end up everywhere: in the address bar, in the browser
history, in the server's access records, in a screenshot. The body of a POST is not part of the URL, so
it does not show up in the address bar or the history.

</details>
''')

# ---------------------------------------------------------------------------------------------
nb.md(r'''
## Tests

Run this cell before you submit. It takes URLs apart and builds a query from your dictionary, without
the network, so it works offline too.
''')

nb.code(r'''
from requests import Request                          # to build a URL without sending it

test = urlsplit("http://localhost:8888/lab?theme=dark#top")   # a URL with every part
assert (test.scheme, test.hostname, test.port, test.path) == ("http", "localhost", 8888, "/lab"), "parts wrong"
assert dict(parse_qsl(test.query)) == {"theme": "dark"} and test.fragment == "top", "query or fragment wrong"
assert port_of(urlsplit(example_url)) == (443, "not written, default for https"), "default port of https wrong"
assert port_of(urlsplit("http://example.org/"))[0] == 80, "default port of http wrong"

assert isinstance(params, dict), "params should be a dictionary, with curly braces"
for name in ("latitude", "longitude", "forecast_days"):   # the three entries of your line
    assert name in params, f"params has no {name!r}; check the spelling and the quotes"
assert 1 <= params["forecast_days"] <= 16, "set forecast_days back to a number from 1 to 16 (step 5)"
assert -90 <= params["latitude"] <= 90 and -180 <= params["longitude"] <= 180, "latitude or longitude out of range"
built = Request("GET", WEATHER, params=params).prepare().url   # the URL requests builds from your params
assert built.startswith(WEATHER + "?"), "the query should follow the path after a ?"
back = dict(parse_qsl(urlsplit(built).query))         # take the built URL apart again
assert back["forecast_days"] == str(params["forecast_days"]), "forecast_days did not make it into the URL"
assert back["timezone"] == "Europe/Vienna" and "Europe%2FVienna" in built, "the / in the timezone should be %2F"
print(f"✓ All green. Your dictionary becomes  ...?{urlsplit(built).query}")
''')

nb.md(r'''
## Where you stand now

You can take any URL apart, know that a name becomes a number before anything happens, and can ask a
machine for something yourself, in Python, and read whether it worked from one number. You changed a
question by turning a query parameter, and you know that a web app on your phone is, at first, just a
file a server handed out.

Next session: the answer of a sensor, in JSON, read properly into a table.

---

### Terms to learn

''' + TERMS_FOOTER + r'''

| term | in one sentence |
|---|---|
| URL | a web address: scheme, host, port, path, query and fragment, always in that order |
| IP address and DNS | the number of a machine on the internet, and the phone book that turns names into these numbers |
| port | the door on a machine that picks the service: 80 for http, 443 for https |
| HTTP GET and POST | GET asks for something named in the URL; POST sends data in the body |
| status code | the three-digit verdict of every answer: 200 OK, 404 not found, 400 bad question |
| query parameter | a name=value pair after the ? of a URL that changes the question |
''')

# ---------------------------------------------------------------------------------------------
nb.md(homework_header(
    "three URLs from your day",
    """In class you took one URL apart, asked its machine for it, and changed a query parameter of the
weather service. Now do it with your own day: collect three URLs you actually used this week (your URL
from step 2 can be one of them), take them apart, fetch one of them, and change one of its query
parameters. So at least one of the three needs a `?` with parameters; a search on almost any site
gives you one.

Ideas: the Wiener Linien route home, a flat or bike search on willhaben, a YouTube video at a certain
minute, a Wikipedia search, a shop with a filter, the weather for your holiday town. Copy them straight
from the address bar; long, ugly URLs are the interesting ones. If a site answers 403 because it does
not talk to programs, that is a result too: report it, or fetch another of your three. Don't spend more
than a few minutes on any one site. And if there is no network at all when you run it, say so in your
answers; that is not your fault.""",
    """The cells come with a complete worked example: a flat search, a video and a Wikipedia search, copied
as they were, tracking junk included, and example answers under the questions. Run it once first, then
replace it with your own URLs."""))

nb.code(r'''
# YOUR CHOICE: three URLs from your own week, copied from the address bar, each between quotes
my_urls = [
    "https://www.willhaben.at/iad/immobilien/mietwohnungen/wien?rows=30&PRICE_TO=900&sort=1&utm_source=newsletter&utm_medium=email",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s&si=Xk3fPq7rLm2Wn8Zt",
    "https://de.wikipedia.org/w/index.php?search=Karlskirche&title=Spezial%3ASuche&ns0=1",
]

# YOUR CHOICE: which of the three to fetch (1, 2 or 3), and the same URL with one query parameter changed
fetch_number = 3
changed_url = "https://de.wikipedia.org/w/index.php?search=Stephansdom&title=Spezial%3ASuche&ns0=1"
''')

nb.code(r'''
# checks your choices and finds the parameter you changed; you do not need to change anything here
from urllib.parse import parse_qs                     # like parse_qsl, but name -> list of values
assert isinstance(my_urls, list) and len(my_urls) == 3, "my_urls needs exactly three URLs, in square brackets"
for u in my_urls + [changed_url]:                     # every URL through the check from step 2
    problem = url_problem(u)                          # None if fine, else what to fix
    assert problem is None, f"{problem}  This one: {u!r}"
assert fetch_number in (1, 2, 3), "fetch_number is 1, 2 or 3"
chosen = my_urls[fetch_number - 1].strip()            # Python counts from 0, you count from 1
before = parse_qs(urlsplit(chosen).query, keep_blank_values=True)       # its parameters, name -> values
after = parse_qs(urlsplit(changed_url).query, keep_blank_values=True)   # those of the changed URL
assert before, "the URL you fetch needs a ? with at least one parameter, so you can change one"
diff = [n for n in sorted(set(before) | set(after)) if before.get(n) != after.get(n)]   # what differs
assert diff, "changed_url is the same as the one you fetch; change one value after a ="
if len(diff) > 1:
    print(f"Note: more than one parameter differs ({', '.join(diff)}). One is enough, but fine.")
for n in diff:
    old, new = ", ".join(before.get(n, ["(not there)"])), ", ".join(after.get(n, ["(gone)"]))   # as text
    print(f"✓ you changed {n}: {old}  →  {new}")
''', hidden=True)

nb.code(r'''
for number, u in enumerate(my_urls, start=1):         # your three URLs, one after the other
    print(f"--- URL {number}")
    take_apart(u)                                     # the helper from step 1
''')

nb.code(r'''
results = {}                                          # what came back, original and changed
for label, u in (("original", chosen), ("changed", changed_url.strip())):
    print(f"--- {label}: {u}")
    answer = fetch(u)                                 # GET it
    if answer is not None:
        report(answer)                                # status code, content type, size
        results[label] = answer
    print()
''')

nb.code(r'''
# the two answers side by side: size in kB, status code on the bar
labels = [k for k in ("original", "changed") if k in results]
if labels:
    fig = px.bar(x=labels, y=[len(results[k].content) / 1000 for k in labels], height=360,
                 text=[f"status {results[k].status_code}" for k in labels],
                 labels={"x": "", "y": "size of the answer [kB]"},
                 title=f"what changing {', '.join(diff)} did to the answer")
    fig.show()                                        # draw it
else:
    print("Nothing came back, so there is nothing to plot. Check your network and run the cell above again.")
''', hidden=True)

nb.md(r'''
### Your answers

One to three sentences per question, about your own URLs.

1. **Parameters.** Which of your three URLs has the most query parameters? Pick two of them and guess
   what they tell the server.
2. **What came back.** Status code, content type and size of the one you fetched. A page for people or
   data for programs? Was there a redirect, and is the size about what you expected?
3. **One knob turned.** What did your change do: a different answer, the same answer, an error? How can
   you tell from status code, size and final URL?
4. **A program instead of you.** Which of your URLs would you let a program fetch every morning, which
   parameter would it change each day, and what would you want from the answer?

<details>
<summary>Example answers for the worked example. Click to see what a good answer looks like.</summary>

1. The willhaben search has five: `rows=30` is probably how many ads per page and `PRICE_TO=900` the
   highest rent. `utm_source` and `utm_medium` say I came from the newsletter e-mail; they are for
   willhaben's statistics, the page would be the same without them.
2. Wikipedia answered 200 with `text/html`, about 73 kB, a page for people. It went through a 302
   first: the search found a page with that exact name and sent me straight to `/wiki/Karlskirche`.
   That turned out to be a list of all the churches called Karlskirche, not the one at Karlsplatz,
   which explains why it is small.
3. With `search=Stephansdom` I got 200 again, but about 876 kB, twelve times as much, and the final URL
   ended in `/wiki/Stephansdom`: a real article this time. So it answered a different question. Same
   size and same URL would have made me suspect the server ignored my change, though I couldn't be
   sure from that alone.
4. The willhaben search, with `PRICE_TO` fixed and the program checking every morning for new ads under
   900 €. I would only want the new ones, not the whole page of 30 ads every time, which is probably
   why such sites offer alerts instead.

These fit the example only, and the sizes were measured on 12 October 2026; they change when the
pages change. Your answers are about your own URLs.

</details>

*Your text here.*
''')

nb.write("02_web")
