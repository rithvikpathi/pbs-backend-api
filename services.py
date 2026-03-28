import requests
import networkx as nx
import math
from fastapi import HTTPException
import config

# --- DYNAMIC DATA FETCHING ---

def get_feed_url(feed_name: str) -> str:
    """Hunts down the specific feed URL from the master list."""
    try:
        response = requests.get(config.MASTER_URL)
        response.raise_for_status()
        master_data = response.json()
        
        # Dig through the JSON to find the exact feed we need
        feeds = master_data.get("data", {}).get("en", {}).get("feeds", [])
        for feed in feeds:
            if feed.get("name") == feed_name:
                return feed.get("url")
                
        raise ValueError(f"Feed '{feed_name}' is missing from the master directory.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Master directory error: {str(e)}")

def fetch_data(feed_name: str) -> dict:
    """Grabs the URL and pulls the actual live JSON payload."""
    url = get_feed_url(feed_name)
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("data", {})
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch {url}: {str(e)}")


# --- THE MATH & GRAPH ENGINE ---

def haversine(lat1, lon1, lat2, lon2):
    """The big brain math for getting accurate distances across the globe."""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2 * config.EARTH_RADIUS * math.asin(math.sqrt(a))

def nearest_station(lat, lon, stations):
    """Finds the absolute closest dock to a given coordinate."""
    return min(stations, key=lambda s: haversine(lat, lon, s["lat"], s["lon"]))

def get_live_routing_stations():
    """Merges static coords with live status so we don't route to empty docks."""
    info_data = fetch_data("station_information").get("stations", [])
    status_data = fetch_data("station_status").get("stations", [])
    
    status_map = {s["station_id"]: s for s in status_data}
    stations = []

    for s in info_data:
        st = status_map.get(s["station_id"])
        # If there are bikes, it's a valid node. Otherwise, skip it.
        if st and st.get("num_bikes_available", 0) > 0:
            stations.append({
                "id": s["station_id"],
                "name": s["name"],
                "lat": s["lat"],
                "lon": s["lon"]
            })
    return stations

def build_graph(stations):
    """Maps out the network graph and connects nodes within our safe 30-min ride limit."""
    G = nx.Graph()
    for s in stations:
        G.add_node(s["id"], name=s["name"], coord=(s["lat"], s["lon"]))

    for i in range(len(stations)):
        for j in range(i + 1, len(stations)):
            s1, s2 = stations[i], stations[j]
            d = haversine(s1["lat"], s1["lon"], s2["lat"], s2["lon"])
            # Only connect them if we can make the hop without getting charged
            if d <= config.MAX_RIDE_KM:
                G.add_edge(s1["id"], s2["id"], weight=d)
    return G