#!/usr/bin/env python3
"""
Geocode every place in src/data/places.json using the free Nominatim
(OpenStreetMap) API. Tries "<name>, <city>, <state>" first, then falls back
to "<city>, <state>". Caches results so re-runs are cheap and only fetch
new/changed entries.

Respects Nominatim's usage policy: 1 request/sec, custom User-Agent.
"""
import json
import os
import time
import urllib.request
import urllib.parse

BASE = os.path.join(os.path.dirname(__file__), "..", "src", "data")
PLACES = os.path.join(BASE, "places.json")
CACHE = os.path.join(os.path.dirname(__file__), "geocode_cache.json")

UA = "new-england-bucket-list-app/1.0 (personal family project)"

with open(PLACES, encoding="utf-8") as f:
    places = json.load(f)

if os.path.exists(CACHE):
    with open(CACHE, encoding="utf-8") as f:
        cache = json.load(f)
else:
    cache = {}


def query_nominatim(q):
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({
        "q": q, "format": "json", "limit": 1, "countrycodes": "us"
    })
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    return None


def geocode(p):
    candidates = []
    cs = f"{p['city']}, {p['state']}".strip(", ")
    if p["state"]:  # only try venue-level if we have a real state
        candidates.append(f"{p['name']}, {cs}, USA")
    candidates.append(f"{cs}, USA")
    for q in candidates:
        if q in cache:
            result = cache[q]
        else:
            try:
                result = query_nominatim(q)
            except Exception as e:
                print(f"  ERROR for '{q}': {e}")
                result = None
            cache[q] = result
            with open(CACHE, "w", encoding="utf-8") as f:
                json.dump(cache, f, indent=2)
            time.sleep(1.1)
        if result:
            return result, q
    return None, None


total = len(places)
for i, p in enumerate(places):
    if p.get("lat") is not None:
        continue
    coords, used_query = geocode(p)
    if coords:
        p["lat"], p["lng"] = coords
        print(f"[{i+1}/{total}] {p['name']!r} -> {coords} (via {used_query!r})")
    else:
        print(f"[{i+1}/{total}] {p['name']!r} -> NOT FOUND")

with open(PLACES, "w", encoding="utf-8") as f:
    json.dump(places, f, indent=2, ensure_ascii=False)

missing = [p["name"] for p in places if p.get("lat") is None]
print(f"\nDone. {len(places) - len(missing)}/{len(places)} geocoded.")
if missing:
    print("Missing:", missing)
