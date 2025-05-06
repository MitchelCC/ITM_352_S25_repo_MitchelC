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
    and float(trip["trip_miles"]) > 0 #filtering out trips less than 0 miles
]

fares = [float(trip["fare"]) for trip in filtered_data]
trip_miles = [float(trip["trip_miles"]) for trip in filtered_data]

plt.figure(figsize=(10, 6))
plt.scatter(fares, trip_miles, alpha=0.6, edgecolor='k', color='blue')
plt.xlabel("Fare ($)", fontsize=12)
plt.ylabel("Trip Miles", fontsize=12)
plt.title("Fares vs. Trip Miles (Trips from Area 8)", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)

# Save to file
plt.savefig('FaresXmiles.png', dpi=300, bbox_inches='tight')
plt.show()