import requests
from config import CLIMATIQ_KEY

# Global cache to remember working IDs across requests to save API calls
WORKING_ID_CACHE = {}

def get_transport_emissions(mode, distance, weight):
    # Fallback factors (kg CO2e per tonne-km) used if all API attempts fail
    fallback_factors = {
        "Rail": 0.02, "Cargo Ship": 0.015, "Diesel Truck": 0.1, "Electric Truck": 0.05, "Air Freight": 0.5
    }

    # If already cached, try it first
    if mode in WORKING_ID_CACHE:
        working_id = WORKING_ID_CACHE[mode]
        res = call_climatiq(working_id, distance, weight)
        if res: return res

    # 1. LIST OF PRIORITIZED CANDIDATES (Fast path)
    candidates = {
        "Rail": ["freight_train-route_type_na-fuel_type_na"],
        "Cargo Ship": ["sea_freight-vessel_type_container-distance_uplift_included"],
        "Diesel Truck": ["freight_vehicle-vehicle_type_truck_transportation-fuel_source_diesel", "freight_truck"],
        "Electric Truck": ["freight_vehicle-vehicle_type_truck_transportation-fuel_source_electricity"],
        "Air Freight": ["freight_flight-route_type_na-distance_na-weight_na-rf_na"]
    }.get(mode, [])

    for act_id in candidates:
        res = call_climatiq(act_id, distance, weight)
        if res:
            WORKING_ID_CACHE[mode] = act_id
            return res

    # 2. RUNTIME SEARCH FALLBACK (Search queries for broader results)
    search_queries = {
        "Rail": "rail freight",
        "Cargo Ship": "cargo ship",
        "Diesel Truck": "diesel truck",
        "Electric Truck": "electric truck",
        "Air Freight": "air freight"
    }
    
    query = search_queries.get(mode, mode)
    try:
        search_url = "https://api.climatiq.io/data/v1/search"
        headers = {"Authorization": f"Bearer {CLIMATIQ_KEY}"}
        # Broader search without category restriction
        params = {"query": query, "results_per_page": 1}
        resp = requests.get(search_url, headers=headers, params=params, timeout=5)
        
        if resp.status_code == 200:
            results = resp.json().get("results", [])
            if results:
                discovered_id = results[0]["activity_id"]
                res = call_climatiq(discovered_id, distance, weight)
                if res:
                    WORKING_ID_CACHE[mode] = discovered_id
                    return res
    except:
        pass

    # 3. ABSOLUTE FALLBACK (Silent)
    return fallback_factors[mode] * distance * weight

def call_climatiq(activity_id, distance, weight):
    """Helper to call estimate API with a specific ID"""
    try:
        url = "https://api.climatiq.io/data/v1/estimate"
        headers = {"Authorization": f"Bearer {CLIMATIQ_KEY}"}
        payload = {
            "emission_factor": {
                "activity_id": activity_id,
                "data_version": "^0"  # Ensures the most compatible data version
            },
            "parameters": {
                "distance": distance, "distance_unit": "km",
                "weight": weight, "weight_unit": "kg"
            }
        }
        r = requests.post(url, json=payload, headers=headers, timeout=3)
        if r.status_code == 200:
            return r.json().get("co2e", 0) * 1000 # To Grams
    except:
        pass
    return None
