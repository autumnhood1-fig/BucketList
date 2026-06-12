import type { Place } from "../types/place";
import type { Filters } from "../types/filters";

export function placeMatchesFilters(
  place: Place,
  filters: Filters,
  isVisited: (id: string) => boolean,
): boolean {
  if (filters.search.trim()) {
    const query = filters.search.trim().toLowerCase();
    const matches =
      place.name.toLowerCase().includes(query) || place.city.toLowerCase().includes(query);
    if (!matches) return false;
  }

  if (filters.categories.length) {
    const placeCategories = [place.category, ...(place.tags ?? [])];
    if (!filters.categories.some((c) => placeCategories.includes(c))) {
      return false;
    }
  }

  if (filters.indoorOutdoor.length && !filters.indoorOutdoor.includes(place.indoorOutdoor)) {
    return false;
  }

  if (filters.priceTiers.length) {
    const matchesPrice = filters.priceTiers.some((tier) => {
      if (tier === "free") return place.priceTier === "free" || place.oslFree;
      return place.priceTier === tier;
    });
    if (!matchesPrice) return false;
  }

  if (filters.discountOnly && !place.discount) {
    return false;
  }

  if (filters.seasonality.length && !filters.seasonality.includes(place.seasonality)) {
    return false;
  }

  if (filters.states.length && !filters.states.includes(place.state)) {
    return false;
  }

  if (filters.driveBuckets.length) {
    if (!place.driveBucket || !filters.driveBuckets.includes(place.driveBucket)) {
      return false;
    }
  }

  if (filters.visited !== "all") {
    const v = isVisited(place.id);
    if (filters.visited === "visited" && !v) return false;
    if (filters.visited === "not-visited" && v) return false;
  }

  return true;
}
