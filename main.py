from fastapi import FastAPI, HTTPException, Query

import crud
import database
from isochrone import get_places_within_isochrone
from models import Place, PlaceCreate, PlaceUpdate

# Create the FastAPI app

app = FastAPI(
    title="Places API with Isochrone Filtering",
    description=(
        "A beginner-friendly REST API to manage places (cafes, hospitals, etc.) "
        "and filter them by travel-time radius using isochrone polygons."
    ),
    version="1.0.0",
)

# Root — health check


@app.get("/", tags=["Health"])
def root():
    """Simple health-check endpoint."""
    return {"message": "Places API is running! Visit /docs for the interactive UI."}


# CRUD — Create

@app.post("/places", response_model=Place, status_code=201, tags=["Places"])
def add_place(data: PlaceCreate):
    """
    Add a new place.

    Send a JSON body with:
    - name (string)
    - latitude (float)
    - longitude (float)
    """
    new_place = crud.create_place(data)
    return new_place


# CRUD — Read All

@app.get("/places", response_model=list[Place], tags=["Places"])
def list_places():
    """Return all places stored in the database."""
    return crud.get_all_places()

# CRUD — Read One

@app.get("/places/{place_id}", response_model=Place, tags=["Places"])
def get_place(place_id: int):
    """Return a single place by ID. Raises 404 if not found."""
    place = crud.get_place_by_id(place_id)
    if not place:
        raise HTTPException(status_code=404, detail=f"Place with id={place_id} not found.")
    return place

# CRUD — Update

@app.put("/places/{place_id}", response_model=Place, tags=["Places"])
def update_place(place_id: int, data: PlaceUpdate):
    """
    Update one or more fields of an existing place.
    Only the fields you send will be updated.
    """
    updated = crud.update_place(place_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Place with id={place_id} not found.")
    return updated

# CRUD — Delete

@app.delete("/places/{place_id}", tags=["Places"])
def delete_place(place_id: int):
    """Delete a place by ID. Returns a confirmation message."""
    success = crud.delete_place(place_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Place with id={place_id} not found.")
    return {"message": f"Place {place_id} deleted successfully."}

# Isochrone — Filter places by travel-time radius

@app.get("/places/isochrone/filter", response_model=list[Place], tags=["Isochrone"])
def places_in_isochrone(
    lat: float = Query(..., description="Latitude of the origin point", example=17.4126),
    lon: float = Query(..., description="Longitude of the origin point", example=78.4483),
    range: int = Query(..., description="Travel-time radius in minutes", example=10, ge=1, le=60),
):
    """ Return all places reachable within `range` minutes of driving from (lat, lon) """
    
    all_places = database.places_db
    matching = get_places_within_isochrone(lat, lon, range, all_places)
    return matching
