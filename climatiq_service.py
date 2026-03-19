import requests
from config import CLIMATIQ_KEY

# Global cache to remember working IDs for the session
WORKING_ID_CACHE = {}

def get_transport_emissions(mode, distance, weight):
    # Mapping modes to a prioritized list of candidate activity IDs
    # We try these in order until one works. This handles plan differences (403) and DB changes (400).
    mode_candidates = {
        "Rail": [
            "freight_train-route_type_na-fuel_type_na",
            "freight_train-route_type_rail_transportation-fuel_type_na"
        ],
        "Cargo Ship": [
            "sea_freight-vessel_type_container-distance_uplift_included",
            "sea_freight-vessel_type_general_cargo-route_type_na"
        ],
        "Diesel Truck": [
            "freight_vehicle-vehicle_type_truck_transport-fuel_source_diesel-vehicle_weight_na-percentage_load_na",
            "freight_vehicle-vehicle_type_truck_transportation-fuel_source_diesel",
            "freight_truck"
        ],
        "Electric Truck": [
            "freight_vehicle-vehicle_type_truck_transport-fuel_source_electricity-vehicle_weight_na-percentage_load_na",
            "freight_vehicle-vehicle_type_truck_transportation-fuel_source_electricity",
            "freight_vehicle-vehicle_type_truck_transport-fuel_source_bev"
        ],
        "Air Freight": [
            "freight_flight-route_type_na-distance_na-weight_na-rf_na",
            "freight_flight-route_type_international-distance_na-weight_na"
        ]
    }

    # Fallback factors (kg CO2e per tonne-km)
    fallback = {
        "Rail": 0.02, "Cargo Ship": 0.015, "Diesel Truck": 0.1, "Electric Truck": 0.05, "Air Freight": 0.5
    }    
    
    # Try working ID from cache first
    candidates = mode_candidates.get(mode, [])
    if mode in WORKING_ID_CACHE:
        candidates = [WORKING_ID_CACHE[mode]] + [c for c in candidates if c != WORKING_ID_CACHE[mode]]

    url = "https://api.climatiq.io/data/v1/estimate"
    headers = {"Authorization": f"Bearer {CLIMATIQ_KEY}"}

    last_error = "No candidates found"
    
    for activity_id in candidates:
        try:
            payload = {
                "emission_factor": {
                    "activity_id": activity_id,
                    "data_version": "^0"  # Mandatory for recent Climatiq versions
                },
                "parameters": {
                    "distance": distance, "distance_unit": "km",
                    "weight": weight, "weight_unit": "kg"
                }
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                WORKING_ID_CACHE[mode] = activity_id  # Save working ID
                return result["co2e"] * 1000  # KG to Grams
            else:
                last_error = f"{response.status_code}: {response.text}"
                continue # Try next ID
                
        except Exception as e:
            last_error = str(e)
            continue

    # If all candidates fail, use fallback
    import streamlit as st
    st.warning(f"Climatiq API info ({mode}): Using industry fallback due to plan/data limits ({last_error})")
    return fallback[mode] * distance * weight
