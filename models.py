# models.py
# Pydantic models define the shape and validation rules for our data.

from pydantic import BaseModel
from typing import Optional


class Place(BaseModel):
    """Represents a physical location (e.g., cafe, hospital, school)."""
    id: int
    name: str
    latitude: float
    longitude: float


class PlaceCreate(BaseModel):
    """Used when creating a new place (no ID needed — it's assigned automatically)."""
    name: str
    latitude: float
    longitude: float


class PlaceUpdate(BaseModel):
    """Used when updating a place. All fields are optional so you can update just one."""
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None