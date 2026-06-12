import { useMemo, useState } from "react";
import placesData from "./data/places.json";
import type { Place } from "./types/place";
import { EMPTY_FILTERS, type Filters } from "./types/filters";
import { MapView } from "./components/MapView";
import { PlaceListView } from "./components/PlaceListView";
import { FilterPanel } from "./components/FilterPanel";
import { useVisited } from "./hooks/useVisited";
import { placeMatchesFilters } from "./lib/filterPlaces";

const places = placesData as Place[];

const CATEGORIES = Array.from(
  new Set(places.flatMap((p) => [p.category, ...(p.tags ?? [])])),
).sort();
const STATES = Array.from(new Set(places.map((p) => p.state).filter(Boolean))).sort();

function App() {
  const [filters, setFilters] = useState<Filters>(EMPTY_FILTERS);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [viewMode, setViewMode] = useState<"map" | "list">("map");
  const { isVisited, toggleVisited } = useVisited();

  const filteredPlaces = useMemo(
    () => places.filter((p) => placeMatchesFilters(p, filters, isVisited)),
    [filters, isVisited],
  );

  return (
    <div className="flex h-dvh w-full flex-col md:flex-row">
      {/* Header (mobile only) */}
      <header className="flex items-center justify-between border-b border-gray-200 bg-white px-4 py-3 md:hidden">
        <h1 className="text-lg font-bold text-gray-900">New England Bucket List</h1>
        <div className="flex items-center gap-2">
          <ViewToggle viewMode={viewMode} onChange={setViewMode} />
          <button
            className="rounded-md bg-blue-600 px-3 py-1.5 text-sm font-medium text-white"
            onClick={() => setDrawerOpen(true)}
          >
            Filters
          </button>
        </div>
      </header>

      {/* Sidebar (desktop) */}
      <aside className="hidden w-80 shrink-0 border-r border-gray-200 bg-white md:flex md:flex-col">
        <div className="border-b border-gray-200 px-4 py-4">
          <h1 className="text-xl font-bold text-gray-900">New England Bucket List</h1>
          <p className="text-sm text-gray-500">Family adventures near Providence, RI</p>
        </div>
        <FilterPanel
          filters={filters}
          onChange={setFilters}
          categories={CATEGORIES}
          states={STATES}
          resultCount={filteredPlaces.length}
          totalCount={places.length}
        />
      </aside>

      {/* Map / List */}
      <main className="relative flex-1">
        <div className="absolute top-3 right-3 z-[1000] hidden md:block">
          <ViewToggle viewMode={viewMode} onChange={setViewMode} />
        </div>
        {viewMode === "map" ? (
          <MapView places={filteredPlaces} isVisited={isVisited} toggleVisited={toggleVisited} />
        ) : (
          <PlaceListView places={filteredPlaces} isVisited={isVisited} toggleVisited={toggleVisited} />
        )}
      </main>

      {/* Mobile drawer */}
      {drawerOpen && (
        <div className="fixed inset-0 z-[1000] flex md:hidden">
          <div
            className="absolute inset-0 bg-black/30"
            onClick={() => setDrawerOpen(false)}
          />
          <div className="relative ml-auto flex h-full w-[85%] max-w-sm flex-col bg-white shadow-xl">
            <div className="flex items-center justify-end border-b border-gray-200 px-4 py-2">
              <button
                className="text-sm font-medium text-gray-500"
                onClick={() => setDrawerOpen(false)}
              >
                Close ✕
              </button>
            </div>
            <FilterPanel
              filters={filters}
              onChange={setFilters}
              categories={CATEGORIES}
              states={STATES}
              resultCount={filteredPlaces.length}
              totalCount={places.length}
            />
          </div>
        </div>
      )}
    </div>
  );
}

function ViewToggle({
  viewMode,
  onChange,
}: {
  viewMode: "map" | "list";
  onChange: (mode: "map" | "list") => void;
}) {
  return (
    <div className="flex rounded-md border border-gray-200 bg-white p-0.5 shadow-sm">
      {(["map", "list"] as const).map((mode) => (
        <button
          key={mode}
          onClick={() => onChange(mode)}
          className={`rounded px-3 py-1 text-sm font-medium capitalize ${
            viewMode === mode ? "bg-blue-600 text-white" : "text-gray-600 hover:bg-gray-100"
          }`}
        >
          {mode}
        </button>
      ))}
    </div>
  );
}

export default App;
