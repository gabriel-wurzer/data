"""Writes vienna_sensors.json (five luftdaten-info sensors) and sensor_fallback.json (saved API answers,
keyed by the full request URL) for session 3. Device ids checked against api.sensoto.io on 12.10.2026:
all five have daily temperature from January 2024 to 24 July 2026 (network-wide gap 25 July to 8 October 2026)."""
import json
from pathlib import Path
import requests

HERE = Path(__file__).parent
BASE = "https://api.sensoto.io/v1/organizations/open/networks/luftdaten-info/devices/"

sensors = [
    {"district": "Leopoldstadt", "district_number": 2, "near": "Untere Donaustraße", "device": "19330-u2edkcj6uj4", "model": "DHT22"},
    {"district": "Favoriten", "district_number": 10, "near": "Rotenhofgasse", "device": "70488-u2edh9b3bsk", "model": "BME280"},
    {"district": "Penzing", "district_number": 14, "near": "Linzer Straße", "device": "48206-u2ed4nbjj2n", "model": "DHT22"},
    {"district": "Floridsdorf", "district_number": 21, "near": "Wolfgang-Riese-Gasse", "device": "77803-u2edt8wps66", "model": "DHT22"},
    {"district": "Donaustadt", "district_number": 22, "near": "Klara-Blum-Gasse", "device": "39321-u2ef203xn64", "model": "DHT22"},
]
for s in sensors:
    lon, lat = requests.get(BASE + s["device"], timeout=60).json()["geometry"]["coordinates"]
    s["location"] = {"lat": round(lat, 4), "lon": round(lon, 4)}

info = {"network": "luftdaten-info", "source": "sensor.community, served by api.sensoto.io",
        "measures": "air temperature", "unit": "°C", "sensors": sensors}
(HERE / "vienna_sensors.json").write_text(json.dumps(info, indent=2, ensure_ascii=False), encoding="utf-8")

requests_to_save = [(s["device"], iv) for s in sensors
                    for iv in ("R30/2025-10-17T00:00/P1D", "R60/2025-10-17T00:00/PT12H")]
requests_to_save.append(("48206-u2ed4nbjj2n", "R7/2025-03-13T00:00/P1D"))   # the worked homework example

saved = {}
for device, interval in requests_to_save:
    req = requests.Request("GET", BASE + device + "/sensors/temperature/measurements",
                           params={"interval": interval, "agg": "MEAN"}).prepare()
    r = requests.get(req.url, timeout=120)
    r.raise_for_status()
    saved[req.url] = r.json()
    print(len(saved[req.url]), req.url)
(HERE / "sensor_fallback.json").write_text(json.dumps(saved, indent=1, ensure_ascii=False), encoding="utf-8")
print("written", len(saved), "answers")
