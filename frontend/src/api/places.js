import apiClient from "./client";

export function fetchPlaces() {
  return apiClient.get("/places").then((res) => res.data);
}

export function fetchPlace(placeId) {
  return apiClient.get(`/places/${placeId}`).then((res) => res.data);
}
