#!/usr/bin/env python3
"""
One-time parser: turns scripts/data-source/raw_extract.txt (extracted from the
Kid_Friendly_Places.docx master list) into src/data/places.json.

Output is hand-reviewed afterwards - this script gets us ~90% of the way there.
"""
import json
import re
import os

SRC = os.path.join(os.path.dirname(__file__), "data-source", "raw_extract.txt")
OUT = os.path.join(os.path.dirname(__file__), "..", "src", "data", "places.json")

with open(SRC, encoding="utf-8") as f:
    raw_lines = [l.rstrip("\n") for l in f.readlines()]

# unescape a few entities pandoc/extract left behind
def clean(s):
    return (s.replace("&amp;", "&")
             .replace("&#x2019;", "’")
             .replace("&#x201C;", "“")
             .replace("&#x201D;", "”")
             .replace("&quot;", '"')
             .replace("&lt;", "<")
             .replace("&gt;", ">")
             .strip())

lines = [clean(l) for l in raw_lines]

# Section boundaries: (start_line_1indexed, end_line_1indexed_inclusive, category_name, mode)
SECTIONS = [
    (4, 334, "Museum / Learning Center", "standard"),
    (336, 463, "Zoo / Aquarium / Animals", "standard"),
    (465, 566, "Amusement / Theme Park", "standard"),
    (568, 607, "Nature Coaster / Ride", "standard"),
    (609, 632, "Cave / Geology", "cave"),
    (634, 699, "Splash Pad", "simple"),
    (701, 718, "Troll Hunting", "simple"),
    (720, 788, "Playground", "simple"),
    (790, 807, "Lighthouse", "simple"),
    (809, 963, "Farm / Pick-Your-Own", "standard"),
    (965, 1081, "Hiking / Nature", "simple"),
    (1083, 1165, "Garden", "standard"),
    (1167, 1190, "Sculpture / Art Park", "standard"),
    (1192, 1227, "Ferry", "standard"),
    (1229, 1264, "Kayaking / Boat", "standard"),
    (1266, 1330, "Eating + Play", "standard"),
    (1332, 1372, "Novel Shop", "standard"),
    (1374, 1436, "Beach (Sandy)", "beach"),
    (1438, 1470, "Sea Glass Beach", "beach"),
    (1472, 1509, "Tide Pools", "beach"),
    (1511, 1651, "City & Town Trip", "trip"),
]

CITY_RE = re.compile(r".+,\s*[A-Z]{2}$")
NUM_RE = re.compile(r"^\d+(\.\d+)?$")
INOUT_RE = re.compile(r"^(Indoor|Outdoor|Both)\s*$", re.I)

HOURS_KEYWORDS = ["Daily", "Seasonal", "Weekend", "season", "Limited", "Timed tickets",
                  "May-", "Apr-", "Sept-", "Jan-", "call ahead", "VERIFY"]

# header rows to skip per section (table headers like "Attraction", "City/State", etc.)
HEADER_WORDS = {"attraction", "city/state", "city / state", "min", "mins", "mins.",
                "admission", "in/out", "discounts / bundles", "library (osl) pass + ebt",
                "hours", "dist", "(min)", "in/", "out", "est.", "time", "why a kid would like it",
                "admission "}


def get_section(start, end):
    return [l for l in lines[start - 1:end] if l.strip() != ""]


def is_city_state(s):
    return bool(CITY_RE.match(s.strip())) or s.strip() in {
        "RI/MA border", "Various, MA", "Aquidneck Island, RI"
    }


def classify_extra(line, item):
    l = line.strip()
    if INOUT_RE.match(l):
        item["indoorOutdoor"] = l.capitalize() if l.lower() != "both" else "Both"
        # normalize
        norm = l.strip().lower()
        item["indoorOutdoor"] = {"indoor": "Indoor", "outdoor": "Outdoor", "both": "Both"}[norm]
        return
    if "museums for all" in l.lower() or l.lower().startswith("yes -") or l.lower().startswith("yes-") \
            or "library (osl)" in l.lower() or "narm members" in l.lower():
        item.setdefault("oslRaw", []).append(l)
        return
    if any(k.lower() in l.lower() for k in HOURS_KEYWORDS):
        item["hours"] = l
        return
    if l.startswith("~$") or l.startswith("$") or l.lower().startswith("free") \
            or l.lower().startswith("donation") or "admission" in l.lower() or "/person" in l.lower() \
            or re.match(r"^[~]?\$", l):
        if "admission" not in item:
            item["admission"] = l
        else:
            item.setdefault("extra", []).append(l)
        return
    # default -> discount/bundle note
    item.setdefault("discountRaw", []).append(l)


def parse_standard(rows, category):
    out = []
    i = 0
    n = len(rows)
    while i < n:
        line = rows[i].strip()
        if line.lower() in HEADER_WORDS:
            i += 1
            continue
        # find name = current line, look ahead for city/state on next line
        if i + 1 < n and is_city_state(rows[i + 1]):
            name = line
            city_state = rows[i + 1].strip()
            i += 2
            mins = None
            if i < n and NUM_RE.match(rows[i].strip()):
                mins = float(rows[i].strip())
                i += 1
            item = {"name": name, "cityState": city_state, "driveMinutes": mins, "category": category}
            # gather extras until next name (next line followed by city/state, or numeric pattern start)
            while i < n:
                nxt = rows[i].strip()
                if i + 1 < n and is_city_state(rows[i + 1]) and nxt.lower() not in HEADER_WORDS:
                    break
                if nxt.lower() in HEADER_WORDS:
                    i += 1
                    continue
                classify_extra(nxt, item)
                i += 1
            out.append(item)
        else:
            # couldn't find a city/state pairing - emit raw for manual review
            out.append({"name": line, "cityState": None, "driveMinutes": None,
                         "category": category, "_unparsed": True})
            i += 1
    return out


def parse_simple(rows, category):
    # Name, City/State, Mins   (no extras)
    out = []
    i = 0
    n = len(rows)
    while i < n:
        line = rows[i].strip()
        if line.lower() in HEADER_WORDS:
            i += 1
            continue
        if i + 1 < n and is_city_state(rows[i + 1]):
            name = line
            city_state = rows[i + 1].strip()
            i += 2
            mins = None
            if i < n and NUM_RE.match(rows[i].strip()):
                mins = float(rows[i].strip())
                i += 1
            out.append({"name": name, "cityState": city_state, "driveMinutes": mins, "category": category})
        else:
            out.append({"name": line, "cityState": None, "driveMinutes": None,
                         "category": category, "_unparsed": True})
            i += 1
    return out


def parse_cave(rows, category):
    # Name, Admission, City/State, Mins
    out = []
    i = 0
    n = len(rows)
    while i < n:
        line = rows[i].strip()
        if line.lower() in HEADER_WORDS:
            i += 1
            continue
        if i + 2 < n and is_city_state(rows[i + 2]):
            name = line
            admission = rows[i + 1].strip()
            city_state = rows[i + 2].strip()
            mins = None
            if i + 3 < n and NUM_RE.match(rows[i + 3].strip()):
                mins = float(rows[i + 3].strip())
                i += 4
            else:
                i += 3
            out.append({"name": name, "cityState": city_state, "driveMinutes": mins,
                         "category": category, "admission": admission})
        else:
            out.append({"name": line, "cityState": None, "driveMinutes": None,
                         "category": category, "_unparsed": True})
            i += 1
    return out


def parse_beach(rows, category):
    # Name, City/State, Mins, optional discount/pass note line(s)
    out = []
    i = 0
    n = len(rows)
    while i < n:
        line = rows[i].strip()
        if line.lower() in HEADER_WORDS:
            i += 1
            continue
        if i + 1 < n and is_city_state(rows[i + 1]):
            name = line
            city_state = rows[i + 1].strip()
            i += 2
            mins = None
            if i < n and NUM_RE.match(rows[i].strip()):
                mins = float(rows[i].strip())
                i += 1
            item = {"name": name, "cityState": city_state, "driveMinutes": mins, "category": category}
            while i < n:
                nxt = rows[i].strip()
                if i + 1 < n and is_city_state(rows[i + 1]) and nxt.lower() not in HEADER_WORDS:
                    break
                if nxt.lower() in HEADER_WORDS:
                    i += 1
                    continue
                item.setdefault("discountRaw", []).append(nxt)
                i += 1
            out.append(item)
        else:
            out.append({"name": line, "cityState": None, "driveMinutes": None,
                         "category": category, "_unparsed": True})
            i += 1
    return out


def parse_trip(rows, category):
    # Name, City/State, Mins, "why a kid would like it" (details)
    out = []
    i = 0
    n = len(rows)
    while i < n:
        line = rows[i].strip()
        if line.lower() in HEADER_WORDS or "sorted closest-first" in line.lower():
            i += 1
            continue
        if i + 1 < n and is_city_state(rows[i + 1]):
            name = line
            city_state = rows[i + 1].strip()
            i += 2
            mins = None
            if i < n and NUM_RE.match(rows[i].strip()):
                mins = float(rows[i].strip())
                i += 1
            item = {"name": name, "cityState": city_state, "driveMinutes": mins, "category": category}
            details = []
            while i < n:
                nxt = rows[i].strip()
                if i + 1 < n and is_city_state(rows[i + 1]) and nxt.lower() not in HEADER_WORDS:
                    break
                if nxt.lower() in HEADER_WORDS:
                    i += 1
                    continue
                details.append(nxt)
                i += 1
            if details:
                item["details"] = " ".join(details)
            out.append(item)
        else:
            out.append({"name": line, "cityState": None, "driveMinutes": None,
                         "category": category, "_unparsed": True})
            i += 1
    return out


PARSERS = {
    "standard": parse_standard,
    "simple": parse_simple,
    "cave": parse_cave,
    "beach": parse_beach,
    "trip": parse_trip,
}

all_items = []
for start, end, cat, mode in SECTIONS:
    rows = get_section(start, end)
    items = PARSERS[mode](rows, cat)
    all_items.extend(items)

print(f"Parsed {len(all_items)} items")
unparsed = [it for it in all_items if it.get("_unparsed")]
print(f"Unparsed: {len(unparsed)}")
for u in unparsed:
    print("  UNPARSED:", u["category"], "|", u["name"])

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT.replace("places.json", "places.raw.json"), "w", encoding="utf-8") as f:
    json.dump(all_items, f, indent=2, ensure_ascii=False)

print("Wrote raw output to src/data/places.raw.json")
