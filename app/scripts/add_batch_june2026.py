#!/usr/bin/env python3
"""Add June 2026 batch: playgrounds, beaches, lighthouses, misc."""
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

# ── PLAYGROUNDS (all fully fenced unless noted) ──────────────────────────────
PLAYGROUND_NOTE = 'Fully fenced in.'
PG_NOT_FENCED = 'NOT fully fenced; the back playground area is fenced and somewhat shaded.'

playgrounds = [
    make('Playground','Jordan Park','Lynnfield','MA',70,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='3 Wildewood Dr, Lynnfield, MA 01940'),
    make('Playground','Cambridge Universal Playground','Cambridge','MA',65,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE + ' Note: one small partial opening near the benches in the front.',
         geocode_q='66 Field St, Cambridge, MA 02138'),
    make('Playground','Kidstown','Danvers','MA',75,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='57 Forest St, Danvers, MA 01923'),
    make('Playground','Drummond Playground','North Andover','MA',75,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='Johnson St, North Andover, MA 01845'),
    make('Playground','Penguin Park','Andover','MA',75,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='72 Burnham Rd, Andover, MA 01810'),
    make('Playground','Chadwick Park','North Andover','MA',75,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='411 Sutton St, North Andover, MA 01845'),
    make('Playground','Newmarket Rec','Newmarket','NH',100,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='1 Terrace Dr, Newmarket, NH 03857'),
    make('Playground','Planet Playground','Exeter','NH',90,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='4 Hampton Rd, Exeter, NH 03833'),
    make('Playground','Lower Atkinson Playground','Newburyport','MA',90,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE + ' Located at Newburyport Pioneer Baseball/Softball League.',
         geocode_q='447 Merrimac St, Newburyport, MA 01950'),
    make('Playground','Bartlet Mall','Newburyport','MA',90,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='153 Auburn St, Newburyport, MA 01950'),
    make('Playground','Griffin Park','Windham','NH',90,'Outdoor','free','Free',
         details=PG_NOT_FENCED, geocode_q='111 Range Rd, Windham, NH 03087'),
    make('Playground','Park Street Park','Exeter','NH',90,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='Park St, Exeter, NH 03833'),
    make('Playground','Collins Street Playground','Amesbury','MA',90,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='37 Collins Ave, Amesbury, MA 01913'),
    make('Playground','Cater Park','Portsmouth','NH',100,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='55 Columbia St, Portsmouth, NH 03801'),
    make('Playground','Portsmouth Plains','Portsmouth','NH',100,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='1845 Plains Ave, Portsmouth, NH 03801'),
    # RI playgrounds
    make('Playground','Johnston Memorial Park','Johnston','RI',10,'Outdoor','free','Free',
         tags=['Splash Pad'], details=PLAYGROUND_NOTE,
         geocode_q='Johnston Memorial Park, Johnston, RI'),
    make('Playground','Wilson Park','North Kingstown','RI',20,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='Wilson Park, North Kingstown, RI'),
    make('Playground','Hilltop Playground','Cranston','RI',15,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='Hilltop Playground, Cranston, RI'),
    make('Playground','Village Playground','Cranston','RI',15,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='Village Playground, Cranston, RI'),
    make('Playground','India Point Park','Providence','RI',15,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE + ' Great waterfront views of the Providence River.',
         geocode_q='India Point Park, Providence, RI'),
    make('Playground','Cooney Playground','Cranston','RI',15,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='Cooney Playground, Cranston, RI'),
    make('Playground','Gladys Potter Park','Providence','RI',15,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='Gladys Potter Park, Providence, RI'),
    make('Playground','Summit Avenue Playground','Providence','RI',15,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='Summit Avenue Playground, Providence, RI'),
    make('Playground','Encompass Park','North Providence','RI',15,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='Encompass Park, North Providence, RI'),
    make('Playground','Captain Stephen Olney Memorial Park','North Providence','RI',15,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='Stephen Olney Memorial Park, North Providence, RI'),
    make('Playground','Brassil Playground','Providence','RI',15,'Outdoor','free','Free',
         details=PLAYGROUND_NOTE, geocode_q='Brassil Playground, Providence, RI'),
]

# ── SANDY BEACHES ─────────────────────────────────────────────────────────────
sandy_beaches = [
    make('Beach (Sandy)','Wingaersheek Beach','Gloucester','MA',75,'Outdoor','free',
         'Free beach; parking $25 (weekday) – $48 (peak summer weekend)',
         season='warm', details='Crystal-clear calm water, tidal sandbars at low tide, gorgeous views. Parking can be a challenge on peak days.',
         geocode_q='Wingaersheek Beach, Gloucester, MA'),
    make('Beach (Sandy)','Town Neck Beach','Sandwich','MA',70,'Outdoor','free',
         'Free beach; small parking fee ~$10-15 (seasonal)',
         season='warm', geocode_q='Town Neck Beach, Sandwich, MA'),
    make('Beach (Sandy)','Chapaquoit Beach','Falmouth','MA',80,'Outdoor','free',
         'Free; small town parking lot',
         season='warm', geocode_q='Chapaquoit Beach, Falmouth, MA'),
    make('Beach (Sandy)','Duxbury Beach','Duxbury','MA',70,'Outdoor','free',
         'Free beach; non-resident parking ~$30-50/day',
         season='warm', geocode_q='Duxbury Beach, Duxbury, MA'),
    make('Beach (Sandy)','Waterford Beach','Waterford','CT',50,'Outdoor','free',
         'CT state beach; $7 parking (in-state) or $15 (out-of-state)',
         season='warm', geocode_q='Waterford Beach, Waterford, CT'),
    make('Beach (Sandy)','Marinelli Beach','Oak Bluffs','MA',45,'Outdoor','free',
         'Free beach; accessible via Martha\'s Vineyard ferry',
         season='warm', geocode_q='Seaview Ave, Oak Bluffs, MA'),
    make('Beach (Sandy)','The Knob','Falmouth','MA',80,'Outdoor','free',
         'Free; short Trustees conservation trail walk to a scenic point',
         season='year-round', details='Short ~10-min walk along Quissett Harbor leads to a rocky/sandy point with beautiful views. Not a swimming beach.',
         geocode_q='The Knob, Quissett Harbor, Falmouth, MA'),
    make('Beach (Sandy)','South Beach','Edgartown','MA',45,'Outdoor','free',
         'Free beach; parking fee ~$20-30/day (or bike/shuttle in)',
         season='warm', details='Accessible via Martha\'s Vineyard ferry. South Beach is a long barrier beach on the Atlantic side of the Vineyard.',
         geocode_q='South Beach, Edgartown, MA'),
    make('Beach (Sandy)','East Beach','Chappaquiddick','MA',45,'Outdoor','free',
         'Free beach; Chappaquiddick Ferry ~$12 round-trip/person then drive/bike to beach',
         season='warm', details='Accessible via Martha\'s Vineyard ferry, then the little Chappy Ferry to Chappaquiddick Island. Wild and uncrowded Atlantic-facing beach.',
         geocode_q='East Beach, Chappaquiddick, MA'),
    make('Beach (Sandy)','Niantic Bay Boardwalk','East Lyme','CT',50,'Outdoor','free',
         '$20 parking (beach only) or $40 parking + boardwalk access',
         season='warm', default_visited=True,
         geocode_q='Niantic Bay Boardwalk, East Lyme, CT'),
]

# ── SEA GLASS BEACHES ────────────────────────────────────────────────────────
seaglass_beaches = [
    make('Sea Glass Beach','Hampton Beach','Hampton','NH',100,'Outdoor','free',
         'Free beach; parking ~$10-25/day (municipal lots)',
         season='warm', details='Busy boardwalk beach with sea glass found in rockier sections. Also has an arcade, food, and amusements along the strip.',
         geocode_q='Hampton Beach, Hampton, NH'),
    make('Sea Glass Beach','Rye Harbor State Park','Rye','NH',95,'Outdoor','free',
         'Free; small NH state park parking lot',
         season='year-round', details='Rocky coastline known for sea glass hunting, especially after storms.',
         geocode_q='Rye Harbor State Park, Rye, NH'),
    make('Sea Glass Beach','Popham Beach State Park','Phippsburg','ME',180,'Outdoor','under50',
         '~$8 adult / $1 child (Maine resident ~$4); state park',
         season='warm', details='Long sandy barrier beach with tidal pools and sea glass. One of Maine\'s best beaches.',
         geocode_q='Popham Beach State Park, Phippsburg, ME'),
    make('Sea Glass Beach','Old Orchard Beach','Old Orchard Beach','ME',150,'Outdoor','free',
         'Free beach; paid parking ~$10-20/day; boardwalk rides extra',
         season='warm', details='Classic Maine beach town with a pier and amusements. Sea glass found in rocky sections away from the main swimming area.',
         geocode_q='Old Orchard Beach, ME'),
    make('Sea Glass Beach','Ogunquit Beach','Ogunquit','ME',140,'Outdoor','free',
         'Free beach; parking ~$4-7/hr or $30-35/day in main lots',
         season='warm', details='Beautiful 3.5-mile sandy beach. Sea glass can be found toward the rockier ends. The Marginal Way cliff walk is nearby.',
         geocode_q='Ogunquit Beach, Ogunquit, ME'),
]

# ── LIGHTHOUSES ───────────────────────────────────────────────────────────────
lighthouses = [
    make('Lighthouse','Beavertail Lighthouse','Jamestown','RI',35,'Outdoor','free',
         'Free (museum); $5 tower climb; grounds always free',
         season='year-round', hours='Museum open mid-Jun–Labor Day; grounds always accessible',
         details='Can go inside — museum free, tower climb $5. Beautiful rocky point at the southern tip of Conanicut Island. Stunning views of Narragansett Bay.',
         geocode_q='774 Beavertail Rd, Jamestown, RI 02835'),
    make('Lighthouse','Point Judith Lighthouse','Narragansett','RI',30,'Outdoor','free',
         'Free (exterior always accessible; guided tours available)',
         season='year-round', hours='Exterior always open; interior tours vary (check USCG schedule)',
         details='Can go inside on scheduled open house days. Iconic octagonal lighthouse at the mouth of Narragansett Bay. Close to the Block Island Ferry.',
         geocode_q='Point Judith Lighthouse, Narragansett, RI'),
    make('Lighthouse','North Light + Maritime Museum','New Shoreham','RI',100,'Outdoor','free',
         'Free or small fee (confirm on-site); ferry to Block Island required (~$30+ round trip adult)',
         season='warm', hours='Museum open weekends Memorial Day–Columbus Day; daily Jul–Aug',
         details='Tower is NOT open to public, but the lighthouse keeper\'s house is a maritime interpretive museum you can walk through. Located at the northern tip of Block Island — 0.5-mile beach walk from Settlers\' Rock.',
         geocode_q='North Lighthouse, Block Island, RI'),
    make('Lighthouse','Pomham Rocks Lighthouse','East Providence','RI',15,'Outdoor','under50',
         '$50/person (non-members); ~$25 members; includes 15-min boat ride to lantern room',
         season='warm', hours='Seasonal tours; check Save the Bay schedule',
         details='Can go inside — 15-minute boat ride to access. Run by Save the Bay. Stunning 19th-century lighthouse on a small island in the Providence River.',
         geocode_q='Pomham Rocks Lighthouse, East Providence, RI'),
    make('Lighthouse','Southeast Light','New Shoreham','RI',100,'Outdoor','under50',
         '$20 adult / free for children under 9; ferry to Block Island required',
         season='warm', hours='Open daily in season (mid-Jun–Labor Day)',
         details='Can go inside. Iconic Victorian Gothic lighthouse on dramatic 200-ft clay bluffs on Block Island. One of the most picturesque lighthouses in New England.',
         geocode_q='Southeast Light, Block Island, RI'),
    # Bonus lighthouses from research
    make('Lighthouse','Nubble Light (Cape Neddick)','York','ME',150,'Outdoor','free',
         'Free to view from shore; island is off-limits',
         season='year-round', details='One of the most photographed lighthouses in the US. Sits on a small island just offshore — view from Sohier Park. Spectacular at sunset.',
         geocode_q='Nubble Lighthouse, York, ME'),
    make('Lighthouse','Portland Head Light','Cape Elizabeth','ME',165,'Outdoor','free',
         'Free to visit; small museum ~$5 adult',
         season='year-round', hours='Museum seasonal; grounds always open',
         details='Maine\'s oldest lighthouse (1791), commissioned by George Washington. Beautiful setting at Fort Williams Park. Museum inside keeper\'s house.',
         geocode_q='Portland Head Light, Cape Elizabeth, ME'),
    make('Lighthouse','Nobska Lighthouse','Falmouth','MA',80,'Outdoor','free',
         'Free; grounds open year-round',
         season='year-round', hours='Open for tours limited summer dates',
         details='Working lighthouse at the entrance to Vineyard Sound. Overlooks the Elizabeth Islands with views toward Martha\'s Vineyard. Short walk from the parking area.',
         geocode_q='Nobska Lighthouse, Falmouth, MA'),
    make('Lighthouse','Gay Head Light (Aquinnah)','Aquinnah','MA',45,'Outdoor','under50',
         'Free to view; $5 to climb (seasonal)',
         season='warm', hours='Open summer evenings for sunset climbs (Fri-Sun)',
         details='Can go inside (seasonal). Perched on dramatic multi-colored clay cliffs at the western tip of Martha\'s Vineyard. The cliffs themselves are stunning. Accessible via MV ferry.',
         geocode_q='Gay Head Lighthouse, Aquinnah, MA'),
    make('Lighthouse','Marshall Point Lighthouse','Port Clyde','ME',210,'Outdoor','free',
         'Free; museum donation appreciated',
         season='year-round', hours='Museum open Memorial Day–Columbus Day',
         details='Famous from the movie "Forrest Gump" — this is the lighthouse Forrest ran to at the end of his cross-country run. Beautiful setting on a rocky point. Free to visit.',
         geocode_q='Marshall Point Lighthouse, Port Clyde, ME'),
    make('Lighthouse','Pemaquid Point Lighthouse','Bristol','ME',210,'Outdoor','under50',
         '~$5 adult; fishermen\'s museum included',
         season='warm', hours='Open daily May–Columbus Day',
         details='Can go inside. One of the most scenic lighthouses in Maine, perched on dramatic wave-sculpted rock ledges. Excellent tide pool exploration nearby. Appears on the Maine quarter.',
         geocode_q='Pemaquid Point Lighthouse, Bristol, ME'),
    make('Lighthouse','West Quoddy Head Light','Lubec','ME',360,'Outdoor','under50',
         '~$5 for the state park',
         season='warm', details='Easternmost point in the United States. Distinctive red-and-white candy-striped lighthouse. A bucket-list landmark.',
         geocode_q='West Quoddy Head Lighthouse, Lubec, ME'),
]

# ── HIKING / NATURE ───────────────────────────────────────────────────────────
hiking = [
    make('Hiking / Nature','Thimble Islands Walk','Branford','CT',60,'Outdoor','free',
         'Free',
         season='year-round', details='2-mile there-and-back walk along a marsh at Tilcon Rd. Views of island mansions on the Thimble Islands. Flat and easy. May be better suited to older children.',
         geocode_q='Tilcon Rd, Branford, CT'),
    make('Hiking / Nature','Stratham Hill Park (Pump Park)','Stratham','NH',85,'Outdoor','free',
         'Free',
         season='year-round',
         geocode_q='270 Portsmouth Ave, Stratham, NH 03885'),
]

# ── HISTORY ───────────────────────────────────────────────────────────────────
history = [
    make('History','Fort Wetherill State Park','Jamestown','RI',35,'Outdoor','free',
         'Free; state park',
         season='year-round', details='WWII and earlier coastal fortification with bunkers you can explore. Dramatic rocky cliffs overlooking the East Passage of Narragansett Bay. Great spot for picnics.',
         geocode_q='Fort Wetherill State Park, Jamestown, RI'),
    make('Museum / Learning Center','Strawberry Banke Museum','Portsmouth','NH',100,'Both','under50',
         '~$20 adult / $10 child (under 5 free)',
         season='warm', hours='Open May–Oct (outdoor area year-round)',
         details='Living history museum on 10 acres of original buildings in Portsmouth\'s South End. Costumed interpreters reenact life from the 1600s-1950s — people churning butter, demonstrating crafts, etc. Excellent for all ages.',
         tags=['History'],
         geocode_q='14 Hancock St, Portsmouth, NH 03801'),
]

# ── AMUSEMENT ─────────────────────────────────────────────────────────────────
amusement = [
    make('Amusement / Theme Park','The Dinosaur Place','Oakdale','CT',70,'Outdoor','under50',
         '$19.99 ages 2–59 / free under 2',
         season='warm', hours='Open daily late May–early Sep; weekends in shoulder season',
         details='1.5-mile nature trail winding through life-size dinosaur sculptures in the woods, plus splash pad and mini-golf. Great for young kids who love dinosaurs.',
         geocode_q='1650 Hartford Pike, Oakdale, CT'),
    make('Zoo / Aquarium / Animals','Eastleigh Farm (Cow Safari)','Framingham','MA',65,'Outdoor','under50',
         '~$3/person wagon ride; admission otherwise low',
         season='warm', hours='May–Oct, weekends',
         details='100-acre animal sanctuary farm with a "Cow Safari" wagon ride through the pastures. Kids get up-close with cows, chickens, sheep, and more.',
         geocode_q='1062 Edmands Rd, Framingham, MA 01701'),
]

# ── MUSEUM / LEARNING CENTER ──────────────────────────────────────────────────
museums = [
    make('Museum / Learning Center','Squam Lakes Natural Science Center','Holderness','NH',130,'Both','under50',
         '~$19 adult / $14 child (3-15) / free under 3',
         season='warm', hours='Open daily May–Nov',
         details='Walk a ¾-mile trail past native animals in natural habitats: black bears, mountain lions, otters, raptors, turtles and more. Also offers boat cruises on Squam Lake (separate ticket). Wonderful for young children.',
         geocode_q='23 Science Center Rd, Holderness, NH 03245'),
]

# ── ROADSIDE ATTRACTIONS ──────────────────────────────────────────────────────
roadside = [
    make('Roadside Attraction','Giant Chair (World\'s Largest Windsor Chair)','Gardner','MA',90,'Outdoor','free',
         'Free; outdoor landmark',
         season='year-round', details='Gardner MA is "The Chair City" — this 20-ft tall (3,000-lb) Windsor chair at 130 Elm St has been a landmark since 1976. Quick photo stop.',
         geocode_q='130 Elm St, Gardner, MA 01440'),
    make('Roadside Attraction','Eartha (World\'s Largest Rotating Globe)','Yarmouth','ME',165,'Indoor','free',
         'Free; viewable through glass at the Garmin/DeLorme building',
         season='year-round', hours='Mon–Fri business hours (viewable through lobby glass)',
         details='Eartha is a 41.5-foot rotating globe — the world\'s largest. Located inside the former DeLorme (now Garmin) headquarters. Best viewed on a weekday.',
         geocode_q='2 DeLorme Dr, Yarmouth, ME 04096'),
]

ALL_NEW = playgrounds + sandy_beaches + seaglass_beaches + lighthouses + hiking + history + amusement + museums + roadside

# ── Load, dedupe, geocode, save ───────────────────────────────────────────────
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

# ── Mark specific existing places as defaultVisited ───────────────────────────
FORCE_VISITED = {
    'novel-shop-book-barn',
    # Niantic Bay Boardwalk and Niantic Children's Museum will be added by a second script
    # once the research agent confirms the children's museum address
}
for place in places:
    if place['id'] in FORCE_VISITED and not place.get('defaultVisited'):
        place['defaultVisited'] = True
        print(f'Marked visited: {place["name"]}')

with open(PLACES_FILE, 'w') as f:
    json.dump(places, f, indent=2)

print(f'\nDone. Added {added}, skipped {skipped}. Total: {len(places)}')
