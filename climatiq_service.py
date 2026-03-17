import requests
from config import CLIMATIQ_KEY

#Translates human-friendly transport names into specific activity_id strings required by the Climatiq API
mode_map = {
    "Rail": "freight_train",
    "Cargo Ship": "freight_ship",
    "Diesel Truck": "freight_truck",
    "Electric Truck": "freight_truck",
    "Air Freight": "freight_plane"
}

def get_transport_emissions(mode,distance,weight):
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

    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    return result["co2e"]       #Extracts and returns CO2 equivalent in kg 
