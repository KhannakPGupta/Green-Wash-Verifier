import requests
from config import CLIMATIQ_KEY

def get_transport_emissions(mode,distance,weight):

    #Translates human-friendly transport names into specific activity_id strings required by the Climatiq API
    mode_map = {
        "Rail": "freight_train-route_type_na-fuel_type_na",
        "Cargo Ship": "sea_freight-vessel_type_container-distance_uplift_included",
        "Diesel Truck": "freight_vehicle-vehicle_type_truck_transportation-fuel_source_diesel-vehicle_weight_na-percentage_load_na-load_type_na-distance_uplift_na",
        "Electric Truck": "freight_vehicle-vehicle_type_truck_transportation-fuel_source_electricity-vehicle_weight_na-percentage_load_na-load_type_na-distance_uplift_na",
        "Air Freight": "freight_flight-route_type_na-distance_na-weight_na-rf_na"
    }

    fallback = {
            "Rail": 0.02,
            "Cargo Ship": 0.015,
            "Diesel Truck": 0.1,
            "Electric Truck": 0.05,
            "Air Freight": 0.5
        }    
    
    try:
        url = "https://api.climatiq.io/data/v1/estimate"
        headers={"Authorization":f"Bearer {CLIMATIQ_KEY}"}   #Bearer Token Authentication

        #The data
        payload = {
            "emission_factor": {
                "activity_id": mode_map[mode]
            },
            "parameters": {
                "distance": distance,
                "distance_unit": "km",
                "weight": weight,
                "weight_unit": "kg"
            }
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        response.raise_for_status()
        result = response.json()
        return result["co2e"]       #Extracts and returns CO2 equivalent in kg 

    except requests.exceptions.Timeout:
        return fallback[mode]*distance*weight
    except requests.exceptions.ConnectionError:
        return fallback[mode]*distance*weight
    except Exception as e:
        import streamlit as st
        st.error(f"Climatiq API Error ({mode}): {e}")
        return fallback[mode]*distance*weight
