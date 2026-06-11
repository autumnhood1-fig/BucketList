import L from "leaflet";
import { categoryColor } from "./categoryStyle";

const iconCache = new Map<string, L.DivIcon>();

export function placeIcon(category: string, visited: boolean): L.DivIcon {
  const key = `${category}-${visited}`;
  const cached = iconCache.get(key);
  if (cached) return cached;

  const color = categoryColor(category);
  const html = `
    <div style="
      width: 22px; height: 22px; border-radius: 50% 50% 50% 0;
      background: ${color};
      transform: rotate(-45deg);
      border: 2px solid white;
      box-shadow: 0 1px 3px rgba(0,0,0,0.4);
      ${visited ? "opacity: 0.45;" : ""}
    ">
      ${visited ? `<div style="
        transform: rotate(45deg);
        color: white; font-size: 12px; font-weight: bold;
        display:flex; align-items:center; justify-content:center;
        width:100%; height:100%;
      ">✓</div>` : ""}
    </div>`;

  const icon = L.divIcon({
    html,
    className: "place-marker",
    iconSize: [22, 22],
    iconAnchor: [11, 22],
    popupAnchor: [0, -22],
  });
  iconCache.set(key, icon);
  return icon;
}

export function homeIcon(): L.DivIcon {
  return L.divIcon({
    html: `
      <div style="
        width: 28px; height: 28px; border-radius: 50%;
        background: #1d4ed8; border: 3px solid white;
        box-shadow: 0 1px 4px rgba(0,0,0,0.5);
        display:flex; align-items:center; justify-content:center;
        font-size: 14px;
      ">🏠</div>`,
    className: "home-marker",
    iconSize: [28, 28],
    iconAnchor: [14, 14],
  });
}
