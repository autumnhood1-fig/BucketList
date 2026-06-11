import type { Place } from "../types/place";
import { PRICE_TIER_LABELS } from "../types/filters";

interface Props {
  place: Place;
  visited: boolean;
  onToggleVisited: (id: string) => void;
}

export function PlacePopup({ place, visited, onToggleVisited }: Props) {
  return (
    <div className="min-w-[220px] max-w-[280px] text-sm">
      <div className="font-semibold text-base mb-0.5">{place.name}</div>
      <div className="text-gray-500 mb-1">
        {place.city}{place.state ? `, ${place.state}` : ""}
        {place.driveMinutes != null && (
          <span> · ~{place.driveMinutes} min drive</span>
        )}
      </div>

      <div className="flex flex-wrap gap-1 mb-2">
        <span className="px-1.5 py-0.5 rounded bg-gray-100 text-gray-700 text-xs">
          {place.indoorOutdoor}
        </span>
        <span className="px-1.5 py-0.5 rounded bg-gray-100 text-gray-700 text-xs">
          {PRICE_TIER_LABELS[place.priceTier]}
          {place.oslFree && "*"}
        </span>
        {place.discount && (
          <span className="px-1.5 py-0.5 rounded bg-amber-100 text-amber-800 text-xs">
            Discount/Bundle
          </span>
        )}
        <span className="px-1.5 py-0.5 rounded bg-gray-100 text-gray-700 text-xs">
          {place.seasonal ? "Seasonal" : "Year-round"}
        </span>
      </div>

      <div className="space-y-1 text-gray-700">
        <div><span className="font-medium">Cost:</span> {place.priceNote}</div>
        {place.oslNote && (
          <div>
            <span className="font-medium">OSL / Library Pass:</span> {place.oslNote}
          </div>
        )}
        {place.discountNote && (
          <div>
            <span className="font-medium">Discount:</span> {place.discountNote}
          </div>
        )}
        {place.hours && (
          <div><span className="font-medium">Hours:</span> {place.hours}</div>
        )}
        {place.details && <div>{place.details}</div>}
        {place.oslFree && (
          <div className="text-xs text-gray-400">
            *Free with the OSL library museum pass (subject to availability)
          </div>
        )}
      </div>

      <label className="mt-3 flex items-center gap-2 cursor-pointer select-none">
        <input
          type="checkbox"
          checked={visited}
          onChange={() => onToggleVisited(place.id)}
          className="h-4 w-4"
        />
        <span className="text-sm font-medium">Visited</span>
      </label>
    </div>
  );
}
