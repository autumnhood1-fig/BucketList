#!/usr/bin/env python3
"""Add June 2026 batch B: indoor play, roadside attractions, Niantic Museum, more lighthouses."""
import json, re, sys, time, urllib.request, urllib.parse

PLACES_FILE = 'src/data/places.json'

def slug(s):
    s = s.lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

def geocode(query):
    url = 'https://nominatim.openstreetmap.org/search?q=' + urllib.parse.quote(query) + '&format=json&limit=1'
    req = urllib.request.Request(url, headers={'User-Agent': 'BucketListApp/1.0 autumnhood1@gmail.com'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        time.sleep(1.1)
        if data:
            return round(float(data[0]['lat']), 7), round(float(data[0]['lon']), 7)
    except Exception as e:
        print(f'  GEOCODE ERR: {e}', file=sys.stderr)
        time.sleep(1.1)
    return None, None

def make(category, name, city, state, drive_min, io, price_tier, price_note,
         season='year-round', hours=None, details=None, osl_free=False, osl_note=None,
         discount=False, discount_note=None, tags=None, default_visited=False,
         lat=None, lng=None, geocode_q=None):
    db = '<30' if drive_min < 30 else '30-60' if drive_min < 60 else '60-90' if drive_min < 90 else '90+'
    pid = slug(category) + '-' + slug(name)
    d = {
        'id': pid,
        'name': name,
        'category': category,
        'city': city,
        'state': state,
        'driveMinutes': drive_min,
        'driveBucket': db,
        'indoorOutdoor': io,
        'priceTier': price_tier,
        'priceNote': price_note,
        'oslFree': osl_free,
        'oslNote': osl_note,
        'discount': discount,
        'discountNote': discount_note,
        'seasonality': season,
        'hours': hours,
        'details': details,
        'lat': lat,
        'lng': lng,
    }
    if tags:
        d['tags'] = tags
    if default_visited:
        d['defaultVisited'] = True
    if geocode_q:
        d['_q'] = geocode_q
    return d

TODDLER_NOTE = 'Better suited for younger toddlers (great for the littles, less stimulating for older kids).'

indoor_play = [
    make('Indoor Play','Playtime RI','Smithfield','RI',20,'Indoor','under50',
         '$15/child; 1–2 adults included; extra adults $5; under 1 free with paying sibling',
         details=TODDLER_NOTE,
         geocode_q='151 Douglas Pike, Smithfield, RI 02917'),
    make('Indoor Play','The Sensory Play Place','Johnston','RI',10,'Indoor','under50',
         'Pricing by session — call or check website; (401) 203-3157',
         details=TODDLER_NOTE,
         geocode_q='1395 Atwood Ave, Johnston, RI 02919'),
    make('Indoor Play','SharkBay Playspace','West Warwick','RI',20,'Indoor','under50',
         '$15/child (all-day); adults free',
         details=TODDLER_NOTE,
         geocode_q='320 Washington St, West Warwick, RI 02893'),
    make('Indoor Play','Little Lattes Play Cafe','Coventry','RI',25,'Indoor','under50',
         'Timed 2-hr sessions; pricing by session — call (401) 859-1235',
         details=TODDLER_NOTE,
         geocode_q='57 Sandy Bottom Rd, Coventry, RI 02816'),
    make('Indoor Play','Simply Play','Seekonk','MA',25,'Indoor','under50',
         'Walk-in pricing — call (508) 557-0122; memberships from $40/mo',
         details=TODDLER_NOTE + ' (Located in Seekonk MA, near the Fall River area)',
         geocode_q='1460 Fall River Ave, Seekonk, MA 02771'),
    make('Indoor Play','FUNdamentals LLC','East Providence','RI',15,'Indoor','under50',
         'Open play packages $65 for 5 sessions; monthly $47.99/child; infants under 12 mo free with paying sibling',
         details=TODDLER_NOTE,
         geocode_q='1365 Wampanoag Trail, East Providence, RI 02915'),
]

niantic_museum = [
    make('Museum / Learning Center','Niantic Children\'s Museum','East Lyme','CT',50,'Indoor','under50',
         '$12/person; under 12 months free; military $9; SNAP/EBT $1',
         discount=True,
         discount_note='ACM Reciprocal Network member: 50% off with qualifying partner museum membership (e.g. Boston Children\'s Museum)',
         default_visited=True,
         geocode_q='409 Main St, East Lyme, CT 06357'),
]

roadside = [
    make('Roadside Attraction','World\'s Tallest Uncle Sam Statue','Danbury','CT',120,'Outdoor','free',
         'Free; outdoor landmark',
         season='year-round',
         details='38-foot fiberglass Uncle Sam statue outside the Danbury Railway Museum — originally stood at the Danbury Fair (closed 1981), moved to Lake George NY, then returned to Danbury in 2019.',
         geocode_q='120 White St, Danbury, CT 06810'),
    make('Roadside Attraction','World\'s Largest Telephone (Hand-Crank)','Bryant Pond','ME',210,'Outdoor','free',
         'Free; outdoor monument',
         season='year-round',
         details='14-foot replica of a hand-cranked candlestick phone at Remembrance Park. Bryant Pond was the last US town to use hand-crank telephone exchange, switched off in 1983.',
         geocode_q='1 N Main St, Bryant Pond, ME 04219'),
    make('Roadside Attraction','Giant Coffee Pot of Bedford','Bedford','PA',420,'Outdoor','free',
         'Free; roadside landmark',
         season='year-round',
         details='18-foot coffee pot built in 1927 on W. Pitt Street. One of the oldest roadside attractions in PA. A fun PA road-trip stop.',
         geocode_q='714 W Pitt St, Bedford, PA 15522'),
    make('Roadside Attraction','Giant Quarter','Everett','PA',420,'Outdoor','free',
         'Free; roadside landmark at Down River Golf Course',
         season='year-round',
         geocode_q='134 Rivers Bend Dr, Everett, PA 15537'),
    make('Roadside Attraction','Pied Piper of Bedford','Schellsburg','PA',420,'Outdoor','free',
         'Free; view from road (private property)',
         season='year-round',
         details='18-foot fiberglass Pied Piper on Route 30 in Schellsburg PA (Bedford County), remnant of a closed Story Land children\'s park from the 1980s.',
         geocode_q='3565 Lincoln Hwy, Schellsburg, PA 15559'),
]

lighthouses_b = [
    make('Lighthouse','Rose Island Lighthouse','Newport','RI',35,'Outdoor','under50',
         '~$10 island fee + ~$20 ferry (Jamestown-Newport Ferry); overnight stays available',
         season='warm', hours='Mid-May to mid-Oct (ferry season)',
         details='Can go inside — full lighthouse museum and Fort Hamilton barracks tours. Accessible only by ferry from Newport or by kayak (~1 mile). Stunning setting in Newport Harbor.',
         geocode_q='Rose Island, Newport, RI'),
    make('Lighthouse','Highland Light (Cape Cod Light)','Truro','MA',110,'Outdoor','under50',
         '$10 adult / $6 student / $8 senior; must be 48"+ to climb tower',
         season='warm', hours='Open daily May–late Oct',
         details='Can go inside — tallest lighthouse on Cape Cod. Inside Cape Cod National Seashore on dramatic cliffs.',
         geocode_q='27 Highland Light Rd, Truro, MA 02666'),
    make('Lighthouse','Nauset Light','Eastham','MA',100,'Outdoor','free',
         'Free; donations accepted',
         season='warm', hours='Guided tours Sundays May–Oct; Wednesdays Jul–Aug',
         details='Can go inside on tour days. Classic red-and-white Cape Cod lighthouse near Nauset Light Beach. Three Sisters lighthouses nearby.',
         geocode_q='120 Nauset Light Beach Rd, Eastham, MA 02642'),
    make('Lighthouse','Stonington Harbor Light (Lighthouse Museum)','Stonington','CT',65,'Indoor','under50',
         '$10 adult / $6 child / $25 family',
         season='warm', hours='Open daily summer; call ahead for shoulder season',
         details='Can go inside — this historic lighthouse is now a museum (one of the nation\'s first, opened 1927). Lovely village setting in Stonington CT.',
         geocode_q='7 Water St, Stonington, CT 06378'),
    make('Lighthouse','Wood Island Lighthouse','Biddeford Pool','ME',175,'Outdoor','under50',
         '$35 adult (13+) / $20 child; boat tour July–August only',
         season='warm', hours='Tours Jul–Aug; departs from Biddeford Pool',
         details='Can go inside — guided tour includes keeper\'s house and tower climb (ages 10+). Accessible only by boat. Full interior access and ghost legend.',
         geocode_q='Wood Island Lighthouse, Biddeford Pool, ME'),
]

ALL_NEW = indoor_play + niantic_museum + roadside + lighthouses_b

# Load, dedupe, geocode, save
places = json.load(open(PLACES_FILE))
existing_ids = {p['id'] for p in places}
existing_names = {p['name'].lower().strip() for p in places}

added = 0
skipped = 0
for place in ALL_NEW:
    q = place.pop('_q', None)
    pid = place['id']
    name_lower = place['name'].lower().strip()

    if pid in existing_ids or name_lower in existing_names:
        print(f'SKIP (exists): {place["name"]}')
        skipped += 1
        continue

    if place['lat'] is None and q:
        print(f'Geocoding: {place["name"]} ({q})')
        lat, lng = geocode(q)
        place['lat'] = lat
        place['lng'] = lng
        if lat is None:
            print(f'  WARNING: no coords for {place["name"]}')

    places.append(place)
    existing_ids.add(pid)
    existing_names.add(name_lower)
    added += 1
    print(f'  + {place["name"]} ({place["category"]}) [{place["lat"]}, {place["lng"]}]')

with open(PLACES_FILE, 'w') as f:
    json.dump(places, f, indent=2)

print(f'\nDone. Added {added}, skipped {skipped}. Total: {len(places)}')
