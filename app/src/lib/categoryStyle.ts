// Color per category, used for map markers and filter chips.
export const CATEGORY_COLORS: Record<string, string> = {
  "Museum / Learning Center": "#7c3aed",
  "Zoo / Aquarium / Animals": "#059669",
  "Amusement / Theme Park": "#db2777",
  "Nature Coaster / Ride": "#ea580c",
  "Cave / Geology": "#78716c",
  "Splash Pad": "#0ea5e9",
  "Troll Hunting": "#65a30d",
  "Playground": "#f59e0b",
  "Lighthouse": "#dc2626",
  "Farm / Pick-Your-Own": "#ca8a04",
  "Hiking / Nature": "#16a34a",
  "Garden": "#22c55e",
  "Sculpture / Art Park": "#9333ea",
  "Ferry": "#2563eb",
  "Kayaking / Boat": "#0891b2",
  "Eating + Play": "#f97316",
  "Novel Shop": "#a16207",
  "Beach (Sandy)": "#facc15",
  "Sea Glass Beach": "#06b6d4",
  "Tide Pools": "#14b8a6",
  "City & Town Trip": "#6366f1",
};

export const DEFAULT_COLOR = "#6b7280";

export function categoryColor(category: string): string {
  return CATEGORY_COLORS[category] ?? DEFAULT_COLOR;
}
