import matplotlib.pyplot as plt
import json
import requests

file_id = "1-kvj2Ore88PGzZ9J7_lPBOvNf5C1ohpQ"
url = f"https://drive.google.com/uc?export=download&id={file_id}"

response = requests.get(url)
response.raise_for_status

data = json.loads(response.text)

filtered_data = [
    trip for trip in data 
    if "fare" in trip and trip["fare"].strip() 
    and "trip_miles" in trip and trip["trip_miles"].strip()
]

fares = [float(trip["fare"]) for trip in filtered_data]
trip_miles = [float(trip["trip_miles"]) for trip in filtered_data]

plt.figure(figsize=(10, 6))
plt.plot(
    fares, 
    trip_miles, 
    linestyle="none", 
    marker="v",          #"v" for triangle_down markers
    markersize=8, 
    alpha=0.2,           #0.2 transparency
    color="cyan",       
    markeredgecolor="black" 
)
plt.xlabel("Fare ($)", fontsize=12)
plt.ylabel("Trip Miles", fontsize=12)
plt.title("Fares vs. Trip Miles (Stylish Version)", fontsize=14, pad=20)
plt.grid(True, linestyle="--", alpha=0.3)
plt.show()