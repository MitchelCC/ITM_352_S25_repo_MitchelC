import matplotlib.pyplot as plt
import requests
import json


file_id = "1-kjcJHN_pCJfB-f3_2xgQNF5U-5PitjU"
url = f"https://drive.google.com/uc?export=download&id={file_id}"
response = requests.get(url)
response.raise_for_status()  


data = json.loads(response.text)

# filtering rows with valid "fare" and "tips" values 
filtered_data = [
    trip for trip in data 
    if "fare" in trip and trip["fare"].strip() 
    and "tips" in trip and trip["tips"].strip()
]

#extract fares and tips as numeric values
fares = [float(trip["fare"]) for trip in filtered_data]
tips = [float(trip["tips"]) for trip in filtered_data]


plt.figure(figsize=(10, 6))
plt.scatter(fares, tips, alpha=0.6, edgecolor='k', color='blue')
plt.xlabel("Fare ($)")
plt.ylabel("Tips ($)")
plt.title("Relationship Between Fares and Tips (Trip Miles > 1)")
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()