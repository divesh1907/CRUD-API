# 📍 Places API with Isochrone Filtering

A beginner-friendly **FastAPI** project that combines basic CRUD operations with **isochrone-based geo-filtering** — find which places are reachable within X minutes of driving from any point.

---

## 🗂 Project Structure

```
fastapi-isochrone/
│
├── main.py          # FastAPI app + all route definitions
├── models.py        # Pydantic schemas (Place, PlaceCreate, PlaceUpdate)
├── database.py      # In-memory list of places (10 sample Hyderabad locations)
├── crud.py          # CRUD helper functions
├── isochrone.py     # ORS API call + Shapely polygon filtering
│
├── requirements.txt # Python dependencies
└── README.md        # This file
```

---

## ⚙️ Setup & Installation

### 1. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Set your OpenRouteService API key
Get a free key at https://openrouteservice.org/dev/#/signup

```bash
export ORS_API_KEY=your_key_here        # Mac/Linux
set ORS_API_KEY=your_key_here           # Windows CMD
$env:ORS_API_KEY="your_key_here"        # Windows PowerShell
```

> **Without a key:** The app still works using a mock square polygon (~2 km around your point).

### 4. Run the server
```bash
uvicorn main:app --reload
```

The server starts at: **http://127.0.0.1:8000**

---

## 📖 Interactive API Docs

FastAPI auto-generates a web UI where you can test every endpoint:

| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000/docs | Swagger UI (click & test) |
| http://127.0.0.1:8000/redoc | ReDoc (clean reference) |

---

## 🔌 API Endpoints

### CRUD

| Method | URL | Description |
|--------|-----|-------------|
| `GET` | `/places` | Get all places |
| `GET` | `/places/{id}` | Get one place by ID |
| `POST` | `/places` | Add a new place |
| `PUT` | `/places/{id}` | Update a place |
| `DELETE` | `/places/{id}` | Delete a place |

### Isochrone

| Method | URL | Description |
|--------|-----|-------------|
| `GET` | `/places/isochrone/filter?lat=...&lon=...&range=...` | Places reachable within N minutes |

---

## 🧪 Example API Requests

### Get all places
```bash
curl http://127.0.0.1:8000/places
```

**Response:**
```json
[
  { "id": 1, "name": "Cafe Coffee Day - Banjara Hills", "latitude": 17.4126, "longitude": 78.4483 },
  { "id": 2, "name": "Apollo Hospital - Jubilee Hills",  "latitude": 17.4239, "longitude": 78.4738 },
  ...
]
```

---

### Get one place
```bash
curl http://127.0.0.1:8000/places/3
```

**Response:**
```json
{ "id": 3, "name": "Kendriya Vidyalaya - Begumpet", "latitude": 17.4432, "longitude": 78.4671 }
```

---

### Add a new place
```bash
curl -X POST http://127.0.0.1:8000/places \
  -H "Content-Type: application/json" \
  -d '{"name": "Lumbini Park", "latitude": 17.4132, "longitude": 78.4720}'
```

**Response:**
```json
{ "id": 11, "name": "Lumbini Park", "latitude": 17.4132, "longitude": 78.472 }
```

---

### Update a place
```bash
curl -X PUT http://127.0.0.1:8000/places/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Cafe Coffee Day - Updated"}'
```

---

### Delete a place
```bash
curl -X DELETE http://127.0.0.1:8000/places/5
```

**Response:**
```json
{ "message": "Place 5 deleted successfully." }
```

---

### Isochrone filter (mock mode — no API key needed)
```bash
curl "http://127.0.0.1:8000/places/isochrone/filter?lat=17.4126&lon=78.4483&range=10"
```

**Response (places within ~2 km mock polygon):**
```json
[
  { "id": 1, "name": "Cafe Coffee Day - Banjara Hills", "latitude": 17.4126, "longitude": 78.4483 },
  { "id": 4, "name": "GVK One Mall - Banjara Hills",    "latitude": 17.42,   "longitude": 78.4482 }
]
```

---

## 🗺 How Isochrone Filtering Works

```
User sends lat/lon/range
        │
        ▼
[isochrone.py] calls ORS API  ──► returns GeoJSON polygon
        │                          (area reachable in N minutes)
        ▼
Shapely converts polygon to shape object
        │
        ▼
For each place → create Shapely Point(lon, lat)
        │
        ▼
polygon.contains(point)?
   YES → include in results
   NO  → skip
        │
        ▼
Return filtered list of places
```

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `fastapi` | Web framework for building the API |
| `uvicorn` | ASGI server that runs FastAPI |
| `pydantic` | Data validation and schemas |
| `requests` | HTTP calls to ORS Isochrone API |
| `shapely` | Geometry: polygon containment checks |
