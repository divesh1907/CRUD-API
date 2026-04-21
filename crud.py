# crud.py
# Contains all Create, Read, Update, Delete logic.
# Works directly with the in-memory list from database.py.

import database
from models import Place, PlaceCreate, PlaceUpdate


def get_all_places() -> list[Place]:
    """Return every place in the database."""
    return database.places_db


def get_place_by_id(place_id: int) -> Place | None:
    """Find and return a single place by its ID. Returns None if not found."""
    for place in database.places_db:
        if place.id == place_id:
            return place
    return None


def create_place(data: PlaceCreate) -> Place:
    """Add a new place to the database and return it."""
    global database  # we need access to next_id counter

    # Assign a new unique ID
    new_id = database.next_id
    database.next_id += 1  # bump the counter for next time

    # Build the full Place object
    new_place = Place(
        id=new_id,
        name=data.name,
        latitude=data.latitude,
        longitude=data.longitude,
    )

    # Add to our in-memory list
    database.places_db.append(new_place)
    return new_place


def update_place(place_id: int, data: PlaceUpdate) -> Place | None:
    """Update an existing place's fields. Only updates fields that are provided."""
    for index, place in enumerate(database.places_db):
        if place.id == place_id:
            # Build an updated copy — only override fields that were provided
            updated = place.model_copy(update=data.model_dump(exclude_none=True))
            database.places_db[index] = updated
            return updated
    return None  # Not found


def delete_place(place_id: int) -> bool:
    """Remove a place from the database. Returns True if deleted, False if not found."""
    for index, place in enumerate(database.places_db):
        if place.id == place_id:
            database.places_db.pop(index)
            return True
    return False