from fastapi import APIRouter, HTTPException, Query
import networkx as nx

from models import RouteResponse, Segment
import services

# --- API ROUTES ---
router = APIRouter()

@router.get("/stations", tags=["Stations"])
def get_stations():
    """Spits out all static station info."""
    return services.fetch_data("station_information").get("stations", [])

@router.get("/status", tags=["Status"])
def get_station_status():
    """Live check for available bikes and open docks."""
    return services.fetch_data("station_status").get("stations", [])

@router.get("/pricing", tags=["System Info"])
def get_pricing():
    """Pulls current passes and system pricing."""
    return services.fetch_data("system_pricing_plans").get("plans", [])

@router.get("/station/{station_id}", tags=["Stations"])
def get_single_station(station_id: str):
    """Fuses static details and live availability for one specific dock."""
    info_data = services.fetch_data("station_information").get("stations", [])
    status_data = services.fetch_data("station_status").get("stations", [])
    
    info = next((s for s in info_data if s.get("station_id") == station_id), None)
    status = next((s for s in status_data if s.get("station_id") == station_id), None)
    
    if not info or not status:
        raise HTTPException(status_code=404, detail="Station completely MIA.")
        
    return {
        "station_id": station_id,
        "name": info.get("name"),
        "capacity": info.get("capacity"),
        "bikes_available": status.get("num_bikes_available"),
        "docks_available": status.get("num_docks_available"),
        "lat": info.get("lat"),
        "lon": info.get("lon")
    }

@router.get("/smart_route", response_model=RouteResponse, tags=["Routing"])
def smart_route(
    start_lat: float = Query(...),
    start_lon: float = Query(...),
    end_lat: float = Query(...),
    end_lon: float = Query(...)
):
    """The core MVP feature: calculates the optimal 30-min node-hopping route."""
    stations = services.get_live_routing_stations()
    if not stations:
        raise HTTPException(status_code=503, detail="Zero bikes available system-wide right now.")

    start_station = services.nearest_station(start_lat, start_lon, stations)
    end_station = services.nearest_station(end_lat, end_lon, stations)

    G = services.build_graph(stations)

    # Try to find the shortest safe path
    try:
        path_ids = nx.shortest_path(G, start_station["id"], end_station["id"], weight="weight")
    except nx.NetworkXNoPath:
        # Fallback if no safe relay route exists, just blast straight there
        path_ids = [start_station["id"], end_station["id"]]

    id_map = {s["id"]: s for s in stations}
    route_segments = []

    # 1. Walk to the very first dock
    walk_start_dist = services.haversine(start_lat, start_lon, start_station["lat"], start_station["lon"])
    route_segments.append(Segment(
        from_location="Your Location",
        to_location=start_station["name"],
        distance_km=round(walk_start_dist, 2),
        mode="walk"
    ))

    # 2. Map out the bike relay hops
    for i in range(len(path_ids) - 1):
        s1, s2 = id_map[path_ids[i]], id_map[path_ids[i + 1]]
        d = services.haversine(s1["lat"], s1["lon"], s2["lat"], s2["lon"])
        route_segments.append(Segment(
            from_location=s1["name"],
            to_location=s2["name"],
            distance_km=round(d, 2),
            mode="bike"
        ))

    # 3. Final walk from the last dock to the actual destination
    walk_end_dist = services.haversine(end_station["lat"], end_station["lon"], end_lat, end_lon)
    route_segments.append(Segment(
        from_location=end_station["name"],
        to_location="Your Destination",
        distance_km=round(walk_end_dist, 2),
        mode="walk"
    ))

    return RouteResponse(total_stations_used=len(path_ids), route=route_segments)