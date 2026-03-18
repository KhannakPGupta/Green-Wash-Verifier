import requests
from config import CLIMATIQ_KEY

def get_transport_emissions(mode,distance,weight):

    #Translates human-friendly transport names into specific activity_id strings required by the Climatiq API
    mode_map = {
        "Rail": "freight_train",
        "Cargo Ship": "freight_ship",
        "Diesel Truck": "freight_truck",
        "Electric Truck": "freight_truck",
        "Air Freight": "freight_plane"
    }

    fallback = {
            "Rail": 0.02,
            "Cargo Ship": 0.015,
            "Diesel Truck": 0.1,
            "Electric Truck": 0.05,
            "Air Freight": 0.5
        }    
    
    try:
        url = "https://beta3.api.climatiq.io/estimate"
        headers={"Authorization":f"Bearer{CLIMATIQ_KEY}"}   #Bearer Token Authentication

        #The data
        payload = {
            "emission_factor": {
                "activity_id": mode_map[mode],
                "data_version": "^7"    # ^ symbol tells API to use latest dynamic version of emission data
            },
            "parameters": {
                "distance": distance,
                "distance_unit": "km",
                "weight": weight,
                "weight_unit": "kg"
            }
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        result = response.json()
        return result["co2e"]       #Extracts and returns CO2 equivalent in kg 

    except requests.exceptions.Timeout:
        return fallback[mode]*distance*weight
    except requests.exceptions.ConnectionError:
        return fallback[mode]*distance*weight
    except Exception:
        return fallback[mode]*distance*weight
