export type PriceTier = "free" | "under50" | "over50" | "varies";
export type IndoorOutdoor = "Indoor" | "Outdoor" | "Both";
export type DriveBucket = "<30" | "30-60" | "60-90" | "90+";
export type Seasonality = "year-round" | "warm" | "cold";

export interface Place {
  id: string;
  name: string;
  category: string;
  tags?: string[];
  city: string;
  state: string;
  driveMinutes: number | null;
  driveBucket: DriveBucket | null;
  indoorOutdoor: IndoorOutdoor;
  priceTier: PriceTier;
  priceNote: string;
  oslFree: boolean;
  oslNote: string | null;
  discount: boolean;
  discountNote: string | null;
  seasonality: Seasonality;
  hours: string | null;
  details: string | null;
  lat: number | null;
  lng: number | null;
}
