import requests

url_cli = "https://api.climatiq.io/data/v1/estimate"
headers_cli = {"Authorization": "Bearer fake_token_for_testing"}
payload_cli = {
    "emission_factor": {
        "activity_id": "freight_truck",
        "data_version": "^7"
    },
    "parameters": {
        "distance": 200,
        "distance_unit": "km",
        "weight": 1.0,
        "weight_unit": "kg"
    }
}

try:
    res_cli = requests.post(url_cli, json=payload_cli, headers=headers_cli, timeout=10)
    print("Climatiq Status:", res_cli.status_code)
    print("Climatiq Response:", res_cli.text[:300])
except Exception as e:
    print("Climatiq Exception:", e)


url_ors = "https://api.openrouteservice.org/v2/directions/driving-car"
headers_ors = {"Authorization": "fake_token_for_testing", "Content-Type": "application/json"}
payload_ors = {"coordinates": [[77.59, 12.97], [72.87, 19.07]]}

try:
    res_ors = requests.post(url_ors, json=payload_ors, headers=headers_ors, timeout=10)
    print("ORS Status:", res_ors.status_code)
    print("ORS Response:", res_ors.text[:300])
except Exception as e:
    print("ORS Exception:", e)

