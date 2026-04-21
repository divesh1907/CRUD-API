from fastapi import FastAPI, HTTPException, Query
from typing import List

from models import Place
from database import places_db, next_id
from isochrone import get_places_within_isochrone

app = FastAPI(title="Places API with Isochrone Filtering")


# --------------------------------------------------------------------------
# ROOT
# --------------------------------------------------------------------------

@app.get("/")
def root():
    return {"message": "Welcome to Places API 🚀"}


# --------------------------------------------------------------------------
# GET ALL PLACES
# --------------------------------------------------------------------------

@app.get("/places", response_model=List[Place])
def get_places():
    return places_db


# --------------------------------------------------------------------------
# GET PLACE BY ID
# --------------------------------------------------------------------------

@app.get("/places/{place_id}", response_model=Place)
def get_place(place_id: int):
    for place in places_db:
        if place.id == place_id:
            return place
    raise HTTPException(status_code=404, detail="Place not found")


# --------------------------------------------------------------------------
# CREATE PLACE
# --------------------------------------------------------------------------

@app.post("/places", response_model=Place)
def create_place(place: Place):
    global next_id

    new_place = Place(
        id=next_id,
        name=place.name,
        latitude=place.latitude,
        longitude=place.longitude,
    )

    places_db.append(new_place)
    next_id += 1

    return new_place


# --------------------------------------------------------------------------
# UPDATE PLACE
# --------------------------------------------------------------------------

@app.put("/places/{place_id}", response_model=Place)
def update_place(place_id: int, updated_place: Place):
    for index, place in enumerate(places_db):
        if place.id == place_id:
            updated_place.id = place_id
            places_db[index] = updated_place
            return updated_place

    raise HTTPException(status_code=404, detail="Place not found")


# --------------------------------------------------------------------------
# DELETE PLACE
# --------------------------------------------------------------------------

@app.delete("/places/{place_id}")
def delete_place(place_id: int):
    for index, place in enumerate(places_db):
        if place.id == place_id:
            places_db.pop(index)
            return {"message": "Place deleted successfully"}

    raise HTTPException(status_code=404, detail="Place not found")


# --------------------------------------------------------------------------
# ISOCHRONE FILTER (MAIN FEATURE)
# --------------------------------------------------------------------------

@app.get("/places/isochrone/filter", response_model=List[Place])
def filter_places_by_isochrone(
    lat: float,
    lon: float,
    range: int = Query(..., ge=1, le=60)
):
    """
    Returns places reachable within X minutes from given location.
    """

    return get_places_within_isochrone(
        lat=lat,
        lon=lon,
        range_minutes=range,
        all_places=places_db
    )


# --------------------------------------------------------------------------
# OPTIONAL: SEARCH BY NAME
# --------------------------------------------------------------------------

@app.get("/places/search", response_model=List[Place])
def search_places(q: str):
    return [
        place for place in places_db
        if q.lower() in place.name.lower()
    ]