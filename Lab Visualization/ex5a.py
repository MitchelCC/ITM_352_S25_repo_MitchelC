import matplotlib.pyplot as plt
import json
import requests

file_id = "1-kvj2Ore88PGzZ9J7_lPBOvNf5C1ohpQ"
url = f"https://drive.google.com/uc?export=download&id={file_id}"

response = requests.get(url)
response.raise_for_status

data = json.loads(response.text)
#filter valid entries
filtered_data = [
    trip for trip in data 
    if "fare" in trip and trip["fare"].strip() 
    and "trip_miles" in trip and trip["trip_miles"].strip()
]
#converting to numerical values
fares = [float(trip["fare"]) for trip in filtered_data]
trip_miles = [float(trip["trip_miles"]) for trip in filtered_data]

plt.figure(figsize=(10, 6))
plt.scatter(fares, trip_miles, alpha=0.6, edgecolor='k', color='green')
plt.xlabel("Fare ($)")
plt.ylabel("Trip Miles")
plt.title("Fares vs. Trip Miles (Trips from Area 8)")
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()