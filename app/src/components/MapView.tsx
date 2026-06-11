import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import MarkerClusterGroup from "react-leaflet-cluster";
import type { Place } from "../types/place";
import { HOME } from "../lib/constants";
import { placeIcon, homeIcon } from "../lib/icons";
import { PlacePopup } from "./PlacePopup";

interface Props {
  places: Place[];
  isVisited: (id: string) => boolean;
  toggleVisited: (id: string) => void;
}

export function MapView({ places, isVisited, toggleVisited }: Props) {
  return (
    <MapContainer
      center={[HOME.lat, HOME.lng]}
      zoom={9}
      scrollWheelZoom
      className="h-full w-full"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <Marker position={[HOME.lat, HOME.lng]} icon={homeIcon()}>
        <Popup>
          <div className="font-semibold">{HOME.name}</div>
          <div className="text-sm text-gray-500">{HOME.address}</div>
        </Popup>
      </Marker>

      <MarkerClusterGroup chunkedLoading maxClusterRadius={50}>
        {places
          .filter((p) => p.lat != null && p.lng != null)
          .map((place) => (
            <Marker
              key={place.id}
              position={[place.lat as number, place.lng as number]}
              icon={placeIcon(place.category, isVisited(place.id))}
            >
              <Popup>
                <PlacePopup
                  place={place}
                  visited={isVisited(place.id)}
                  onToggleVisited={toggleVisited}
                />
              </Popup>
            </Marker>
          ))}
      </MarkerClusterGroup>
    </MapContainer>
  );
}
