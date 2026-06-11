import type { DriveBucket, IndoorOutdoor, PriceTier, Seasonality } from "./place";

export type VisitedFilter = "all" | "visited" | "not-visited";
export type SeasonFilter = Seasonality;

export interface Filters {
  categories: string[];
  indoorOutdoor: IndoorOutdoor[];
  priceTiers: PriceTier[];
  discountOnly: boolean;
  seasonality: SeasonFilter[];
  states: string[];
  driveBuckets: DriveBucket[];
  visited: VisitedFilter;
}

export const EMPTY_FILTERS: Filters = {
  categories: [],
  indoorOutdoor: [],
  priceTiers: [],
  discountOnly: false,
  seasonality: [],
  states: [],
  driveBuckets: [],
  visited: "all",
};

export const DRIVE_BUCKETS: DriveBucket[] = ["<30", "30-60", "60-90", "90+"];
export const DRIVE_BUCKET_LABELS: Record<DriveBucket, string> = {
  "<30": "< 30 min",
  "30-60": "30-60 min",
  "60-90": "60-90 min",
  "90+": "90+ min",
};

export const PRICE_TIERS: PriceTier[] = ["free", "under50", "over50"];
export const PRICE_TIER_LABELS: Record<PriceTier, string> = {
  free: "Free",
  under50: "Under $50",
  over50: "Over $50",
  varies: "Varies",
};

export const INDOOR_OUTDOOR_OPTIONS: IndoorOutdoor[] = ["Indoor", "Outdoor", "Both"];

export const SEASON_FILTERS: SeasonFilter[] = ["year-round", "warm", "cold"];
export const SEASON_LABELS: Record<SeasonFilter, string> = {
  "year-round": "Year-round",
  warm: "Warm weather",
  cold: "Cold weather",
};
