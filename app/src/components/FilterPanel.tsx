import type { Filters, VisitedFilter } from "../types/filters";
import {
  DRIVE_BUCKETS,
  DRIVE_BUCKET_LABELS,
  EMPTY_FILTERS,
  INDOOR_OUTDOOR_OPTIONS,
  PRICE_TIERS,
  PRICE_TIER_LABELS,
  SEASON_FILTERS,
  SEASON_LABELS,
} from "../types/filters";
import type { DriveBucket, IndoorOutdoor, PriceTier } from "../types/place";
import { FilterSection } from "./FilterSection";
import { Checkbox } from "./Checkbox";
import { categoryColor } from "../lib/categoryStyle";

interface Props {
  filters: Filters;
  onChange: (filters: Filters) => void;
  categories: string[];
  states: string[];
  resultCount: number;
  totalCount: number;
}

function toggleItem<T>(list: T[], item: T): T[] {
  return list.includes(item) ? list.filter((i) => i !== item) : [...list, item];
}

export function FilterPanel({ filters, onChange, categories, states, resultCount, totalCount }: Props) {
  const set = <K extends keyof Filters>(key: K, value: Filters[K]) =>
    onChange({ ...filters, [key]: value });

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between px-4 pt-4 pb-2">
        <h2 className="text-lg font-bold text-gray-900">Filters</h2>
        <button
          className="text-xs font-medium text-blue-600 hover:underline"
          onClick={() => onChange(EMPTY_FILTERS)}
        >
          Reset all
        </button>
      </div>
      <div className="px-4 pb-2 text-sm text-gray-500">
        Showing <span className="font-semibold text-gray-800">{resultCount}</span> of {totalCount}
      </div>

      <div className="flex-1 overflow-y-auto px-4 pb-8">
        <FilterSection title="Visited">
          <div className="flex gap-1">
            {(["all", "not-visited", "visited"] as VisitedFilter[]).map((v) => (
              <button
                key={v}
                onClick={() => set("visited", v)}
                className={`flex-1 rounded px-2 py-1 text-xs font-medium capitalize ${
                  filters.visited === v
                    ? "bg-blue-600 text-white"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                }`}
              >
                {v === "all" ? "All" : v === "not-visited" ? "Not visited" : "Visited"}
              </button>
            ))}
          </div>
        </FilterSection>

        <FilterSection title="Drive Time from Home">
          {DRIVE_BUCKETS.map((b: DriveBucket) => (
            <Checkbox
              key={b}
              label={DRIVE_BUCKET_LABELS[b]}
              checked={filters.driveBuckets.includes(b)}
              onChange={() => set("driveBuckets", toggleItem(filters.driveBuckets, b))}
            />
          ))}
        </FilterSection>

        <FilterSection title="Category" defaultOpen={false}>
          {categories.map((c) => (
            <Checkbox
              key={c}
              label={c}
              swatch={categoryColor(c)}
              checked={filters.categories.includes(c)}
              onChange={() => set("categories", toggleItem(filters.categories, c))}
            />
          ))}
        </FilterSection>

        <FilterSection title="Indoor / Outdoor">
          {INDOOR_OUTDOOR_OPTIONS.map((o: IndoorOutdoor) => (
            <Checkbox
              key={o}
              label={o}
              checked={filters.indoorOutdoor.includes(o)}
              onChange={() => set("indoorOutdoor", toggleItem(filters.indoorOutdoor, o))}
            />
          ))}
        </FilterSection>

        <FilterSection title="Price">
          {PRICE_TIERS.map((p: PriceTier) => (
            <Checkbox
              key={p}
              label={p === "free" ? "Free (incl. OSL pass*)" : PRICE_TIER_LABELS[p]}
              checked={filters.priceTiers.includes(p)}
              onChange={() => set("priceTiers", toggleItem(filters.priceTiers, p))}
            />
          ))}
          <div className="pt-1 text-xs text-gray-400">
            *Includes places that are free with the OSL library museum pass
          </div>
        </FilterSection>

        <FilterSection title="Discount / Bundle">
          <Checkbox
            label="Has a discount or bundle deal"
            checked={filters.discountOnly}
            onChange={() => set("discountOnly", !filters.discountOnly)}
          />
        </FilterSection>

        <FilterSection title="Seasonality">
          {SEASON_FILTERS.map((s) => (
            <Checkbox
              key={s}
              label={SEASON_LABELS[s]}
              checked={filters.seasonality.includes(s)}
              onChange={() => set("seasonality", toggleItem(filters.seasonality, s))}
            />
          ))}
        </FilterSection>

        <FilterSection title="State" defaultOpen={false}>
          {states.map((s) => (
            <Checkbox
              key={s}
              label={s}
              checked={filters.states.includes(s)}
              onChange={() => set("states", toggleItem(filters.states, s))}
            />
          ))}
        </FilterSection>
      </div>
    </div>
  );
}
