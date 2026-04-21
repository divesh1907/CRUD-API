# database.py
# This acts as our "database" — just a Python list stored in memory.
# All data is lost when the server restarts (no real DB needed for this project).

from models import Place

# --------------------------------------------------------------------------
# Sample places in Hyderabad, India (realistic coordinates)
# --------------------------------------------------------------------------
places_db: list[Place] = [
    Place(id=1,  name="Cafe Coffee Day - Banjara Hills",  latitude=17.4126, longitude=78.4483),
    Place(id=2,  name="Apollo Hospital - Jubilee Hills",   latitude=17.4239, longitude=78.4738),
    Place(id=3,  name="Kendriya Vidyalaya - Begumpet",     latitude=17.4432, longitude=78.4671),
    Place(id=4,  name="GVK One Mall - Banjara Hills",      latitude=17.4200, longitude=78.4482),
    Place(id=5,  name="Charminar",                          latitude=17.3616, longitude=78.4747),
    Place(id=6,  name="IKEA Hyderabad - HITEC City",       latitude=17.4435, longitude=78.3772),
    Place(id=7,  name="Hussain Sagar Lake",                 latitude=17.4239, longitude=78.4738),
    Place(id=8,  name="Birla Mandir",                       latitude=17.4062, longitude=78.4691),
    Place(id=9,  name="Golconda Fort",                      latitude=17.3833, longitude=78.4011),
    Place(id=10, name="Inorbit Mall - HITEC City",          latitude=17.4344, longitude=78.3815),
]

# Counter to generate unique IDs for new places
next_id: int = 11