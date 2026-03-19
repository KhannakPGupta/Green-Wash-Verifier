import requests
from config import CLIMATIQ_KEY

def get_transport_emissions(mode, distance, weight):
    # Mapping for the modern Climatiq Intermodal Freight API
    # This endpoint is more robust and better suited for transport logistics
    mode_configs = {
        "Rail": {"transport_mode": "rail"},
        "Cargo Ship": {"transport_mode": "sea", "sea_details": {"vessel_type": "container_ship"}},
        "Diesel Truck": {"transport_mode": "road", "road_details": {"vehicle_type": "truck", "fuel_source": "diesel"}},
        "Electric Truck": {"transport_mode": "road", "road_details": {"vehicle_type": "truck", "fuel_source": "electricity"}},
        "Air Freight": {"transport_mode": "air"}
    }

    # Fallback factors (kg CO2e per tonne-km)
    fallback = {
        "Rail": 0.02,
        "Cargo Ship": 0.015,
        "Diesel Truck": 0.1,
        "Electric Truck": 0.05,
        "Air Freight": 0.5
    }    
    
    try:
        # Using the dedicated Intermodal Freight endpoint
        url = "https://api.climatiq.io/freight/v1/intermodal"
        headers = {"Authorization": f"Bearer {CLIMATIQ_KEY}"}

        # Build the payload for the intermodal endpoint
        config = mode_configs.get(mode, {"transport_mode": "road"})
        payload = {
            "route": [
                {
                    **config,
                    "distance": distance,
                    "distance_unit": "km",
                    "weight": weight,
                    "weight_unit": "kg"
                }
            ]
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        
        if response.status_code != 200:
            try:
                error_data = response.json()
                error_msg = error_data.get("error", {}).get("message", response.text)
            except:
                error_msg = response.text
            raise Exception(f"{response.status_code} - {error_msg}")

        result = response.json()
        # The intermodal endpoint returns a total co2e for the whole route
        return result["co2e"] * 1000  # Convert kg to grams for frontend consistency

    except Exception as e:
        import streamlit as st
        st.error(f"Climatiq API Error ({mode}): {e}")
        return fallback[mode] * distance * weight
