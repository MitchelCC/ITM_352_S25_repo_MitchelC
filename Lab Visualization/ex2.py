import matplotlib.pyplot as plt
import json
import requests

file_id = "1-kvj2Ore88PGzZ9J7_lPBOvNf5C1ohpQ"
url = f"https://drive.google.com/uc?export=download&id={file_id}"

response = requests.get(url)
response.raise_for_status

data = json.loads(response.text)

trip_miles = [
    float(trip["trip_miles"]) 
    for trip in data 
    if "trip_miles" in trip and trip["trip_miles"].strip()
]

# Define bins and plot histogram
bins = list(range(0, 25, 2))  # 0–2, 2–4, ..., 22–24
plt.hist(trip_miles, bins=bins, edgecolor="black", alpha=0.7)
plt.xlabel("Trip Miles")
plt.ylabel("Frequency")
plt.title("Distribution of Trip Miles from Area 8")
plt.show()
