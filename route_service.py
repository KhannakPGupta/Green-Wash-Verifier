import requests         #Library to send HTTP requests to API
from config import ORS_KEY          #Pulling API key

#Function to get longitude and latitude
def get_distance(start_coords,end_coords):
    url="https://api.openrouteservice.org/v2/directions/driving-car"
    headers={"Authorization":ORS_KEY,               #Gives permission to use the service
             "Content-Type":"application/json"}     #Informs server that data is being sent in json format
    
    #Actual data being sent
    payload={"coordinates":[start_coords,end_coords]}

    #Hits API - send data to url and waits for reply
    response=requests.post(url,json=payload,headers=headers, timeout=5)
    response.raise_for_status()

    #Converts raw text response to Python dictionary for easy access
    data = response.json()

    #Drills through nested response layers of API. Returns distance in m converted to km
    distance=data["routes"][0]["summary"]["distance"]/1000

    return round(distance,2)
    