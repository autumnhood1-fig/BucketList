#!/usr/bin/env python3
"""
Stage 2: turn places.raw.json into the final src/data/places.json
- applies hand patches for the handful of rows that didn't parse cleanly
- derives priceTier, oslFree, discount, seasonal, indoorOutdoor, driveBucket
"""
import json
import re
import os

BASE = os.path.join(os.path.dirname(__file__), "..", "src", "data")
RAW = os.path.join(BASE, "places.raw.json")
OUT = os.path.join(BASE, "places.json")

with open(RAW, encoding="utf-8") as f:
    items = json.load(f)


def find(name):
    for it in items:
        if it["name"] == name:
            return it
    raise KeyError(name)


# ---- Patches for rows that didn't parse cleanly ----

# 1. Hogpen Hill Farms swallowed Chesterwood's row
hh = find("Hogpen Hill Farms (Edward Tufte)")
hh.pop("discountRaw", None)
hh.pop("extra", None)
items.append({
    "name": "Chesterwood",
    "cityState": "Stockbridge, MA",
    "driveMinutes": 135.0,
    "category": "Sculpture / Art Park",
    "admission": "~$20 adult; under 12 free; sculptor's studio + grounds",
})

# 2. Rainforest Cafe - location unclear, attach to Providence Place Mall area
rf = find("Rainforest Cafe (themed dining)")
rf["cityState"] = "Providence, RI"
rf["driveMinutes"] = 10.0
rf["indoorOutdoor"] = "Indoor"
rf["details"] = "Location TBD - verify nearest Rainforest Cafe (Providence Place Mall historically)."
rf["admission"] = "Varies"
del items[items.index(rf)]
items.append(rf)
# remove the leftover stray rows
items[:] = [it for it in items if it["name"] not in
            ("Providence Place Mall? / verify nearest", "Indoor")]

# 3. Stateline Farm - vague location
sf = find("Stateline Farm / pony rides (verify)")
sf["cityState"] = "RI/MA border"
sf["driveMinutes"] = 15.0
sf["details"] = "Pony rides + farm animals for young kids. Location needs verification (RI/MA border area)."
sf.pop("discountRaw", None)

# 4. City & Town Trips section got tangled where the attraction name itself
#    is a "City, ST" string (Plymouth, Manchester-by-the-Sea, Exeter, South Berwick)
#    and the Eliot/Stratham row got merged into Provincetown's details.
prov = find("Provincetown / Cape Cod towns")
prov["details"] = "Whale-watch boats leave from here, dunes to run, taffy shops, Pilgrim Monument to climb."

dux = find("Duxbury (beach + Powder Point Bridge)")
dux["details"] = "Walk the long wooden Powder Point Bridge, tide flats with crabs, calm beach."

salem = find("Salem (waterfront, witch lore, museums)")
salem["details"] = "Pirate museum, tall ship, friendly-spooky vibe, harbor; not-too-scary for a 5yo if you skip the gory exhibits."

items.append({"name": "Plymouth, MA", "cityState": "Plymouth, MA", "driveMinutes": 50.0,
               "category": "City & Town Trip",
               "details": "Plymouth Rock, Mayflower II ship to board, waterfront, Plimoth Patuxet living history nearby; very kid-graspable history."})
items.append({"name": "Manchester-by-the-Sea, MA", "cityState": "Manchester-by-the-Sea, MA", "driveMinutes": 75.0,
               "category": "City & Town Trip",
               "details": "Singing Beach (sand actually squeaks!), harbor, ice cream; classic North Shore beach-town day."})
items.append({"name": "Exeter, NH", "cityState": "Exeter, NH", "driveMinutes": 85.0,
               "category": "City & Town Trip",
               "details": "Pretty riverfront downtown, bandstand, swan-filled river, ice cream, Water St shops; gentle small-town wander."})
items.append({"name": "South Berwick, ME", "cityState": "South Berwick, ME", "driveMinutes": 85.0,
               "category": "City & Town Trip",
               "details": "Storybook small town (Hamilton House + Vaughan Woods trails along the river); quiet, scenic, low-key."})
items.append({"name": "Eliot, ME / Stratham, NH (Seacoast border towns)", "cityState": "Eliot, ME", "driveMinutes": 90.0,
               "category": "City & Town Trip",
               "details": "Quiet Seacoast towns near Portsmouth; pair with Stratham Hill Park playground + nearby Alnoba/sculpture. Add-on to a Portsmouth day."})

# remove the broken "name == sentence, cityState == City, ST" rows that these replace
_BROKEN_TRIP_NAMES = {
    "Walk the long wooden Powder Point Bridge, tide flats with crabs, calm beach.",
    "A whole village of book sheds outdoors with resident cats and goats to find - like a treasure hunt.",
    "Pirate museum, tall ship, friendly-spooky vibe, harbor; not-too-scary for a 5yo if you skip the gory exhibits.",
    "Pretty riverfront downtown, bandstand, swan-filled river, ice cream, Water St shops; gentle small-town wander.",
}
items[:] = [it for it in items if it["name"] not in _BROKEN_TRIP_NAMES]

# 5. deCordova / Alnoba - admission text got misclassified
dc = find("deCordova")
dc["admission"] = dc.pop("oslRaw")[0]
al = find("Alnoba")
al["admission"] = al.pop("hours")

# ---- City/State overrides for odd strings ----
CITY_STATE_OVERRIDES = {
    "RI/MA border": ("RI/MA border", ""),
    "W.  Stockbridge,MA": ("W. Stockbridge", "MA"),
    "Tupper Lake,NY": ("Tupper Lake", "NY"),
}


def split_city_state(cs):
    if cs in CITY_STATE_OVERRIDES:
        return CITY_STATE_OVERRIDES[cs]
    if "," in cs:
        city, state = cs.rsplit(",", 1)
        return city.strip(), state.strip()
    return cs.strip(), ""


# ---- Category defaults ----
INOUT_DEFAULT = {
    "Museum / Learning Center": "Indoor",
    "Zoo / Aquarium / Animals": "Outdoor",
    "Amusement / Theme Park": "Outdoor",
    "Nature Coaster / Ride": "Outdoor",
    "Cave / Geology": "Both",
    "Splash Pad": "Outdoor",
    "Troll Hunting": "Outdoor",
    "Playground": "Outdoor",
    "Lighthouse": "Outdoor",
    "Farm / Pick-Your-Own": "Outdoor",
    "Hiking / Nature": "Outdoor",
    "Garden": "Outdoor",
    "Sculpture / Art Park": "Outdoor",
    "Ferry": "Outdoor",
    "Kayaking / Boat": "Outdoor",
    "Eating + Play": "Both",
    "Novel Shop": "Indoor",
    "Beach (Sandy)": "Outdoor",
    "Sea Glass Beach": "Outdoor",
    "Tide Pools": "Outdoor",
    "City & Town Trip": "Outdoor",
}

SEASONAL_DEFAULT_TRUE = {"Beach (Sandy)", "Splash Pad", "Amusement / Theme Park", "Farm / Pick-Your-Own"}

SEASON_RE = re.compile(
    r"season|\(fall\)|\(spring\)|\(summer\)|\(winter\)|may-|apr-|jun-|jul-|aug-|sep-|oct-|nov-|"
    r"weekends?\s|memorial day|labor day|jul-aug",
    re.I,
)
DISCOUNT_KEYWORD_RE = re.compile(
    r"%\s*off|half price|half-price|bogo|reciprocal|combo|citypass|go city|passport|"
    r"free entry to all|narm members|discount",
    re.I,
)
PRICE_RE = re.compile(r"\$\s*([\d.]+)")


def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


SLUG_COUNTS = {}


def make_id(category, name):
    base = f"{slugify(category)}-{slugify(name)}"
    n = SLUG_COUNTS.get(base, 0)
    SLUG_COUNTS[base] = n + 1
    return base if n == 0 else f"{base}-{n+1}"


places = []
for it in items:
    category = it["category"]
    name = it["name"]
    city, state = split_city_state(it.get("cityState") or "")
    drive_minutes = it.get("driveMinutes")

    if drive_minutes is None:
        drive_bucket = None
    elif drive_minutes < 30:
        drive_bucket = "<30"
    elif drive_minutes <= 60:
        drive_bucket = "30-60"
    elif drive_minutes <= 90:
        drive_bucket = "60-90"
    else:
        drive_bucket = "90+"

    osl_lines = it.get("oslRaw", [])
    osl_lines = [l for l in osl_lines if
                  re.match(r"^yes\s*-", l, re.I) or "museums for all" in l.lower() or "library (osl)" in l.lower()]
    osl_note = " | ".join(osl_lines) if osl_lines else None
    osl_free = any(re.match(r"^yes\s*-.*\bfree\b", l, re.I) for l in osl_lines)

    discount_raw = it.get("discountRaw", [])
    discount_note = " | ".join(discount_raw) if discount_raw else None
    discount = bool(discount_note) or (osl_note is not None and DISCOUNT_KEYWORD_RE.search(osl_note))

    # price text: first field that looks price-ish
    price_candidates = []
    if it.get("admission"):
        price_candidates.append(it["admission"])
    price_candidates.extend(osl_lines)
    if it.get("hours"):
        price_candidates.append(it["hours"])
    price_candidates.extend(discount_raw)
    price_candidates.extend(it.get("extra", []))

    price_text = None
    for c in price_candidates:
        if "$" in c or re.search(r"\bfree\b", c, re.I) or re.search(r"\bdonation\b", c, re.I):
            price_text = c
            break

    if category == "City & Town Trip":
        price_tier = "varies"
        price_note = "Cost varies by activity"
    elif price_text:
        nums = [float(n) for n in PRICE_RE.findall(price_text)]
        if nums:
            price_tier = "free" if max(nums) == 0 else ("under50" if max(nums) < 50 else "over50")
        else:
            price_tier = "free"
        price_note = price_text
    elif category in ("Beach (Sandy)", "Sea Glass Beach", "Tide Pools"):
        price_tier = "free"
        price_note = "Free; parking may apply ($5-$30)"
    else:
        price_tier = "free"
        price_note = "Free"

    # seasonal
    text_blob = " ".join(filter(None, [
        it.get("admission"), it.get("hours"), osl_note, discount_note,
        it.get("details"), " ".join(it.get("extra", []))
    ]))
    if SEASON_RE.search(text_blob):
        seasonal = True
    elif "year-round" in text_blob.lower() or "year round" in text_blob.lower():
        seasonal = False
    else:
        seasonal = category in SEASONAL_DEFAULT_TRUE

    indoor_outdoor = it.get("indoorOutdoor") or INOUT_DEFAULT.get(category, "Both")

    place = {
        "id": make_id(category, name),
        "name": name,
        "category": category,
        "city": city,
        "state": state,
        "driveMinutes": drive_minutes,
        "driveBucket": drive_bucket,
        "indoorOutdoor": indoor_outdoor,
        "priceTier": price_tier,
        "priceNote": price_note,
        "oslFree": osl_free,
        "oslNote": osl_note,
        "discount": bool(discount),
        "discountNote": discount_note,
        "seasonal": seasonal,
        "hours": it.get("hours") if it.get("hours") != it.get("admission") else None,
        "details": it.get("details"),
        "lat": None,
        "lng": None,
    }
    places.append(place)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(places, f, indent=2, ensure_ascii=False)

print(f"Wrote {len(places)} places to {OUT}")

# sanity report
no_drive = [p["name"] for p in places if p["driveMinutes"] is None]
print("Missing drive time:", no_drive)
