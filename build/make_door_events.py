"""Sample log of one classroom door, as the occupancy-sensor web app would write it.

Friday lecture 09:00 to 11:00, 20 students plus the lecturer. The sensor makes three mistakes:
two students walking in side by side are counted once, someone loitering in the doorway in the
break is counted as an extra "out", and one dithering student is counted "in" twice. Net -1, so
after everyone has left the occupancy ends at -1, the only implausible value in the file.
"""
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(16)
day = datetime(2026, 10, 16)
OFFSET = "+02:00"                                        # Vienna, summer time until 25 October
out_path = Path(__file__).resolve().parent.parent / "data" / "door_events_sample.csv"


def at(hm, spread=0):
    h, m = map(int, hm.split(":"))
    return day + timedelta(hours=h, minutes=m, seconds=random.uniform(0, spread * 60))


events = []                                              # (time, event)

# lecturer and 20 students arrive, mostly 08:50 to 09:05, three late
events.append((at("08:43", 2), "in"))
arrivals = sorted(at("08:50", 15) for _ in range(17)) + [at("09:07", 3), at("09:13", 4), at("09:21", 3)]
pair = 6                                                 # this one walks in next to the one before
arrivals[pair] = arrivals[pair - 1] + timedelta(seconds=1)
events += [(t, "in") for i, t in enumerate(arrivals) if i != pair]   # miscount 1: pair seen as one

# one student out to the toilet and back
t = at("09:26", 2)
events += [(t, "out"), (t + timedelta(minutes=4, seconds=random.randint(0, 50)), "in")]

# break: 13 leave, 11 come back, two go home
leaving = sorted(at("09:45", 5) for _ in range(13))
events += [(t, "out") for t in leaving]
returning = sorted(at("09:55", 7) for _ in range(11))
events += [(t, "in") for t in returning]
events.append((at("09:51", 1), "out"))                   # miscount 2: someone standing in the door
events.append((returning[5] + timedelta(seconds=3), "in"))   # miscount 3: one returner dithers, counted twice

# end: everyone leaves 11:00 to 11:04, lecturer last
true_after_break = 21 - 13 + 11
events += [(t, "out") for t in sorted(at("11:00", 3) for _ in range(true_after_break - 1))]
events.append((at("11:04", 1), "out"))

events.sort()
for i in range(1, len(events)):                          # the sensor needs a moment between two passages
    if events[i][0] - events[i - 1][0] < timedelta(seconds=2):
        events[i] = (events[i - 1][0] + timedelta(seconds=2), events[i][1])
occ, lines = 0, ["time,event,occupancy"]
for t, e in events:
    occ += 1 if e == "in" else -1
    lines.append(f"{t:%Y-%m-%dT%H:%M:%S}{OFFSET},{e},{occ}")
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"{len(events)} events, max occupancy {max(int(l.rsplit(',', 1)[1]) for l in lines[1:])}, final {occ} -> {out_path}")
