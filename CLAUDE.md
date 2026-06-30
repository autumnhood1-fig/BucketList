# Bucket List — Project Guide for Claude

## What this is
A personal family bucket-list map app for **Autumn Hood** and her husband **Evan**, who live near Providence, RI. The app shows a Leaflet map (and list view) of kid-friendly places across New England and the Northeast, with filters, visited tracking, and rich place details. Their kids are named **August** (younger, toddler) and **Leo** (older).

Live URL: **https://bucket-list-rho-weld.vercel.app/**
GitHub: **https://github.com/autumnhood1-fig/BucketList.git**
Branch: `main` → Vercel auto-deploys on every push

---

## Repo layout
```
Bucket/
  app/                   ← Vite+React+TS+Tailwind v4 (root for Vercel)
    src/
      data/places.json   ← THE DATA FILE — single source of truth
      types/place.ts     ← Place interface
      types/filters.ts   ← Filters interface + constants
      lib/filterPlaces.ts
      lib/categoryStyle.ts  ← CATEGORY_COLORS map + categoryColor()
      hooks/useVisited.ts
      components/
        FilterPanel.tsx
        MapView.tsx
        PlaceListView.tsx
        PlacePopup.tsx
    scripts/             ← one-off Python geocoding scripts (run from app/)
  Kid_Friendly_Places.docx   ← original hand-curated source doc (not authoritative anymore)
  CLAUDE.md              ← this file
```

---

## Tech stack
- React 19 + TypeScript + Vite + Tailwind CSS v4
- Leaflet (react-leaflet) for the map
- Places data: static JSON — no backend
- Visited state: `localStorage` key `"bucket-list-visited"`, seeded from `defaultVisited` field
- Geocoding: Nominatim/OpenStreetMap via Python scripts with 1.1s rate-limit delay
- Deploy: `git push origin main` → Vercel auto-deploys (root dir = `app`)

---

## Place schema (`src/types/place.ts`)
```ts
interface Place {
  id: string;            // kebab-case, e.g. "playground-jordan-park"
  name: string;
  category: string;      // primary category — used for map pin color
  tags?: string[];       // additional categories (multi-tag support)
  defaultVisited?: boolean; // if true, seeded as visited on first load
  city: string;
  state: string;         // 2-letter abbreviation
  driveMinutes: number | null;
  driveBucket: "<30" | "30-60" | "60-90" | "90+" | null;
  indoorOutdoor: "Indoor" | "Outdoor" | "Both";
  priceTier: "free" | "under50" | "over50" | "varies";
  priceNote: string;     // human-readable pricing
  oslFree: boolean;      // free with Ocean State Libraries museum pass
  oslNote: string | null;
  discount: boolean;     // has a discount/bundle available
  discountNote: string | null;
  seasonality: "year-round" | "warm" | "cold";
  hours: string | null;
  details: string | null;
  lat: number | null;
  lng: number | null;
}
```

**Multi-tagging**: A place can appear under multiple category filters. Set `category` to the primary category (determines pin color) and add extra categories to `tags: []`. The filter logic checks both.

**defaultVisited**: If `true`, the place is seeded as visited in localStorage on the user's first load (or if they've never explicitly toggled it). Use this for places Autumn/Evan have already been to. IDs set so far: `novel-shop-book-barn`, `beach-sandy-niantic-bay-boardwalk`.

---

## Categories and colors (`src/lib/categoryStyle.ts`)
| Category | Color |
|---|---|
| Museum / Learning Center | `#7c3aed` purple |
| Zoo / Aquarium / Animals | `#059669` green |
| Amusement / Theme Park | `#db2777` pink |
| Nature Coaster / Ride | `#ea580c` orange |
| Cave / Geology | `#78716c` warm gray |
| Splash Pad | `#0ea5e9` sky |
| Troll Hunting | `#65a30d` lime |
| Playground | `#f59e0b` amber |
| Lighthouse | `#dc2626` red |
| Farm / Pick-Your-Own | `#ca8a04` gold |
| Hiking / Nature | `#16a34a` green |
| Garden | `#22c55e` light green |
| Sculpture / Art Park | `#9333ea` violet |
| Ferry | `#2563eb` blue |
| Kayaking / Boat | `#0891b2` cyan |
| Eating + Play | `#f97316` orange |
| Novel Shop | `#a16207` amber-dark |
| Beach (Sandy) | `#facc15` yellow |
| Sea Glass Beach | `#06b6d4` cyan |
| Tide Pools | `#14b8a6` teal |
| City & Town Trip | `#6366f1` indigo |
| Movie / Drive-In | `#be185d` rose |
| Roadside Oddity | `#475569` slate |
| Roadside Attraction | `#92400e` brown |
| Spooky | `#581c87` dark purple |
| History | `#854d0e` dark amber |
| Pop Culture | `#db2777` pink |
| Indoor Play | `#ec4899` hot pink |

**To add a new category**: add an entry to `CATEGORY_COLORS` in `categoryStyle.ts` and use the exact same string as `category` or in `tags[]` in `places.json`.

---

## Drive time convention
All drive times are from **Providence, RI** (home base). Buckets:
- `<30` = under 30 min
- `30-60` = 30–60 min
- `60-90` = 60–90 min
- `90+` = over 90 min

Martha's Vineyard ferry destinations use the drive + ferry time as one combined estimate (~45 min).
Block Island ferry destinations ~100 min total.

---

## Geocoding workflow
Scripts live in `app/scripts/`. Always run them from the `app/` directory:
```bash
cd app
python3 scripts/your_script.py
```
Nominatim rate limit: **1 request/second** — the scripts sleep 1.1s between calls.
User-Agent must be set (required by Nominatim TOS).

IDs are derived: `slug(category) + '-' + slug(name)` where slug = lowercase, non-alphanumeric → `-`.

---

## Deployment workflow
1. Edit `app/src/data/places.json` (or any source file)
2. `npx tsc -b` (type-check; run from `app/`)
3. `npm run build` (verify build; run from `app/`)
4. `git add ... && git commit -m "..."` (from repo root `Bucket/`)
5. `git push` → Vercel auto-deploys

**Autumn's preference**: she is not technical — she approves all actions in Claude. She's comfortable with Claude pushing directly to main once she sees what changes are being made.

---

## Permissions (`.claude/settings.local.json`)
The project has broad auto-approvals for: Read, Edit, Write, Glob, Grep, all `Bash(python3 *)`, `Bash(npm run *)`, `Bash(npx *)`, `Bash(git *)`, `Bash(ls *)`, `Bash(cat *)`, `WebSearch`.

---

## OSL (Ocean State Libraries) pass
Many RI cultural institutions offer free or discounted admission with the OSL library museum pass (available to RI library card holders). Set `oslFree: true` and `oslNote` to describe the benefit. When `oslFree: true`, filtering by "Free" includes the place.

---

## Common discount programs to check for new places
- **NARM** (North American Reciprocal Museum) — free at all NARM member museums
- **The Trustees** membership — free at all Trustees of Reservations sites (MA)
- **Mass Audubon** membership — free at all Mass Audubon sanctuaries
- **Go City Boston** pass — may cover many Boston-area attractions
- **Blue Star Museums** — free for active military + up to 5 family members
- **Museums for All / SNAP** — free/reduced for EBT card holders
- **OSL (Ocean State Libraries)** pass — RI library card holders get free passes

---

## Current state (as of session ending ~June 30, 2026)
`places.json` has **499 entries**.

### Committed and live on Vercel
- Multi-tag support (`tags?: string[]` field, filter checks both category + tags)
- `defaultVisited?: boolean` field — seeded in localStorage on load
- New categories: Roadside Attraction, Spooky, History, Pop Culture, Indoor Play
- 17 places added from Evan's hand-curated spreadsheet (Big Blue Bug, Roger Wheeler Beach, etc.)
- 69 attribute corrections (indoor/outdoor, discount, OSL)
- Search bar (filters by name or city)
- Maine Maritime Museum added with full pricing

### PENDING — scripts written but NOT yet run
Two scripts in `app/scripts/` need to be run from `app/`:

**`add_batch_june2026.py`** — adds ~55 places:
- 26 playgrounds (15 with exact addresses in MA/NH, 11 RI playgrounds)
- 9 sandy beaches (Wingaersheek, Town Neck, Chapaquoit, Duxbury, Waterford, etc.)
- 5 sea glass beaches (Hampton, Rye Harbor, Popham, Old Orchard, Ogunquit)
- 11 lighthouses (Beavertail, Point Judith, North Light, Pomham Rocks, SE Light, Nubble, Portland Head, Nobska, Gay Head, Marshall Point, Pemaquid)
- Thimble Island trail (Branford CT), Stratham Hill Park
- Fort Wetherill (Jamestown RI), Strawberry Banke (Portsmouth NH)
- Dinosaur Place (Oakdale CT), Eastleigh Farm/Cow Safari (Framingham MA)
- Squam Lakes Natural Science Center (Holderness NH)
- Giant Chair (Gardner MA), Eartha globe (Yarmouth ME)

**`add_batch_june2026b.py`** — adds indoor play + roadside attractions:
- 6 indoor play places (Playtime RI, Sensory Play Place, Sharkbay, Little Lattes, Simply Play, Fundamentals LLC)
- Niantic Children's Museum (East Lyme CT) — mark `defaultVisited: true`
- World's Largest Uncle Sam (Danbury CT, 120 White St) 
- World's Largest Rotary Phone (Bryant Pond ME, 1 N Main St)
- Giant Coffee Pot (Bedford PA, 714 W Pitt St)
- Giant Quarter (Everett PA, Down River Golf Course)
- Pied Piper statue (Schellsburg PA, 3565 Lincoln Hwy)
- Rose Island Lighthouse (Newport RI, ferry-access only)
- Stonington Harbor Light Museum (Stonington CT), Wood Island Lighthouse (Biddeford Pool ME)
- Highland Light (Truro MA), Nauset Light (Eastham MA)
- West Quoddy Head Light (Lubec ME)

### ALSO PENDING from a big batch request (not yet scripted)
The user sent a large request that includes these categories + places still needing to be added/scripted:
- **Spooky places**: Witch's Dungeon Classic Movie Museum (Plainville CT), Salem Witch Museum, Witch History Museum, Salem Witch Board Museum, Witch Dungeon Museum, Halloween Museum of Salem, International Monster Museum, The Lost Museum (all Salem MA), VAMPA Vampire Museum (Doylestown PA), Pine Bush UFO Museum (Pine Bush NY), Paranormal Museum of NJ (Asbury Park NJ)
- **Amusement parks**: Dutch Wonderland (PA), Canobie Lake Park (NH), Land of Make Believe (NJ), Story Land (NH), Storybook Land (NJ), Fairy Tale Forest (NJ), Sesame Place (PA), Santa's Village NH (year-round), Planet Snoopy (PA)
- **History / living history**: Tag existing places appropriately; add reenactment/costumed-interpreter sites
- **Pop Culture**: Author landmarks (Stephen King house Bangor ME, HP Lovecraft Providence RI, Dr. Seuss Springfield MA, Mark Twain Hartford CT, Emily Dickinson Amherst MA), famous filming locations (Parish shoe sign Jumanji NH, Forrest Gump lighthouse already added as Marshall Point)
- **Various**: World's largest general store PA, Ringing Rocks (Bucks County PA), PA Grand Canyon, Dave Wenzel Tree House, Smith Memorial Playhouse (Philadelphia PA), Hershey's Chocolate World (Hershey PA), Treehouse Playground of Lititz PA, Traveler Books & Restaurant CT (3 free books with every meal), Paper House (Rockport MA), Four Brothers Drive-In (Amenia NY), Jenkinson's Boardwalk (NJ), Retro McDonald's (Roslyn NY), Coney Island NY, Jell-O Museum (LeRoy NY), Clear Kayak at Green Lakes State Park NY, Cayuga Nature Center treehouse NY, The Wild Center Tupper Lake NY
- **Tagging existing places**: Cryptozoology Museum ME should get "Spooky" tag; RISD Museum, Eric Carle Museum, Norman Rockwell Museum, others should get "Pop Culture" tag; Plimoth Patuxent, Mystic Seaport, whaling museums etc. should get "History" tag

---

## Gotchas / known issues
- **Nominatim won't find businesses by name** — use street addresses for geocoding, not business names. If a business name doesn't work, look up the address first.
- **The scripts must be run from `app/`** (not from repo root `Bucket/`) because they reference `src/data/places.json` as a relative path.
- **ID collisions**: The `make()` helper generates IDs as `slug(category)+'-'+slug(name)`. If two places have the same category + name slug, the second will be skipped (dedup by id). Check for near-duplicates before adding.
- **Multi-category places**: When a place should appear under more than one category filter, put the primary category in `category` (this controls pin color) and extras in `tags: []`.
- **Martha's Vineyard / Block Island**: These require ferry access. driveMinutes reflects drive + ferry combined. Note ferry cost in priceNote.
- **PA places**: Bedford PA, Everett PA, Schellsburg PA are all 6-7 hours from Providence. These are for multi-day road trips, not day trips.
- **"Spooky" Salem**: Many Salem MA spooky museums are clustered on Essex St. Several haven't been added yet. Verify they still exist before adding — Salem's small museum scene changes frequently.
- **defaultVisited seeding**: Only seeds visited on first load for that specific device/browser. Does NOT sync across devices. Each family member needs to set their own visited state.
