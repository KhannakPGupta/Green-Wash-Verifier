import requests
from config import CLIMATIQ_KEY

def get_transport_emissions(mode,distance,weight):

    # Translates human-friendly transport names into specific activity_id strings required by the Climatiq API
    # Updated to more standard IDs that are less likely to break
    mode_map = {
        "Rail": "freight_train-route_type_na-fuel_type_na",
        "Cargo Ship": "sea_freight-vessel_type_container-distance_uplift_included",
        "Diesel Truck": "freight_vehicle-vehicle_type_truck_transport-fuel_source_diesel-vehicle_weight_na-percentage_load_na",
        "Electric Truck": "freight_vehicle-vehicle_type_truck_transport-fuel_source_electricity-vehicle_weight_na-percentage_load_na",
        "Air Freight": "freight_flight-route_type_na-distance_na-weight_na-rf_na"
    }

    # Fallback factors (kg CO2e per tonne-km)
    # The formula (factor * dist * weight) with these factors results in grams.
    fallback = {
            "Rail": 0.02,
            "Cargo Ship": 0.015,
            "Diesel Truck": 0.1,
            "Electric Truck": 0.05,
            "Air Freight": 0.5
        }    
    
    try:
        url = "https://api.climatiq.io/data/v1/estimate"
        headers={"Authorization":f"Bearer {CLIMATIQ_KEY}"}

        payload = {
            "emission_factor": {
                "activity_id": mode_map[mode],
                "data_version": "^7"  # Ensures compatibility with latest database
            },
            "parameters": {
                "distance": distance,
                "distance_unit": "km",
                "weight": weight,
                "weight_unit": "kg"
            }
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        
        # If the request failed, try to extract error details
        if response.status_code != 200:
            try:
                error_data = response.json()
                if isinstance(error_data, dict):
                    # Handle both {"error": {"message": "..."}} and {"message": "..."} formats
                    inner_error = error_data.get("error", {})
                    if isinstance(inner_error, dict):
                        error_msg = inner_error.get("message", response.text)
                    else:
                        error_msg = error_data.get("message", response.text)
                else:
                    error_msg = str(error_data)
            except Exception:
                error_msg = response.text
                
            raise Exception(f"{response.status_code} - {error_msg}")

        result = response.json()
        return result["co2e"] * 1000  # Convert kg CO2e to grams for frontend consistency

    except Exception as e:
        import streamlit as st
        # Log error to Streamlit but continue with fallback
        st.error(f"Climatiq API Error ({mode}): {e}")
        return fallback[mode] * distance * weight
