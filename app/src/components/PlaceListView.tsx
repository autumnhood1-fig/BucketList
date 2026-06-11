import type { Place } from "../types/place";
import { PRICE_TIER_LABELS, SEASON_LABELS } from "../types/filters";
import { categoryColor } from "../lib/categoryStyle";

interface Props {
  places: Place[];
  isVisited: (id: string) => boolean;
  toggleVisited: (id: string) => void;
}

export function PlaceListView({ places, isVisited, toggleVisited }: Props) {
  const sorted = [...places].sort((a, b) => (a.driveMinutes ?? Infinity) - (b.driveMinutes ?? Infinity));

  if (sorted.length === 0) {
    return (
      <div className="flex h-full items-center justify-center p-8 pt-20 text-center text-gray-500">
        No places match the current filters.
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto bg-gray-50 pt-12">
      <ul className="divide-y divide-gray-200">
        {sorted.map((place) => {
          const visited = isVisited(place.id);
          return (
            <li key={place.id} className="bg-white px-4 py-3">
              <div className="flex items-start justify-between gap-2">
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <span
                      className="inline-block h-2.5 w-2.5 shrink-0 rounded-full"
                      style={{ background: categoryColor(place.category) }}
                    />
                    <span className="truncate font-semibold text-gray-900">{place.name}</span>
                  </div>
                  <div className="mt-0.5 text-sm text-gray-500">
                    {place.city}
                    {place.state ? `, ${place.state}` : ""}
                    {place.driveMinutes != null && <span> · ~{place.driveMinutes} min drive</span>}
                  </div>
                  <div className="mt-1.5 flex flex-wrap gap-1">
                    <span className="rounded bg-gray-100 px-1.5 py-0.5 text-xs text-gray-700">
                      {place.category}
                    </span>
                    <span className="rounded bg-gray-100 px-1.5 py-0.5 text-xs text-gray-700">
                      {place.indoorOutdoor}
                    </span>
                    <span className="rounded bg-gray-100 px-1.5 py-0.5 text-xs text-gray-700">
                      {PRICE_TIER_LABELS[place.priceTier]}
                      {place.oslFree && "*"}
                    </span>
                    {place.discount && (
                      <span className="rounded bg-amber-100 px-1.5 py-0.5 text-xs text-amber-800">
                        Discount/Bundle
                      </span>
                    )}
                    <span className="rounded bg-gray-100 px-1.5 py-0.5 text-xs text-gray-700">
                      {SEASON_LABELS[place.seasonality]}
                    </span>
                  </div>
                  {place.details && (
                    <p className="mt-1.5 text-sm text-gray-600">{place.details}</p>
                  )}
                </div>
                <label className="flex shrink-0 cursor-pointer select-none items-center gap-1.5 pt-0.5">
                  <input
                    type="checkbox"
                    checked={visited}
                    onChange={() => toggleVisited(place.id)}
                    className="h-4 w-4"
                  />
                  <span className="text-xs font-medium text-gray-600">Visited</span>
                </label>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
