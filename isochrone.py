# isochrone.py
# Handles two things:
#   1. Calling the OpenRouteService (ORS) Isochrone API to get a travel polygon
#   2. Using Shapely to check which places fall inside that polygon

import os
import requests
from shapely.geometry import shape, Point

from models import Place


# --------------------------------------------------------------------------
# ORS Isochrone API settings
# Set your API key as an environment variable:  ORS_API_KEY=your_key_here
# --------------------------------------------------------------------------
ORS_API_URL = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjY5ZGFlM2E0ZWJjZDQ5OWViNzBiMTIyODJjOGU3YzI3IiwiaCI6Im11cm11cjY0In0="
ORS_API_KEY = os.getenv("ORS_API_KEY", "")  # reads from environment, empty = mock mode


# --------------------------------------------------------------------------
# Step 1: Get the isochrone polygon from ORS (or fall back to a mock)
# --------------------------------------------------------------------------

def fetch_isochrone_polygon(lat: float, lon: float, range_minutes: int) -> dict:
    """
    Calls ORS API to get a GeoJSON polygon representing the area reachable
    within `range_minutes` minutes of driving from (lat, lon).

    If no API key is set, returns a mock square polygon for testing.
    """

    if not ORS_API_KEY:
        # ---- MOCK MODE ----
        # Return a simple square bounding box (~2 km around the point).
        # Good enough for local testing without an API key.
        print("⚠️  No ORS_API_KEY found — using mock polygon (square ~2 km around point).")
        delta = 0.02  # roughly 2 km
        mock_polygon = {
            "type": "Polygon",
            "coordinates": [[
                [lon - delta, lat - delta],
                [lon + delta, lat - delta],
                [lon + delta, lat + delta],
                [lon - delta, lat + delta],
                [lon - delta, lat - delta],  # close the ring
            ]]
        }
        return mock_polygon

    # ---- REAL ORS CALL ----
    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json",
    }
    body = {
        "locations": [[lon, lat]],          # ORS expects [longitude, latitude]
        "range": [range_minutes * 60],       # ORS uses seconds, not minutes
        "range_type": "time",
    }

    response = requests.post(ORS_API_URL, json=body, headers=headers, timeout=10)
    response.raise_for_status()             # raises exception for HTTP errors

    geojson = response.json()

    # ORS returns a FeatureCollection; we want the first feature's geometry
    polygon_geometry = geojson["features"][0]["geometry"]
    return polygon_geometry


# --------------------------------------------------------------------------
# Step 2: Filter places that lie inside the polygon
# --------------------------------------------------------------------------

def filter_places_in_polygon(places: list[Place], polygon_geojson: dict) -> list[Place]:
    """
    Given a list of places and a GeoJSON polygon, returns only the places
    whose coordinates fall inside the polygon.

    Uses Shapely:
      - `shape()` converts GeoJSON dict → Shapely geometry object
      - `Point()` represents a single lat/lon coordinate
      - `.contains()` checks if the polygon includes the point
    """

    # Convert GeoJSON polygon dict → Shapely shape object
    polygon = shape(polygon_geojson)

    inside = []
    for place in places:
        # Create a Shapely Point — note: (longitude, latitude) order for geo
        point = Point(place.longitude, place.latitude)

        if polygon.contains(point):
            inside.append(place)

    return inside


# --------------------------------------------------------------------------
# Convenience wrapper used by the API endpoint
# --------------------------------------------------------------------------

def get_places_within_isochrone(
    lat: float,
    lon: float,
    range_minutes: int,
    all_places: list[Place],
) -> list[Place]:
    """
    Full pipeline:
      1. Fetch isochrone polygon from ORS (or mock)
      2. Filter places inside that polygon
      3. Return matching places
    """
    polygon = fetch_isochrone_polygon(lat, lon, range_minutes)
    return filter_places_in_polygon(all_places, polygon)