import requests         #Library to send HTTP requests to API
from config import ORS_KEY          #Pulling API key

#Function to get longitude and latitude
def get_distance(start_coords,end_coords):
    url="https://api.openrouteservice.org/v2/directions/driving-car"
    # Robust key handling
    auth_header = ORS_KEY if ORS_KEY.startswith("Bearer ") else f"Bearer {ORS_KEY}"
    headers = {"Authorization": auth_header, "Content-Type": "application/json"}
    
    # Actual data being sent
    payload = {"coordinates": [start_coords, end_coords]}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        
        if response.status_code != 200:
            raise Exception(f"{response.status_code} - {response.text}")

        data = response.json()
        distance = data["routes"][0]["summary"]["distance"] / 1000
    except Exception as e:
        import streamlit as st
        st.error(f"OpenRouteService API Error: {e}")
        distance = 2500.0

    return round(distance, 2)
    