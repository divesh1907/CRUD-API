import os
import requests
from dotenv import load_dotenv
from shapely.geometry import shape, Point

from models import Place

load_dotenv()

MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY", "")

# --------------------------------------------------------------------------
# Step 1: Fetch isochrone polygon from Mapbox
# --------------------------------------------------------------------------

def fetch_isochrone_polygon(lat: float, lon: float, range_minutes: int) -> dict:
    """
    Calls Mapbox Isochrone API and returns polygon GeoJSON.
    """

    if not MAPBOX_API_KEY:
        print("⚠️ No MAPBOX_API_KEY found — using mock polygon")
        return mock_polygon(lat, lon)

    try:
        # Mapbox expects minutes directly
        url = f"https://api.mapbox.com/isochrone/v1/mapbox/driving/{lon},{lat}"

        params = {
            "contours_minutes": range_minutes,
            "polygons": "true",
            "access_token": MAPBOX_API_KEY,
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        return data["features"][0]["geometry"]

    except Exception as e:
        print(f"❌ Mapbox error: {e}")
        print("⚠️ Falling back to mock polygon")
        return mock_polygon(lat, lon)


# --------------------------------------------------------------------------
# Mock fallback (still useful)
# --------------------------------------------------------------------------

def mock_polygon(lat, lon):
    delta = 0.02
    return {
        "type": "Polygon",
        "coordinates": [[
            [lon - delta, lat - delta],
            [lon + delta, lat - delta],
            [lon + delta, lat + delta],
            [lon - delta, lat + delta],
            [lon - delta, lat - delta],
        ]]
    }


# --------------------------------------------------------------------------
# Step 2: Filter places inside polygon
# --------------------------------------------------------------------------

def filter_places_in_polygon(places: list[Place], polygon_geojson: dict) -> list[Place]:
    polygon = shape(polygon_geojson)

    inside = []
    for place in places:
        point = Point(place.longitude, place.latitude)

        if polygon.contains(point):
            inside.append(place)

    return inside


# --------------------------------------------------------------------------
# Main wrapper
# --------------------------------------------------------------------------

def get_places_within_isochrone(
    lat: float,
    lon: float,
    range_minutes: int,
    all_places: list[Place],
) -> list[Place]:

    polygon = fetch_isochrone_polygon(lat, lon, range_minutes)
    return filter_places_in_polygon(all_places, polygon)