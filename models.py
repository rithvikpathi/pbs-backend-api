from pydantic import BaseModel

# --- API RESPONSE SCHEMAS ---
# Keeping the data strictly typed so the frontend doesn't crash

class Segment(BaseModel):
    from_location: str
    to_location: str
    distance_km: float
    mode: str  # Strictly "walk" or "bike"

class RouteResponse(BaseModel):
    total_stations_used: int
    route: list[Segment]